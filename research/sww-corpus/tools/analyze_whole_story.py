"""Whole-story arithmetic, following ANALYSIS-PLAN and deviations D1-D8.

python3 -I analyze_whole_story.py RESULTS_DIR [--quotechecks DIRECTORY]

No coder input is changed. Outputs summary.json, matching.csv, flags.csv,
quotation_sample.json and others_mentioned.json. Codes/quotes/names never decide identity.
"""
import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

W2_CODES = {'disbelieved', 'blamed_punished_or_counter_accused',
            'condition_as_dismissal', 'protected_itself'}
NON_INST = {'the_person', 'family_or_friends', 'other_victims',
            'journalists_podcast_or_virality'}
THRESH = {'W1': .4, 'W2': .3, 'W3': .5}
METRICS = (*THRESH, 'W3_protected_only', 'never_reached', 'harmed_ever')
CLAUDE = [1, 2, 3, 4, 5, 6, 13, 14, 15, 16, 17, 18, 19, 22, 24]
CODEX = [7, 8, 9, 10, 11, 12, 17, 20, 21, 23, 25, 26]
LABELS = {'all': 'Mixed: Claude unblinded / Codex blinded',
          'claude': 'Claude unblinded', 'codex': 'Codex blinded',
          'all_codex17': 'Mixed: Claude unblinded / Codex blinded; Codex S17 substituted'}


def norm(name):
    # Keep parenthetical harm labels and digits; remove punctuation, not their contents.
    return ' '.join(re.sub(r'\[unnamed\]|[^a-z0-9 ]', ' ', name.lower()).split())


def wilson(k, n, z=1.96):
    if not n:
        return [None, None]
    p, zz = k/n, z*z
    center = (p + zz/(2*n))/(1 + zz/n)
    half = z*math.sqrt(p*(1-p)/n + zz/(4*n*n))/(1 + zz/n)
    return [max(0.0, center-half), min(1.0, center+half)]


def rate(k, n):
    return {'k': k, 'n': n, 'rate': k/n if n else None, 'ci95': wilson(k, n)}


def agreement(pairs):
    pairs = [(a, b) for a, b in pairs if a is not None and b is not None]
    n = len(pairs)
    if not n:
        return {'n': 0, 'pct_agree': None, 'kappa': None}
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    po = sum(a == b for a, b in pairs)/n
    pe = sum(ca[k]*cb[k] for k in ca.keys() | cb.keys())/(n*n)
    return {'n': n, 'pct_agree': po, 'kappa': (po-pe)/(1-pe) if pe < 1 else None}


def indicator(p):
    worker = p.get('decisive_work_by')
    reached, outcome = p.get('reached_institution'), p.get('outcome')
    assert worker in NON_INST | {'institution', 'unclear', None}, worker
    assert reached in {'yes', 'no', 'unclear'}, reached
    assert outcome in {'protected', 'partly_protected', 'not_protected',
                       'harmed_by_institution', 'never_reached'}, outcome
    return dict(reached=reached, outcome=outcome, protected=outcome == 'protected',
                prot_any=outcome in {'protected', 'partly_protected'},
                W2=any(c['response'] in W2_CODES for c in p.get('contacts', [])),
                W3=None if worker in {None, 'unclear'} else worker in NON_INST,
                harmed_ever=p['harmed_by_institution_ever'],
                alone='person_account_alone' in p.get('evidence_types', []),
                central=p['role_in_story'] == 'central_survivor',
                contacts=len(p.get('contacts', [])),
                reasons=(p.get('never_reached') or {}).get('reasons') or [])


def value(p, metric):
    i = p['i']
    if metric in {'W1', 'W2', 'harmed_ever'}:
        if i['reached'] != 'yes':
            return None
        return i['protected'] if metric == 'W1' else i[metric]
    if metric in {'W3', 'W3_protected_only'}:
        eligible = i['protected'] if metric == 'W3_protected_only' else i['prot_any']
        return i['W3'] if eligible else None
    if metric == 'never_reached':
        return i['reached'] == 'no' if i['reached'] in {'yes', 'no'} else None
    raise ValueError(metric)


def own(records):
    out = {'people': len(records), 'unknown_reached': sum(p['i']['reached'] == 'unclear' for p in records),
           'protected_unknown_worker': sum(p['i']['prot_any'] and p['i']['W3'] is None for p in records)}
    for metric in METRICS:
        vals = [value(p, metric) for p in records]
        known = [v for v in vals if v is not None]
        out[metric] = dict(rate(sum(known), len(known)), omitted=len(records)-len(known))
    out['contacts_total'] = sum(p['i']['contacts'] for p in records)
    out['contacts_mean'] = out['contacts_total']/len(records) if records else None
    return out


def agreed(pairs, metric):
    k = n = disagreed = omitted = 0
    for a, b in pairs:
        x, y = value(a, metric), value(b, metric)
        if x is None or y is None:
            omitted += 1
        elif x != y:
            disagreed += 1
        else:
            k += x
            n += 1
    return dict(rate(k, n), eligible=n+disagreed, disagreed=disagreed,
                omitted=omitted, matched_total=len(pairs))


def evaluate(pairs, left, right):
    return {'matched': len(pairs),
            'headline': {m: agreed(pairs, m) for m in METRICS},
            'own': {'left': own(left), 'right': own(right)},
            'central_only': {
                'agreed': {m: agreed([(a,b) for a,b in pairs if a['i']['central'] and b['i']['central']],m)
                           for m in METRICS},
                'own': {'left': own([p for p in left if p['i']['central']]),
                        'right': own([p for p in right if p['i']['central']])}},
            'agreement': fields_agreement(pairs, left, right),
            'never_reached_reasons': reasons(pairs, left, right)}


def fields_agreement(pairs, left, right):
    fields = {'reached': 'reached', 'outcome': 'outcome', 'W2_indicator': 'W2',
              'W3_indicator': 'W3', 'harmed_ever': 'harmed_ever', 'account_alone': 'alone'}
    out = {label: agreement([(a['i'][f], b['i'][f]) for a,b in pairs]) for label,f in fields.items()}
    out['W2_eligible'] = agreement([(value(a,'W2'), value(b,'W2')) for a,b in pairs])
    out['W3_eligible'] = agreement([(value(a,'W3'), value(b,'W3')) for a,b in pairs])
    out['person_finding'] = dict(rate(len(pairs),len(left)+len(right)-len(pairs)),
                                 left_total=len(left),right_total=len(right))
    out['contacts'] = {side: {'total': sum(p['i']['contacts'] for p in records),
                              'per_person': sum(p['i']['contacts'] for p in records)/len(records) if records else None}
                       for side,records in [('left',left),('right',right)]}
    return out


def reasons(pairs, left, right):
    out = {}
    for side,records in [('left',left),('right',right)]:
        c = Counter()
        for p in records:
            if p['i']['reached'] == 'no':
                c.update(set(p['i']['reasons']))
        out[side] = dict(sorted(c.items()))
    both = Counter()
    for a,b in pairs:
        if a['i']['reached'] == b['i']['reached'] == 'no':
            both.update(set(a['i']['reasons']) & set(b['i']['reasons']))
    out['both'] = dict(sorted(both.items()))
    return out


class Union:
    def __init__(self, keys):
        self.parent = {k:k for k in keys}

    def root(self, k):
        if self.parent[k] != k:
            self.parent[k] = self.root(self.parent[k])
        return self.parent[k]

    def join(self, a, b):
        self.parent[self.root(b)] = self.root(a)


def read_inputs(directory):
    docs, recs = {}, {}
    for path in sorted((directory/'coded').glob('s*.json')):
        d = json.loads(path.read_text())
        assert path.stem == f"s{d['season']:02}_{d['coder']}", path
        docs[path.stem] = d
        ids = set()
        for p in d['persons']:
            pid = p['person_id']
            assert pid not in ids, (path, pid)
            ids.add(pid)
            key = path.stem,pid
            recs[key] = dict(key=key, season=d['season'], coder=d['coder'], raw=p, i=indicator(p))
    return docs,recs


def make_matches(directory, docs, recs, comparisons):
    hand = defaultdict(list)
    for r in csv.DictReader((directory/'matching_hand.csv').open()):
        hand[int(r['season']),r['left_coder'],r['right_coder']].append(r)
    assert set(hand) <= set(comparisons)
    rows, matches = [], {}
    for season, lc, rc in comparisons:
        lf,rf = f's{season:02}_{lc}',f's{season:02}_{rc}'
        pa = {p['person_id']: recs[lf,p['person_id']] for p in docs[lf]['persons']}
        pb = {p['person_id']: recs[rf,p['person_id']] for p in docs[rf]['persons']}
        ua,ub = set(),set()
        pairs = []
        def add(a,b,method,reason):
            for pid,records,used in [(a,pa,ua),(b,pb,ub)]:
                if pid:
                    assert pid in records and pid not in used, (season,lc,rc,pid)
                    used.add(pid)
            assert reason and (a or b)
            rows.append([season,lc,rc,a,b,method,reason])
            if a and b:
                pairs.append((pa[a],pb[b]))
        for r in hand[season,lc,rc]:
            add(r['A_id'],r['B_id'],'hand' if r['A_id'] and r['B_id'] else 'hand-unmatched',r['reason'])
        na,nb = defaultdict(list),defaultdict(list)
        for pid,p in pa.items():
            if pid not in ua:
                na[norm(p['raw']['name'])].append(pid)
        for pid,p in pb.items():
            if pid not in ub:
                nb[norm(p['raw']['name'])].append(pid)
        for n in sorted(na):
            if n and len(na[n]) == len(nb[n]) == 1:
                add(na[n][0],nb[n][0],'auto-name','Unique normalized full name; identity reviewed before calculation.')
        assert ua == set(pa) and ub == set(pb), (season,lc,rc,'missing unmatched disposition')
        matches[season,lc,rc] = sorted(pairs,key=lambda pair:pair[0]['key'])
    with (directory/'matching.csv').open('w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['season','left_coder','right_coder','A_id','B_id','method','reason'])
        w.writerows(rows)
    return matches


def repeat_union(directory, recs, matches):
    u=Union(recs)
    # All identity-only matches, including S17 cross-family matches, propagate identity.
    for pairs in matches.values():
        for a,b in pairs:
            u.join(a['key'],b['key'])
    seen=set()
    for r in csv.DictReader((directory/'repeat_links.csv').open()):
        a=(r['from_file'],r['from_id']); b=(r['to_file'],r['to_id'])
        assert a in recs and b in recs and (a,b) not in seen
        assert recs[a]['season'] < recs[b]['season'] and r['reason']
        seen.add((a,b));u.join(a,b)
    return u


def unique_records(records, union):
    seen=set();out=[]
    for p in sorted(records,key=lambda p:(p['season'],p['key'])):
        ident=union.root(p['key'])
        if ident not in seen:
            seen.add(ident);out.append(p)
    return out


def unique_pairs(pairs, union):
    seen=set();out=[]
    for a,b in sorted(pairs,key=lambda pair:(pair[0]['season'],pair[0]['key'])):
        ident=union.root(a['key'])
        if ident not in seen:
            seen.add(ident);out.append((a,b))
    return out


def quote_flags(qdir, docs, recs):
    if qdir is None:
        return None,{}
    flags=set();report={}
    for stem,d in docs.items():
        path=qdir/(stem+'.json.quotecheck.json')
        assert path.exists(),path
        rows=json.loads(path.read_text());by_pid=defaultdict(list)
        for pid,field,score,where in rows:
            if not isinstance(score,(float,int)) or score < .8:
                if (stem,pid) in recs:
                    flags.add((stem,pid))
                by_pid[pid].append({'field':field,'score':score,'where':where})
        for p in d['persons']:
            if not p.get('outcome_quote'):
                flags.add((stem,p['person_id']))
                by_pid[p['person_id']].append({'field':'outcome','score':'missing','where':None})
        tested=[r for r in rows if isinstance(r[2],(float,int))]
        report[stem]={'tested':len(tested),'found':sum(r[2]>=.8 for r in tested),
                      'found_rate':sum(r[2]>=.8 for r in tested)/len(tested) if tested else None,
                      'too_short':sum(r[2]=='too-short' for r in rows),
                      'other_episode':sum(r[2]>=.8 and r[3]=='other-episode' for r in tested),
                      'failures':dict(by_pid)}
    return flags,report


def framing(docs, recs, union, variants):
    out={}
    for family,seasons,coders in [('claude',[2,3,4,13,22,24],['POS','NEG','A','B']),
                                   ('codex',[13],['CPOS','CNEG','A','B'])]:
        out[family]={'label': 'Claude unblinded' if family=='claude' else 'Codex blinded; neutral S13 A/B is Claude unblinded',
                     'seasons':seasons,'variants':{}}
        for variant,(dedup,excluded) in variants.items():
            rates={}
            for coder in coders:
                records=[p for p in recs.values() if p['season'] in seasons and p['coder']==coder]
                if dedup:
                    records=unique_records(records,union)
                records=[p for p in records if p['key'] not in excluded]
                rates[coder]=own(records)
            pos,neg=coders[:2]
            bands={}
            for metric in (*THRESH,'never_reached'):
                a,b=rates[pos][metric]['rate'],rates[neg][metric]['rate']
                bands[metric]=abs(a-b) if a is not None and b is not None else None
            out[family]['variants'][variant]={'own':rates,'band':bands}
    return out


def decisions(headline, bands, group):
    out={}
    for metric,threshold in THRESH.items():
        families=['claude','codex'] if group.startswith('all') else [group]
        values=[bands[f][metric] for f in families]
        band=max(values) if all(v is not None for v in values) else None
        h=headline[metric]['rate']
        distance=abs(h-threshold) if h is not None else None
        raw=None if h is None else ('refuted' if (h>=threshold if metric=='W1' else h<threshold) else 'not refuted')
        verdict='not decided by this method' if h is None or band is None or distance<band else raw
        out[metric]={'rate':h,'threshold':threshold,'distance':distance,
                     'family_bands':{f:bands[f][metric] for f in families},'band':band,
                     'threshold_verdict':raw,'verdict':verdict}
    return out


def select_sample(groups, matches, recs):
    sample=[]
    for group,comparisons in groups.items():
        if group=='all_codex17':
            continue
        pairs=[pair for comp in comparisons for pair in matches[comp]]
        for metric in (*THRESH,'never_reached'):
            for category in ['agreed_positive','agreed_negative','disagreed']:
                for a,b in pairs:
                    x,y=value(a,metric),value(b,metric)
                    if x is None or y is None:
                        continue
                    hit=(x!=y) if category=='disagreed' else (x==y and x==(category=='agreed_positive'))
                    if hit:
                        sample.append({'group':group,'metric':metric,'category':category,
                                       'left':a['key'],'right':b['key']})
                        break
    # A source locator for the first no-reach quotation for each recorded reason.
    reason_samples=[];seen=set()
    for p in sorted([p for p in recs.values() if p['coder'] in {'A','B','CA','CB'}], key=lambda p:p['key']):
        if p['i']['reached']!='no':
            continue
        for q in (p['raw'].get('never_reached') or {}).get('quotes') or []:
            reason=q.get('reason')
            if reason not in seen:
                seen.add(reason);reason_samples.append({'record':p['key'],'reason':reason,'source':q.get('source')})
    counts={}
    for metric in (*THRESH,'never_reached'):
        rows=[row for row in sample if row['metric']==metric]
        keys={tuple(row[side]) for row in rows for side in ['left','right']}
        pairs={tuple(tuple(row[side]) for side in ['left','right']) for row in rows}
        counts[metric]={'unique_pairs':len(pairs),'unique_coded_records':len(keys)}
    counts['all']={'unique_coded_records':len({tuple(row[side]) for row in sample for side in ['left','right']})}
    return {'selection':'D7; first eligible positive, negative and disagreement by season/ID; no recoding',
            'counts':counts,'pairs':sample,'reason_examples':reason_samples}


def reading_checks(directory, docs):
    counts={row[0]:int(row[1]) for row in csv.reader((directory/'chunk_linecounts.tsv').open(),delimiter='\t')}
    report={}
    for stem,d in docs.items():
        prefix=f"s{d['season']:02}/"
        expected={k for k in counts if k.startswith(prefix)}
        seen=set();issues=[]
        for row in d['reading_log']:
            key=prefix+Path(row['file']).name
            if key in seen or key not in counts or row['last_line_number']!=counts.get(key) or not row['read_in_full']:
                issues.append({'file':key,'reported':row['last_line_number'],'expected':counts.get(key)})
            seen.add(key)
        if seen!=expected:
            issues.append({'missing':sorted(expected-seen),'extra':sorted(seen-expected)})
        report[stem]={'chunks':len(d['reading_log']),'issues':issues}
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--quotechecks',type=Path)
    args=parser.parse_args();d=args.directory
    docs,recs=read_inputs(d)
    primary=[(s,'A','B') if s in CLAUDE else (s,'CA','CB') for s in range(1,27)]
    cross=[(17,a,b) for a in ['A','B'] for b in ['CA','CB']]
    comparisons=primary+[(17,'CA','CB')]+cross
    matches=make_matches(d,docs,recs,comparisons)
    union=repeat_union(d,recs,matches)
    # Assert propagation has not accidentally merged separate records within a coder/season.
    for stem in docs:
        keys=[k for k in recs if k[0]==stem]
        assert len({union.root(k) for k in keys})==len(keys),(stem,'identity collision')
    contradiction={k for k,p in recs.items() if
                   (p['i']['outcome']=='never_reached' and p['i']['reached']!='no') or
                   (p['i']['reached']=='no' and p['i']['outcome']!='never_reached')}
    death={k for k,p in recs.items() if p['raw'].get('deceased') and p['i']['prot_any']}
    qflags,qreport=quote_flags(args.quotechecks,docs,recs)
    with (d/'flags.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['file','person_id','flag'])
        for label,flags in [('reached_outcome_contradiction',contradiction),('deceased_with_protection',death),
                            ('quotation_check',qflags or set())]:
            for stem,pid in sorted(flags):w.writerow([stem+'.json',pid,label])
    variants={
        'season_unchanged':(False,set()),'season_no_contradictions':(False,contradiction),
        'unique_unchanged':(True,set()),'unique_no_contradictions':(True,contradiction),
        'season_no_deceased_protection':(False,death)}
    if qflags is not None:
        variants.update(season_quotes_pass=(False,qflags),unique_quotes_pass=(True,qflags),
                        season_quotes_and_consistency=(False,qflags|contradiction),
                        unique_quotes_and_consistency=(True,qflags|contradiction))
    fr=framing(docs,recs,union,variants)
    groups={'all':primary,'claude':[(s,'A','B') for s in CLAUDE],
            'codex':[(s,'CA','CB') for s in CODEX],
            'all_codex17':[(17,'CA','CB') if c[0]==17 else c for c in primary]}
    result={'method':'ANALYSIS-PLAN.md; DEVIATIONS.md D1-D8; inputs unchanged',
            'labels':LABELS,'flags':{'contradictions':len(contradiction),'deceased_protection':len(death),
                                    'quote_records':len(qflags) if qflags is not None else None},
            'quotation_checks':qreport,'framing':fr,'groups':{}}
    result['flags']['by_file']={}
    for label,flags in [('contradiction',contradiction),('deceased_protection',death),('quotation',qflags or set())]:
        result['flags']['by_file'][label]=dict(sorted(Counter(k[0] for k in flags).items()))
    result['reading_log_checks']=reading_checks(d,docs)
    result['reading_log_totals']={'entries':sum(len(doc['reading_log']) for doc in docs.values()),
                                  'files':len(docs),'files_with_issues':sum(bool(x['issues']) for x in result['reading_log_checks'].values())}
    result['quotation_totals_by_coder']={}
    for stem,q in qreport.items():
        c=stem.split('_',1)[1]
        t=result['quotation_totals_by_coder'].setdefault(c,dict(tested=0,found=0,too_short=0,other_episode=0,person_records_flagged=0))
        for k in ['tested','found','too_short','other_episode']:t[k]+=q[k]
        t['person_records_flagged']+=sum(key[0]==stem for key in qflags)
    for totals in result['quotation_totals_by_coder'].values():
        totals['found_rate']=totals['found']/totals['tested'] if totals['tested'] else None
    result['quotation_totals']={k:sum(t[k] for t in result['quotation_totals_by_coder'].values())
                                for k in ['tested','found','too_short','other_episode','person_records_flagged']}
    totals=result['quotation_totals']
    totals['found_rate']=totals['found']/totals['tested'] if totals['tested'] else None
    for group,comps in groups.items():
        pairs=[pair for comp in comps for pair in matches[comp]]
        left=[p for s,a,b in comps for k,p in recs.items() if k[0]==f's{s:02}_{a}']
        right=[p for s,a,b in comps for k,p in recs.items() if k[0]==f's{s:02}_{b}']
        report={'label':LABELS[group],'seasons':[c[0] for c in comps],'variants':{},'by_season':{}}
        for variant,(dedup,excluded) in variants.items():
            # Earliest matched/own appearance retained BEFORE flags, eligibility and agreement.
            pp=unique_pairs(pairs,union) if dedup else pairs
            ll=unique_records(left,union) if dedup else left
            rr=unique_records(right,union) if dedup else right
            pp=[(a,b) for a,b in pp if a['key'] not in excluded and b['key'] not in excluded]
            ll=[p for p in ll if p['key'] not in excluded];rr=[p for p in rr if p['key'] not in excluded]
            ev=evaluate(pp,ll,rr)
            bands={f:fr[f]['variants'][variant]['band'] for f in fr}
            ev['decision']=decisions(ev['headline'],bands,group)
            report['variants'][variant]=ev
        for s,a,b in comps:
            ll=[p for p in left if p['season']==s];rr=[p for p in right if p['season']==s]
            report['by_season'][s]={'coders':[a,b],'label':'Claude unblinded' if a=='A' else 'Codex blinded',
                                     **evaluate(matches[s,a,b],ll,rr)}
        result['groups'][group]=report
    result['s17_crosscheck']={}
    for s,a,b in cross+[(17,'A','B'),(17,'CA','CB')]:
        ll=[p for p in recs.values() if p['season']==s and p['coder']==a]
        rr=[p for p in recs.values() if p['season']==s and p['coder']==b]
        result['s17_crosscheck'][a+'-'+b]=evaluate(matches[s,a,b],ll,rr)
    c17=result['s17_crosscheck']['A-B'];x17=result['s17_crosscheck']['CA-CB']
    result['s17_family_differences']={}
    for stream,claude,codex in [('agreed',c17['headline'],x17['headline']),
                                ('left_own',c17['own']['left'],x17['own']['left']),
                                ('right_own',c17['own']['right'],x17['own']['right'])]:
        result['s17_family_differences'][stream]={}
        for m in METRICS:
            cr,xr=claude[m]['rate'],codex[m]['rate']
            result['s17_family_differences'][stream][m]=cr-xr if cr is not None and xr is not None else None
    others={}
    for comp in primary+[(17,'CA','CB')]:
        s,a,b=comp
        for coder in [a,b]:
            stem=f's{s:02}_{coder}';entries=docs[stem].get('others_mentioned') or []
            # Descriptions and quotes can contain uncharged people's names; publish IDs/counts only.
            numeric=[o['count_stated'] for o in entries if isinstance(o.get('count_stated'),(int,float))]
            others[stem]={'entries':len(entries),'numeric_subtotal_with_overlap':sum(numeric),
                           'numeric_entries':len(numeric),
                           'rows':[{'other_id':f'other{i}','count_stated':o.get('count_stated'),
                                    'reached_institution':o.get('reached_institution')} for i,o in enumerate(entries)]}
    result['others_mentioned']=others
    (d/'others_mentioned.json').write_text(json.dumps(others,indent=2)+'\n')
    (d/'quotation_sample.json').write_text(json.dumps(select_sample(groups,matches,recs),indent=2)+'\n')
    (d/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Validated identities and wrote analysis; quotation checks:', 'included' if qflags is not None else 'PENDING')
    for group in groups:
        ev=result['groups'][group]['variants']['season_unchanged']
        print(group,[(m,ev['headline'][m]['k'],ev['headline'][m]['n'],ev['decision'][m]['verdict']) for m in THRESH])


if __name__=='__main__':
    main()

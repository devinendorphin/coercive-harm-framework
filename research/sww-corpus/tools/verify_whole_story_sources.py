"""Verify frozen episode selection and actual reading endpoints against committed inputs.

python3 -I verify_whole_story_sources.py RESULTS_DIR TRANSCRIPT_DIR READING_DIR

Writes source_validation.json. Uses full transcript text and the original frozen assignments;
no coding or matching decisions are made. Transcripts/reading folders stay outside the repo.
"""
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import corpus

results,source,reading=map(Path,sys.argv[1:4])
index=results/'episode_index.txt'
rows=[line.split() for line in index.read_text().splitlines() if len(line.split())==3]
episodes=corpus.frozen_episodes(str(source),str(index))
expected=sorted((row[0],int(row[1]),row[2]) for row in rows)
actual=sorted((str(e['season']) if e['season'] else 'UNASSIGNED',corpus.epnum(e['slug']),e['slug']) for e in episodes)
assert actual==expected, 'frozen episode selection/assignment mismatch'
assert {p.stem for p in source.glob('*.json')}=={row[2] for row in rows}, 'non-frozen transcripts in source folder'
subprocess.run([sys.executable,'-I',str(Path(__file__).with_name('prepare_reading.py')),
                str(source),str(reading),str(results.parent.parent/'whole_story'),
                '--frozen-index',str(index)],check=True,stdout=subprocess.DEVNULL)

def counts(path):
    with path.open() as f:
        return {row[0]:(int(row[1]),int(row[2])) for row in csv.reader(f,delimiter='\t')}

old=counts(results/'chunk_linecounts.tsv');new=counts(reading/'linecounts.tsv')
keys=sorted(old.keys()|new.keys())
line_diff=[{'file':key,'original':old.get(key),'rebuilt':new.get(key)} for key in keys
           if key not in old or key not in new or old[key][0]!=new[key][0]]
word_diff=[{'file':key,'original':old.get(key),'rebuilt':new.get(key)} for key in keys if old.get(key)!=new.get(key)]
endpoint=[];checked=0
for path in sorted((results/'coded').glob('*.json')):
    doc=json.loads(path.read_text())
    for row in doc['reading_log']:
        key=f"s{doc['season']:02}/"+Path(row['file']).name;checked+=1
        if key not in new or row['last_line_number']!=new[key][0] or not row['read_in_full']:
            endpoint.append({'file':path.name,'chunk':key,'reported':row['last_line_number'],'actual':new.get(key)})
seasons={e['slug']:e['season'] for e in episodes}
report={'canonical_files':len(rows),'episodes_after_corpus_rules':len(episodes),
        'unassigned_episodes':sum(e['season'] is None for e in episodes),'frozen_index_matches':actual==expected,
        'original_reading_files':len(old),'rebuilt_reading_files':len(new),
        'linecount_differences':line_diff,'wordcount_differences':word_diff,
        'reading_endpoints_checked':checked,'endpoint_discrepancies':endpoint,
        'method':'Full canonical transcript files with original selections and inherited season assignments restored from episode_index.txt.',
        'slug_only_assignment_differences':[
            {'slug':e['slug'],'slug_only_season':e['season'],'original_season':seasons[e['slug']]}
            for e in corpus.episodes(str(source)) if e['season']!=seasons[e['slug']]],
        'coder_input_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((results/'coded').glob('*.json'))}}
(results/'source_validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['coder_input_sha256','method','slug_only_assignment_differences']}))
if line_diff or word_diff or endpoint:
    raise SystemExit(1)

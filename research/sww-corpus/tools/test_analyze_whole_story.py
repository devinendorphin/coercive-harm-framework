"""Checks of analysis rules with synthetic records; no recoding or headline fixtures."""
import unittest
import json
import tempfile
from pathlib import Path
import analyze_whole_story as a


def rec(key,season,reached='yes',outcome='protected',worker=True):
    return {'key':key,'season':season,'i':{
        'reached':reached,'outcome':outcome,'protected':outcome=='protected',
        'prot_any':outcome in ['protected','partly_protected'],'W3':worker,'W2':False}}


class AnalysisRules(unittest.TestCase):
    def test_harm_labels_and_numbered_people_remain_distinct(self):
        self.assertNotEqual(a.norm('A (school harm)'),a.norm('A (partner harm)'))
        self.assertNotEqual(a.norm('[unnamed] Child 1'),a.norm('[unnamed] Child 2'))

    def test_protection_eligibility_does_not_require_reached_yes(self):
        x=rec(('s01_A','P1'),1,reached='unclear')
        y=rec(('s01_B','P1'),1)
        self.assertIs(a.value(x,'W3'),True)
        self.assertIsNone(a.value(x,'W1'))
        self.assertEqual(a.agreed([(x,y)],'W1')['omitted'],1)
        self.assertEqual(a.agreed([(x,y)],'W3')['n'],1)

    def test_disagreement_and_missing_worker_do_not_enter_denominator(self):
        x=rec(('s01_A','P1'),1)
        y=rec(('s01_B','P1'),1,worker=False)
        self.assertEqual(a.agreed([(x,y)],'W3')['disagreed'],1)
        self.assertEqual(a.agreed([(x,y)],'W3')['n'],0)
        y['i']['W3']=None
        self.assertEqual(a.agreed([(x,y)],'W3')['omitted'],1)

    def test_earliest_is_selected_before_eligibility_or_exclusion(self):
        x=rec(('s01_A','P1'),1,reached='unclear')
        y=rec(('s01_B','P1'),1)
        z=rec(('s02_A','P1'),2)
        u=a.Union([x['key'],y['key'],z['key']])
        u.join(x['key'],y['key']);u.join(x['key'],z['key'])
        self.assertEqual(a.unique_records([z,x],u),[x])
        kept=a.unique_pairs([(z,y),(x,y)],u)
        self.assertEqual(kept,[(x,y)])
        self.assertEqual(a.agreed(kept,'W1')['n'],0)
        self.assertEqual([p for p in a.unique_records([z,x],u) if p['key']!=x['key']],[])

    def test_exact_rate_and_larger_family_band(self):
        h={k:{'rate':.3996 if k=='W1' else .7} for k in a.THRESH}
        bands={'claude':{k:.0005 for k in a.THRESH},'codex':{k:.0001 for k in a.THRESH}}
        self.assertEqual(a.decisions(h,bands,'all')['W1']['verdict'],'not decided by this method')
        self.assertEqual(a.decisions(h,bands,'codex')['W1']['verdict'],'not refuted')
        bands['codex']['W1']=None
        self.assertEqual(a.decisions(h,bands,'all')['W1']['verdict'],'not decided by this method')

    def test_zero_denominator_and_chance_agreement(self):
        self.assertIsNone(a.rate(0,0)['rate'])
        self.assertEqual(a.agreement([(False,False),(True,False)])['pct_agree'],.5)
        self.assertIsNone(a.agreement([(False,False)])['kappa'])

    def test_quotation_flags_separate_people_from_other_mentions(self):
        people=[{'person_id':pid,'outcome_quote':'An actual outcome quotation'}
                for pid in ['P1','P2','P3']]+[{'person_id':'P4','outcome_quote':None}]
        docs={'s01_A':{'persons':people}}
        records={('s01_A',p['person_id']):{} for p in people}
        rows=[['P1','outcome',.79,'cited'],['P2','contact1','too-short',None],
              ['P3','outcome',1.0,'cited'],['P4','outcome','too-short',None],
              ['other0','others_mentioned',.4,'cited']]
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)
            (directory/'s01_A.json.quotecheck.json').write_text(json.dumps(rows))
            flags,report=a.quote_flags(directory,docs,records)
        self.assertEqual(flags,{('s01_A','P1'),('s01_A','P2'),('s01_A','P4')})
        self.assertEqual(report['s01_A']['tested'],3)
        self.assertEqual(report['s01_A']['found'],1)
        self.assertEqual(report['s01_A']['found_rate'],1/3)


if __name__=='__main__':
    unittest.main()

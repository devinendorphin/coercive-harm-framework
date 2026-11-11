"""Regression checks for canonical transcripts whose discarded twin carried the season."""
import json
import tempfile
import unittest
from pathlib import Path
import corpus


class FrozenCorpus(unittest.TestCase):
    def test_original_season_and_full_text_survive_without_the_twin(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            text='The entire original transcript, without shortening or summarizing.'
            (root/'data-points-child-abuse.json').write_text(json.dumps({
                'slug':'data-points-child-abuse','title':'Data Points','notes':'',
                'text':text,'segments':[[0,text]]}))
            index=root/'index.txt';index.write_text('17 999 data-points-child-abuse\n1 unique episodes; 0 unassigned\n')
            self.assertIsNone(corpus.season_of('data-points-child-abuse'))
            episodes=corpus.frozen_episodes(str(root),str(index))
            self.assertEqual(len(episodes),1)
            self.assertEqual(episodes[0]['season'],17)
            self.assertEqual(episodes[0]['text'],text)
            self.assertEqual(episodes[0]['segments'],[[0,text]])
            corpus.dump(str(root),17,str(root/'reading'),episodes_override=episodes)
            self.assertIn(text,(root/'reading'/'s17_01.txt').read_text())

    def test_duplicate_selection_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'sample.json').write_text(json.dumps({'slug':'sample','text':'Full text'}))
            index=root/'index.txt';index.write_text('1 999 sample\n1 999 sample\n')
            with self.assertRaises(AssertionError):
                corpus.frozen_episodes(str(root),str(index))


if __name__=='__main__':
    unittest.main()

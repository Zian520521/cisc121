"""Unit tests for CISC 121 shuttle ranking; run `python -m unittest -v`."""
import unittest
from app import parse_stops, merge_sort_steps, ranking_markdown


class ProjectTests(unittest.TestCase):
    def check(self, data, expected):
        items = parse_stops(data)
        ranked, frames = merge_sort_steps(items)
        self.assertEqual([x['count'] for x in ranked], expected)
        self.assertEqual(len(ranked), len(items))
        self.assertTrue(frames)
        self.assertEqual(frames[0]['action'], 'Start')
        self.assertEqual(frames[-1]['action'], 'Finished')

    def test_typical(self):
        self.check('Union,45\nLibrary,20\nResidence,70\nGym,35', [70,45,35,20])

    def test_single(self):
        self.check('One,0', [0])

    def test_same_count_stable(self):
        ranked, frames = merge_sort_steps(parse_stops('First,7\nSecond,7\nThird,10'))
        self.assertEqual([x['name'] for x in ranked], ['Third','First','Second'])

    def test_zero_and_high(self):
        self.check('A,0\nB,100000\nC,2', [100000,2,0])

    def test_reverse_order(self):
        self.check('A,0\nB,1\nC,2\nD,3', [3,2,1,0])

    def test_invalid_counts(self):
        for text in ['A,-1', 'A,2.5', 'A,hello', 'A,100001', 'A,']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_stops(text)

    def test_invalid_names_and_format(self):
        for text in ['', 'A', ',1', 'A,1\na,3', 'A,1,2']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_stops(text)

    def test_limit(self):
        data='\n'.join(f'Stop{i},{i}' for i in range(25))
        with self.assertRaises(ValueError):
            parse_stops(data)

    def test_explanation(self):
        ranked, _ = merge_sort_steps(parse_stops('A,2\nB,5'))
        self.assertIn('B', ranking_markdown(ranked))
        self.assertIn('Dispatch recommendation', ranking_markdown(ranked))

if __name__ == '__main__':
    unittest.main()

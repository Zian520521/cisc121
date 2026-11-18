"""Automated tests for the CISC 121 Merge Sort shuttle stop project."""
import unittest
from app import parse_stops, merge_sort_steps, ranking_markdown

class ProjectTests(unittest.TestCase):
    def check(self, text, expected):
        stops = parse_stops(text)
        ranked, steps = merge_sort_steps(stops)
        self.assertEqual([s["count"] for s in ranked], expected)
        self.assertEqual(steps[0]["action"], "Start")
        self.assertEqual(steps[-1]["action"], "Finished")

    def test_typical(self):
        self.check("Union,45\nLibrary,20\nResidence,70\nGym,35", [70, 45, 35, 20])

    def test_single(self):
        self.check("Only,0", [0])

    def test_stable_ties(self):
        ranked, _ = merge_sort_steps(parse_stops("First,7\nSecond,7\nThird,10"))
        self.assertEqual([s["name"] for s in ranked], ["Third", "First", "Second"])

    def test_zero_and_upper_bound(self):
        self.check("A,0\nB,100000\nC,2", [100000,2,0])

    def test_reverse_order(self):
        self.check("A,0\nB,1\nC,2\nD,3", [3,2,1,0])

    def test_invalid_counts(self):
        for text in ("A,-1", "A,2.5", "A,hello", "A,100001", "A,"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_stops(text)

    def test_invalid_names(self):
        for text in ("", "A", ",1", "A,1\na,3", "A,1,2"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_stops(text)

    def test_limit(self):
        with self.assertRaises(ValueError):
            parse_stops("\n".join(f"Stop{i},{i}" for i in range(25)))

    def test_result_explanation(self):
        ranked, _ = merge_sort_steps(parse_stops("A,2\nB,5"))
        self.assertIn("B", ranking_markdown(ranked))
        self.assertIn("Dispatch recommendation", ranking_markdown(ranked))

if __name__ == "__main__":
    unittest.main()

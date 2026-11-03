import math, tempfile, unittest
from evidence_rl.data.schema import assign_split, validate_sample
from evidence_rl.env.tool_parser import parse_action
from evidence_rl.env.budget_env import BudgetEnv
from evidence_rl.evidence.credit import *
from evidence_rl.logging_utils import RunWriter
from evidence_rl.planner.allocators import Arm, allocate
from evidence_rl.planner.gittins import gittins_index

class T(unittest.TestCase):
    def test_parser_and_failures(self):
        self.assertEqual(parse_action('<answer>x</answer>').answer, 'x')
        self.assertEqual(parse_action('<grounding>{"bbox_2d":[0.2,0.1,0.1,0.5]}</grounding>').error, 'bad_bbox')
        self.assertEqual(parse_action('hello').kind, 'invalid')
    def test_budget(self):
        e = BudgetEnv(1, lambda b: 'o')
        act = '<grounding>{"bbox_2d":[0.1,0.1,0.2,0.2]}</grounding>'
        self.assertEqual(e.step(act)['status'], 'observed')
        self.assertEqual(e.step(act)['reason'], 'over_budget')
    def test_trace_formula(self):
        d = [2.0, 1.0, 1.0, .1]
        got = trace_turn_credit([-(x - .1) for x in d], 3, .8, .1)
        dl = [math.log(2), 0, math.log(10)]
        self.assertAlmostEqual(got[1], (dl[1] + .8 * dl[2]) / 1.8)
        self.assertGreater(got[1], got[0])
    def test_toy_functions(self):
        AND = lambda s: .9 if {'a', 'b'} <= s else .2
        self.assertEqual(evidence_group('abc', AND)[0], frozenset('ab'))
        OR = lambda s: .9 if s & {'a', 'b'} else .2
        self.assertEqual(len(evidence_group('ab', OR)[0]), 1)
        self.assertEqual(evidence_group('ab', lambda s: .5)[0], frozenset())
        REP = lambda s: .9 if ('a' in s and ({'b', 'd'} & s)) else .2
        self.assertEqual(len(evidence_group('abd', REP)[0]), 2)
        HARM = lambda s: (.9 if {'a', 'b'} <= s else .2) - (.3 if 'h' in s else 0)
        self.assertEqual(evidence_group('abh', HARM)[0], frozenset('ab'))
    def test_outcome_dominance(self):
        self.assertLess(bounded_lambda([.72, .72, -1.21], 1.5) * 1.5, 1.93)
    def test_shuffled_marginal(self):
        c = {'a': 1, 'b': -1, 'c': 0}
        self.assertCountEqual(shuffled(c, 3).values(), c.values())
    def test_gittins(self):
        self.assertGreater(gittins_index(1, 1), .5)
        self.assertGreater(gittins_index(6, 2), gittins_index(2, 6))
    def test_allocate_budget(self):
        arms = [Arm('a', 1, 8, 2), Arm('b', 1, 2, 8), Arm('c', 2)]
        for m in ['uniform', 'random', 'gittins', 'ucb', 'neyman']:
            c = allocate(arms, 10, m)
            self.assertLessEqual(c['a'] + c['b'] + 2 * c['c'], 10)
        g = allocate(arms, 10, 'gittins')
        self.assertGreater(g['a'], g['b'])
    def test_group_split(self):
        self.assertEqual(assign_split('doc1'), assign_split('doc1'))
    def test_schema(self):
        self.assertIn('no_gold_candidate', validate_sample(dict(sample_id=1, image_group_id=1, question='', answer='', answer_type='mc', thumbnail='', candidates=[{'id': 'a'}], structure_tag='x')))
    def test_writer_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            RunWriter(d, 'x', {}).close({})
            with self.assertRaises(FileExistsError):
                RunWriter(d, 'x', {})
if __name__ == '__main__':
    unittest.main()

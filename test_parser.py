import unittest
from main import get_code_from_statement

class TestGetCodeFromStatement(unittest.TestCase):
    def test_example_1(self):
        input_str = "matcha(clay)→(¬workhome(clay)∧¬matcha(clay))"
        expected_output = 'Implies(noun_predicates["matcha"](variables["clay"]), And(Not(noun_predicates["workhome"](variables["clay"])),Not(noun_predicates["matcha"](variables["clay"]))))'
        result = get_code_from_statement(input_str)
        self.assertEqual(result, expected_output)

    def test_example_2(self):
        input_str = "israpper(x) ∧ releasedalbum(x,y) → israpalbum(y)"
        expected_output = 'Implies(And(noun_predicates["israpper"](variables["x"]),verb_predicates["releasedalbum"](variables["x"], variables["y"])), noun_predicates["israpalbum"](variables["y"]))'
        result = get_code_from_statement(input_str)
        self.assertEqual(result, expected_output)

    def test_example_3(self):
        input_str = "∀xisrapper(x) → israpalbum(x)"
        expected_output = 'Implies(Forall(variables["x"], noun_predicates["israpper"](variables["x"])), noun_predicates["israpalbum"](variables["x"]))'
        result = get_code_from_statement(input_str)
        self.assertEqual(result, expected_output)

    def test_example_4(self):
        input_str = "∀x(israpper(x) → israpalbum(x))"
        expected_output = 'Forall(variables["x"], Implies(noun_predicates["israpper"](variables["x"]), noun_predicates["israpalbum"](variables["x"])))'
        result = get_code_from_statement(input_str)
        self.assertEqual(result, expected_output)

    def test_example_5(self):
        input_str = "∀x∀y(israpper(x) ∧ releasedalbum(x,y) → israpalbum(y))"
        expected_output = 'Forall([variables["x"], variables["y"]], Implies(And(noun_predicates["israpper"](variables["x"]),verb_predicates["releasedalbum"](variables["x"], variables["y"])), noun_predicates["israpalbum"](variables["y"])))'
        result = get_code_from_statement(input_str)
        self.assertEqual(result, expected_output)

    def test_example_6(self):
        input_str = "∀x∃y(directedby(y,x)→filmmaker(x))"
        expected_output = 'Forall(variables["x"], Exists(variables["y"], Implies(verb_predicates["directedby"](variables["y"], variables["x"]), noun_predicates["filmmaker"](variables["x"]))))'
        result = get_code_from_statement(input_str)
        self.assertEqual(result, expected_output)

    def test_example_7(self):
        input_str = "∀x(¬be(x,perfect)→¬play(sam,x))"
        expected_output = 'Forall(variables["x"], Implies(Not(verb_predicates["be"](variables["x"], variables["perfect"])), Not(verb_predicates["play"](variables["sam"], variables["x"]))))'
        result = get_code_from_statement(input_str)
        self.assertEqual(result, expected_output)

if __name__ == "test_parser.py":
    unittest.main()
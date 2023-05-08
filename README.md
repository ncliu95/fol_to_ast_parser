# First Order Logic to Abstract Syntax Tree Parser

Part of the Commonsense Reasoning Project (https://github.com/S-Bryce/commonsense_reasoning)

This parser takes FOL statements 
```
∀x(drinks(x)→dependent(x))

∀x(drinks(x)⊕jokes(x))

∀x(jokes(x)→¬unaware(x))

(student(rina)∧unaware(rina))⊕¬(student(rina)∨unaware(rina))

¬(dependent(rina)∧student(rina))→(dependent(rina)∧student(rina))⊕¬(dependent(rina)∨student(rina))
```

and translates them into code executable for LTN.

```python
Forall(variables["x"], Implies(noun_predicates["drinks"](variables["x"]), noun_predicates["dependent"](variables["x"])))

Forall(variables["x"], Or(And(noun_predicates["drinks"](variables["x"]), Not(noun_predicates["jokes"](variables["x"]))), And(Not(noun_predicates["drinks"](variables["x"])), noun_predicates["jokes"](variables["x"]))))

Forall(variables["x"], Implies(noun_predicates["jokes"](variables["x"]), Not(noun_predicates["unaware"](variables["x"]))))

Or(And(And(noun_predicates["student"](variables["rina"]),noun_predicates["unaware"](variables["rina"])), Not(Not(Or(noun_predicates["student"](variables["rina"]),noun_predicates["unaware"](variables["rina"]))))), And(Not(And(noun_predicates["student"](variables["rina"]),noun_predicates["unaware"](variables["rina"]))), Not(Or(noun_predicates["student"](variables["rina"]),noun_predicates["unaware"](variables["rina"])))))

Implies(Not(And(noun_predicates["dependent"](variables["rina"]),noun_predicates["student"](variables["rina"]))), Or(And(And(noun_predicates["dependent"](variables["rina"]),noun_predicates["student"](variables["rina"])), Not(Not(Or(noun_predicates["dependent"](variables["rina"]),noun_predicates["student"](variables["rina"]))))), And(Not(And(noun_predicates["dependent"](variables["rina"]),noun_predicates["student"](variables["rina"]))), Not(Or(noun_predicates["dependent"](variables["rina"]),noun_predicates["student"](variables["rina"]))))))
```

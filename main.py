import re

from lark import Lark, Transformer
# Define FOL grammar
fol_grammar = r"""
    start: expr

    expr: paren_expr
        | FORALL VARIABLE FORALL VARIABLE FORALL VARIABLE "(" expr ")" -> fff
        | FORALL VARIABLE FORALL VARIABLE EXISTS VARIABLE "(" expr ")" -> ffe
        | FORALL VARIABLE EXISTS VARIABLE EXISTS VARIABLE "(" expr ")" -> fee
        | EXISTS VARIABLE EXISTS VARIABLE EXISTS VARIABLE "(" expr ")" -> eee
        | EXISTS VARIABLE EXISTS VARIABLE FORALL VARIABLE "(" expr ")" -> eef
        | EXISTS VARIABLE FORALL VARIABLE FORALL VARIABLE "(" expr ")" -> eff
        | FORALL VARIABLE EXISTS VARIABLE FORALL VARIABLE "(" expr ")" -> fef
        | EXISTS VARIABLE FORALL VARIABLE EXISTS VARIABLE "(" expr ")" -> efe
        | FORALL VARIABLE FORALL VARIABLE "(" expr ")" -> doubleforall
        | EXISTS VARIABLE EXISTS VARIABLE "(" expr ")" -> doubleexists
        | FORALL VARIABLE EXISTS VARIABLE "(" expr ")" -> for_exists
        | EXISTS VARIABLE FORALL VARIABLE "(" expr ")" -> exists_for
        | FORALL VARIABLE "(" expr ")" -> forall
        | EXISTS VARIABLE "(" expr ")" -> exists

        | NOT atom -> not_
        | expr IMPLIES expr -> implies
        | expr AND expr -> _and
        | expr OR expr -> _or
        | expr IFF expr -> iff
        | expr XOR expr -> xor
        | NOT expr -> not_

        | FORALL VARIABLE FORALL VARIABLE FORALL VARIABLE atom -> fff
        | FORALL VARIABLE FORALL VARIABLE EXISTS VARIABLE atom -> ffe
        | FORALL VARIABLE EXISTS VARIABLE EXISTS VARIABLE atom -> fee
        | EXISTS VARIABLE EXISTS VARIABLE EXISTS VARIABLE atom -> eee
        | EXISTS VARIABLE EXISTS VARIABLE FORALL VARIABLE atom -> eef
        | EXISTS VARIABLE FORALL VARIABLE FORALL VARIABLE atom -> eff
        | FORALL VARIABLE EXISTS VARIABLE FORALL VARIABLE atom -> fef
        | EXISTS VARIABLE FORALL VARIABLE EXISTS VARIABLE atom -> efe
        | FORALL VARIABLE FORALL VARIABLE atom -> doubleforall
        | EXISTS VARIABLE EXISTS VARIABLE atom -> doubleexists
        | FORALL VARIABLE EXISTS VARIABLE atom -> for_exists
        | EXISTS VARIABLE FORALL VARIABLE atom -> exists_for
        | FORALL VARIABLE atom -> forall
        | EXISTS VARIABLE atom -> exists

        | atom

    paren_expr: "(" expr ")"


    atom: RELATION
        | PREDICATE
        | VARIABLE

    PREDICATE: IDENT "(" IDENT ")"
    RELATION: IDENT "(" IDENT "," IDENT ")"
    VARIABLE: /[xyz]/
    IDENT: /[a-zA-Z0-9!@#$&_`.+,-]+/

    NOT: "¬"
    AND: "∧" | "^"
    OR: "∨"
    IMPLIES: "→"
    IFF: "↔"
    XOR: "⊕"
    FORALL: "∀"
    EXISTS: "∃"

    %import common.WS
    %ignore WS
"""
# Instantiate Lark parser
fol_parser = Lark(fol_grammar, start='start')


def main():
    # Instantiate Lark parser
    fol_parser = Lark(fol_grammar, start='start')
    fol_transformer = FOLTransformer()
    # FOL statements
    # fol_statements = """
    # ∀x∀y(israpper(x) ∧ releasedalbum(x,y) → israpalbum(y))
    # ∀x(israpper(x) → israpalbum(x))
    # ∀x ∃y (holdingcompany(x) → company(y) ∧ holds(x, y))
    # """
    fol_statements = [
        "∃x(country(x)nearby(medeempire,x)∧plotstoswallowup(medeempire,x))"
    ]

    # Split statements and parse each one

    for statement in fol_statements:
        statement = statement.lower().replace(" ", "").strip()
        print(f"Code for statement: \n{get_code_from_statement(statement)}")


class FOLTransformer(Transformer):
    def not_(self, args):
        return f"Not({get_deepest_node(args[1])})"

    def _and(self, args):
        return f"And({get_deepest_node(args[0])},{get_deepest_node(args[2])})"

    def _or(self, args):
        return f"Or({get_deepest_node(args[0])},{get_deepest_node(args[2])})"

    def implies(self, args):
        return f"Implies({get_deepest_node(args[0])}, {get_deepest_node(args[2])})"

    def iff(self, args):
        a = get_deepest_node(args[0])
        b = get_deepest_node(args[2])
        return f"Or(And({a}, {b}), And(Not({a}), Not({b})))"

    def xor(self, args):
        a = get_deepest_node(args[0])
        b = get_deepest_node(args[2])
        return f"Or(And({a}, Not({b})), And(Not({a}), {b}))"

    def forall(self, args):
        return f'Forall(variables["{get_deepest_node(args[1])}"], {get_deepest_node(args[2])})'

    def doubleforall(self, args):
        return f'Forall([variables["{get_deepest_node(args[1])}"], variables["{get_deepest_node(args[3])}"]], {get_deepest_node(args[4])})'

    def exists(self, args):
        return f'Exists(variables["{get_deepest_node(args[1])}"], {get_deepest_node(args[2])})'

    def doubleexists(self, args):
        return f'Exists([variables["{get_deepest_node(args[1])}"], variables["{get_deepest_node(args[3])}"]], {get_deepest_node(args[4])})'

    def for_exists(self, args):
        return f'Forall(variables["{get_deepest_node(args[1])}"], Exists(variables["{get_deepest_node(args[3])}"], {get_deepest_node(args[4])}))'

    def exists_for(self, args):
        return f'Exists(variables["{get_deepest_node(args[1])}"], Forall(variables["{get_deepest_node(args[3])}"], {get_deepest_node(args[4])}))'

    def fff(self, args):
        return f'Forall([variables["{get_deepest_node(args[1])}"], variables["{get_deepest_node(args[3])}"], variables["{get_deepest_node(args[5])}"]], {get_deepest_node(args[6])})'

    def eee(self, args):
        return f'Exists([variables["{get_deepest_node(args[1])}"], variables["{get_deepest_node(args[3])}"], variables["{get_deepest_node(args[5])}"]], {get_deepest_node(args[6])})'

    def ffe(self, args):
        return f'Forall([variables["{get_deepest_node(args[1])}"], variables["{get_deepest_node(args[3])}"]], Exists(variables["{get_deepest_node(args[5])}"], {get_deepest_node(args[6])}))'

    def fee(self, args):
        return f'Exists(variables["{get_deepest_node(args[1])}"], Exists([variables["{get_deepest_node(args[3])}"], variables["{get_deepest_node(args[5])}"]], {get_deepest_node(args[6])}))'

    def eff(self, args):
        return f'Exists(variables["{get_deepest_node(args[1])}"], Forall([variables["{get_deepest_node(args[3])}"], variables["{get_deepest_node(args[5])}"]], {get_deepest_node(args[6])}))'

    def eef(self, args):
        return f'Exists([variables["{get_deepest_node(args[1])}"], variables["{get_deepest_node(args[3])}"]], Forall(variables["{get_deepest_node(args[5])}"], {get_deepest_node(args[6])})'

    def fef(self, args):
        return f'Forall(variables["{get_deepest_node(args[1])}"], Exists(variables["{get_deepest_node(args[3])}"], Forall(variables["{get_deepest_node(args[5])}"], {get_deepest_node(args[6])})))'

    def efe(self, args):
        return f'Exists(variables["{get_deepest_node(args[1])}"], Forall(variables["{get_deepest_node(args[3])}"], Exists(variables["{get_deepest_node(args[5])}"], {get_deepest_node(args[6])})))'

    # NOUN
    def PREDICATE(self, args):
        var_pattern = r'\((.*?)\)'
        var = re.findall(var_pattern, args)
        noun_pattern = r'[^()]*'
        noun = re.findall(noun_pattern, args)
        return f'noun_predicates["{noun[0]}"](variables["{var[0]}"])'

    #  VERB
    def RELATION(self, args):
        var_pattern = r'\((.*?)\)'
        var = re.findall(var_pattern, args)
        vars = var[0].split(",")
        verb_pattern = r'[^()]*'
        verb = re.findall(verb_pattern, args)
        return f'verb_predicates["{verb[0]}"](variables["{vars[0]}"], variables["{vars[1]}"])'

    def VARIABLE(self, args):
        return str(args[0])

    def IDENT(self, args):
        return str(args[0])

    def start(self, args):
        return get_deepest_node(args[0])


def get_deepest_node(node):
    if type(node) == str:
        return node
    else:
        return get_deepest_node(node.children[0])


def get_code_from_statement(statement):
    fol_parser = Lark(fol_grammar, start='start')
    fol_transformer = FOLTransformer()
    tree = fol_parser.parse(statement)
    code = fol_transformer.transform(tree)
    return code


if __name__ == "__main__":
    main()
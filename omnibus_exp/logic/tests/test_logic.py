from .. import interpret as interpret_
from .. import parse as parse_


class Solver:

    def __init__(self, rules_text) -> None:
        super().__init__()

        rules = parse_.Parser(rules_text).parse_rules()
        self.database = interpret_.Database(rules)

    def find_solutions(self, query_text):
        query = parse_.Parser(query_text).parse_query()
        return self.database.find_solutions(query)


def test_simple_goal_query():
    rules_text = """
        brother_sister(joe, monica).
        brother_sister(eric, erica).
        brother_sister(jim, rebecca).
    """

    goal_text = """
        brother_sister(jim, rebecca).
    """

    solver = Solver(rules_text)
    solution = solver.find_solutions(goal_text)

    assert solution


def test_simple_goal_query2():
    rules_text = """
        brother_sister(joe, monica).
        brother_sister(eric, erica).
        brother_sister(jim, rebecca).
    """

    goal_text = """
        brother_sister(joe, rebecca).
    """

    solver = Solver(rules_text)
    solution = solver.find_solutions(goal_text)

    assert not solution


def test_simple_variable_query():
    rules_text = """
        father_child(mike, john).
        father_child(eric, sarah).
        father_child(bob, jim).
    """

    query_text = """
        father_child(X, sarah).
    """

    solver = Solver(rules_text)
    solutions = solver.find_solutions(query_text)

    assert len(solutions.get('X')) == 1
    assert str(solutions.get('X').pop()) == 'eric'


def test_multi_variable_solutions():
    rules_text = """
        is_tall(jack, yes).
        is_tall(eric, no).
        is_tall(johnny, yes).
        is_tall(mark, no).
    """

    query_text = """
        is_tall(Y, yes)
    """

    solver = Solver(rules_text)
    solutions = solver.find_solutions(query_text)

    assert len(solutions.get('Y')) == 2

    assert any('jack' in str(solution) for solution in solutions.get('Y'))
    assert any('johnny' in str(solution) for solution in solutions.get('Y'))


def test_find_bad_dog():
    rules_text = """
        bad_dog(Dog) :-
           bites(Dog, Person),
           is_person(Person),
           is_dog(Dog).

        bites(fido, postman).
        is_person(postman).
        is_dog(fido).
    """

    query_text = """
        bad_dog( X )
    """

    solver = Solver(rules_text)
    solutions = solver.find_solutions(query_text)

    assert len(solutions.get("X")) == 1
    assert any('fido' in str(solution) for solution in solutions.get('X'))


def test_rule_sub():
    rules_text = """
        descendant(X, Y) :- offspring(X, Y).
        descendant(X, Z) :- offspring(X, Y), descendant(Y, Z).

        offspring(abraham, ishmael).
        offspring(abraham, isaac).
        offspring(isaac, esau).
        offspring(isaac, jacob).
    """

    query_text = """
        descendant(abraham, X).
    """

    solver = Solver(rules_text)
    solutions = solver.find_solutions(query_text)

    assert len(solutions.get('X')) == 4

    assert any('ishmael' in str(solution) for solution in solutions.get('X'))
    assert any('isaac' in str(solution) for solution in solutions.get('X'))
    assert any('esau' in str(solution) for solution in solutions.get('X'))
    assert any('jacob' in str(solution) for solution in solutions.get('X'))


def test_rule_sub2():
    rules_text = """
        father_child(massimo, ridge).
        father_child(eric, thorne).
        father_child(thorne, alexandria).

        mother_child(stephanie, chloe).
        mother_child(stephanie, kristen).
        mother_child(stephanie, felicia).

        parent_child(X, Y) :- father_child(X, Y).
        parent_child(X, Y) :- mother_child(X, Y).

        sibling(X, Y) :- parent_child(Z, X), parent_child(Z, Y).
    """

    query_text = """
        sibling(X, felicia)
    """

    solver = Solver(rules_text)
    solutions = solver.find_solutions(query_text)

    assert len(solutions.get('X')) == 3

    assert any('chloe' in str(solution) for solution in solutions.get('X'))
    assert any('kristen' in str(solution) for solution in solutions.get('X'))
    assert any('felicia' in str(solution) for solution in solutions.get('X'))


def test_multiple_var_query():
    rules_text = """
        father(jack, susan).
        father(jack, ray).
        father(david, liza).
        father(david, john).
        father(john, peter).
        father(john, mary).
        mother(karen, susan).
        mother(karen, ray).
        mother(amy, liza).
        mother(amy, john).
        mother(susan, peter).
        mother(susan, mary).

        parent(X, Y) :- father(X, Y).
        parent(X, Y) :- mother(X, Y).
        grandfather(X, Y) :- father(X, Z), parent(Z, Y).
        grandmother(X, Y) :- mother(X, Z), parent(Z, Y).
        grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
    """

    query_text = """
        grandparent(X, Y)
    """

    solver = Solver(rules_text)
    solution_map = solver.find_solutions(query_text)
    solutions = list(zip(solution_map.get('X'), solution_map.get('Y')))

    assert len(solutions) == 8

    assert any('(jack, peter)' in str(solution) for solution in solutions)
    assert any('(jack, mary)' in str(solution) for solution in solutions)
    assert any('(david, peter)' in str(solution) for solution in solutions)
    assert any('(david, mary)' in str(solution) for solution in solutions)
    assert any('(karen, peter)' in str(solution) for solution in solutions)
    assert any('(karen, mary)' in str(solution) for solution in solutions)
    assert any('(amy, peter)' in str(solution) for solution in solutions)
    assert any('(amy, peter)' in str(solution) for solution in solutions)


def test_einstein_puzzle():
    rules_text = """
        exists(A, list(A, _, _, _, _)).
        exists(A, list(_, A, _, _, _)).
        exists(A, list(_, _, A, _, _)).
        exists(A, list(_, _, _, A, _)).
        exists(A, list(_, _, _, _, A)).

        rightOf(R, L, list(L, R, _, _, _)).
        rightOf(R, L, list(_, L, R, _, _)).
        rightOf(R, L, list(_, _, L, R, _)).
        rightOf(R, L, list(_, _, _, L, R)).

        middle(A, list(_, _, A, _, _)).

        first(A, list(A, _, _, _, _)).

        nextTo(A, B, list(B, A, _, _, _)).
        nextTo(A, B, list(_, B, A, _, _)).
        nextTo(A, B, list(_, _, B, A, _)).
        nextTo(A, B, list(_, _, _, B, A)).
        nextTo(A, B, list(A, B, _, _, _)).
        nextTo(A, B, list(_, A, B, _, _)).
        nextTo(A, B, list(_, _, A, B, _)).
        nextTo(A, B, list(_, _, _, A, B)).

        puzzle(Houses) :-
              exists(house(red, english, _, _, _), Houses),
              exists(house(_, spaniard, _, _, dog), Houses),
              exists(house(green, _, coffee, _, _), Houses),
              exists(house(_, ukrainian, tea, _, _), Houses),
              rightOf(house(green, _, _, _, _),
              house(ivory, _, _, _, _), Houses),
              exists(house(_, _, _, oldgold, snails), Houses),
              exists(house(yellow, _, _, kools, _), Houses),
              middle(house(_, _, milk, _, _), Houses),
              first(house(_, norwegian, _, _, _), Houses),
              nextTo(house(_, _, _, chesterfield, _), house(_, _, _, _, fox), Houses),
              nextTo(house(_, _, _, kools, _),house(_, _, _, _, horse), Houses),
              exists(house(_, _, orangejuice, luckystike, _), Houses),
              exists(house(_, japanese, _, parliament, _), Houses),
              nextTo(house(_, norwegian, _, _, _), house(blue, _, _, _, _), Houses),
              exists(house(_, _, water, _, _), Houses),
              exists(house(_, _, _, _, zebra), Houses).

        solution(WaterDrinker, ZebraOwner) :-
              puzzle(Houses),
              exists(house(_, WaterDrinker, water, _, _), Houses),
              exists(house(_, ZebraOwner, _, _, zebra), Houses).
    """

    query_text = """
        solution(WaterDrinker, ZebraOwner)
    """

    solver = Solver(rules_text)
    solutions = solver.find_solutions(query_text)

    assert any('norwegian' in str(solution) for solution in solutions.get('WaterDrinker'))
    assert any('japanese' in str(solution) for solution in solutions.get('ZebraOwner'))


def test_alternate_einstein_puzzle():
    rules_text = """
        exists(A, list(A, _, _, _, _)).
        exists(A, list(_, A, _, _, _)).
        exists(A, list(_, _, A, _, _)).
        exists(A, list(_, _, _, A, _)).
        exists(A, list(_, _, _, _, A)).

        rightOf(R, L, list(L, R, _, _, _)).
        rightOf(R, L, list(_, L, R, _, _)).
        rightOf(R, L, list(_, _, L, R, _)).
        rightOf(R, L, list(_, _, _, L, R)).

        middle(A, list(_, _, A, _, _)).

        first(A, list(A, _, _, _, _)).

        nextTo(A, B, list(B, A, _, _, _)).
        nextTo(A, B, list(_, B, A, _, _)).
        nextTo(A, B, list(_, _, B, A, _)).
        nextTo(A, B, list(_, _, _, B, A)).
        nextTo(A, B, list(A, B, _, _, _)).
        nextTo(A, B, list(_, A, B, _, _)).
        nextTo(A, B, list(_, _, A, B, _)).
        nextTo(A, B, list(_, _, _, A, B)).

        puzzle(Houses) :-
              exists(house(red, british, _, _, _), Houses),
              exists(house(_, swedish, _, _, dog), Houses),
              exists(house(green, _, coffee, _, _), Houses),
              exists(house(_, danish, tea, _, _), Houses),
              rightOf(house(white, _, _, _, _), house(green, _, _, _, _), Houses),
              exists(house(_, _, _, pall_mall, bird), Houses),
              exists(house(yellow, _, _, dunhill, _), Houses),
              middle(house(_, _, milk, _, _), Houses),
              first(house(_, norwegian, _, _, _), Houses),
              nextTo(house(_, _, _, blend, _), house(_, _, _, _, cat), Houses),
              nextTo(house(_, _, _, dunhill, _),house(_, _, _, _, horse), Houses),
              exists(house(_, _, beer, bluemaster, _), Houses),
              exists(house(_, german, _, prince, _), Houses),
              nextTo(house(_, norwegian, _, _, _), house(blue, _, _, _, _), Houses),
              nextTo(house(_, _, _, blend, _), house(_, _, water_, _, _), Houses).

        solution(FishOwner) :-
          puzzle(Houses),
          exists(house(_, FishOwner, _, _, fish), Houses).
    """

    query_text = """
        solution(FishOwner)
    """

    solver = Solver(rules_text)
    solutions = solver.find_solutions(query_text)

    assert len(solutions.get('FishOwner')) == 1
    assert 'german' in [str(solution) for solution in solutions.get('FishOwner')]

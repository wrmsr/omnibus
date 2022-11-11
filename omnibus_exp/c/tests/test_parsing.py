from .. import parsing


def test_parsing():
    for s in [
        'int main(const int argc, const char * const *argv) {\nreturn 0;\n}\n',
    ]:
        print(s)
        print(parsing.parse(s))
        print()

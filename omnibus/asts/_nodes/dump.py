import ast
import typing as ta


def main() -> None:
    clss: ta.Set[type] = {
        obj
        for att in dir(ast)
        for obj in [getattr(ast, att, None)]
        if isinstance(obj, type) and issubclass(obj, ast.AST)
    }

    sclss: ta.Dict[type, ta.Set[type]] = {}
    for cls in clss:
        for bcls in cls.__bases__:
            if bcls in clss:
                sclss.setdefault(bcls, set()).add(cls)

    def dump(cls, indent):
        print(('  ' * indent) + cls.__name__)
        for scls in sorted(sclss.get(cls, []), key=lambda sc: sc.__name__):
            dump(scls, indent + 1)
    dump(ast.AST, 0)


if __name__ == '__main__':
    main()

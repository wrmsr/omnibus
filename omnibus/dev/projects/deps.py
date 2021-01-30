import dataclasses as dc
import logging
import os.path

from ... import argparse as ap
from ... import logs
from ..deps import files as dfs
from ..deps import parsing as dp
from ..deps import pip as dpi


log = logging.getLogger(__name__)


class Cli(ap.Cli):

    @ap.command(
        ap.arg('req_file', metavar='req-file'),
        ap.arg('-W', '--write', action='store_true'),
        ap.arg('--interp'),
    )
    def updates(self) -> None:
        fp = os.path.abspath(self.args.req_file)
        de = dfs.read_dep_env(fp)

        explicit_dep_names = {d.name for d in de.deps}
        pinned_dep_names = {d.name for d in de.deps if any(v.op == '==' for v in d.vers)}

        interp = None
        if self.args.interp:
            interp = os.path.expanduser(self.args.interp)
        pip_deps = dpi.get_pip_deps(interp=interp)

        updated = set()

        file_rewrites = {}
        for df in de.files:
            new_lines = []
            for line in df.lines:
                if (
                        isinstance(line, dfs.DepLine) and
                        'auto' in line.hot_comments and
                        line.dep.name in pip_deps.by_name
                ):
                    pip_dep = pip_deps.by_name[line.dep.name]
                    if len(line.dep.vers) == 1 and line.dep.vers[0] != pip_dep.latest_version:
                        line = dc.replace(
                            line,
                            dep=dc.replace(
                                line.dep,
                                vers=[dp.Version('==', pip_dep.latest_version)],
                            ),
                        )
                        updated.add(line.dep.name)

                new_lines.append(dfs.render_line(line))

            file_rewrites[df.path] = '\n'.join([*new_lines, ''])

        if self.args.write:
            for p, s in file_rewrites.items():
                with open(p, 'w') as f:
                    f.write(s)

        disp_labels = ['Package', 'Version', 'Latest', 'Type']
        disp_atts = ['name', 'version', 'latest_version', 'latest_filetype']

        ps = [
            max([len(l)] + [len(getattr(e, k)) for e in pip_deps if e.name not in updated])
            for l, k in zip(disp_labels, disp_atts)
        ]
        print(' '.join(l.ljust(p) for l, p in zip(disp_labels, ps)))

        for pred in [
            lambda n: n in pinned_dep_names,
            lambda n: n not in pinned_dep_names and n in explicit_dep_names,
            lambda n: n not in pinned_dep_names and n not in explicit_dep_names,
        ]:
            print(' '.join('-' * p for p in ps))
            for e in pip_deps:
                if e.name not in updated and pred(e.name.lower()):
                    print(' '.join(getattr(e, k).ljust(p) for k, p in zip(disp_atts, ps)))


def main():
    logs.configure_standard_logging(logging.INFO)
    cli = Cli()
    cli()


if __name__ == '__main__':
    main()

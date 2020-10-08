# .venv/bin/pip list -o --format=json
import json
import re
import sys
dct = json.loads(sys.stdin.read())
vers = {e['name']: e['latest_version'] for e in dct}
rpls = [(re.compile(rf'^{n}==[0-9a-zA-Z\-_\.]+[ ]+#@auto$'), f'{n}=={v}  #@auto') for n, v in vers.items()]
for fn in ['requirements.txt', 'requirements-dev.txt', 'requirements-exp.txt']:
    with open(fn, 'r') as f:
        lines = f.readlines()
    rlines = []
    for line in lines:
        for pat, rpl in rpls:
            if pat.fullmatch(line.strip()):
                rlines.append(rpl + '\n')
                break
        else:
            rlines.append(line)
    with open(fn, 'w') as f:
        f.write(''.join(rlines))

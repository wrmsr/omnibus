# .venv/bin/pip list -o --format=json
import json
import re
dct = json.loads('[{"name": "awscli", "version": "1.18.155", "latest_version": "1.18.156", "latest_filetype": "wheel"}, {"name": "boto3", "version": "1.15.14", "latest_version": "1.15.15", "latest_filetype": "wheel"}, {"name": "boto3-stubs", "version": "1.15.14.0", "latest_version": "1.15.15.0", "latest_filetype": "wheel"}, {"name": "botocore", "version": "1.18.14", "latest_version": "1.18.15", "latest_filetype": "wheel"}, {"name": "ddtrace", "version": "0.42.0", "latest_version": "0.43.0", "latest_filetype": "wheel"}]')
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
    print(''.join(rlines))
    print()

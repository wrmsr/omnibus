import json
lst = json.loads('[{"name": "awscli", "version": "1.18.155", "latest_version": "1.18.156", "latest_filetype": "wheel"}, {"name": "boto3", "version": "1.15.14", "latest_version": "1.15.15", "latest_filetype": "wheel"}, {"name": "boto3-stubs", "version": "1.15.14.0", "latest_version": "1.15.15.0", "latest_filetype": "wheel"}, {"name": "botocore", "version": "1.18.14", "latest_version": "1.18.15", "latest_filetype": "wheel"}, {"name": "ddtrace", "version": "0.42.0", "latest_version": "0.43.0", "latest_filetype": "wheel"}]')
ls = ['Package', 'Version', 'Latest', 'Type']
ks = ['name', 'version', 'latest_version', 'latest_filetype']
ps = [max([len(l)] + [len(e[k]) for e in lst]) for l, k in zip(ls, ks)]
print(' '.join(l.ljust(p) for l, p in zip(ls, ps)))
print(' '.join('-' * p for p in ps))
for e in lst:
    print(' '.join(e[k].ljust(p) for k, p in zip(ks, ps)))

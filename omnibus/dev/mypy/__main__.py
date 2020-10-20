import re
import sys


from mypy.__main__ import console_entry


sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
console_entry()

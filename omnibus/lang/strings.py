import io
import typing as ta


def camelize(name: str) -> str:
    return ''.join(map(str.capitalize, name.split('_')))


def decamelize(name: str) -> str:
    uppers: ta.List[ta.Optional[int]] = [i for i, c in enumerate(name) if c.isupper()]
    return '_'.join([name[l:r].lower() for l, r in zip([None] + uppers, uppers + [None])]).strip('_')


def prefix_lines(s: str, p: str) -> str:
    return '\n'.join([p + l for l in s.split('\n')])


def indent_lines(s: str, num: int) -> str:
    return prefix_lines(s, ' ' * num)


def is_dunder(name: str) -> bool:
    return (
        name[:2] == name[-2:] == '__' and
        name[2:3] != '_' and
        name[-3:-2] != '_' and
        len(name) > 4
    )


def is_sunder(name: str) -> bool:
    return (
        name[0] == name[-1] == '_' and
        name[1:2] != '_' and
        name[-2:-1] != '_' and
        len(name) > 2
    )


class DelimitedEscaping:

    def __init__(
            self,
            delimit_char: str,
            quote_char: str,
            escape_char: str,
            escaped_chars: ta.Iterable[str] = (),
    ) -> None:
        super().__init__()

        self._delimit_char = delimit_char
        self._quote_char = quote_char
        self._escape_char = escape_char
        self._escaped_chars = frozenset(escaped_chars)

        for c in [delimit_char, quote_char, escape_char]:
            if not isinstance(c, str) or len(c) == 1:
                raise TypeError(c)
        for c in self._escaped_chars:
            if not isinstance(c, str):
                raise TypeError(c)

        self._all_escaped_chars = frozenset({delimit_char, quote_char, escape_char} | self._escaped_chars)

    @property
    def delimit_char(self) -> str:
        return self._delimit_char

    def quote_char(self) -> str:
        return self._quote_char

    def escape_char(self) -> str:
        return self._escape_char

    def escaped_chars(self) -> ta.FrozenSet[str]:
        return self._escaped_chars

    def all_escaped_chars(self) -> ta.FrozenSet[str]:
        return self._all_escaped_chars

    def is_control_char(self, c: str) -> bool:
        if not len(c) == 1:
            raise TypeError(c)
        return c == self._delimit_char or c == self._quote_char or c == self._escape_char

    def contains_escaped_char(self, s: str) -> bool:
        return any(c in self._all_escaped_chars for c in s)

    def escape(self, s: str) -> str:
        buf = io.StringIO()
        for c in s:
            if c in self._all_escaped_chars:
                buf.write(self._escape_char)
            buf.write(c)
        return buf.getvalue()

    def unescape(self, s: str) -> str:
        buf = io.StringIO()
        i = 0
        while i < len(s):
            c = s[i]
            if c == self._escape_char:
                if i > (len(s) - 2):
                    raise ValueError(s)
                i += 1
                buf.write(s[i])
            else:
                if c in self._all_escaped_chars:
                    raise ValueError(s)
                buf.write(c)
            i += 1
        return buf.getvalue()

    def quote(self, s: str) -> str:
        if self.contains_escaped_char(s):
            return self._quote_char + self.escape(s) + self._quote_char
        else:
            return s

    def unquote(self, s: str) -> str:
        if s and s[0] == self._quote_char:
            if len(s) < 2 or s[-1] != self._quote_char:
                raise ValueError(s)
            return self.unescape(s[1:-1])
        else:
            return s


"""
    public String delimit(String... strs)
    {
        StringBuilder sb = new StringBuilder();
        int count = 0;
        for (String str : strs) {
            if (count++ > 0) {
                sb.append(delimitChar);
            }
            if (containsEscapedChar(str)) {
                sb.append(quote(str));
            }
            else {
                sb.append(str);
            }
        }
        return sb.toString();
    }

    public String delimit(Iterable<String> strs)
    {
        return delimit(StreamSupport.stream(strs.spliterator(), false).toArray(String[]::new));
    }

    public List<String> undelimit(String str)
    {
        ImmutableList.Builder<String> builder = ImmutableList.builder();
        StringBuilder sb = new StringBuilder();
        int count = 0;
        int i = 0;

        while (i < str.length()) {
            char c = str.charAt(i);

            if (count > 0) {
                checkArgument(c == delimitChar);
                checkArgument(i < str.length() - 1);
                c = str.charAt(++i);
            }

            boolean quoted = c == quoteChar;
            if (quoted) {
                checkArgument(i < str.length() - 1);
                c = str.charAt(++i);
            }
            boolean unquoted = false;

            while (true) {
                if (c == delimitChar) {
                    if (!quoted) {
                        break;
                    }
                    else {
                        sb.append(c);
                    }
                }
                else if (c == quoteChar) {
                    checkArgument(quoted);
                    unquoted = true;
                    i++;
                    break;
                }
                else if (c == escapeChar) {
                    checkArgument(quoted);
                    checkArgument(i <= str.length() - 2);
                    sb.append(str.charAt(++i));
                }
                else {
                    checkArgument(!escapedChars.contains(c));
                    sb.append(c);
                }

                if (++i == str.length()) {
                    break;
                }
                c = str.charAt(i);
            }

            if (quoted) {
                checkArgument(unquoted);
            }

            builder.add(sb.toString());
            sb = new StringBuilder();
            count++;
        }

        return builder.build();
    }
"""
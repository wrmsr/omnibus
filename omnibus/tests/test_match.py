from .. import match as oma


def test_match():
    capture = oma.Capture()
    pattern = oma.Pattern.typed(int).captured(capture)
    match = oma.DefaultMatcher().match(pattern, 5)
    assert match.captures.get(capture) == 5

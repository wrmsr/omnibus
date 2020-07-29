"""
MIT License

Copyright (c) 2017 Gu Pengfei

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from .. import pcre2


def test_abc():
    p = pcre2.PCRE2(r'hello.+'.encode())
    match = p.search('this is hello world.'.encode())
    assert match is not None
    match = p.search('this should be not found.'.encode())
    assert match is None


def test_group():
    content = 'this is hello world.'.encode()

    p = pcre2.PCRE2('hello.+'.encode())
    match = p.search(content)
    assert match.group(0) == b'hello world.'

    p = pcre2.PCRE2(r'(hello)(.+)'.encode())
    match = p.search(content)
    assert match.group(0) == b'hello world.'
    assert match.group(1) == b'hello'
    assert match.group(2) == b' world.'
    assert list(match.groups()) == [b'hello', b' world.']


def test_chinese():
    content = '我来到北京敏感词广场，请遵守中华人民共和国法律.'.encode()
    p = pcre2.PCRE2(r'共和国.+'.encode())
    match = p.search(content)
    assert match.group(0) == '共和国法律.'.encode()

    p = pcre2.PCRE2(r'(北京)(\w+)广场'.encode())
    match = p.search(content)
    assert match is None

    p = pcre2.PCRE2(r'(北京)(\w+)广场'.encode(), pcre2.UTF | pcre2.UCP)
    match = p.search(content)
    assert match.group(0) == '北京敏感词广场'.encode()
    assert match.group(1) == '北京'.encode()
    assert match.group(2) == '敏感词'.encode()
    assert list(match.groups()) == ['北京'.encode(), '敏感词'.encode()]

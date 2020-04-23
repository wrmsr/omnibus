# flake8: noqa
from ... import lang


class Examples(lang.ValueEnum):
    """
    https://github.com/chyh1990/yaml-rust/blob/360a34d75bb64357cfdbc5bb706bcde9a0ecbc23/tests/specexamples.rs.inc
    """

    EX2_1 = "- Mark McGwire\n- Sammy Sosa\n- Ken Griffey"
    EX2_2 = "hr:  65    # Home runs\navg: 0.278 # Batting average\nrbi: 147   # Runs Batted In"
    EX2_3 = "american:\n- Boston Red Sox\n- Detroit Tigers\n- New York Yankees\nnational:\n- New York Mets\n- Chicago Cubs\n- Atlanta Braves"
    EX2_4 = "-\n  name: Mark McGwire\n  hr:   65\n  avg:  0.278\n-\n  name: Sammy Sosa\n  hr:   63\n  avg:  0.288"
    EX2_5 = "- [name        , hr, avg  ]\n- [Mark McGwire, 65, 0.278]\n- [Sammy Sosa  , 63, 0.288]"
    EX2_6 = "Mark McGwire: {hr: 65, avg: 0.278}\nSammy Sosa: {\n    hr: 63,\n    avg: 0.288\n  }"
    EX2_7 = "# Ranking of 1998 home runs\n---\n- Mark McGwire\n- Sammy Sosa\n- Ken Griffey\n\n# Team ranking\n---\n- Chicago Cubs\n- St Louis Cardinals"
    EX2_8 = "---\ntime: 20:03:20\nplayer: Sammy Sosa\naction: strike (miss)\n...\n---\ntime: 20:03:47\nplayer: Sammy Sosa\naction: grand slam\n..."
    EX2_9 = "---\nhr: # 1998 hr ranking\n  - Mark McGwire\n  - Sammy Sosa\nrbi:\n  # 1998 rbi ranking\n  - Sammy Sosa\n  - Ken Griffey"
    EX2_10 = "---\nhr:\n  - Mark McGwire\n  # Following node labeled SS\n  - &SS Sammy Sosa\nrbi:\n  - *SS # Subsequent occurrence\n  - Ken Griffey"
    EX2_11 = "? - Detroit Tigers\n  - Chicago cubs\n:\n  - 2001-07-23\n\n? [ New York Yankees,\n    Atlanta Braves ]\n: [ 2001-07-02, 2001-08-12,\n    2001-08-14 ]"
    EX2_12 = "---\n# Products purchased\n- item    : Super Hoop\n  quantity: 1\n- item    : Basketball\n  quantity: 4\n- item    : Big Shoes\n  quantity: 1"
    EX2_13 = "# ASCII Art\n--- |\n  \\//||\\/||\n  // ||  ||__"
    EX2_14 = "--- >\n  Mark McGwire's\n  year was crippled\n  by a knee injury."
    EX2_15 = ">\n Sammy Sosa completed another\n fine season with great stats.\n \n   63 Home Runs\n   0.288 Batting Average\n \n What a year!"
    EX2_16 = "name: Mark McGwire\naccomplishment: >\n  Mark set a major league\n  home run record in 1998.\nstats: |\n  65 Home Runs\n  0.278 Batting Average\n"
    EX2_17 = "unicode: \"Sosa did fine.\\u263A\"\ncontrol: \"\\b1998\\t1999\\t2000\\n\"\nhex esc: \"\\x0d\\x0a is \\r\\n\"\n\nsingle: '\"Howdy!\" he cried.'\nquoted: ' # Not a ''comment''.'\ntie-fighter: '|\\-*-/|'"
    EX2_18 = "plain:\n  This unquoted scalar\n  spans many lines.\n\nquoted: \"So does this\n  quoted scalar.\\n\""
    EX2_23 = "---\nnot-date: !!str 2002-04-28\n\npicture: !!binary |\n R0lGODlhDAAMAIQAAP//9/X\n 17unp5WZmZgAAAOfn515eXv\n Pz7Y6OjuDg4J+fn5OTk6enp\n 56enmleECcgggoBADs=\n\napplication specific tag: !something |\n The semantics of the tag\n above may be different for\n different documents."
    EX2_24 = "%TAG ! tag:clarkevans.com,2002:\n--- !shape\n  # Use the ! handle for presenting\n  # tag:clarkevans.com,2002:circle\n- !circle\n  center: &ORIGIN {x: 73, y: 129}\n  radius: 7\n- !line\n  start: *ORIGIN\n  finish: { x: 89, y: 102 }\n- !label\n  start: *ORIGIN\n  color: 0xFFEEBB\n  text: Pretty vector drawing."
    EX2_25 = "# Sets are represented as a\n# Mapping where each key is\n# associated with a null value\n--- !!set\n? Mark McGwire\n? Sammy Sosa\n? Ken Griffey"
    EX2_26 = "# Ordered maps are represented as\n# A sequence of mappings, with\n# each mapping having one key\n--- !!omap\n- Mark McGwire: 65\n- Sammy Sosa: 63\n- Ken Griffey: 58"
    EX2_27 = "--- !<tag:clarkevans.com,2002:invoice>\ninvoice: 34843\ndate   : 2001-01-23\nbill-to: &id001\n    given  : Chris\n    family : Dumars\n    address:\n        lines: |\n            458 Walkman Dr.\n            Suite #292\n        city    : Royal Oak\n        state   : MI\n        postal  : 48046\nship-to: *id001\nproduct:\n    - sku         : BL394D\n      quantity    : 4\n      description : Basketball\n      price       : 450.00\n    - sku         : BL4438H\n      quantity    : 1\n      description : Super Hoop\n      price       : 2392.00\ntax  : 251.42\ntotal: 4443.52\ncomments:\n    Late afternoon is best.\n    Backup contact is Nancy\n    Billsmer @ 338-4338."
    EX2_28 = "---\nTime: 2001-11-23 15:01:42 -5\nUser: ed\nWarning:\n  This is an error message\n  for the log file\n---\nTime: 2001-11-23 15:02:31 -5\nUser: ed\nWarning:\n  A slightly different error\n  message.\n---\nDate: 2001-11-23 15:03:17 -5\nUser: ed\nFatal:\n  Unknown variable \"bar\"\nStack:\n  - file: TopClass.py\n    line: 23\n    code: |\n      x = MoreObject(\"345\\n\")\n  - file: MoreClass.py\n    line: 58\n    code: |-\n      foo = bar"
    EX5_3 = "sequence:\n- one\n- two\nmapping:\n  ? sky\n  : blue\n  sea : green"
    EX5_4 = "sequence: [ one, two, ]\nmapping: { sky: blue, sea: green }"
    EX5_5 = "# Comment only."
    EX5_6 = "anchored: !local &anchor value\nalias: *anchor"
    EX5_7 = "literal: |\n  some\n  text\nfolded: >\n  some\n  text\n"
    EX5_8 = "single: 'text'\ndouble: \"text\""
    EX5_11 = "|\n  Line break (no glyph)\n  Line break (glyphed)\n"
    EX5_12 = "# Tabs and spaces\nquoted: \"Quoted\t\"\nblock:	|\n  void main() {\n  \tprintf(\"Hello, world!\\n\");\n  }"
    EX5_13 = "\"Fun with \\\\\n\\\" \\a \\b \\e \\f \\\n\\n \\r \\t \\v \\0 \\\n\\  \\_ \\N \\L \\P \\\n\\x41 \\u0041 \\U00000041\""
    EX5_14 = "Bad escapes:\n  \"\\c\n  \\xq-\""
    EX6_1 = "  # Leading comment line spaces are\n   # neither content nor indentation.\n    \nNot indented:\n By one space: |\n    By four\n      spaces\n Flow style: [    # Leading spaces\n   By two,        # in flow style\n  Also by two,    # are neither\n  \tStill by two   # content nor\n    ]             # indentation."
    EX6_2 = "? a\n: -\tb\n  -  -\tc\n     - d"
    EX6_3 = "- foo:\t bar\n- - baz\n  -\tbaz"
    EX6_4 = "plain: text\n  lines\nquoted: \"text\n  \tlines\"\nblock: |\n  text\n   \tlines\n"
    EX6_5 = "Folding:\n  \"Empty line\n   \t\n  as a line feed\"\nChomping: |\n  Clipped empty lines\n "
    EX6_6 = ">-\n  trimmed\n  \n \n\n  as\n  space"
    EX6_7 = ">\n  foo \n \n  \t bar\n\n  baz\n"
    EX6_8 = "\"\n  foo \n \n  \t bar\n\n  baz\n\""
    EX6_9 = "key:    # Comment\n  value"
    EX6_10 = "  # Comment\n   \n\n"
    EX6_11 = "key:    # Comment\n        # lines\n  value\n\n"
    EX6_12 = "{ first: Sammy, last: Sosa }:\n# Statistics:\n  hr:  # Home runs\n     65\n  avg: # Average\n   0.278"
    EX6_13 = "%FOO  bar baz # Should be ignored\n               # with a warning.\n--- \"foo\""
    EX6_14 = "%YAML 1.3 # Attempt parsing\n           # with a warning\n---\n\"foo\""
    EX6_15 = "%YAML 1.2\n%YAML 1.1\nfoo"
    EX6_16 = "%TAG !yaml! tag:yaml.org,2002:\n---\n!yaml!str \"foo\""
    EX6_17 = "%TAG ! !foo\n%TAG ! !foo\nbar"
    EX6_18 = "# Private\n!foo \"bar\"\n...\n# Global\n%TAG ! tag:example.com,2000:app/\n---\n!foo \"bar\""
    EX6_19 = "%TAG !! tag:example.com,2000:app/\n---\n!!int 1 - 3 # Interval, not integer"
    EX6_20 = "%TAG !e! tag:example.com,2000:app/\n---\n!e!foo \"bar\""
    EX6_21 = "%TAG !m! !my-\n--- # Bulb here\n!m!light fluorescent\n...\n%TAG !m! !my-\n--- # Color here\n!m!light green"
    EX6_22 = "%TAG !e! tag:example.com,2000:app/\n---\n- !e!foo \"bar\""
    EX6_23 = "!!str &a1 \"foo\":\n  !!str bar\n&a2 baz : *a1"
    EX6_24 = "!<tag:yaml.org,2002:str> foo :\n  !<!bar> baz"
    EX6_25 = "- !<!> foo\n- !<$:?> bar\n"
    EX6_26 = "%TAG !e! tag:example.com,2000:app/\n---\n- !local foo\n- !!str bar\n- !e!tag%21 baz\n"
    EX6_27a = "%TAG !e! tag:example,2000:app/\n---\n- !e! foo"
    EX6_27b = "%TAG !e! tag:example,2000:app/\n---\n- !h!bar baz"
    EX6_28 = "# Assuming conventional resolution:\n- \"12\"\n- 12\n- ! 12"
    EX6_29 = "First occurrence: &anchor Value\nSecond occurrence: *anchor"
    EX7_1 = "First occurrence: &anchor Foo\nSecond occurrence: *anchor\nOverride anchor: &anchor Bar\nReuse anchor: *anchor"
    EX7_2 = "{\n  foo : !!str,\n  !!str : bar,\n}"
    EX7_3 = "{\n  ? foo :,\n  : bar,\n}\n"
    EX7_4 = "\"implicit block key\" : [\n  \"implicit flow key\" : value,\n ]"
    EX7_5 = "\"folded \nto a space,\t\n \nto a line feed, or \t\\\n \\ \tnon-content\""
    EX7_6 = "\" 1st non-empty\n\n 2nd non-empty \n\t3rd non-empty \""
    EX7_7 = " 'here''s to \"quotes\"'"
    EX7_8 = "'implicit block key' : [\n  'implicit flow key' : value,\n ]"
    EX7_9 = "' 1st non-empty\n\n 2nd non-empty \n\t3rd non-empty '"
    EX7_10 = "# Outside flow collection:\n- ::vector\n- \": - ()\"\n- Up, up, and away!\n- -123\n- http://example.com/foo#bar\n# Inside flow collection:\n- [ ::vector,\n  \": - ()\",\n  \"Up, up, and away!\",\n  -123,\n  http://example.com/foo#bar ]"
    EX7_11 = "implicit block key : [\n  implicit flow key : value,\n ]"
    EX7_12 = "1st non-empty\n\n 2nd non-empty \n\t3rd non-empty"
    EX7_13 = "- [ one, two, ]\n- [three ,four]"
    EX7_14 = "[\n\"double\n quoted\", 'single\n           quoted',\nplain\n text, [ nested ],\nsingle: pair,\n]"
    EX7_15 = "- { one : two , three: four , }\n- {five: six,seven : eight}"
    EX7_16 = "{\n? explicit: entry,\nimplicit: entry,\n?\n}"
    EX7_17 = "{\nunquoted : \"separate\",\nhttp://foo.com,\nomitted value:,\n: omitted key,\n}"
    EX7_18 = "{\n\"adjacent\":value,\n\"readable\":value,\n\"empty\":\n}"
    EX7_19 = "[\nfoo: bar\n]"
    EX7_20 = "[\n? foo\n bar : baz\n]"
    EX7_21 = "- [ YAML : separate ]\n- [ : empty key entry ]\n- [ {JSON: like}:adjacent ]"
    EX7_22 = "[ foo\n bar: invalid,"  # Note: we don't check (on purpose) the >1K chars for an implicit key
    EX7_23 = "- [ a, b ]\n- { a: b }\n- \"a\"\n- 'b'\n- c"
    EX7_24 = "- !!str \"a\"\n- 'b'\n- &anchor \"c\"\n- *anchor\n- !!str"
    EX8_1 = "- | # Empty header\n literal\n- >1 # Indentation indicator\n  folded\n- |+ # Chomping indicator\n keep\n\n- >1- # Both indicators\n  strip\n"
    EX8_2 = "- |\n detected\n- >\n \n  \n  # detected\n- |1\n  explicit\n- >\n \t\n detected\n"
    EX8_3a = "- |\n  \n text"
    EX8_3b = "- >\n  text\n text"
    EX8_3c = "- |2\n text"
    EX8_4 = "strip: |-\n  text\nclip: |\n  text\nkeep: |+\n  text\n"
    EX8_5 = " # Strip\n  # Comments:\nstrip: |-\n  # text\n  \n # Clip\n  # comments:\n\nclip: |\n  # text\n \n # Keep\n  # comments:\n\nkeep: |+\n  # text\n\n # Trail\n  # Comments\n"
    EX8_6 = "strip: >-\n\nclip: >\n\nkeep: |+\n\n"
    EX8_7 = "|\n literal\n \ttext\n\n"
    EX8_8 = "|\n \n  \n  literal\n   \n  \n  text\n\n # Comment\n"
    EX8_9 = ">\n folded\n text\n\n"
    EX8_10 = ">\n\n folded\n line\n\n next\n line\n   * bullet\n\n   * list\n   * lines\n\n last\n line\n\n# Comment\n"
    EX8_11 = EX8_10
    EX8_12 = EX8_10
    EX8_13 = EX8_10
    EX8_14 = "block sequence:\n  - one\n  - two : three\n"
    EX8_15 = "- # Empty\n- |\n block node\n- - one # Compact\n  - two # sequence\n- one: two # Compact mapping\n"
    EX8_16 = "block mapping:\n key: value\n"
    EX8_17 = "? explicit key # Empty value\n? |\n  block key\n: - one # Explicit compact\n  - two # block value\n"
    EX8_18 = "plain key: in-line value\n:  # Both empty\n\"quoted key\":\n- entry\n"
    EX8_19 = "- sun: yellow\n- ? earth: blue\n  : moon: white\n"
    EX8_20 = "-\n  \"flow in block\"\n- >\n Block scalar\n- !!map # Block collection\n  foo : bar\n"
    EX8_21 = "literal: |2\n  value\nfolded:\n   !foo\n  >1\n value\n"
    EX8_22 = "sequence: !!seq\n- entry\n- !!seq\n - nested\nmapping: !!map\n foo: bar\n"

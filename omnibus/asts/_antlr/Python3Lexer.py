# flake8: noqa
# Generated from Python3.g4 by ANTLR 4.8
from ..._vendor.antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


from ..._vendor.antlr4.Token import CommonToken
import re
import importlib

# Allow languages to extend the lexer and parser, by loading the parser dynamically
module_path = __name__[:-5]
language_name = __name__.split('.')[-1]
language_name = language_name[:-5]  # Remove Lexer from name
LanguageParser = getattr(importlib.import_module('{}Parser'.format(module_path)), '{}Parser'.format(language_name))



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2c")
        buf.write("\u0385\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\t")
        buf.write("C\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\4J\tJ\4K\tK\4L\t")
        buf.write("L\4M\tM\4N\tN\4O\tO\4P\tP\4Q\tQ\4R\tR\4S\tS\4T\tT\4U\t")
        buf.write("U\4V\tV\4W\tW\4X\tX\4Y\tY\4Z\tZ\4[\t[\4\\\t\\\4]\t]\4")
        buf.write("^\t^\4_\t_\4`\t`\4a\ta\4b\tb\4c\tc\4d\td\4e\te\4f\tf\4")
        buf.write("g\tg\4h\th\4i\ti\4j\tj\4k\tk\4l\tl\4m\tm\4n\tn\4o\to\4")
        buf.write("p\tp\4q\tq\4r\tr\4s\ts\4t\tt\4u\tu\4v\tv\4w\tw\4x\tx\4")
        buf.write("y\ty\4z\tz\4{\t{\4|\t|\4}\t}\3\2\3\2\5\2\u00fe\n\2\3\3")
        buf.write("\3\3\3\3\5\3\u0103\n\3\3\4\3\4\3\4\3\4\5\4\u0109\n\4\3")
        buf.write("\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3")
        buf.write("\t\3\t\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\13\3\13")
        buf.write("\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3")
        buf.write("\r\3\r\3\r\3\16\3\16\3\16\3\17\3\17\3\17\3\17\3\17\3\20")
        buf.write("\3\20\3\20\3\20\3\20\3\21\3\21\3\21\3\21\3\21\3\21\3\22")
        buf.write("\3\22\3\22\3\22\3\23\3\23\3\23\3\24\3\24\3\24\3\24\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\30\3\30\3\30")
        buf.write("\3\30\3\30\3\30\3\30\3\31\3\31\3\31\3\32\3\32\3\32\3\32")
        buf.write("\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\35\3\35\3\35\3\35")
        buf.write("\3\35\3\36\3\36\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3\37")
        buf.write("\3\37\3 \3 \3 \3 \3 \3 \3!\3!\3!\3!\3!\3!\3\"\3\"\3\"")
        buf.write("\3\"\3#\3#\3#\3#\3#\3$\3$\3$\3$\3$\3$\3$\3$\3$\3%\3%\3")
        buf.write("%\3%\3%\3%\3&\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3\'\3\'\3")
        buf.write("(\3(\3(\5(\u01cc\n(\3(\3(\5(\u01d0\n(\3(\5(\u01d3\n(\5")
        buf.write("(\u01d5\n(\3(\3(\3)\3)\7)\u01db\n)\f)\16)\u01de\13)\3")
        buf.write("*\3*\3*\3*\3*\5*\u01e5\n*\3*\3*\5*\u01e9\n*\3+\3+\3+\3")
        buf.write("+\3+\5+\u01f0\n+\3+\3+\5+\u01f4\n+\3,\3,\5,\u01f8\n,\3")
        buf.write(",\7,\u01fb\n,\f,\16,\u01fe\13,\3,\6,\u0201\n,\r,\16,\u0202")
        buf.write("\5,\u0205\n,\3-\3-\3-\6-\u020a\n-\r-\16-\u020b\3.\3.\3")
        buf.write(".\6.\u0211\n.\r.\16.\u0212\3/\3/\3/\6/\u0218\n/\r/\16")
        buf.write("/\u0219\3\60\3\60\5\60\u021e\n\60\3\61\3\61\5\61\u0222")
        buf.write("\n\61\3\61\3\61\3\62\3\62\3\63\3\63\3\63\3\63\3\64\3\64")
        buf.write("\3\65\3\65\3\65\3\66\3\66\3\66\3\67\3\67\38\38\39\39\3")
        buf.write(":\3:\3:\3;\3;\3<\3<\3<\3=\3=\3=\3>\3>\3?\3?\3@\3@\3A\3")
        buf.write("A\3A\3B\3B\3B\3C\3C\3D\3D\3E\3E\3F\3F\3G\3G\3G\3H\3H\3")
        buf.write("I\3I\3I\3J\3J\3J\3K\3K\3L\3L\3M\3M\3M\3N\3N\3N\3O\3O\3")
        buf.write("O\3P\3P\3P\3Q\3Q\3Q\3R\3R\3S\3S\3S\3T\3T\3T\3U\3U\3U\3")
        buf.write("V\3V\3V\3W\3W\3W\3X\3X\3X\3Y\3Y\3Y\3Z\3Z\3Z\3[\3[\3[\3")
        buf.write("\\\3\\\3\\\3]\3]\3]\3]\3^\3^\3^\3^\3_\3_\3_\3_\3`\3`\3")
        buf.write("`\3`\3a\3a\3a\5a\u02aa\na\3a\3a\3b\3b\3c\3c\3c\7c\u02b3")
        buf.write("\nc\fc\16c\u02b6\13c\3c\3c\3c\3c\7c\u02bc\nc\fc\16c\u02bf")
        buf.write("\13c\3c\5c\u02c2\nc\3d\3d\3d\3d\3d\7d\u02c9\nd\fd\16d")
        buf.write("\u02cc\13d\3d\3d\3d\3d\3d\3d\3d\3d\7d\u02d6\nd\fd\16d")
        buf.write("\u02d9\13d\3d\3d\3d\5d\u02de\nd\3e\3e\5e\u02e2\ne\3f\3")
        buf.write("f\3g\3g\3g\3g\5g\u02ea\ng\3h\3h\3i\3i\3j\3j\3k\3k\3l\3")
        buf.write("l\3m\5m\u02f7\nm\3m\3m\3m\3m\5m\u02fd\nm\3n\3n\5n\u0301")
        buf.write("\nn\3n\3n\3o\3o\5o\u0307\no\3o\7o\u030a\no\fo\16o\u030d")
        buf.write("\13o\3p\3p\3p\5p\u0312\np\3p\7p\u0315\np\fp\16p\u0318")
        buf.write("\13p\3q\3q\5q\u031c\nq\3q\3q\5q\u0320\nq\3q\7q\u0323\n")
        buf.write("q\fq\16q\u0326\13q\3r\3r\3r\7r\u032b\nr\fr\16r\u032e\13")
        buf.write("r\3r\3r\3r\3r\7r\u0334\nr\fr\16r\u0337\13r\3r\5r\u033a")
        buf.write("\nr\3s\3s\3s\3s\3s\7s\u0341\ns\fs\16s\u0344\13s\3s\3s")
        buf.write("\3s\3s\3s\3s\3s\3s\7s\u034e\ns\fs\16s\u0351\13s\3s\3s")
        buf.write("\3s\5s\u0356\ns\3t\3t\5t\u035a\nt\3u\5u\u035d\nu\3v\5")
        buf.write("v\u0360\nv\3w\5w\u0363\nw\3x\3x\3x\3y\6y\u0369\ny\ry\16")
        buf.write("y\u036a\3z\3z\7z\u036f\nz\fz\16z\u0372\13z\3{\3{\5{\u0376")
        buf.write("\n{\3{\5{\u0379\n{\3{\3{\5{\u037d\n{\3|\5|\u0380\n|\3")
        buf.write("}\3}\5}\u0384\n}\6\u02ca\u02d7\u0342\u034f\2~\3\3\5\4")
        buf.write("\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17")
        buf.write("\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63")
        buf.write("\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-")
        buf.write("Y.[/]\60_\61a\62c\63e\64g\65i\66k\67m8o9q:s;u<w=y>{?}")
        buf.write("@\177A\u0081B\u0083C\u0085D\u0087E\u0089F\u008bG\u008d")
        buf.write("H\u008fI\u0091J\u0093K\u0095L\u0097M\u0099N\u009bO\u009d")
        buf.write("P\u009fQ\u00a1R\u00a3S\u00a5T\u00a7U\u00a9V\u00abW\u00ad")
        buf.write("X\u00afY\u00b1Z\u00b3[\u00b5\\\u00b7]\u00b9^\u00bb_\u00bd")
        buf.write("`\u00bfa\u00c1b\u00c3c\u00c5\2\u00c7\2\u00c9\2\u00cb\2")
        buf.write("\u00cd\2\u00cf\2\u00d1\2\u00d3\2\u00d5\2\u00d7\2\u00d9")
        buf.write("\2\u00db\2\u00dd\2\u00df\2\u00e1\2\u00e3\2\u00e5\2\u00e7")
        buf.write("\2\u00e9\2\u00eb\2\u00ed\2\u00ef\2\u00f1\2\u00f3\2\u00f5")
        buf.write("\2\u00f7\2\u00f9\2\3\2\33\b\2HHTTWWhhttww\4\2HHhh\4\2")
        buf.write("TTtt\4\2DDdd\4\2QQqq\4\2ZZzz\4\2LLll\6\2\f\f\16\17))^")
        buf.write("^\6\2\f\f\16\17$$^^\3\2^^\3\2\63;\3\2\62;\3\2\629\5\2")
        buf.write("\62;CHch\3\2\62\63\4\2GGgg\4\2--//\7\2\2\13\r\16\20(*")
        buf.write("]_\u0081\7\2\2\13\r\16\20#%]_\u0081\4\2\2]_\u0081\3\2")
        buf.write("\2\u0081\4\2\13\13\"\"\4\2\f\f\16\17\u0129\2C\\aac|\u00ac")
        buf.write("\u00ac\u00b7\u00b7\u00bc\u00bc\u00c2\u00d8\u00da\u00f8")
        buf.write("\u00fa\u0243\u0252\u02c3\u02c8\u02d3\u02e2\u02e6\u02f0")
        buf.write("\u02f0\u037c\u037c\u0388\u0388\u038a\u038c\u038e\u038e")
        buf.write("\u0390\u03a3\u03a5\u03d0\u03d2\u03f7\u03f9\u0483\u048c")
        buf.write("\u04d0\u04d2\u04fb\u0502\u0511\u0533\u0558\u055b\u055b")
        buf.write("\u0563\u0589\u05d2\u05ec\u05f2\u05f4\u0623\u063c\u0642")
        buf.write("\u064c\u0670\u0671\u0673\u06d5\u06d7\u06d7\u06e7\u06e8")
        buf.write("\u06f0\u06f1\u06fc\u06fe\u0701\u0701\u0712\u0712\u0714")
        buf.write("\u0731\u074f\u076f\u0782\u07a7\u07b3\u07b3\u0906\u093b")
        buf.write("\u093f\u093f\u0952\u0952\u095a\u0963\u097f\u097f\u0987")
        buf.write("\u098e\u0991\u0992\u0995\u09aa\u09ac\u09b2\u09b4\u09b4")
        buf.write("\u09b8\u09bb\u09bf\u09bf\u09d0\u09d0\u09de\u09df\u09e1")
        buf.write("\u09e3\u09f2\u09f3\u0a07\u0a0c\u0a11\u0a12\u0a15\u0a2a")
        buf.write("\u0a2c\u0a32\u0a34\u0a35\u0a37\u0a38\u0a3a\u0a3b\u0a5b")
        buf.write("\u0a5e\u0a60\u0a60\u0a74\u0a76\u0a87\u0a8f\u0a91\u0a93")
        buf.write("\u0a95\u0aaa\u0aac\u0ab2\u0ab4\u0ab5\u0ab7\u0abb\u0abf")
        buf.write("\u0abf\u0ad2\u0ad2\u0ae2\u0ae3\u0b07\u0b0e\u0b11\u0b12")
        buf.write("\u0b15\u0b2a\u0b2c\u0b32\u0b34\u0b35\u0b37\u0b3b\u0b3f")
        buf.write("\u0b3f\u0b5e\u0b5f\u0b61\u0b63\u0b73\u0b73\u0b85\u0b85")
        buf.write("\u0b87\u0b8c\u0b90\u0b92\u0b94\u0b97\u0b9b\u0b9c\u0b9e")
        buf.write("\u0b9e\u0ba0\u0ba1\u0ba5\u0ba6\u0baa\u0bac\u0bb0\u0bbb")
        buf.write("\u0c07\u0c0e\u0c10\u0c12\u0c14\u0c2a\u0c2c\u0c35\u0c37")
        buf.write("\u0c3b\u0c62\u0c63\u0c87\u0c8e\u0c90\u0c92\u0c94\u0caa")
        buf.write("\u0cac\u0cb5\u0cb7\u0cbb\u0cbf\u0cbf\u0ce0\u0ce0\u0ce2")
        buf.write("\u0ce3\u0d07\u0d0e\u0d10\u0d12\u0d14\u0d2a\u0d2c\u0d3b")
        buf.write("\u0d62\u0d63\u0d87\u0d98\u0d9c\u0db3\u0db5\u0dbd\u0dbf")
        buf.write("\u0dbf\u0dc2\u0dc8\u0e03\u0e32\u0e34\u0e35\u0e42\u0e48")
        buf.write("\u0e83\u0e84\u0e86\u0e86\u0e89\u0e8a\u0e8c\u0e8c\u0e8f")
        buf.write("\u0e8f\u0e96\u0e99\u0e9b\u0ea1\u0ea3\u0ea5\u0ea7\u0ea7")
        buf.write("\u0ea9\u0ea9\u0eac\u0ead\u0eaf\u0eb2\u0eb4\u0eb5\u0ebf")
        buf.write("\u0ebf\u0ec2\u0ec6\u0ec8\u0ec8\u0ede\u0edf\u0f02\u0f02")
        buf.write("\u0f42\u0f49\u0f4b\u0f6c\u0f8a\u0f8d\u1002\u1023\u1025")
        buf.write("\u1029\u102b\u102c\u1052\u1057\u10a2\u10c7\u10d2\u10fc")
        buf.write("\u10fe\u10fe\u1102\u115b\u1161\u11a4\u11aa\u11fb\u1202")
        buf.write("\u124a\u124c\u124f\u1252\u1258\u125a\u125a\u125c\u125f")
        buf.write("\u1262\u128a\u128c\u128f\u1292\u12b2\u12b4\u12b7\u12ba")
        buf.write("\u12c0\u12c2\u12c2\u12c4\u12c7\u12ca\u12d8\u12da\u1312")
        buf.write("\u1314\u1317\u131a\u135c\u1382\u1391\u13a2\u13f6\u1403")
        buf.write("\u166e\u1671\u1678\u1683\u169c\u16a2\u16ec\u16f0\u16f2")
        buf.write("\u1702\u170e\u1710\u1713\u1722\u1733\u1742\u1753\u1762")
        buf.write("\u176e\u1770\u1772\u1782\u17b5\u17d9\u17d9\u17de\u17de")
        buf.write("\u1822\u1879\u1882\u18aa\u1902\u191e\u1952\u196f\u1972")
        buf.write("\u1976\u1982\u19ab\u19c3\u19c9\u1a02\u1a18\u1d02\u1dc1")
        buf.write("\u1e02\u1e9d\u1ea2\u1efb\u1f02\u1f17\u1f1a\u1f1f\u1f22")
        buf.write("\u1f47\u1f4a\u1f4f\u1f52\u1f59\u1f5b\u1f5b\u1f5d\u1f5d")
        buf.write("\u1f5f\u1f5f\u1f61\u1f7f\u1f82\u1fb6\u1fb8\u1fbe\u1fc0")
        buf.write("\u1fc0\u1fc4\u1fc6\u1fc8\u1fce\u1fd2\u1fd5\u1fd8\u1fdd")
        buf.write("\u1fe2\u1fee\u1ff4\u1ff6\u1ff8\u1ffe\u2073\u2073\u2081")
        buf.write("\u2081\u2092\u2096\u2104\u2104\u2109\u2109\u210c\u2115")
        buf.write("\u2117\u2117\u211a\u211f\u2126\u2126\u2128\u2128\u212a")
        buf.write("\u212a\u212c\u2133\u2135\u213b\u213e\u2141\u2147\u214b")
        buf.write("\u2162\u2185\u2c02\u2c30\u2c32\u2c60\u2c82\u2ce6\u2d02")
        buf.write("\u2d27\u2d32\u2d67\u2d71\u2d71\u2d82\u2d98\u2da2\u2da8")
        buf.write("\u2daa\u2db0\u2db2\u2db8\u2dba\u2dc0\u2dc2\u2dc8\u2dca")
        buf.write("\u2dd0\u2dd2\u2dd8\u2dda\u2de0\u3007\u3009\u3023\u302b")
        buf.write("\u3033\u3037\u303a\u303e\u3043\u3098\u309d\u30a1\u30a3")
        buf.write("\u30fc\u30fe\u3101\u3107\u312e\u3133\u3190\u31a2\u31b9")
        buf.write("\u31f2\u3201\u3402\u4db7\u4e02\u9fbd\ua002\ua48e\ua802")
        buf.write("\ua803\ua805\ua807\ua809\ua80c\ua80e\ua824\uac02\ud7a5")
        buf.write("\uf902\ufa2f\ufa32\ufa6c\ufa72\ufadb\ufb02\ufb08\ufb15")
        buf.write("\ufb19\ufb1f\ufb1f\ufb21\ufb2a\ufb2c\ufb38\ufb3a\ufb3e")
        buf.write("\ufb40\ufb40\ufb42\ufb43\ufb45\ufb46\ufb48\ufbb3\ufbd5")
        buf.write("\ufd3f\ufd52\ufd91\ufd94\ufdc9\ufdf2\ufdfd\ufe72\ufe76")
        buf.write("\ufe78\ufefe\uff23\uff3c\uff43\uff5c\uff68\uffc0\uffc4")
        buf.write("\uffc9\uffcc\uffd1\uffd4\uffd9\uffdc\uffde\u0096\2\62")
        buf.write(";\u0302\u0371\u0485\u0488\u0593\u05bb\u05bd\u05bf\u05c1")
        buf.write("\u05c1\u05c3\u05c4\u05c6\u05c7\u05c9\u05c9\u0612\u0617")
        buf.write("\u064d\u0660\u0662\u066b\u0672\u0672\u06d8\u06de\u06e1")
        buf.write("\u06e6\u06e9\u06ea\u06ec\u06ef\u06f2\u06fb\u0713\u0713")
        buf.write("\u0732\u074c\u07a8\u07b2\u0903\u0905\u093e\u093e\u0940")
        buf.write("\u094f\u0953\u0956\u0964\u0965\u0968\u0971\u0983\u0985")
        buf.write("\u09be\u09be\u09c0\u09c6\u09c9\u09ca\u09cd\u09cf\u09d9")
        buf.write("\u09d9\u09e4\u09e5\u09e8\u09f1\u0a03\u0a05\u0a3e\u0a3e")
        buf.write("\u0a40\u0a44\u0a49\u0a4a\u0a4d\u0a4f\u0a68\u0a73\u0a83")
        buf.write("\u0a85\u0abe\u0abe\u0ac0\u0ac7\u0ac9\u0acb\u0acd\u0acf")
        buf.write("\u0ae4\u0ae5\u0ae8\u0af1\u0b03\u0b05\u0b3e\u0b3e\u0b40")
        buf.write("\u0b45\u0b49\u0b4a\u0b4d\u0b4f\u0b58\u0b59\u0b68\u0b71")
        buf.write("\u0b84\u0b84\u0bc0\u0bc4\u0bc8\u0bca\u0bcc\u0bcf\u0bd9")
        buf.write("\u0bd9\u0be8\u0bf1\u0c03\u0c05\u0c40\u0c46\u0c48\u0c4a")
        buf.write("\u0c4c\u0c4f\u0c57\u0c58\u0c68\u0c71\u0c84\u0c85\u0cbe")
        buf.write("\u0cbe\u0cc0\u0cc6\u0cc8\u0cca\u0ccc\u0ccf\u0cd7\u0cd8")
        buf.write("\u0ce8\u0cf1\u0d04\u0d05\u0d40\u0d45\u0d48\u0d4a\u0d4c")
        buf.write("\u0d4f\u0d59\u0d59\u0d68\u0d71\u0d84\u0d85\u0dcc\u0dcc")
        buf.write("\u0dd1\u0dd6\u0dd8\u0dd8\u0dda\u0de1\u0df4\u0df5\u0e33")
        buf.write("\u0e33\u0e36\u0e3c\u0e49\u0e50\u0e52\u0e5b\u0eb3\u0eb3")
        buf.write("\u0eb6\u0ebb\u0ebd\u0ebe\u0eca\u0ecf\u0ed2\u0edb\u0f1a")
        buf.write("\u0f1b\u0f22\u0f2b\u0f37\u0f37\u0f39\u0f39\u0f3b\u0f3b")
        buf.write("\u0f40\u0f41\u0f73\u0f86\u0f88\u0f89\u0f92\u0f99\u0f9b")
        buf.write("\u0fbe\u0fc8\u0fc8\u102e\u1034\u1038\u103b\u1042\u104b")
        buf.write("\u1058\u105b\u1361\u1361\u136b\u1373\u1714\u1716\u1734")
        buf.write("\u1736\u1754\u1755\u1774\u1775\u17b8\u17d5\u17df\u17df")
        buf.write("\u17e2\u17eb\u180d\u180f\u1812\u181b\u18ab\u18ab\u1922")
        buf.write("\u192d\u1932\u193d\u1948\u1951\u19b2\u19c2\u19ca\u19cb")
        buf.write("\u19d2\u19db\u1a19\u1a1d\u1dc2\u1dc5\u2041\u2042\u2056")
        buf.write("\u2056\u20d2\u20de\u20e3\u20e3\u20e7\u20ed\u302c\u3031")
        buf.write("\u309b\u309c\ua804\ua804\ua808\ua808\ua80d\ua80d\ua825")
        buf.write("\ua829\ufb20\ufb20\ufe02\ufe11\ufe22\ufe25\ufe35\ufe36")
        buf.write("\ufe4f\ufe51\uff12\uff1b\uff41\uff41\2\u03a9\2\3\3\2\2")
        buf.write("\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2")
        buf.write("\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25")
        buf.write("\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3")
        buf.write("\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2")
        buf.write("\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2")
        buf.write("\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\2")
        buf.write("9\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2")
        buf.write("\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2")
        buf.write("\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2")
        buf.write("\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3")
        buf.write("\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i")
        buf.write("\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2\2")
        buf.write("s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2")
        buf.write("\2}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2")
        buf.write("\2\2\2\u0085\3\2\2\2\2\u0087\3\2\2\2\2\u0089\3\2\2\2\2")
        buf.write("\u008b\3\2\2\2\2\u008d\3\2\2\2\2\u008f\3\2\2\2\2\u0091")
        buf.write("\3\2\2\2\2\u0093\3\2\2\2\2\u0095\3\2\2\2\2\u0097\3\2\2")
        buf.write("\2\2\u0099\3\2\2\2\2\u009b\3\2\2\2\2\u009d\3\2\2\2\2\u009f")
        buf.write("\3\2\2\2\2\u00a1\3\2\2\2\2\u00a3\3\2\2\2\2\u00a5\3\2\2")
        buf.write("\2\2\u00a7\3\2\2\2\2\u00a9\3\2\2\2\2\u00ab\3\2\2\2\2\u00ad")
        buf.write("\3\2\2\2\2\u00af\3\2\2\2\2\u00b1\3\2\2\2\2\u00b3\3\2\2")
        buf.write("\2\2\u00b5\3\2\2\2\2\u00b7\3\2\2\2\2\u00b9\3\2\2\2\2\u00bb")
        buf.write("\3\2\2\2\2\u00bd\3\2\2\2\2\u00bf\3\2\2\2\2\u00c1\3\2\2")
        buf.write("\2\2\u00c3\3\2\2\2\3\u00fd\3\2\2\2\5\u0102\3\2\2\2\7\u0108")
        buf.write("\3\2\2\2\t\u010a\3\2\2\2\13\u010e\3\2\2\2\r\u0115\3\2")
        buf.write("\2\2\17\u011b\3\2\2\2\21\u0120\3\2\2\2\23\u0127\3\2\2")
        buf.write("\2\25\u012a\3\2\2\2\27\u0131\3\2\2\2\31\u013a\3\2\2\2")
        buf.write("\33\u0141\3\2\2\2\35\u0144\3\2\2\2\37\u0149\3\2\2\2!\u014e")
        buf.write("\3\2\2\2#\u0154\3\2\2\2%\u0158\3\2\2\2\'\u015b\3\2\2\2")
        buf.write(")\u015f\3\2\2\2+\u0167\3\2\2\2-\u016c\3\2\2\2/\u0173\3")
        buf.write("\2\2\2\61\u017a\3\2\2\2\63\u017d\3\2\2\2\65\u0181\3\2")
        buf.write("\2\2\67\u0185\3\2\2\29\u0188\3\2\2\2;\u018d\3\2\2\2=\u0192")
        buf.write("\3\2\2\2?\u0198\3\2\2\2A\u019e\3\2\2\2C\u01a4\3\2\2\2")
        buf.write("E\u01a8\3\2\2\2G\u01ad\3\2\2\2I\u01b6\3\2\2\2K\u01bc\3")
        buf.write("\2\2\2M\u01c2\3\2\2\2O\u01d4\3\2\2\2Q\u01d8\3\2\2\2S\u01e4")
        buf.write("\3\2\2\2U\u01ef\3\2\2\2W\u0204\3\2\2\2Y\u0206\3\2\2\2")
        buf.write("[\u020d\3\2\2\2]\u0214\3\2\2\2_\u021d\3\2\2\2a\u0221\3")
        buf.write("\2\2\2c\u0225\3\2\2\2e\u0227\3\2\2\2g\u022b\3\2\2\2i\u022d")
        buf.write("\3\2\2\2k\u0230\3\2\2\2m\u0233\3\2\2\2o\u0235\3\2\2\2")
        buf.write("q\u0237\3\2\2\2s\u0239\3\2\2\2u\u023c\3\2\2\2w\u023e\3")
        buf.write("\2\2\2y\u0241\3\2\2\2{\u0244\3\2\2\2}\u0246\3\2\2\2\177")
        buf.write("\u0248\3\2\2\2\u0081\u024a\3\2\2\2\u0083\u024d\3\2\2\2")
        buf.write("\u0085\u0250\3\2\2\2\u0087\u0252\3\2\2\2\u0089\u0254\3")
        buf.write("\2\2\2\u008b\u0256\3\2\2\2\u008d\u0258\3\2\2\2\u008f\u025b")
        buf.write("\3\2\2\2\u0091\u025d\3\2\2\2\u0093\u0260\3\2\2\2\u0095")
        buf.write("\u0263\3\2\2\2\u0097\u0265\3\2\2\2\u0099\u0267\3\2\2\2")
        buf.write("\u009b\u026a\3\2\2\2\u009d\u026d\3\2\2\2\u009f\u0270\3")
        buf.write("\2\2\2\u00a1\u0273\3\2\2\2\u00a3\u0276\3\2\2\2\u00a5\u0278")
        buf.write("\3\2\2\2\u00a7\u027b\3\2\2\2\u00a9\u027e\3\2\2\2\u00ab")
        buf.write("\u0281\3\2\2\2\u00ad\u0284\3\2\2\2\u00af\u0287\3\2\2\2")
        buf.write("\u00b1\u028a\3\2\2\2\u00b3\u028d\3\2\2\2\u00b5\u0290\3")
        buf.write("\2\2\2\u00b7\u0293\3\2\2\2\u00b9\u0296\3\2\2\2\u00bb\u029a")
        buf.write("\3\2\2\2\u00bd\u029e\3\2\2\2\u00bf\u02a2\3\2\2\2\u00c1")
        buf.write("\u02a9\3\2\2\2\u00c3\u02ad\3\2\2\2\u00c5\u02c1\3\2\2\2")
        buf.write("\u00c7\u02dd\3\2\2\2\u00c9\u02e1\3\2\2\2\u00cb\u02e3\3")
        buf.write("\2\2\2\u00cd\u02e9\3\2\2\2\u00cf\u02eb\3\2\2\2\u00d1\u02ed")
        buf.write("\3\2\2\2\u00d3\u02ef\3\2\2\2\u00d5\u02f1\3\2\2\2\u00d7")
        buf.write("\u02f3\3\2\2\2\u00d9\u02fc\3\2\2\2\u00db\u0300\3\2\2\2")
        buf.write("\u00dd\u0304\3\2\2\2\u00df\u030e\3\2\2\2\u00e1\u0319\3")
        buf.write("\2\2\2\u00e3\u0339\3\2\2\2\u00e5\u0355\3\2\2\2\u00e7\u0359")
        buf.write("\3\2\2\2\u00e9\u035c\3\2\2\2\u00eb\u035f\3\2\2\2\u00ed")
        buf.write("\u0362\3\2\2\2\u00ef\u0364\3\2\2\2\u00f1\u0368\3\2\2\2")
        buf.write("\u00f3\u036c\3\2\2\2\u00f5\u0373\3\2\2\2\u00f7\u037f\3")
        buf.write("\2\2\2\u00f9\u0383\3\2\2\2\u00fb\u00fe\5S*\2\u00fc\u00fe")
        buf.write("\5U+\2\u00fd\u00fb\3\2\2\2\u00fd\u00fc\3\2\2\2\u00fe\4")
        buf.write("\3\2\2\2\u00ff\u0103\5\7\4\2\u0100\u0103\5_\60\2\u0101")
        buf.write("\u0103\5a\61\2\u0102\u00ff\3\2\2\2\u0102\u0100\3\2\2\2")
        buf.write("\u0102\u0101\3\2\2\2\u0103\6\3\2\2\2\u0104\u0109\5W,\2")
        buf.write("\u0105\u0109\5Y-\2\u0106\u0109\5[.\2\u0107\u0109\5]/\2")
        buf.write("\u0108\u0104\3\2\2\2\u0108\u0105\3\2\2\2\u0108\u0106\3")
        buf.write("\2\2\2\u0108\u0107\3\2\2\2\u0109\b\3\2\2\2\u010a\u010b")
        buf.write("\7f\2\2\u010b\u010c\7g\2\2\u010c\u010d\7h\2\2\u010d\n")
        buf.write("\3\2\2\2\u010e\u010f\7t\2\2\u010f\u0110\7g\2\2\u0110\u0111")
        buf.write("\7v\2\2\u0111\u0112\7w\2\2\u0112\u0113\7t\2\2\u0113\u0114")
        buf.write("\7p\2\2\u0114\f\3\2\2\2\u0115\u0116\7t\2\2\u0116\u0117")
        buf.write("\7c\2\2\u0117\u0118\7k\2\2\u0118\u0119\7u\2\2\u0119\u011a")
        buf.write("\7g\2\2\u011a\16\3\2\2\2\u011b\u011c\7h\2\2\u011c\u011d")
        buf.write("\7t\2\2\u011d\u011e\7q\2\2\u011e\u011f\7o\2\2\u011f\20")
        buf.write("\3\2\2\2\u0120\u0121\7k\2\2\u0121\u0122\7o\2\2\u0122\u0123")
        buf.write("\7r\2\2\u0123\u0124\7q\2\2\u0124\u0125\7t\2\2\u0125\u0126")
        buf.write("\7v\2\2\u0126\22\3\2\2\2\u0127\u0128\7c\2\2\u0128\u0129")
        buf.write("\7u\2\2\u0129\24\3\2\2\2\u012a\u012b\7i\2\2\u012b\u012c")
        buf.write("\7n\2\2\u012c\u012d\7q\2\2\u012d\u012e\7d\2\2\u012e\u012f")
        buf.write("\7c\2\2\u012f\u0130\7n\2\2\u0130\26\3\2\2\2\u0131\u0132")
        buf.write("\7p\2\2\u0132\u0133\7q\2\2\u0133\u0134\7p\2\2\u0134\u0135")
        buf.write("\7n\2\2\u0135\u0136\7q\2\2\u0136\u0137\7e\2\2\u0137\u0138")
        buf.write("\7c\2\2\u0138\u0139\7n\2\2\u0139\30\3\2\2\2\u013a\u013b")
        buf.write("\7c\2\2\u013b\u013c\7u\2\2\u013c\u013d\7u\2\2\u013d\u013e")
        buf.write("\7g\2\2\u013e\u013f\7t\2\2\u013f\u0140\7v\2\2\u0140\32")
        buf.write("\3\2\2\2\u0141\u0142\7k\2\2\u0142\u0143\7h\2\2\u0143\34")
        buf.write("\3\2\2\2\u0144\u0145\7g\2\2\u0145\u0146\7n\2\2\u0146\u0147")
        buf.write("\7k\2\2\u0147\u0148\7h\2\2\u0148\36\3\2\2\2\u0149\u014a")
        buf.write("\7g\2\2\u014a\u014b\7n\2\2\u014b\u014c\7u\2\2\u014c\u014d")
        buf.write("\7g\2\2\u014d \3\2\2\2\u014e\u014f\7y\2\2\u014f\u0150")
        buf.write("\7j\2\2\u0150\u0151\7k\2\2\u0151\u0152\7n\2\2\u0152\u0153")
        buf.write("\7g\2\2\u0153\"\3\2\2\2\u0154\u0155\7h\2\2\u0155\u0156")
        buf.write("\7q\2\2\u0156\u0157\7t\2\2\u0157$\3\2\2\2\u0158\u0159")
        buf.write("\7k\2\2\u0159\u015a\7p\2\2\u015a&\3\2\2\2\u015b\u015c")
        buf.write("\7v\2\2\u015c\u015d\7t\2\2\u015d\u015e\7{\2\2\u015e(\3")
        buf.write("\2\2\2\u015f\u0160\7h\2\2\u0160\u0161\7k\2\2\u0161\u0162")
        buf.write("\7p\2\2\u0162\u0163\7c\2\2\u0163\u0164\7n\2\2\u0164\u0165")
        buf.write("\7n\2\2\u0165\u0166\7{\2\2\u0166*\3\2\2\2\u0167\u0168")
        buf.write("\7y\2\2\u0168\u0169\7k\2\2\u0169\u016a\7v\2\2\u016a\u016b")
        buf.write("\7j\2\2\u016b,\3\2\2\2\u016c\u016d\7g\2\2\u016d\u016e")
        buf.write("\7z\2\2\u016e\u016f\7e\2\2\u016f\u0170\7g\2\2\u0170\u0171")
        buf.write("\7r\2\2\u0171\u0172\7v\2\2\u0172.\3\2\2\2\u0173\u0174")
        buf.write("\7n\2\2\u0174\u0175\7c\2\2\u0175\u0176\7o\2\2\u0176\u0177")
        buf.write("\7d\2\2\u0177\u0178\7f\2\2\u0178\u0179\7c\2\2\u0179\60")
        buf.write("\3\2\2\2\u017a\u017b\7q\2\2\u017b\u017c\7t\2\2\u017c\62")
        buf.write("\3\2\2\2\u017d\u017e\7c\2\2\u017e\u017f\7p\2\2\u017f\u0180")
        buf.write("\7f\2\2\u0180\64\3\2\2\2\u0181\u0182\7p\2\2\u0182\u0183")
        buf.write("\7q\2\2\u0183\u0184\7v\2\2\u0184\66\3\2\2\2\u0185\u0186")
        buf.write("\7k\2\2\u0186\u0187\7u\2\2\u01878\3\2\2\2\u0188\u0189")
        buf.write("\7P\2\2\u0189\u018a\7q\2\2\u018a\u018b\7p\2\2\u018b\u018c")
        buf.write("\7g\2\2\u018c:\3\2\2\2\u018d\u018e\7V\2\2\u018e\u018f")
        buf.write("\7t\2\2\u018f\u0190\7w\2\2\u0190\u0191\7g\2\2\u0191<\3")
        buf.write("\2\2\2\u0192\u0193\7H\2\2\u0193\u0194\7c\2\2\u0194\u0195")
        buf.write("\7n\2\2\u0195\u0196\7u\2\2\u0196\u0197\7g\2\2\u0197>\3")
        buf.write("\2\2\2\u0198\u0199\7e\2\2\u0199\u019a\7n\2\2\u019a\u019b")
        buf.write("\7c\2\2\u019b\u019c\7u\2\2\u019c\u019d\7u\2\2\u019d@\3")
        buf.write("\2\2\2\u019e\u019f\7{\2\2\u019f\u01a0\7k\2\2\u01a0\u01a1")
        buf.write("\7g\2\2\u01a1\u01a2\7n\2\2\u01a2\u01a3\7f\2\2\u01a3B\3")
        buf.write("\2\2\2\u01a4\u01a5\7f\2\2\u01a5\u01a6\7g\2\2\u01a6\u01a7")
        buf.write("\7n\2\2\u01a7D\3\2\2\2\u01a8\u01a9\7r\2\2\u01a9\u01aa")
        buf.write("\7c\2\2\u01aa\u01ab\7u\2\2\u01ab\u01ac\7u\2\2\u01acF\3")
        buf.write("\2\2\2\u01ad\u01ae\7e\2\2\u01ae\u01af\7q\2\2\u01af\u01b0")
        buf.write("\7p\2\2\u01b0\u01b1\7v\2\2\u01b1\u01b2\7k\2\2\u01b2\u01b3")
        buf.write("\7p\2\2\u01b3\u01b4\7w\2\2\u01b4\u01b5\7g\2\2\u01b5H\3")
        buf.write("\2\2\2\u01b6\u01b7\7d\2\2\u01b7\u01b8\7t\2\2\u01b8\u01b9")
        buf.write("\7g\2\2\u01b9\u01ba\7c\2\2\u01ba\u01bb\7m\2\2\u01bbJ\3")
        buf.write("\2\2\2\u01bc\u01bd\7c\2\2\u01bd\u01be\7u\2\2\u01be\u01bf")
        buf.write("\7{\2\2\u01bf\u01c0\7p\2\2\u01c0\u01c1\7e\2\2\u01c1L\3")
        buf.write("\2\2\2\u01c2\u01c3\7c\2\2\u01c3\u01c4\7y\2\2\u01c4\u01c5")
        buf.write("\7c\2\2\u01c5\u01c6\7k\2\2\u01c6\u01c7\7v\2\2\u01c7N\3")
        buf.write("\2\2\2\u01c8\u01c9\6(\2\2\u01c9\u01d5\5\u00f1y\2\u01ca")
        buf.write("\u01cc\7\17\2\2\u01cb\u01ca\3\2\2\2\u01cb\u01cc\3\2\2")
        buf.write("\2\u01cc\u01cd\3\2\2\2\u01cd\u01d0\7\f\2\2\u01ce\u01d0")
        buf.write("\4\16\17\2\u01cf\u01cb\3\2\2\2\u01cf\u01ce\3\2\2\2\u01d0")
        buf.write("\u01d2\3\2\2\2\u01d1\u01d3\5\u00f1y\2\u01d2\u01d1\3\2")
        buf.write("\2\2\u01d2\u01d3\3\2\2\2\u01d3\u01d5\3\2\2\2\u01d4\u01c8")
        buf.write("\3\2\2\2\u01d4\u01cf\3\2\2\2\u01d5\u01d6\3\2\2\2\u01d6")
        buf.write("\u01d7\b(\2\2\u01d7P\3\2\2\2\u01d8\u01dc\5\u00f7|\2\u01d9")
        buf.write("\u01db\5\u00f9}\2\u01da\u01d9\3\2\2\2\u01db\u01de\3\2")
        buf.write("\2\2\u01dc\u01da\3\2\2\2\u01dc\u01dd\3\2\2\2\u01ddR\3")
        buf.write("\2\2\2\u01de\u01dc\3\2\2\2\u01df\u01e5\t\2\2\2\u01e0\u01e1")
        buf.write("\t\3\2\2\u01e1\u01e5\t\4\2\2\u01e2\u01e3\t\4\2\2\u01e3")
        buf.write("\u01e5\t\3\2\2\u01e4\u01df\3\2\2\2\u01e4\u01e0\3\2\2\2")
        buf.write("\u01e4\u01e2\3\2\2\2\u01e4\u01e5\3\2\2\2\u01e5\u01e8\3")
        buf.write("\2\2\2\u01e6\u01e9\5\u00c5c\2\u01e7\u01e9\5\u00c7d\2\u01e8")
        buf.write("\u01e6\3\2\2\2\u01e8\u01e7\3\2\2\2\u01e9T\3\2\2\2\u01ea")
        buf.write("\u01f0\t\5\2\2\u01eb\u01ec\t\5\2\2\u01ec\u01f0\t\4\2\2")
        buf.write("\u01ed\u01ee\t\4\2\2\u01ee\u01f0\t\5\2\2\u01ef\u01ea\3")
        buf.write("\2\2\2\u01ef\u01eb\3\2\2\2\u01ef\u01ed\3\2\2\2\u01f0\u01f3")
        buf.write("\3\2\2\2\u01f1\u01f4\5\u00e3r\2\u01f2\u01f4\5\u00e5s\2")
        buf.write("\u01f3\u01f1\3\2\2\2\u01f3\u01f2\3\2\2\2\u01f4V\3\2\2")
        buf.write("\2\u01f5\u01fc\5\u00cfh\2\u01f6\u01f8\7a\2\2\u01f7\u01f6")
        buf.write("\3\2\2\2\u01f7\u01f8\3\2\2\2\u01f8\u01f9\3\2\2\2\u01f9")
        buf.write("\u01fb\5\u00d1i\2\u01fa\u01f7\3\2\2\2\u01fb\u01fe\3\2")
        buf.write("\2\2\u01fc\u01fa\3\2\2\2\u01fc\u01fd\3\2\2\2\u01fd\u0205")
        buf.write("\3\2\2\2\u01fe\u01fc\3\2\2\2\u01ff\u0201\7\62\2\2\u0200")
        buf.write("\u01ff\3\2\2\2\u0201\u0202\3\2\2\2\u0202\u0200\3\2\2\2")
        buf.write("\u0202\u0203\3\2\2\2\u0203\u0205\3\2\2\2\u0204\u01f5\3")
        buf.write("\2\2\2\u0204\u0200\3\2\2\2\u0205X\3\2\2\2\u0206\u0207")
        buf.write("\7\62\2\2\u0207\u0209\t\6\2\2\u0208\u020a\5\u00d3j\2\u0209")
        buf.write("\u0208\3\2\2\2\u020a\u020b\3\2\2\2\u020b\u0209\3\2\2\2")
        buf.write("\u020b\u020c\3\2\2\2\u020cZ\3\2\2\2\u020d\u020e\7\62\2")
        buf.write("\2\u020e\u0210\t\7\2\2\u020f\u0211\5\u00d5k\2\u0210\u020f")
        buf.write("\3\2\2\2\u0211\u0212\3\2\2\2\u0212\u0210\3\2\2\2\u0212")
        buf.write("\u0213\3\2\2\2\u0213\\\3\2\2\2\u0214\u0215\7\62\2\2\u0215")
        buf.write("\u0217\t\5\2\2\u0216\u0218\5\u00d7l\2\u0217\u0216\3\2")
        buf.write("\2\2\u0218\u0219\3\2\2\2\u0219\u0217\3\2\2\2\u0219\u021a")
        buf.write("\3\2\2\2\u021a^\3\2\2\2\u021b\u021e\5\u00d9m\2\u021c\u021e")
        buf.write("\5\u00dbn\2\u021d\u021b\3\2\2\2\u021d\u021c\3\2\2\2\u021e")
        buf.write("`\3\2\2\2\u021f\u0222\5_\60\2\u0220\u0222\5\u00ddo\2\u0221")
        buf.write("\u021f\3\2\2\2\u0221\u0220\3\2\2\2\u0222\u0223\3\2\2\2")
        buf.write("\u0223\u0224\t\b\2\2\u0224b\3\2\2\2\u0225\u0226\7\60\2")
        buf.write("\2\u0226d\3\2\2\2\u0227\u0228\7\60\2\2\u0228\u0229\7\60")
        buf.write("\2\2\u0229\u022a\7\60\2\2\u022af\3\2\2\2\u022b\u022c\7")
        buf.write(",\2\2\u022ch\3\2\2\2\u022d\u022e\7*\2\2\u022e\u022f\b")
        buf.write("\65\3\2\u022fj\3\2\2\2\u0230\u0231\7+\2\2\u0231\u0232")
        buf.write("\b\66\4\2\u0232l\3\2\2\2\u0233\u0234\7.\2\2\u0234n\3\2")
        buf.write("\2\2\u0235\u0236\7<\2\2\u0236p\3\2\2\2\u0237\u0238\7=")
        buf.write("\2\2\u0238r\3\2\2\2\u0239\u023a\7,\2\2\u023a\u023b\7,")
        buf.write("\2\2\u023bt\3\2\2\2\u023c\u023d\7?\2\2\u023dv\3\2\2\2")
        buf.write("\u023e\u023f\7]\2\2\u023f\u0240\b<\5\2\u0240x\3\2\2\2")
        buf.write("\u0241\u0242\7_\2\2\u0242\u0243\b=\6\2\u0243z\3\2\2\2")
        buf.write("\u0244\u0245\7~\2\2\u0245|\3\2\2\2\u0246\u0247\7`\2\2")
        buf.write("\u0247~\3\2\2\2\u0248\u0249\7(\2\2\u0249\u0080\3\2\2\2")
        buf.write("\u024a\u024b\7>\2\2\u024b\u024c\7>\2\2\u024c\u0082\3\2")
        buf.write("\2\2\u024d\u024e\7@\2\2\u024e\u024f\7@\2\2\u024f\u0084")
        buf.write("\3\2\2\2\u0250\u0251\7-\2\2\u0251\u0086\3\2\2\2\u0252")
        buf.write("\u0253\7/\2\2\u0253\u0088\3\2\2\2\u0254\u0255\7\61\2\2")
        buf.write("\u0255\u008a\3\2\2\2\u0256\u0257\7\'\2\2\u0257\u008c\3")
        buf.write("\2\2\2\u0258\u0259\7\61\2\2\u0259\u025a\7\61\2\2\u025a")
        buf.write("\u008e\3\2\2\2\u025b\u025c\7\u0080\2\2\u025c\u0090\3\2")
        buf.write("\2\2\u025d\u025e\7}\2\2\u025e\u025f\bI\7\2\u025f\u0092")
        buf.write("\3\2\2\2\u0260\u0261\7\177\2\2\u0261\u0262\bJ\b\2\u0262")
        buf.write("\u0094\3\2\2\2\u0263\u0264\7>\2\2\u0264\u0096\3\2\2\2")
        buf.write("\u0265\u0266\7@\2\2\u0266\u0098\3\2\2\2\u0267\u0268\7")
        buf.write("?\2\2\u0268\u0269\7?\2\2\u0269\u009a\3\2\2\2\u026a\u026b")
        buf.write("\7@\2\2\u026b\u026c\7?\2\2\u026c\u009c\3\2\2\2\u026d\u026e")
        buf.write("\7>\2\2\u026e\u026f\7?\2\2\u026f\u009e\3\2\2\2\u0270\u0271")
        buf.write("\7>\2\2\u0271\u0272\7@\2\2\u0272\u00a0\3\2\2\2\u0273\u0274")
        buf.write("\7#\2\2\u0274\u0275\7?\2\2\u0275\u00a2\3\2\2\2\u0276\u0277")
        buf.write("\7B\2\2\u0277\u00a4\3\2\2\2\u0278\u0279\7/\2\2\u0279\u027a")
        buf.write("\7@\2\2\u027a\u00a6\3\2\2\2\u027b\u027c\7-\2\2\u027c\u027d")
        buf.write("\7?\2\2\u027d\u00a8\3\2\2\2\u027e\u027f\7/\2\2\u027f\u0280")
        buf.write("\7?\2\2\u0280\u00aa\3\2\2\2\u0281\u0282\7,\2\2\u0282\u0283")
        buf.write("\7?\2\2\u0283\u00ac\3\2\2\2\u0284\u0285\7B\2\2\u0285\u0286")
        buf.write("\7?\2\2\u0286\u00ae\3\2\2\2\u0287\u0288\7\61\2\2\u0288")
        buf.write("\u0289\7?\2\2\u0289\u00b0\3\2\2\2\u028a\u028b\7\'\2\2")
        buf.write("\u028b\u028c\7?\2\2\u028c\u00b2\3\2\2\2\u028d\u028e\7")
        buf.write("(\2\2\u028e\u028f\7?\2\2\u028f\u00b4\3\2\2\2\u0290\u0291")
        buf.write("\7~\2\2\u0291\u0292\7?\2\2\u0292\u00b6\3\2\2\2\u0293\u0294")
        buf.write("\7`\2\2\u0294\u0295\7?\2\2\u0295\u00b8\3\2\2\2\u0296\u0297")
        buf.write("\7>\2\2\u0297\u0298\7>\2\2\u0298\u0299\7?\2\2\u0299\u00ba")
        buf.write("\3\2\2\2\u029a\u029b\7@\2\2\u029b\u029c\7@\2\2\u029c\u029d")
        buf.write("\7?\2\2\u029d\u00bc\3\2\2\2\u029e\u029f\7,\2\2\u029f\u02a0")
        buf.write("\7,\2\2\u02a0\u02a1\7?\2\2\u02a1\u00be\3\2\2\2\u02a2\u02a3")
        buf.write("\7\61\2\2\u02a3\u02a4\7\61\2\2\u02a4\u02a5\7?\2\2\u02a5")
        buf.write("\u00c0\3\2\2\2\u02a6\u02aa\5\u00f1y\2\u02a7\u02aa\5\u00f3")
        buf.write("z\2\u02a8\u02aa\5\u00f5{\2\u02a9\u02a6\3\2\2\2\u02a9\u02a7")
        buf.write("\3\2\2\2\u02a9\u02a8\3\2\2\2\u02aa\u02ab\3\2\2\2\u02ab")
        buf.write("\u02ac\ba\t\2\u02ac\u00c2\3\2\2\2\u02ad\u02ae\13\2\2\2")
        buf.write("\u02ae\u00c4\3\2\2\2\u02af\u02b4\7)\2\2\u02b0\u02b3\5")
        buf.write("\u00cdg\2\u02b1\u02b3\n\t\2\2\u02b2\u02b0\3\2\2\2\u02b2")
        buf.write("\u02b1\3\2\2\2\u02b3\u02b6\3\2\2\2\u02b4\u02b2\3\2\2\2")
        buf.write("\u02b4\u02b5\3\2\2\2\u02b5\u02b7\3\2\2\2\u02b6\u02b4\3")
        buf.write("\2\2\2\u02b7\u02c2\7)\2\2\u02b8\u02bd\7$\2\2\u02b9\u02bc")
        buf.write("\5\u00cdg\2\u02ba\u02bc\n\n\2\2\u02bb\u02b9\3\2\2\2\u02bb")
        buf.write("\u02ba\3\2\2\2\u02bc\u02bf\3\2\2\2\u02bd\u02bb\3\2\2\2")
        buf.write("\u02bd\u02be\3\2\2\2\u02be\u02c0\3\2\2\2\u02bf\u02bd\3")
        buf.write("\2\2\2\u02c0\u02c2\7$\2\2\u02c1\u02af\3\2\2\2\u02c1\u02b8")
        buf.write("\3\2\2\2\u02c2\u00c6\3\2\2\2\u02c3\u02c4\7)\2\2\u02c4")
        buf.write("\u02c5\7)\2\2\u02c5\u02c6\7)\2\2\u02c6\u02ca\3\2\2\2\u02c7")
        buf.write("\u02c9\5\u00c9e\2\u02c8\u02c7\3\2\2\2\u02c9\u02cc\3\2")
        buf.write("\2\2\u02ca\u02cb\3\2\2\2\u02ca\u02c8\3\2\2\2\u02cb\u02cd")
        buf.write("\3\2\2\2\u02cc\u02ca\3\2\2\2\u02cd\u02ce\7)\2\2\u02ce")
        buf.write("\u02cf\7)\2\2\u02cf\u02de\7)\2\2\u02d0\u02d1\7$\2\2\u02d1")
        buf.write("\u02d2\7$\2\2\u02d2\u02d3\7$\2\2\u02d3\u02d7\3\2\2\2\u02d4")
        buf.write("\u02d6\5\u00c9e\2\u02d5\u02d4\3\2\2\2\u02d6\u02d9\3\2")
        buf.write("\2\2\u02d7\u02d8\3\2\2\2\u02d7\u02d5\3\2\2\2\u02d8\u02da")
        buf.write("\3\2\2\2\u02d9\u02d7\3\2\2\2\u02da\u02db\7$\2\2\u02db")
        buf.write("\u02dc\7$\2\2\u02dc\u02de\7$\2\2\u02dd\u02c3\3\2\2\2\u02dd")
        buf.write("\u02d0\3\2\2\2\u02de\u00c8\3\2\2\2\u02df\u02e2\5\u00cb")
        buf.write("f\2\u02e0\u02e2\5\u00cdg\2\u02e1\u02df\3\2\2\2\u02e1\u02e0")
        buf.write("\3\2\2\2\u02e2\u00ca\3\2\2\2\u02e3\u02e4\n\13\2\2\u02e4")
        buf.write("\u00cc\3\2\2\2\u02e5\u02e6\7^\2\2\u02e6\u02ea\13\2\2\2")
        buf.write("\u02e7\u02e8\7^\2\2\u02e8\u02ea\5O(\2\u02e9\u02e5\3\2")
        buf.write("\2\2\u02e9\u02e7\3\2\2\2\u02ea\u00ce\3\2\2\2\u02eb\u02ec")
        buf.write("\t\f\2\2\u02ec\u00d0\3\2\2\2\u02ed\u02ee\t\r\2\2\u02ee")
        buf.write("\u00d2\3\2\2\2\u02ef\u02f0\t\16\2\2\u02f0\u00d4\3\2\2")
        buf.write("\2\u02f1\u02f2\t\17\2\2\u02f2\u00d6\3\2\2\2\u02f3\u02f4")
        buf.write("\t\20\2\2\u02f4\u00d8\3\2\2\2\u02f5\u02f7\5\u00ddo\2\u02f6")
        buf.write("\u02f5\3\2\2\2\u02f6\u02f7\3\2\2\2\u02f7\u02f8\3\2\2\2")
        buf.write("\u02f8\u02fd\5\u00dfp\2\u02f9\u02fa\5\u00ddo\2\u02fa\u02fb")
        buf.write("\7\60\2\2\u02fb\u02fd\3\2\2\2\u02fc\u02f6\3\2\2\2\u02fc")
        buf.write("\u02f9\3\2\2\2\u02fd\u00da\3\2\2\2\u02fe\u0301\5\u00dd")
        buf.write("o\2\u02ff\u0301\5\u00d9m\2\u0300\u02fe\3\2\2\2\u0300\u02ff")
        buf.write("\3\2\2\2\u0301\u0302\3\2\2\2\u0302\u0303\5\u00e1q\2\u0303")
        buf.write("\u00dc\3\2\2\2\u0304\u030b\5\u00d1i\2\u0305\u0307\7a\2")
        buf.write("\2\u0306\u0305\3\2\2\2\u0306\u0307\3\2\2\2\u0307\u0308")
        buf.write("\3\2\2\2\u0308\u030a\5\u00d1i\2\u0309\u0306\3\2\2\2\u030a")
        buf.write("\u030d\3\2\2\2\u030b\u0309\3\2\2\2\u030b\u030c\3\2\2\2")
        buf.write("\u030c\u00de\3\2\2\2\u030d\u030b\3\2\2\2\u030e\u030f\7")
        buf.write("\60\2\2\u030f\u0316\5\u00d1i\2\u0310\u0312\7a\2\2\u0311")
        buf.write("\u0310\3\2\2\2\u0311\u0312\3\2\2\2\u0312\u0313\3\2\2\2")
        buf.write("\u0313\u0315\5\u00d1i\2\u0314\u0311\3\2\2\2\u0315\u0318")
        buf.write("\3\2\2\2\u0316\u0314\3\2\2\2\u0316\u0317\3\2\2\2\u0317")
        buf.write("\u00e0\3\2\2\2\u0318\u0316\3\2\2\2\u0319\u031b\t\21\2")
        buf.write("\2\u031a\u031c\t\22\2\2\u031b\u031a\3\2\2\2\u031b\u031c")
        buf.write("\3\2\2\2\u031c\u031d\3\2\2\2\u031d\u0324\5\u00d1i\2\u031e")
        buf.write("\u0320\7a\2\2\u031f\u031e\3\2\2\2\u031f\u0320\3\2\2\2")
        buf.write("\u0320\u0321\3\2\2\2\u0321\u0323\5\u00d1i\2\u0322\u031f")
        buf.write("\3\2\2\2\u0323\u0326\3\2\2\2\u0324\u0322\3\2\2\2\u0324")
        buf.write("\u0325\3\2\2\2\u0325\u00e2\3\2\2\2\u0326\u0324\3\2\2\2")
        buf.write("\u0327\u032c\7)\2\2\u0328\u032b\5\u00e9u\2\u0329\u032b")
        buf.write("\5\u00efx\2\u032a\u0328\3\2\2\2\u032a\u0329\3\2\2\2\u032b")
        buf.write("\u032e\3\2\2\2\u032c\u032a\3\2\2\2\u032c\u032d\3\2\2\2")
        buf.write("\u032d\u032f\3\2\2\2\u032e\u032c\3\2\2\2\u032f\u033a\7")
        buf.write(")\2\2\u0330\u0335\7$\2\2\u0331\u0334\5\u00ebv\2\u0332")
        buf.write("\u0334\5\u00efx\2\u0333\u0331\3\2\2\2\u0333\u0332\3\2")
        buf.write("\2\2\u0334\u0337\3\2\2\2\u0335\u0333\3\2\2\2\u0335\u0336")
        buf.write("\3\2\2\2\u0336\u0338\3\2\2\2\u0337\u0335\3\2\2\2\u0338")
        buf.write("\u033a\7$\2\2\u0339\u0327\3\2\2\2\u0339\u0330\3\2\2\2")
        buf.write("\u033a\u00e4\3\2\2\2\u033b\u033c\7)\2\2\u033c\u033d\7")
        buf.write(")\2\2\u033d\u033e\7)\2\2\u033e\u0342\3\2\2\2\u033f\u0341")
        buf.write("\5\u00e7t\2\u0340\u033f\3\2\2\2\u0341\u0344\3\2\2\2\u0342")
        buf.write("\u0343\3\2\2\2\u0342\u0340\3\2\2\2\u0343\u0345\3\2\2\2")
        buf.write("\u0344\u0342\3\2\2\2\u0345\u0346\7)\2\2\u0346\u0347\7")
        buf.write(")\2\2\u0347\u0356\7)\2\2\u0348\u0349\7$\2\2\u0349\u034a")
        buf.write("\7$\2\2\u034a\u034b\7$\2\2\u034b\u034f\3\2\2\2\u034c\u034e")
        buf.write("\5\u00e7t\2\u034d\u034c\3\2\2\2\u034e\u0351\3\2\2\2\u034f")
        buf.write("\u0350\3\2\2\2\u034f\u034d\3\2\2\2\u0350\u0352\3\2\2\2")
        buf.write("\u0351\u034f\3\2\2\2\u0352\u0353\7$\2\2\u0353\u0354\7")
        buf.write("$\2\2\u0354\u0356\7$\2\2\u0355\u033b\3\2\2\2\u0355\u0348")
        buf.write("\3\2\2\2\u0356\u00e6\3\2\2\2\u0357\u035a\5\u00edw\2\u0358")
        buf.write("\u035a\5\u00efx\2\u0359\u0357\3\2\2\2\u0359\u0358\3\2")
        buf.write("\2\2\u035a\u00e8\3\2\2\2\u035b\u035d\t\23\2\2\u035c\u035b")
        buf.write("\3\2\2\2\u035d\u00ea\3\2\2\2\u035e\u0360\t\24\2\2\u035f")
        buf.write("\u035e\3\2\2\2\u0360\u00ec\3\2\2\2\u0361\u0363\t\25\2")
        buf.write("\2\u0362\u0361\3\2\2\2\u0363\u00ee\3\2\2\2\u0364\u0365")
        buf.write("\7^\2\2\u0365\u0366\t\26\2\2\u0366\u00f0\3\2\2\2\u0367")
        buf.write("\u0369\t\27\2\2\u0368\u0367\3\2\2\2\u0369\u036a\3\2\2")
        buf.write("\2\u036a\u0368\3\2\2\2\u036a\u036b\3\2\2\2\u036b\u00f2")
        buf.write("\3\2\2\2\u036c\u0370\7%\2\2\u036d\u036f\n\30\2\2\u036e")
        buf.write("\u036d\3\2\2\2\u036f\u0372\3\2\2\2\u0370\u036e\3\2\2\2")
        buf.write("\u0370\u0371\3\2\2\2\u0371\u00f4\3\2\2\2\u0372\u0370\3")
        buf.write("\2\2\2\u0373\u0375\7^\2\2\u0374\u0376\5\u00f1y\2\u0375")
        buf.write("\u0374\3\2\2\2\u0375\u0376\3\2\2\2\u0376\u037c\3\2\2\2")
        buf.write("\u0377\u0379\7\17\2\2\u0378\u0377\3\2\2\2\u0378\u0379")
        buf.write("\3\2\2\2\u0379\u037a\3\2\2\2\u037a\u037d\7\f\2\2\u037b")
        buf.write("\u037d\4\16\17\2\u037c\u0378\3\2\2\2\u037c\u037b\3\2\2")
        buf.write("\2\u037d\u00f6\3\2\2\2\u037e\u0380\t\31\2\2\u037f\u037e")
        buf.write("\3\2\2\2\u0380\u00f8\3\2\2\2\u0381\u0384\5\u00f7|\2\u0382")
        buf.write("\u0384\t\32\2\2\u0383\u0381\3\2\2\2\u0383\u0382\3\2\2")
        buf.write("\2\u0384\u00fa\3\2\2\2@\2\u00fd\u0102\u0108\u01cb\u01cf")
        buf.write("\u01d2\u01d4\u01dc\u01e4\u01e8\u01ef\u01f3\u01f7\u01fc")
        buf.write("\u0202\u0204\u020b\u0212\u0219\u021d\u0221\u02a9\u02b2")
        buf.write("\u02b4\u02bb\u02bd\u02c1\u02ca\u02d7\u02dd\u02e1\u02e9")
        buf.write("\u02f6\u02fc\u0300\u0306\u030b\u0311\u0316\u031b\u031f")
        buf.write("\u0324\u032a\u032c\u0333\u0335\u0339\u0342\u034f\u0355")
        buf.write("\u0359\u035c\u035f\u0362\u036a\u0370\u0375\u0378\u037c")
        buf.write("\u037f\u0383\n\3(\2\3\65\3\3\66\4\3<\5\3=\6\3I\7\3J\b")
        buf.write("\b\2\2")
        return buf.getvalue()


class Python3Lexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    STRING = 1
    NUMBER = 2
    INTEGER = 3
    DEF = 4
    RETURN = 5
    RAISE = 6
    FROM = 7
    IMPORT = 8
    AS = 9
    GLOBAL = 10
    NONLOCAL = 11
    ASSERT = 12
    IF = 13
    ELIF = 14
    ELSE = 15
    WHILE = 16
    FOR = 17
    IN = 18
    TRY = 19
    FINALLY = 20
    WITH = 21
    EXCEPT = 22
    LAMBDA = 23
    OR = 24
    AND = 25
    NOT = 26
    IS = 27
    NONE = 28
    TRUE = 29
    FALSE = 30
    CLASS = 31
    YIELD = 32
    DEL = 33
    PASS = 34
    CONTINUE = 35
    BREAK = 36
    ASYNC = 37
    AWAIT = 38
    NEWLINE = 39
    NAME = 40
    STRING_LITERAL = 41
    BYTES_LITERAL = 42
    DECIMAL_INTEGER = 43
    OCT_INTEGER = 44
    HEX_INTEGER = 45
    BIN_INTEGER = 46
    FLOAT_NUMBER = 47
    IMAG_NUMBER = 48
    DOT = 49
    ELLIPSIS = 50
    STAR = 51
    OPEN_PAREN = 52
    CLOSE_PAREN = 53
    COMMA = 54
    COLON = 55
    SEMI_COLON = 56
    POWER = 57
    ASSIGN = 58
    OPEN_BRACK = 59
    CLOSE_BRACK = 60
    OR_OP = 61
    XOR = 62
    AND_OP = 63
    LEFT_SHIFT = 64
    RIGHT_SHIFT = 65
    ADD = 66
    MINUS = 67
    DIV = 68
    MOD = 69
    IDIV = 70
    NOT_OP = 71
    OPEN_BRACE = 72
    CLOSE_BRACE = 73
    LESS_THAN = 74
    GREATER_THAN = 75
    EQUALS = 76
    GT_EQ = 77
    LT_EQ = 78
    NOT_EQ_1 = 79
    NOT_EQ_2 = 80
    AT = 81
    ARROW = 82
    ADD_ASSIGN = 83
    SUB_ASSIGN = 84
    MULT_ASSIGN = 85
    AT_ASSIGN = 86
    DIV_ASSIGN = 87
    MOD_ASSIGN = 88
    AND_ASSIGN = 89
    OR_ASSIGN = 90
    XOR_ASSIGN = 91
    LEFT_SHIFT_ASSIGN = 92
    RIGHT_SHIFT_ASSIGN = 93
    POWER_ASSIGN = 94
    IDIV_ASSIGN = 95
    SKIP_ = 96
    UNKNOWN_CHAR = 97

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'def'", "'return'", "'raise'", "'from'", "'import'", "'as'", 
            "'global'", "'nonlocal'", "'assert'", "'if'", "'elif'", "'else'", 
            "'while'", "'for'", "'in'", "'try'", "'finally'", "'with'", 
            "'except'", "'lambda'", "'or'", "'and'", "'not'", "'is'", "'None'", 
            "'True'", "'False'", "'class'", "'yield'", "'del'", "'pass'", 
            "'continue'", "'break'", "'async'", "'await'", "'.'", "'...'", 
            "'*'", "'('", "')'", "','", "':'", "';'", "'**'", "'='", "'['", 
            "']'", "'|'", "'^'", "'&'", "'<<'", "'>>'", "'+'", "'-'", "'/'", 
            "'%'", "'//'", "'~'", "'{'", "'}'", "'<'", "'>'", "'=='", "'>='", 
            "'<='", "'<>'", "'!='", "'@'", "'->'", "'+='", "'-='", "'*='", 
            "'@='", "'/='", "'%='", "'&='", "'|='", "'^='", "'<<='", "'>>='", 
            "'**='", "'//='" ]

    symbolicNames = [ "<INVALID>",
            "STRING", "NUMBER", "INTEGER", "DEF", "RETURN", "RAISE", "FROM", 
            "IMPORT", "AS", "GLOBAL", "NONLOCAL", "ASSERT", "IF", "ELIF", 
            "ELSE", "WHILE", "FOR", "IN", "TRY", "FINALLY", "WITH", "EXCEPT", 
            "LAMBDA", "OR", "AND", "NOT", "IS", "NONE", "TRUE", "FALSE", 
            "CLASS", "YIELD", "DEL", "PASS", "CONTINUE", "BREAK", "ASYNC", 
            "AWAIT", "NEWLINE", "NAME", "STRING_LITERAL", "BYTES_LITERAL", 
            "DECIMAL_INTEGER", "OCT_INTEGER", "HEX_INTEGER", "BIN_INTEGER", 
            "FLOAT_NUMBER", "IMAG_NUMBER", "DOT", "ELLIPSIS", "STAR", "OPEN_PAREN", 
            "CLOSE_PAREN", "COMMA", "COLON", "SEMI_COLON", "POWER", "ASSIGN", 
            "OPEN_BRACK", "CLOSE_BRACK", "OR_OP", "XOR", "AND_OP", "LEFT_SHIFT", 
            "RIGHT_SHIFT", "ADD", "MINUS", "DIV", "MOD", "IDIV", "NOT_OP", 
            "OPEN_BRACE", "CLOSE_BRACE", "LESS_THAN", "GREATER_THAN", "EQUALS", 
            "GT_EQ", "LT_EQ", "NOT_EQ_1", "NOT_EQ_2", "AT", "ARROW", "ADD_ASSIGN", 
            "SUB_ASSIGN", "MULT_ASSIGN", "AT_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", 
            "AND_ASSIGN", "OR_ASSIGN", "XOR_ASSIGN", "LEFT_SHIFT_ASSIGN", 
            "RIGHT_SHIFT_ASSIGN", "POWER_ASSIGN", "IDIV_ASSIGN", "SKIP_", 
            "UNKNOWN_CHAR" ]

    ruleNames = [ "STRING", "NUMBER", "INTEGER", "DEF", "RETURN", "RAISE", 
                  "FROM", "IMPORT", "AS", "GLOBAL", "NONLOCAL", "ASSERT", 
                  "IF", "ELIF", "ELSE", "WHILE", "FOR", "IN", "TRY", "FINALLY", 
                  "WITH", "EXCEPT", "LAMBDA", "OR", "AND", "NOT", "IS", 
                  "NONE", "TRUE", "FALSE", "CLASS", "YIELD", "DEL", "PASS", 
                  "CONTINUE", "BREAK", "ASYNC", "AWAIT", "NEWLINE", "NAME", 
                  "STRING_LITERAL", "BYTES_LITERAL", "DECIMAL_INTEGER", 
                  "OCT_INTEGER", "HEX_INTEGER", "BIN_INTEGER", "FLOAT_NUMBER", 
                  "IMAG_NUMBER", "DOT", "ELLIPSIS", "STAR", "OPEN_PAREN", 
                  "CLOSE_PAREN", "COMMA", "COLON", "SEMI_COLON", "POWER", 
                  "ASSIGN", "OPEN_BRACK", "CLOSE_BRACK", "OR_OP", "XOR", 
                  "AND_OP", "LEFT_SHIFT", "RIGHT_SHIFT", "ADD", "MINUS", 
                  "DIV", "MOD", "IDIV", "NOT_OP", "OPEN_BRACE", "CLOSE_BRACE", 
                  "LESS_THAN", "GREATER_THAN", "EQUALS", "GT_EQ", "LT_EQ", 
                  "NOT_EQ_1", "NOT_EQ_2", "AT", "ARROW", "ADD_ASSIGN", "SUB_ASSIGN", 
                  "MULT_ASSIGN", "AT_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", 
                  "AND_ASSIGN", "OR_ASSIGN", "XOR_ASSIGN", "LEFT_SHIFT_ASSIGN", 
                  "RIGHT_SHIFT_ASSIGN", "POWER_ASSIGN", "IDIV_ASSIGN", "SKIP_", 
                  "UNKNOWN_CHAR", "SHORT_STRING", "LONG_STRING", "LONG_STRING_ITEM", 
                  "LONG_STRING_CHAR", "STRING_ESCAPE_SEQ", "NON_ZERO_DIGIT", 
                  "DIGIT", "OCT_DIGIT", "HEX_DIGIT", "BIN_DIGIT", "POINT_FLOAT", 
                  "EXPONENT_FLOAT", "INT_PART", "FRACTION", "EXPONENT", 
                  "SHORT_BYTES", "LONG_BYTES", "LONG_BYTES_ITEM", "SHORT_BYTES_CHAR_NO_SINGLE_QUOTE", 
                  "SHORT_BYTES_CHAR_NO_DOUBLE_QUOTE", "LONG_BYTES_CHAR", 
                  "BYTES_ESCAPE_SEQ", "SPACES", "COMMENT", "LINE_JOINING", 
                  "ID_START", "ID_CONTINUE" ]

    grammarFileName = "Python3.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    @property
    def tokens(self):
        try:
            return self._tokens
        except AttributeError:
            self._tokens = []
            return self._tokens

    @property
    def indents(self):
        try:
            return self._indents
        except AttributeError:
            self._indents = []
            return self._indents

    @property
    def opened(self):
        try:
            return self._opened
        except AttributeError:
            self._opened = 0
            return self._opened

    @opened.setter
    def opened(self, value):
        self._opened = value

    @property
    def lastToken(self):
        try:
            return self._lastToken
        except AttributeError:
            self._lastToken = None
            return self._lastToken

    @lastToken.setter
    def lastToken(self, value):
        self._lastToken = value

    def reset(self):
        super().reset()
        self.tokens = []
        self.indents = []
        self.opened = 0
        self.lastToken = None

    def emitToken(self, t):
        super().emitToken(t)
        self.tokens.append(t)

    def nextToken(self):
        if self._input.LA(1) == Token.EOF and self.indents:
            for i in range(len(self.tokens)-1,-1,-1):
                if self.tokens[i].type == Token.EOF:
                    self.tokens.pop(i)

            self.emitToken(self.commonToken(LanguageParser.NEWLINE, '\n'))
            while self.indents:
                self.emitToken(self.createDedent())
                self.indents.pop()

            self.emitToken(self.commonToken(LanguageParser.EOF, '<EOF>'))

        next = super().nextToken()
        if next.channel == Token.DEFAULT_CHANNEL:
            self.lastToken = next
        return next if not self.tokens else self.tokens.pop(0)

    def createDedent(self):
        dedent = self.commonToken(LanguageParser.DEDENT, '')
        dedent.line = self.lastToken.line
        return dedent

    def commonToken(self, type, text, indent=0):
        stop = self.getCharIndex()-1-indent
        start = (stop - len(text) + 1) if text else stop
        return CommonToken(self._tokenFactorySourcePair, type, super().DEFAULT_TOKEN_CHANNEL, start, stop)

    @staticmethod
    def getIndentationCount(spaces):
        count = 0
        for ch in spaces:
            if ch == '\t':
                count += 8 - (count % 8)
            else:
                count += 1
        return count

    def atStartOfInput(self):
        return Lexer.column.fget(self) == 0 and Lexer.line.fget(self) == 1


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[38] = self.NEWLINE_action 
            actions[51] = self.OPEN_PAREN_action 
            actions[52] = self.CLOSE_PAREN_action 
            actions[58] = self.OPEN_BRACK_action 
            actions[59] = self.CLOSE_BRACK_action 
            actions[71] = self.OPEN_BRACE_action 
            actions[72] = self.CLOSE_BRACE_action 
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))


    def NEWLINE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 0:

            tempt = Lexer.text.fget(self)
            new_line = re.sub('[^\r\n\f]+', '', tempt)
            spaces = re.sub('[\r\n\f]+', '', tempt)
            la_char = ''
            try:
                la = self._input.LA(1)
                la_char = chr(la)  # Python does not compare char to ints directly
            except ValueError:  # End of file
                pass

            # Strip newlines inside open clauses except if we are near EOF. We keep NEWLINEs near EOF to
            # satisfy the final newline needed by the single_put rule used by the REPL.
            try:
                nextnext_la = self._input.LA(2)
                nextnext_la_char = chr(nextnext_la)
            except ValueError:
                nextnext_eof = True
            else:
                nextnext_eof = False

            if self.opened > 0 or not nextnext_eof and (la_char == '\r' or la_char == '\n' or la_char == '\f' or la_char == '#'):
                self.skip()
            else:
                indent = self.getIndentationCount(spaces)
                previous = self.indents[-1] if self.indents else 0
                self.emitToken(self.commonToken(self.NEWLINE, new_line, indent=indent))  # NEWLINE is actually the '\n' char
                if indent == previous:
                    self.skip()
                elif indent > previous:
                    self.indents.append(indent)
                    self.emitToken(self.commonToken(LanguageParser.INDENT, spaces))
                else:
                    while self.indents and self.indents[-1] > indent:
                        self.emitToken(self.createDedent())
                        self.indents.pop()
                
     

    def OPEN_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 1:
            self.opened += 1
     

    def CLOSE_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 2:
            self.opened -= 1
     

    def OPEN_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 3:
            self.opened += 1
     

    def CLOSE_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 4:
            self.opened -= 1
     

    def OPEN_BRACE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 5:
            self.opened += 1
     

    def CLOSE_BRACE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 6:
            self.opened -= 1
     

    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates is None:
            preds = dict()
            preds[38] = self.NEWLINE_sempred
            self._predicates = preds
        pred = self._predicates.get(ruleIndex, None)
        if pred is not None:
            return pred(localctx, predIndex)
        else:
            raise Exception("No registered predicate for:" + str(ruleIndex))

    def NEWLINE_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 0:
                return self.atStartOfInput()
         

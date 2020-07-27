# flake8: noqa
# type: ignore
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
        buf.write("\5\3\5\3\5\3\5\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7")
        buf.write("\3\b\3\b\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\t\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\13\3\f\3")
        buf.write("\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\16\3")
        buf.write("\16\3\16\3\16\3\17\3\17\3\17\3\17\3\17\3\20\3\20\3\20")
        buf.write("\3\20\3\20\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\22\3\22")
        buf.write("\3\22\3\22\3\22\3\22\3\23\3\23\3\23\3\23\3\23\3\23\3\23")
        buf.write("\3\23\3\24\3\24\3\24\3\24\3\25\3\25\3\25\3\25\3\25\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\27\3\27\3\27\3\30\3\30")
        buf.write("\3\30\3\30\3\30\3\30\3\30\3\31\3\31\3\31\3\32\3\32\3\32")
        buf.write("\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\34")
        buf.write("\3\34\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\35\3\36")
        buf.write("\3\36\3\36\3\36\3\37\3\37\3\37\3 \3 \3 \3 \3 \3!\3!\3")
        buf.write("!\3!\3!\3!\3\"\3\"\3\"\3\"\3\"\3\"\3\"\3#\3#\3#\3#\3#")
        buf.write("\3$\3$\3$\3$\3%\3%\3%\3%\3%\3%\3&\3&\3&\3&\3&\3\'\3\'")
        buf.write("\3\'\3\'\3\'\3\'\3(\3(\3(\5(\u01cc\n(\3(\3(\5(\u01d0\n")
        buf.write("(\3(\5(\u01d3\n(\5(\u01d5\n(\3(\3(\3)\3)\7)\u01db\n)\f")
        buf.write(")\16)\u01de\13)\3*\3*\3*\3*\3*\5*\u01e5\n*\3*\3*\5*\u01e9")
        buf.write("\n*\3+\3+\3+\3+\3+\5+\u01f0\n+\3+\3+\5+\u01f4\n+\3,\3")
        buf.write(",\5,\u01f8\n,\3,\7,\u01fb\n,\f,\16,\u01fe\13,\3,\6,\u0201")
        buf.write("\n,\r,\16,\u0202\5,\u0205\n,\3-\3-\3-\6-\u020a\n-\r-\16")
        buf.write("-\u020b\3.\3.\3.\6.\u0211\n.\r.\16.\u0212\3/\3/\3/\6/")
        buf.write("\u0218\n/\r/\16/\u0219\3\60\3\60\5\60\u021e\n\60\3\61")
        buf.write("\3\61\5\61\u0222\n\61\3\61\3\61\3\62\3\62\3\63\3\63\3")
        buf.write("\63\3\64\3\64\3\64\3\65\3\65\3\66\3\66\3\66\3\67\3\67")
        buf.write("\38\38\39\39\39\3:\3:\3:\3;\3;\3;\3<\3<\3<\3=\3=\3>\3")
        buf.write(">\3?\3?\3@\3@\3@\3A\3A\3B\3B\3B\3B\3C\3C\3C\3D\3D\3E\3")
        buf.write("E\3E\3F\3F\3F\3G\3G\3G\3G\3H\3H\3H\3I\3I\3I\3I\3J\3J\3")
        buf.write("K\3K\3K\3L\3L\3M\3M\3N\3N\3N\3O\3O\3O\3P\3P\3P\3Q\3Q\3")
        buf.write("Q\3R\3R\3S\3S\3S\3T\3T\3T\3U\3U\3U\3V\3V\3V\3W\3W\3X\3")
        buf.write("X\3X\3Y\3Y\3Y\3Y\3Z\3Z\3Z\3[\3[\3[\3[\3\\\3\\\3]\3]\3")
        buf.write("^\3^\3^\3_\3_\3`\3`\3`\3a\3a\3a\5a\u02aa\na\3a\3a\3b\3")
        buf.write("b\3c\3c\3c\7c\u02b3\nc\fc\16c\u02b6\13c\3c\3c\3c\3c\7")
        buf.write("c\u02bc\nc\fc\16c\u02bf\13c\3c\5c\u02c2\nc\3d\3d\3d\3")
        buf.write("d\3d\7d\u02c9\nd\fd\16d\u02cc\13d\3d\3d\3d\3d\3d\3d\3")
        buf.write("d\3d\7d\u02d6\nd\fd\16d\u02d9\13d\3d\3d\3d\5d\u02de\n")
        buf.write("d\3e\3e\5e\u02e2\ne\3f\3f\3g\3g\3g\3g\5g\u02ea\ng\3h\3")
        buf.write("h\3i\3i\3j\3j\3k\3k\3l\3l\3m\5m\u02f7\nm\3m\3m\3m\3m\5")
        buf.write("m\u02fd\nm\3n\3n\5n\u0301\nn\3n\3n\3o\3o\5o\u0307\no\3")
        buf.write("o\7o\u030a\no\fo\16o\u030d\13o\3p\3p\3p\5p\u0312\np\3")
        buf.write("p\7p\u0315\np\fp\16p\u0318\13p\3q\3q\5q\u031c\nq\3q\3")
        buf.write("q\5q\u0320\nq\3q\7q\u0323\nq\fq\16q\u0326\13q\3r\3r\3")
        buf.write("r\7r\u032b\nr\fr\16r\u032e\13r\3r\3r\3r\3r\7r\u0334\n")
        buf.write("r\fr\16r\u0337\13r\3r\5r\u033a\nr\3s\3s\3s\3s\3s\7s\u0341")
        buf.write("\ns\fs\16s\u0344\13s\3s\3s\3s\3s\3s\3s\3s\3s\7s\u034e")
        buf.write("\ns\fs\16s\u0351\13s\3s\3s\3s\5s\u0356\ns\3t\3t\5t\u035a")
        buf.write("\nt\3u\5u\u035d\nu\3v\5v\u0360\nv\3w\5w\u0363\nw\3x\3")
        buf.write("x\3x\3y\6y\u0369\ny\ry\16y\u036a\3z\3z\7z\u036f\nz\fz")
        buf.write("\16z\u0372\13z\3{\3{\5{\u0376\n{\3{\5{\u0379\n{\3{\3{")
        buf.write("\5{\u037d\n{\3|\5|\u0380\n|\3}\3}\5}\u0384\n}\6\u02ca")
        buf.write("\u02d7\u0342\u034f\2~\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21")
        buf.write("\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24")
        buf.write("\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67\359\36;\37")
        buf.write("= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61a\62c\63e\64")
        buf.write("g\65i\66k\67m8o9q:s;u<w=y>{?}@\177A\u0081B\u0083C\u0085")
        buf.write("D\u0087E\u0089F\u008bG\u008dH\u008fI\u0091J\u0093K\u0095")
        buf.write("L\u0097M\u0099N\u009bO\u009dP\u009fQ\u00a1R\u00a3S\u00a5")
        buf.write("T\u00a7U\u00a9V\u00abW\u00adX\u00afY\u00b1Z\u00b3[\u00b5")
        buf.write("\\\u00b7]\u00b9^\u00bb_\u00bd`\u00bfa\u00c1b\u00c3c\u00c5")
        buf.write("\2\u00c7\2\u00c9\2\u00cb\2\u00cd\2\u00cf\2\u00d1\2\u00d3")
        buf.write("\2\u00d5\2\u00d7\2\u00d9\2\u00db\2\u00dd\2\u00df\2\u00e1")
        buf.write("\2\u00e3\2\u00e5\2\u00e7\2\u00e9\2\u00eb\2\u00ed\2\u00ef")
        buf.write("\2\u00f1\2\u00f3\2\u00f5\2\u00f7\2\u00f9\2\3\2\33\b\2")
        buf.write("HHTTWWhhttww\4\2HHhh\4\2TTtt\4\2DDdd\4\2QQqq\4\2ZZzz\4")
        buf.write("\2LLll\6\2\f\f\16\17))^^\6\2\f\f\16\17$$^^\3\2^^\3\2\63")
        buf.write(";\3\2\62;\3\2\629\5\2\62;CHch\3\2\62\63\4\2GGgg\4\2--")
        buf.write("//\7\2\2\13\r\16\20(*]_\u0081\7\2\2\13\r\16\20#%]_\u0081")
        buf.write("\4\2\2]_\u0081\3\2\2\u0081\4\2\13\13\"\"\4\2\f\f\16\17")
        buf.write("\u0129\2C\\aac|\u00ac\u00ac\u00b7\u00b7\u00bc\u00bc\u00c2")
        buf.write("\u00d8\u00da\u00f8\u00fa\u0243\u0252\u02c3\u02c8\u02d3")
        buf.write("\u02e2\u02e6\u02f0\u02f0\u037c\u037c\u0388\u0388\u038a")
        buf.write("\u038c\u038e\u038e\u0390\u03a3\u03a5\u03d0\u03d2\u03f7")
        buf.write("\u03f9\u0483\u048c\u04d0\u04d2\u04fb\u0502\u0511\u0533")
        buf.write("\u0558\u055b\u055b\u0563\u0589\u05d2\u05ec\u05f2\u05f4")
        buf.write("\u0623\u063c\u0642\u064c\u0670\u0671\u0673\u06d5\u06d7")
        buf.write("\u06d7\u06e7\u06e8\u06f0\u06f1\u06fc\u06fe\u0701\u0701")
        buf.write("\u0712\u0712\u0714\u0731\u074f\u076f\u0782\u07a7\u07b3")
        buf.write("\u07b3\u0906\u093b\u093f\u093f\u0952\u0952\u095a\u0963")
        buf.write("\u097f\u097f\u0987\u098e\u0991\u0992\u0995\u09aa\u09ac")
        buf.write("\u09b2\u09b4\u09b4\u09b8\u09bb\u09bf\u09bf\u09d0\u09d0")
        buf.write("\u09de\u09df\u09e1\u09e3\u09f2\u09f3\u0a07\u0a0c\u0a11")
        buf.write("\u0a12\u0a15\u0a2a\u0a2c\u0a32\u0a34\u0a35\u0a37\u0a38")
        buf.write("\u0a3a\u0a3b\u0a5b\u0a5e\u0a60\u0a60\u0a74\u0a76\u0a87")
        buf.write("\u0a8f\u0a91\u0a93\u0a95\u0aaa\u0aac\u0ab2\u0ab4\u0ab5")
        buf.write("\u0ab7\u0abb\u0abf\u0abf\u0ad2\u0ad2\u0ae2\u0ae3\u0b07")
        buf.write("\u0b0e\u0b11\u0b12\u0b15\u0b2a\u0b2c\u0b32\u0b34\u0b35")
        buf.write("\u0b37\u0b3b\u0b3f\u0b3f\u0b5e\u0b5f\u0b61\u0b63\u0b73")
        buf.write("\u0b73\u0b85\u0b85\u0b87\u0b8c\u0b90\u0b92\u0b94\u0b97")
        buf.write("\u0b9b\u0b9c\u0b9e\u0b9e\u0ba0\u0ba1\u0ba5\u0ba6\u0baa")
        buf.write("\u0bac\u0bb0\u0bbb\u0c07\u0c0e\u0c10\u0c12\u0c14\u0c2a")
        buf.write("\u0c2c\u0c35\u0c37\u0c3b\u0c62\u0c63\u0c87\u0c8e\u0c90")
        buf.write("\u0c92\u0c94\u0caa\u0cac\u0cb5\u0cb7\u0cbb\u0cbf\u0cbf")
        buf.write("\u0ce0\u0ce0\u0ce2\u0ce3\u0d07\u0d0e\u0d10\u0d12\u0d14")
        buf.write("\u0d2a\u0d2c\u0d3b\u0d62\u0d63\u0d87\u0d98\u0d9c\u0db3")
        buf.write("\u0db5\u0dbd\u0dbf\u0dbf\u0dc2\u0dc8\u0e03\u0e32\u0e34")
        buf.write("\u0e35\u0e42\u0e48\u0e83\u0e84\u0e86\u0e86\u0e89\u0e8a")
        buf.write("\u0e8c\u0e8c\u0e8f\u0e8f\u0e96\u0e99\u0e9b\u0ea1\u0ea3")
        buf.write("\u0ea5\u0ea7\u0ea7\u0ea9\u0ea9\u0eac\u0ead\u0eaf\u0eb2")
        buf.write("\u0eb4\u0eb5\u0ebf\u0ebf\u0ec2\u0ec6\u0ec8\u0ec8\u0ede")
        buf.write("\u0edf\u0f02\u0f02\u0f42\u0f49\u0f4b\u0f6c\u0f8a\u0f8d")
        buf.write("\u1002\u1023\u1025\u1029\u102b\u102c\u1052\u1057\u10a2")
        buf.write("\u10c7\u10d2\u10fc\u10fe\u10fe\u1102\u115b\u1161\u11a4")
        buf.write("\u11aa\u11fb\u1202\u124a\u124c\u124f\u1252\u1258\u125a")
        buf.write("\u125a\u125c\u125f\u1262\u128a\u128c\u128f\u1292\u12b2")
        buf.write("\u12b4\u12b7\u12ba\u12c0\u12c2\u12c2\u12c4\u12c7\u12ca")
        buf.write("\u12d8\u12da\u1312\u1314\u1317\u131a\u135c\u1382\u1391")
        buf.write("\u13a2\u13f6\u1403\u166e\u1671\u1678\u1683\u169c\u16a2")
        buf.write("\u16ec\u16f0\u16f2\u1702\u170e\u1710\u1713\u1722\u1733")
        buf.write("\u1742\u1753\u1762\u176e\u1770\u1772\u1782\u17b5\u17d9")
        buf.write("\u17d9\u17de\u17de\u1822\u1879\u1882\u18aa\u1902\u191e")
        buf.write("\u1952\u196f\u1972\u1976\u1982\u19ab\u19c3\u19c9\u1a02")
        buf.write("\u1a18\u1d02\u1dc1\u1e02\u1e9d\u1ea2\u1efb\u1f02\u1f17")
        buf.write("\u1f1a\u1f1f\u1f22\u1f47\u1f4a\u1f4f\u1f52\u1f59\u1f5b")
        buf.write("\u1f5b\u1f5d\u1f5d\u1f5f\u1f5f\u1f61\u1f7f\u1f82\u1fb6")
        buf.write("\u1fb8\u1fbe\u1fc0\u1fc0\u1fc4\u1fc6\u1fc8\u1fce\u1fd2")
        buf.write("\u1fd5\u1fd8\u1fdd\u1fe2\u1fee\u1ff4\u1ff6\u1ff8\u1ffe")
        buf.write("\u2073\u2073\u2081\u2081\u2092\u2096\u2104\u2104\u2109")
        buf.write("\u2109\u210c\u2115\u2117\u2117\u211a\u211f\u2126\u2126")
        buf.write("\u2128\u2128\u212a\u212a\u212c\u2133\u2135\u213b\u213e")
        buf.write("\u2141\u2147\u214b\u2162\u2185\u2c02\u2c30\u2c32\u2c60")
        buf.write("\u2c82\u2ce6\u2d02\u2d27\u2d32\u2d67\u2d71\u2d71\u2d82")
        buf.write("\u2d98\u2da2\u2da8\u2daa\u2db0\u2db2\u2db8\u2dba\u2dc0")
        buf.write("\u2dc2\u2dc8\u2dca\u2dd0\u2dd2\u2dd8\u2dda\u2de0\u3007")
        buf.write("\u3009\u3023\u302b\u3033\u3037\u303a\u303e\u3043\u3098")
        buf.write("\u309d\u30a1\u30a3\u30fc\u30fe\u3101\u3107\u312e\u3133")
        buf.write("\u3190\u31a2\u31b9\u31f2\u3201\u3402\u4db7\u4e02\u9fbd")
        buf.write("\ua002\ua48e\ua802\ua803\ua805\ua807\ua809\ua80c\ua80e")
        buf.write("\ua824\uac02\ud7a5\uf902\ufa2f\ufa32\ufa6c\ufa72\ufadb")
        buf.write("\ufb02\ufb08\ufb15\ufb19\ufb1f\ufb1f\ufb21\ufb2a\ufb2c")
        buf.write("\ufb38\ufb3a\ufb3e\ufb40\ufb40\ufb42\ufb43\ufb45\ufb46")
        buf.write("\ufb48\ufbb3\ufbd5\ufd3f\ufd52\ufd91\ufd94\ufdc9\ufdf2")
        buf.write("\ufdfd\ufe72\ufe76\ufe78\ufefe\uff23\uff3c\uff43\uff5c")
        buf.write("\uff68\uffc0\uffc4\uffc9\uffcc\uffd1\uffd4\uffd9\uffdc")
        buf.write("\uffde\u0096\2\62;\u0302\u0371\u0485\u0488\u0593\u05bb")
        buf.write("\u05bd\u05bf\u05c1\u05c1\u05c3\u05c4\u05c6\u05c7\u05c9")
        buf.write("\u05c9\u0612\u0617\u064d\u0660\u0662\u066b\u0672\u0672")
        buf.write("\u06d8\u06de\u06e1\u06e6\u06e9\u06ea\u06ec\u06ef\u06f2")
        buf.write("\u06fb\u0713\u0713\u0732\u074c\u07a8\u07b2\u0903\u0905")
        buf.write("\u093e\u093e\u0940\u094f\u0953\u0956\u0964\u0965\u0968")
        buf.write("\u0971\u0983\u0985\u09be\u09be\u09c0\u09c6\u09c9\u09ca")
        buf.write("\u09cd\u09cf\u09d9\u09d9\u09e4\u09e5\u09e8\u09f1\u0a03")
        buf.write("\u0a05\u0a3e\u0a3e\u0a40\u0a44\u0a49\u0a4a\u0a4d\u0a4f")
        buf.write("\u0a68\u0a73\u0a83\u0a85\u0abe\u0abe\u0ac0\u0ac7\u0ac9")
        buf.write("\u0acb\u0acd\u0acf\u0ae4\u0ae5\u0ae8\u0af1\u0b03\u0b05")
        buf.write("\u0b3e\u0b3e\u0b40\u0b45\u0b49\u0b4a\u0b4d\u0b4f\u0b58")
        buf.write("\u0b59\u0b68\u0b71\u0b84\u0b84\u0bc0\u0bc4\u0bc8\u0bca")
        buf.write("\u0bcc\u0bcf\u0bd9\u0bd9\u0be8\u0bf1\u0c03\u0c05\u0c40")
        buf.write("\u0c46\u0c48\u0c4a\u0c4c\u0c4f\u0c57\u0c58\u0c68\u0c71")
        buf.write("\u0c84\u0c85\u0cbe\u0cbe\u0cc0\u0cc6\u0cc8\u0cca\u0ccc")
        buf.write("\u0ccf\u0cd7\u0cd8\u0ce8\u0cf1\u0d04\u0d05\u0d40\u0d45")
        buf.write("\u0d48\u0d4a\u0d4c\u0d4f\u0d59\u0d59\u0d68\u0d71\u0d84")
        buf.write("\u0d85\u0dcc\u0dcc\u0dd1\u0dd6\u0dd8\u0dd8\u0dda\u0de1")
        buf.write("\u0df4\u0df5\u0e33\u0e33\u0e36\u0e3c\u0e49\u0e50\u0e52")
        buf.write("\u0e5b\u0eb3\u0eb3\u0eb6\u0ebb\u0ebd\u0ebe\u0eca\u0ecf")
        buf.write("\u0ed2\u0edb\u0f1a\u0f1b\u0f22\u0f2b\u0f37\u0f37\u0f39")
        buf.write("\u0f39\u0f3b\u0f3b\u0f40\u0f41\u0f73\u0f86\u0f88\u0f89")
        buf.write("\u0f92\u0f99\u0f9b\u0fbe\u0fc8\u0fc8\u102e\u1034\u1038")
        buf.write("\u103b\u1042\u104b\u1058\u105b\u1361\u1361\u136b\u1373")
        buf.write("\u1714\u1716\u1734\u1736\u1754\u1755\u1774\u1775\u17b8")
        buf.write("\u17d5\u17df\u17df\u17e2\u17eb\u180d\u180f\u1812\u181b")
        buf.write("\u18ab\u18ab\u1922\u192d\u1932\u193d\u1948\u1951\u19b2")
        buf.write("\u19c2\u19ca\u19cb\u19d2\u19db\u1a19\u1a1d\u1dc2\u1dc5")
        buf.write("\u2041\u2042\u2056\u2056\u20d2\u20de\u20e3\u20e3\u20e7")
        buf.write("\u20ed\u302c\u3031\u309b\u309c\ua804\ua804\ua808\ua808")
        buf.write("\ua80d\ua80d\ua825\ua829\ufb20\ufb20\ufe02\ufe11\ufe22")
        buf.write("\ufe25\ufe35\ufe36\ufe4f\ufe51\uff12\uff1b\uff41\uff41")
        buf.write("\2\u03a9\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2")
        buf.write("\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2")
        buf.write("\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2")
        buf.write("\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3")
        buf.write("\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2")
        buf.write("-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3")
        buf.write("\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2")
        buf.write("?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2")
        buf.write("\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2")
        buf.write("\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2")
        buf.write("\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3")
        buf.write("\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o")
        buf.write("\3\2\2\2\2q\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2")
        buf.write("y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\2\u0081")
        buf.write("\3\2\2\2\2\u0083\3\2\2\2\2\u0085\3\2\2\2\2\u0087\3\2\2")
        buf.write("\2\2\u0089\3\2\2\2\2\u008b\3\2\2\2\2\u008d\3\2\2\2\2\u008f")
        buf.write("\3\2\2\2\2\u0091\3\2\2\2\2\u0093\3\2\2\2\2\u0095\3\2\2")
        buf.write("\2\2\u0097\3\2\2\2\2\u0099\3\2\2\2\2\u009b\3\2\2\2\2\u009d")
        buf.write("\3\2\2\2\2\u009f\3\2\2\2\2\u00a1\3\2\2\2\2\u00a3\3\2\2")
        buf.write("\2\2\u00a5\3\2\2\2\2\u00a7\3\2\2\2\2\u00a9\3\2\2\2\2\u00ab")
        buf.write("\3\2\2\2\2\u00ad\3\2\2\2\2\u00af\3\2\2\2\2\u00b1\3\2\2")
        buf.write("\2\2\u00b3\3\2\2\2\2\u00b5\3\2\2\2\2\u00b7\3\2\2\2\2\u00b9")
        buf.write("\3\2\2\2\2\u00bb\3\2\2\2\2\u00bd\3\2\2\2\2\u00bf\3\2\2")
        buf.write("\2\2\u00c1\3\2\2\2\2\u00c3\3\2\2\2\3\u00fd\3\2\2\2\5\u0102")
        buf.write("\3\2\2\2\7\u0108\3\2\2\2\t\u010a\3\2\2\2\13\u010e\3\2")
        buf.write("\2\2\r\u0111\3\2\2\2\17\u0118\3\2\2\2\21\u011e\3\2\2\2")
        buf.write("\23\u0124\3\2\2\2\25\u012a\3\2\2\2\27\u0130\3\2\2\2\31")
        buf.write("\u0139\3\2\2\2\33\u013d\3\2\2\2\35\u0141\3\2\2\2\37\u0146")
        buf.write("\3\2\2\2!\u014b\3\2\2\2#\u0152\3\2\2\2%\u0158\3\2\2\2")
        buf.write("\'\u0160\3\2\2\2)\u0164\3\2\2\2+\u0169\3\2\2\2-\u0170")
        buf.write("\3\2\2\2/\u0173\3\2\2\2\61\u017a\3\2\2\2\63\u017d\3\2")
        buf.write("\2\2\65\u0180\3\2\2\2\67\u0187\3\2\2\29\u018c\3\2\2\2")
        buf.write(";\u0195\3\2\2\2=\u0199\3\2\2\2?\u019c\3\2\2\2A\u01a1\3")
        buf.write("\2\2\2C\u01a7\3\2\2\2E\u01ae\3\2\2\2G\u01b3\3\2\2\2I\u01b7")
        buf.write("\3\2\2\2K\u01bd\3\2\2\2M\u01c2\3\2\2\2O\u01d4\3\2\2\2")
        buf.write("Q\u01d8\3\2\2\2S\u01e4\3\2\2\2U\u01ef\3\2\2\2W\u0204\3")
        buf.write("\2\2\2Y\u0206\3\2\2\2[\u020d\3\2\2\2]\u0214\3\2\2\2_\u021d")
        buf.write("\3\2\2\2a\u0221\3\2\2\2c\u0225\3\2\2\2e\u0227\3\2\2\2")
        buf.write("g\u022a\3\2\2\2i\u022d\3\2\2\2k\u022f\3\2\2\2m\u0232\3")
        buf.write("\2\2\2o\u0234\3\2\2\2q\u0236\3\2\2\2s\u0239\3\2\2\2u\u023c")
        buf.write("\3\2\2\2w\u023f\3\2\2\2y\u0242\3\2\2\2{\u0244\3\2\2\2")
        buf.write("}\u0246\3\2\2\2\177\u0248\3\2\2\2\u0081\u024b\3\2\2\2")
        buf.write("\u0083\u024d\3\2\2\2\u0085\u0251\3\2\2\2\u0087\u0254\3")
        buf.write("\2\2\2\u0089\u0256\3\2\2\2\u008b\u0259\3\2\2\2\u008d\u025c")
        buf.write("\3\2\2\2\u008f\u0260\3\2\2\2\u0091\u0263\3\2\2\2\u0093")
        buf.write("\u0267\3\2\2\2\u0095\u0269\3\2\2\2\u0097\u026c\3\2\2\2")
        buf.write("\u0099\u026e\3\2\2\2\u009b\u0270\3\2\2\2\u009d\u0273\3")
        buf.write("\2\2\2\u009f\u0276\3\2\2\2\u00a1\u0279\3\2\2\2\u00a3\u027c")
        buf.write("\3\2\2\2\u00a5\u027e\3\2\2\2\u00a7\u0281\3\2\2\2\u00a9")
        buf.write("\u0284\3\2\2\2\u00ab\u0287\3\2\2\2\u00ad\u028a\3\2\2\2")
        buf.write("\u00af\u028c\3\2\2\2\u00b1\u028f\3\2\2\2\u00b3\u0293\3")
        buf.write("\2\2\2\u00b5\u0296\3\2\2\2\u00b7\u029a\3\2\2\2\u00b9\u029c")
        buf.write("\3\2\2\2\u00bb\u029e\3\2\2\2\u00bd\u02a1\3\2\2\2\u00bf")
        buf.write("\u02a3\3\2\2\2\u00c1\u02a9\3\2\2\2\u00c3\u02ad\3\2\2\2")
        buf.write("\u00c5\u02c1\3\2\2\2\u00c7\u02dd\3\2\2\2\u00c9\u02e1\3")
        buf.write("\2\2\2\u00cb\u02e3\3\2\2\2\u00cd\u02e9\3\2\2\2\u00cf\u02eb")
        buf.write("\3\2\2\2\u00d1\u02ed\3\2\2\2\u00d3\u02ef\3\2\2\2\u00d5")
        buf.write("\u02f1\3\2\2\2\u00d7\u02f3\3\2\2\2\u00d9\u02fc\3\2\2\2")
        buf.write("\u00db\u0300\3\2\2\2\u00dd\u0304\3\2\2\2\u00df\u030e\3")
        buf.write("\2\2\2\u00e1\u0319\3\2\2\2\u00e3\u0339\3\2\2\2\u00e5\u0355")
        buf.write("\3\2\2\2\u00e7\u0359\3\2\2\2\u00e9\u035c\3\2\2\2\u00eb")
        buf.write("\u035f\3\2\2\2\u00ed\u0362\3\2\2\2\u00ef\u0364\3\2\2\2")
        buf.write("\u00f1\u0368\3\2\2\2\u00f3\u036c\3\2\2\2\u00f5\u0373\3")
        buf.write("\2\2\2\u00f7\u037f\3\2\2\2\u00f9\u0383\3\2\2\2\u00fb\u00fe")
        buf.write("\5S*\2\u00fc\u00fe\5U+\2\u00fd\u00fb\3\2\2\2\u00fd\u00fc")
        buf.write("\3\2\2\2\u00fe\4\3\2\2\2\u00ff\u0103\5\7\4\2\u0100\u0103")
        buf.write("\5_\60\2\u0101\u0103\5a\61\2\u0102\u00ff\3\2\2\2\u0102")
        buf.write("\u0100\3\2\2\2\u0102\u0101\3\2\2\2\u0103\6\3\2\2\2\u0104")
        buf.write("\u0109\5W,\2\u0105\u0109\5Y-\2\u0106\u0109\5[.\2\u0107")
        buf.write("\u0109\5]/\2\u0108\u0104\3\2\2\2\u0108\u0105\3\2\2\2\u0108")
        buf.write("\u0106\3\2\2\2\u0108\u0107\3\2\2\2\u0109\b\3\2\2\2\u010a")
        buf.write("\u010b\7c\2\2\u010b\u010c\7p\2\2\u010c\u010d\7f\2\2\u010d")
        buf.write("\n\3\2\2\2\u010e\u010f\7c\2\2\u010f\u0110\7u\2\2\u0110")
        buf.write("\f\3\2\2\2\u0111\u0112\7c\2\2\u0112\u0113\7u\2\2\u0113")
        buf.write("\u0114\7u\2\2\u0114\u0115\7g\2\2\u0115\u0116\7t\2\2\u0116")
        buf.write("\u0117\7v\2\2\u0117\16\3\2\2\2\u0118\u0119\7c\2\2\u0119")
        buf.write("\u011a\7u\2\2\u011a\u011b\7{\2\2\u011b\u011c\7p\2\2\u011c")
        buf.write("\u011d\7e\2\2\u011d\20\3\2\2\2\u011e\u011f\7c\2\2\u011f")
        buf.write("\u0120\7y\2\2\u0120\u0121\7c\2\2\u0121\u0122\7k\2\2\u0122")
        buf.write("\u0123\7v\2\2\u0123\22\3\2\2\2\u0124\u0125\7d\2\2\u0125")
        buf.write("\u0126\7t\2\2\u0126\u0127\7g\2\2\u0127\u0128\7c\2\2\u0128")
        buf.write("\u0129\7m\2\2\u0129\24\3\2\2\2\u012a\u012b\7e\2\2\u012b")
        buf.write("\u012c\7n\2\2\u012c\u012d\7c\2\2\u012d\u012e\7u\2\2\u012e")
        buf.write("\u012f\7u\2\2\u012f\26\3\2\2\2\u0130\u0131\7e\2\2\u0131")
        buf.write("\u0132\7q\2\2\u0132\u0133\7p\2\2\u0133\u0134\7v\2\2\u0134")
        buf.write("\u0135\7k\2\2\u0135\u0136\7p\2\2\u0136\u0137\7w\2\2\u0137")
        buf.write("\u0138\7g\2\2\u0138\30\3\2\2\2\u0139\u013a\7f\2\2\u013a")
        buf.write("\u013b\7g\2\2\u013b\u013c\7h\2\2\u013c\32\3\2\2\2\u013d")
        buf.write("\u013e\7f\2\2\u013e\u013f\7g\2\2\u013f\u0140\7n\2\2\u0140")
        buf.write("\34\3\2\2\2\u0141\u0142\7g\2\2\u0142\u0143\7n\2\2\u0143")
        buf.write("\u0144\7k\2\2\u0144\u0145\7h\2\2\u0145\36\3\2\2\2\u0146")
        buf.write("\u0147\7g\2\2\u0147\u0148\7n\2\2\u0148\u0149\7u\2\2\u0149")
        buf.write("\u014a\7g\2\2\u014a \3\2\2\2\u014b\u014c\7g\2\2\u014c")
        buf.write("\u014d\7z\2\2\u014d\u014e\7e\2\2\u014e\u014f\7g\2\2\u014f")
        buf.write("\u0150\7r\2\2\u0150\u0151\7v\2\2\u0151\"\3\2\2\2\u0152")
        buf.write("\u0153\7H\2\2\u0153\u0154\7c\2\2\u0154\u0155\7n\2\2\u0155")
        buf.write("\u0156\7u\2\2\u0156\u0157\7g\2\2\u0157$\3\2\2\2\u0158")
        buf.write("\u0159\7h\2\2\u0159\u015a\7k\2\2\u015a\u015b\7p\2\2\u015b")
        buf.write("\u015c\7c\2\2\u015c\u015d\7n\2\2\u015d\u015e\7n\2\2\u015e")
        buf.write("\u015f\7{\2\2\u015f&\3\2\2\2\u0160\u0161\7h\2\2\u0161")
        buf.write("\u0162\7q\2\2\u0162\u0163\7t\2\2\u0163(\3\2\2\2\u0164")
        buf.write("\u0165\7h\2\2\u0165\u0166\7t\2\2\u0166\u0167\7q\2\2\u0167")
        buf.write("\u0168\7o\2\2\u0168*\3\2\2\2\u0169\u016a\7i\2\2\u016a")
        buf.write("\u016b\7n\2\2\u016b\u016c\7q\2\2\u016c\u016d\7d\2\2\u016d")
        buf.write("\u016e\7c\2\2\u016e\u016f\7n\2\2\u016f,\3\2\2\2\u0170")
        buf.write("\u0171\7k\2\2\u0171\u0172\7h\2\2\u0172.\3\2\2\2\u0173")
        buf.write("\u0174\7k\2\2\u0174\u0175\7o\2\2\u0175\u0176\7r\2\2\u0176")
        buf.write("\u0177\7q\2\2\u0177\u0178\7t\2\2\u0178\u0179\7v\2\2\u0179")
        buf.write("\60\3\2\2\2\u017a\u017b\7k\2\2\u017b\u017c\7p\2\2\u017c")
        buf.write("\62\3\2\2\2\u017d\u017e\7k\2\2\u017e\u017f\7u\2\2\u017f")
        buf.write("\64\3\2\2\2\u0180\u0181\7n\2\2\u0181\u0182\7c\2\2\u0182")
        buf.write("\u0183\7o\2\2\u0183\u0184\7d\2\2\u0184\u0185\7f\2\2\u0185")
        buf.write("\u0186\7c\2\2\u0186\66\3\2\2\2\u0187\u0188\7P\2\2\u0188")
        buf.write("\u0189\7q\2\2\u0189\u018a\7p\2\2\u018a\u018b\7g\2\2\u018b")
        buf.write("8\3\2\2\2\u018c\u018d\7p\2\2\u018d\u018e\7q\2\2\u018e")
        buf.write("\u018f\7p\2\2\u018f\u0190\7n\2\2\u0190\u0191\7q\2\2\u0191")
        buf.write("\u0192\7e\2\2\u0192\u0193\7c\2\2\u0193\u0194\7n\2\2\u0194")
        buf.write(":\3\2\2\2\u0195\u0196\7p\2\2\u0196\u0197\7q\2\2\u0197")
        buf.write("\u0198\7v\2\2\u0198<\3\2\2\2\u0199\u019a\7q\2\2\u019a")
        buf.write("\u019b\7t\2\2\u019b>\3\2\2\2\u019c\u019d\7r\2\2\u019d")
        buf.write("\u019e\7c\2\2\u019e\u019f\7u\2\2\u019f\u01a0\7u\2\2\u01a0")
        buf.write("@\3\2\2\2\u01a1\u01a2\7t\2\2\u01a2\u01a3\7c\2\2\u01a3")
        buf.write("\u01a4\7k\2\2\u01a4\u01a5\7u\2\2\u01a5\u01a6\7g\2\2\u01a6")
        buf.write("B\3\2\2\2\u01a7\u01a8\7t\2\2\u01a8\u01a9\7g\2\2\u01a9")
        buf.write("\u01aa\7v\2\2\u01aa\u01ab\7w\2\2\u01ab\u01ac\7t\2\2\u01ac")
        buf.write("\u01ad\7p\2\2\u01adD\3\2\2\2\u01ae\u01af\7V\2\2\u01af")
        buf.write("\u01b0\7t\2\2\u01b0\u01b1\7w\2\2\u01b1\u01b2\7g\2\2\u01b2")
        buf.write("F\3\2\2\2\u01b3\u01b4\7v\2\2\u01b4\u01b5\7t\2\2\u01b5")
        buf.write("\u01b6\7{\2\2\u01b6H\3\2\2\2\u01b7\u01b8\7y\2\2\u01b8")
        buf.write("\u01b9\7j\2\2\u01b9\u01ba\7k\2\2\u01ba\u01bb\7n\2\2\u01bb")
        buf.write("\u01bc\7g\2\2\u01bcJ\3\2\2\2\u01bd\u01be\7y\2\2\u01be")
        buf.write("\u01bf\7k\2\2\u01bf\u01c0\7v\2\2\u01c0\u01c1\7j\2\2\u01c1")
        buf.write("L\3\2\2\2\u01c2\u01c3\7{\2\2\u01c3\u01c4\7k\2\2\u01c4")
        buf.write("\u01c5\7g\2\2\u01c5\u01c6\7n\2\2\u01c6\u01c7\7f\2\2\u01c7")
        buf.write("N\3\2\2\2\u01c8\u01c9\6(\2\2\u01c9\u01d5\5\u00f1y\2\u01ca")
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
        buf.write("\u0223\u0224\t\b\2\2\u0224b\3\2\2\2\u0225\u0226\7-\2\2")
        buf.write("\u0226d\3\2\2\2\u0227\u0228\7-\2\2\u0228\u0229\7?\2\2")
        buf.write("\u0229f\3\2\2\2\u022a\u022b\7(\2\2\u022b\u022c\7?\2\2")
        buf.write("\u022ch\3\2\2\2\u022d\u022e\7(\2\2\u022ej\3\2\2\2\u022f")
        buf.write("\u0230\7/\2\2\u0230\u0231\7@\2\2\u0231l\3\2\2\2\u0232")
        buf.write("\u0233\7?\2\2\u0233n\3\2\2\2\u0234\u0235\7B\2\2\u0235")
        buf.write("p\3\2\2\2\u0236\u0237\7B\2\2\u0237\u0238\7?\2\2\u0238")
        buf.write("r\3\2\2\2\u0239\u023a\7\177\2\2\u023a\u023b\b:\3\2\u023b")
        buf.write("t\3\2\2\2\u023c\u023d\7_\2\2\u023d\u023e\b;\4\2\u023e")
        buf.write("v\3\2\2\2\u023f\u0240\7+\2\2\u0240\u0241\b<\5\2\u0241")
        buf.write("x\3\2\2\2\u0242\u0243\7<\2\2\u0243z\3\2\2\2\u0244\u0245")
        buf.write("\7.\2\2\u0245|\3\2\2\2\u0246\u0247\7\61\2\2\u0247~\3\2")
        buf.write("\2\2\u0248\u0249\7\61\2\2\u0249\u024a\7?\2\2\u024a\u0080")
        buf.write("\3\2\2\2\u024b\u024c\7\60\2\2\u024c\u0082\3\2\2\2\u024d")
        buf.write("\u024e\7\60\2\2\u024e\u024f\7\60\2\2\u024f\u0250\7\60")
        buf.write("\2\2\u0250\u0084\3\2\2\2\u0251\u0252\7?\2\2\u0252\u0253")
        buf.write("\7?\2\2\u0253\u0086\3\2\2\2\u0254\u0255\7@\2\2\u0255\u0088")
        buf.write("\3\2\2\2\u0256\u0257\7@\2\2\u0257\u0258\7?\2\2\u0258\u008a")
        buf.write("\3\2\2\2\u0259\u025a\7\61\2\2\u025a\u025b\7\61\2\2\u025b")
        buf.write("\u008c\3\2\2\2\u025c\u025d\7\61\2\2\u025d\u025e\7\61\2")
        buf.write("\2\u025e\u025f\7?\2\2\u025f\u008e\3\2\2\2\u0260\u0261")
        buf.write("\7>\2\2\u0261\u0262\7>\2\2\u0262\u0090\3\2\2\2\u0263\u0264")
        buf.write("\7>\2\2\u0264\u0265\7>\2\2\u0265\u0266\7?\2\2\u0266\u0092")
        buf.write("\3\2\2\2\u0267\u0268\7>\2\2\u0268\u0094\3\2\2\2\u0269")
        buf.write("\u026a\7>\2\2\u026a\u026b\7?\2\2\u026b\u0096\3\2\2\2\u026c")
        buf.write("\u026d\7/\2\2\u026d\u0098\3\2\2\2\u026e\u026f\7\'\2\2")
        buf.write("\u026f\u009a\3\2\2\2\u0270\u0271\7\'\2\2\u0271\u0272\7")
        buf.write("?\2\2\u0272\u009c\3\2\2\2\u0273\u0274\7,\2\2\u0274\u0275")
        buf.write("\7?\2\2\u0275\u009e\3\2\2\2\u0276\u0277\7>\2\2\u0277\u0278")
        buf.write("\7@\2\2\u0278\u00a0\3\2\2\2\u0279\u027a\7#\2\2\u027a\u027b")
        buf.write("\7?\2\2\u027b\u00a2\3\2\2\2\u027c\u027d\7\u0080\2\2\u027d")
        buf.write("\u00a4\3\2\2\2\u027e\u027f\7}\2\2\u027f\u0280\bS\6\2\u0280")
        buf.write("\u00a6\3\2\2\2\u0281\u0282\7]\2\2\u0282\u0283\bT\7\2\u0283")
        buf.write("\u00a8\3\2\2\2\u0284\u0285\7*\2\2\u0285\u0286\bU\b\2\u0286")
        buf.write("\u00aa\3\2\2\2\u0287\u0288\7~\2\2\u0288\u0289\7?\2\2\u0289")
        buf.write("\u00ac\3\2\2\2\u028a\u028b\7~\2\2\u028b\u00ae\3\2\2\2")
        buf.write("\u028c\u028d\7,\2\2\u028d\u028e\7,\2\2\u028e\u00b0\3\2")
        buf.write("\2\2\u028f\u0290\7,\2\2\u0290\u0291\7,\2\2\u0291\u0292")
        buf.write("\7?\2\2\u0292\u00b2\3\2\2\2\u0293\u0294\7@\2\2\u0294\u0295")
        buf.write("\7@\2\2\u0295\u00b4\3\2\2\2\u0296\u0297\7@\2\2\u0297\u0298")
        buf.write("\7@\2\2\u0298\u0299\7?\2\2\u0299\u00b6\3\2\2\2\u029a\u029b")
        buf.write("\7=\2\2\u029b\u00b8\3\2\2\2\u029c\u029d\7,\2\2\u029d\u00ba")
        buf.write("\3\2\2\2\u029e\u029f\7/\2\2\u029f\u02a0\7?\2\2\u02a0\u00bc")
        buf.write("\3\2\2\2\u02a1\u02a2\7`\2\2\u02a2\u00be\3\2\2\2\u02a3")
        buf.write("\u02a4\7`\2\2\u02a4\u02a5\7?\2\2\u02a5\u00c0\3\2\2\2\u02a6")
        buf.write("\u02aa\5\u00f1y\2\u02a7\u02aa\5\u00f3z\2\u02a8\u02aa\5")
        buf.write("\u00f5{\2\u02a9\u02a6\3\2\2\2\u02a9\u02a7\3\2\2\2\u02a9")
        buf.write("\u02a8\3\2\2\2\u02aa\u02ab\3\2\2\2\u02ab\u02ac\ba\t\2")
        buf.write("\u02ac\u00c2\3\2\2\2\u02ad\u02ae\13\2\2\2\u02ae\u00c4")
        buf.write("\3\2\2\2\u02af\u02b4\7)\2\2\u02b0\u02b3\5\u00cdg\2\u02b1")
        buf.write("\u02b3\n\t\2\2\u02b2\u02b0\3\2\2\2\u02b2\u02b1\3\2\2\2")
        buf.write("\u02b3\u02b6\3\2\2\2\u02b4\u02b2\3\2\2\2\u02b4\u02b5\3")
        buf.write("\2\2\2\u02b5\u02b7\3\2\2\2\u02b6\u02b4\3\2\2\2\u02b7\u02c2")
        buf.write("\7)\2\2\u02b8\u02bd\7$\2\2\u02b9\u02bc\5\u00cdg\2\u02ba")
        buf.write("\u02bc\n\n\2\2\u02bb\u02b9\3\2\2\2\u02bb\u02ba\3\2\2\2")
        buf.write("\u02bc\u02bf\3\2\2\2\u02bd\u02bb\3\2\2\2\u02bd\u02be\3")
        buf.write("\2\2\2\u02be\u02c0\3\2\2\2\u02bf\u02bd\3\2\2\2\u02c0\u02c2")
        buf.write("\7$\2\2\u02c1\u02af\3\2\2\2\u02c1\u02b8\3\2\2\2\u02c2")
        buf.write("\u00c6\3\2\2\2\u02c3\u02c4\7)\2\2\u02c4\u02c5\7)\2\2\u02c5")
        buf.write("\u02c6\7)\2\2\u02c6\u02ca\3\2\2\2\u02c7\u02c9\5\u00c9")
        buf.write("e\2\u02c8\u02c7\3\2\2\2\u02c9\u02cc\3\2\2\2\u02ca\u02cb")
        buf.write("\3\2\2\2\u02ca\u02c8\3\2\2\2\u02cb\u02cd\3\2\2\2\u02cc")
        buf.write("\u02ca\3\2\2\2\u02cd\u02ce\7)\2\2\u02ce\u02cf\7)\2\2\u02cf")
        buf.write("\u02de\7)\2\2\u02d0\u02d1\7$\2\2\u02d1\u02d2\7$\2\2\u02d2")
        buf.write("\u02d3\7$\2\2\u02d3\u02d7\3\2\2\2\u02d4\u02d6\5\u00c9")
        buf.write("e\2\u02d5\u02d4\3\2\2\2\u02d6\u02d9\3\2\2\2\u02d7\u02d8")
        buf.write("\3\2\2\2\u02d7\u02d5\3\2\2\2\u02d8\u02da\3\2\2\2\u02d9")
        buf.write("\u02d7\3\2\2\2\u02da\u02db\7$\2\2\u02db\u02dc\7$\2\2\u02dc")
        buf.write("\u02de\7$\2\2\u02dd\u02c3\3\2\2\2\u02dd\u02d0\3\2\2\2")
        buf.write("\u02de\u00c8\3\2\2\2\u02df\u02e2\5\u00cbf\2\u02e0\u02e2")
        buf.write("\5\u00cdg\2\u02e1\u02df\3\2\2\2\u02e1\u02e0\3\2\2\2\u02e2")
        buf.write("\u00ca\3\2\2\2\u02e3\u02e4\n\13\2\2\u02e4\u00cc\3\2\2")
        buf.write("\2\u02e5\u02e6\7^\2\2\u02e6\u02ea\13\2\2\2\u02e7\u02e8")
        buf.write("\7^\2\2\u02e8\u02ea\5O(\2\u02e9\u02e5\3\2\2\2\u02e9\u02e7")
        buf.write("\3\2\2\2\u02ea\u00ce\3\2\2\2\u02eb\u02ec\t\f\2\2\u02ec")
        buf.write("\u00d0\3\2\2\2\u02ed\u02ee\t\r\2\2\u02ee\u00d2\3\2\2\2")
        buf.write("\u02ef\u02f0\t\16\2\2\u02f0\u00d4\3\2\2\2\u02f1\u02f2")
        buf.write("\t\17\2\2\u02f2\u00d6\3\2\2\2\u02f3\u02f4\t\20\2\2\u02f4")
        buf.write("\u00d8\3\2\2\2\u02f5\u02f7\5\u00ddo\2\u02f6\u02f5\3\2")
        buf.write("\2\2\u02f6\u02f7\3\2\2\2\u02f7\u02f8\3\2\2\2\u02f8\u02fd")
        buf.write("\5\u00dfp\2\u02f9\u02fa\5\u00ddo\2\u02fa\u02fb\7\60\2")
        buf.write("\2\u02fb\u02fd\3\2\2\2\u02fc\u02f6\3\2\2\2\u02fc\u02f9")
        buf.write("\3\2\2\2\u02fd\u00da\3\2\2\2\u02fe\u0301\5\u00ddo\2\u02ff")
        buf.write("\u0301\5\u00d9m\2\u0300\u02fe\3\2\2\2\u0300\u02ff\3\2")
        buf.write("\2\2\u0301\u0302\3\2\2\2\u0302\u0303\5\u00e1q\2\u0303")
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
        buf.write("\u037f\u0383\n\3(\2\3:\3\3;\4\3<\5\3S\6\3T\7\3U\b\b\2")
        buf.write("\2")
        return buf.getvalue()


class Python3Lexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    STRING = 1
    NUMBER = 2
    INTEGER = 3
    AND = 4
    AS = 5
    ASSERT = 6
    ASYNC = 7
    AWAIT = 8
    BREAK = 9
    CLASS = 10
    CONTINUE = 11
    DEF = 12
    DEL = 13
    ELIF = 14
    ELSE = 15
    EXCEPT = 16
    FALSE = 17
    FINALLY = 18
    FOR = 19
    FROM = 20
    GLOBAL = 21
    IF = 22
    IMPORT = 23
    IN = 24
    IS = 25
    LAMBDA = 26
    NONE = 27
    NONLOCAL = 28
    NOT = 29
    OR = 30
    PASS = 31
    RAISE = 32
    RETURN = 33
    TRUE = 34
    TRY = 35
    WHILE = 36
    WITH = 37
    YIELD = 38
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
    ADD = 49
    ADD_ASSIGN = 50
    AND_ASSIGN = 51
    AND_OP = 52
    ARROW = 53
    ASSIGN = 54
    AT = 55
    AT_ASSIGN = 56
    CLOSE_BRACE = 57
    CLOSE_BRACK = 58
    CLOSE_PAREN = 59
    COLON = 60
    COMMA = 61
    DIV = 62
    DIV_ASSIGN = 63
    DOT = 64
    ELLIPSIS = 65
    EQUALS = 66
    GREATER_THAN = 67
    GT_EQ = 68
    IDIV = 69
    IDIV_ASSIGN = 70
    LEFT_SHIFT = 71
    LEFT_SHIFT_ASSIGN = 72
    LESS_THAN = 73
    LT_EQ = 74
    MINUS = 75
    MOD = 76
    MOD_ASSIGN = 77
    MULT_ASSIGN = 78
    NOT_EQ_1 = 79
    NOT_EQ_2 = 80
    NOT_OP = 81
    OPEN_BRACE = 82
    OPEN_BRACK = 83
    OPEN_PAREN = 84
    OR_ASSIGN = 85
    OR_OP = 86
    POWER = 87
    POWER_ASSIGN = 88
    RIGHT_SHIFT = 89
    RIGHT_SHIFT_ASSIGN = 90
    SEMI_COLON = 91
    STAR = 92
    SUB_ASSIGN = 93
    XOR = 94
    XOR_ASSIGN = 95
    SKIP_ = 96
    UNKNOWN_CHAR = 97

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'and'", "'as'", "'assert'", "'async'", "'await'", "'break'", 
            "'class'", "'continue'", "'def'", "'del'", "'elif'", "'else'", 
            "'except'", "'False'", "'finally'", "'for'", "'from'", "'global'", 
            "'if'", "'import'", "'in'", "'is'", "'lambda'", "'None'", "'nonlocal'", 
            "'not'", "'or'", "'pass'", "'raise'", "'return'", "'True'", 
            "'try'", "'while'", "'with'", "'yield'", "'+'", "'+='", "'&='", 
            "'&'", "'->'", "'='", "'@'", "'@='", "'}'", "']'", "')'", "':'", 
            "','", "'/'", "'/='", "'.'", "'...'", "'=='", "'>'", "'>='", 
            "'//'", "'//='", "'<<'", "'<<='", "'<'", "'<='", "'-'", "'%'", 
            "'%='", "'*='", "'<>'", "'!='", "'~'", "'{'", "'['", "'('", 
            "'|='", "'|'", "'**'", "'**='", "'>>'", "'>>='", "';'", "'*'", 
            "'-='", "'^'", "'^='" ]

    symbolicNames = [ "<INVALID>",
            "STRING", "NUMBER", "INTEGER", "AND", "AS", "ASSERT", "ASYNC", 
            "AWAIT", "BREAK", "CLASS", "CONTINUE", "DEF", "DEL", "ELIF", 
            "ELSE", "EXCEPT", "FALSE", "FINALLY", "FOR", "FROM", "GLOBAL", 
            "IF", "IMPORT", "IN", "IS", "LAMBDA", "NONE", "NONLOCAL", "NOT", 
            "OR", "PASS", "RAISE", "RETURN", "TRUE", "TRY", "WHILE", "WITH", 
            "YIELD", "NEWLINE", "NAME", "STRING_LITERAL", "BYTES_LITERAL", 
            "DECIMAL_INTEGER", "OCT_INTEGER", "HEX_INTEGER", "BIN_INTEGER", 
            "FLOAT_NUMBER", "IMAG_NUMBER", "ADD", "ADD_ASSIGN", "AND_ASSIGN", 
            "AND_OP", "ARROW", "ASSIGN", "AT", "AT_ASSIGN", "CLOSE_BRACE", 
            "CLOSE_BRACK", "CLOSE_PAREN", "COLON", "COMMA", "DIV", "DIV_ASSIGN", 
            "DOT", "ELLIPSIS", "EQUALS", "GREATER_THAN", "GT_EQ", "IDIV", 
            "IDIV_ASSIGN", "LEFT_SHIFT", "LEFT_SHIFT_ASSIGN", "LESS_THAN", 
            "LT_EQ", "MINUS", "MOD", "MOD_ASSIGN", "MULT_ASSIGN", "NOT_EQ_1", 
            "NOT_EQ_2", "NOT_OP", "OPEN_BRACE", "OPEN_BRACK", "OPEN_PAREN", 
            "OR_ASSIGN", "OR_OP", "POWER", "POWER_ASSIGN", "RIGHT_SHIFT", 
            "RIGHT_SHIFT_ASSIGN", "SEMI_COLON", "STAR", "SUB_ASSIGN", "XOR", 
            "XOR_ASSIGN", "SKIP_", "UNKNOWN_CHAR" ]

    ruleNames = [ "STRING", "NUMBER", "INTEGER", "AND", "AS", "ASSERT", 
                  "ASYNC", "AWAIT", "BREAK", "CLASS", "CONTINUE", "DEF", 
                  "DEL", "ELIF", "ELSE", "EXCEPT", "FALSE", "FINALLY", "FOR", 
                  "FROM", "GLOBAL", "IF", "IMPORT", "IN", "IS", "LAMBDA", 
                  "NONE", "NONLOCAL", "NOT", "OR", "PASS", "RAISE", "RETURN", 
                  "TRUE", "TRY", "WHILE", "WITH", "YIELD", "NEWLINE", "NAME", 
                  "STRING_LITERAL", "BYTES_LITERAL", "DECIMAL_INTEGER", 
                  "OCT_INTEGER", "HEX_INTEGER", "BIN_INTEGER", "FLOAT_NUMBER", 
                  "IMAG_NUMBER", "ADD", "ADD_ASSIGN", "AND_ASSIGN", "AND_OP", 
                  "ARROW", "ASSIGN", "AT", "AT_ASSIGN", "CLOSE_BRACE", "CLOSE_BRACK", 
                  "CLOSE_PAREN", "COLON", "COMMA", "DIV", "DIV_ASSIGN", 
                  "DOT", "ELLIPSIS", "EQUALS", "GREATER_THAN", "GT_EQ", 
                  "IDIV", "IDIV_ASSIGN", "LEFT_SHIFT", "LEFT_SHIFT_ASSIGN", 
                  "LESS_THAN", "LT_EQ", "MINUS", "MOD", "MOD_ASSIGN", "MULT_ASSIGN", 
                  "NOT_EQ_1", "NOT_EQ_2", "NOT_OP", "OPEN_BRACE", "OPEN_BRACK", 
                  "OPEN_PAREN", "OR_ASSIGN", "OR_OP", "POWER", "POWER_ASSIGN", 
                  "RIGHT_SHIFT", "RIGHT_SHIFT_ASSIGN", "SEMI_COLON", "STAR", 
                  "SUB_ASSIGN", "XOR", "XOR_ASSIGN", "SKIP_", "UNKNOWN_CHAR", 
                  "SHORT_STRING", "LONG_STRING", "LONG_STRING_ITEM", "LONG_STRING_CHAR", 
                  "STRING_ESCAPE_SEQ", "NON_ZERO_DIGIT", "DIGIT", "OCT_DIGIT", 
                  "HEX_DIGIT", "BIN_DIGIT", "POINT_FLOAT", "EXPONENT_FLOAT", 
                  "INT_PART", "FRACTION", "EXPONENT", "SHORT_BYTES", "LONG_BYTES", 
                  "LONG_BYTES_ITEM", "SHORT_BYTES_CHAR_NO_SINGLE_QUOTE", 
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
            actions[56] = self.CLOSE_BRACE_action 
            actions[57] = self.CLOSE_BRACK_action 
            actions[58] = self.CLOSE_PAREN_action 
            actions[81] = self.OPEN_BRACE_action 
            actions[82] = self.OPEN_BRACK_action 
            actions[83] = self.OPEN_PAREN_action 
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

            # Strip newlines inside open clauses except if we are near EOF. We keep NEWLINEs near EOF to satisfy the final newline
            # needed by the single_put rule used by the REPL.
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
                
     

    def CLOSE_BRACE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 1:
            self.opened -= 1
     

    def CLOSE_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 2:
            self.opened -= 1
     

    def CLOSE_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 3:
            self.opened -= 1
     

    def OPEN_BRACE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 4:
            self.opened += 1
     

    def OPEN_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 5:
            self.opened += 1
     

    def OPEN_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 6:
            self.opened += 1
     

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
         

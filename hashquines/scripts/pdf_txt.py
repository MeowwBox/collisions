#!/usr/bin/env python3

# Sets the value of Mako's Txt+PDF hashquine

# Ange Albertini 2023

import hashlib
from argparse import ArgumentParser
import random

HEX_BASE = 16
MD5_LEN = 32
from collisions import *

HEADER_S = 124864
HEADER_MD5 = '7e1e2da0c4f144bb0d749b8eb7982cb3'
MD5_FULL = "66da5e07c0fd4c921679a65931ff8393"

# 480 fastcolls
block_indexes = [
    33, 37, 41, 45, 49, 53, 57, 61, 65, 69, 73, 77, 81, 85, 89, 93, 97, 101,
    105, 109, 113, 117, 121, 125, 129, 133, 137, 141, 145, 149, 153, 157, 161,
    165, 169, 173, 177, 181, 185, 189, 193, 197, 201, 205, 209, 213, 217, 221,
    225, 229, 233, 237, 241, 245, 249, 253, 257, 261, 265, 269, 273, 277, 281,
    285, 289, 293, 297, 301, 305, 309, 313, 317, 321, 325, 329, 333, 337, 341,
    345, 349, 353, 357, 361, 365, 369, 373, 377, 381, 385, 389, 393, 397, 401,
    405, 409, 413, 417, 421, 425, 429, 433, 437, 441, 445, 449, 453, 457, 461,
    465, 469, 473, 477, 481, 485, 489, 493, 497, 501, 505, 509, 513, 517, 521,
    525, 529, 533, 537, 541, 545, 549, 553, 557, 561, 565, 569, 573, 577, 581,
    585, 589, 593, 597, 601, 605, 609, 613, 617, 621, 625, 629, 633, 637, 641,
    645, 649, 653, 657, 661, 665, 669, 673, 677, 681, 685, 689, 693, 697, 701,
    705, 709, 713, 717, 721, 725, 729, 733, 737, 741, 745, 749, 753, 757, 761,
    765, 769, 773, 777, 781, 785, 789, 793, 797, 801, 805, 809, 813, 817, 821,
    825, 829, 833, 837, 841, 845, 849, 853, 857, 861, 865, 869, 873, 877, 881,
    885, 889, 893, 897, 901, 905, 909, 913, 917, 921, 925, 929, 933, 937, 941,
    945, 949, 953, 957, 961, 965, 969, 973, 977, 981, 985, 989, 993, 997, 1001,
    1005, 1009, 1013, 1017, 1021, 1025, 1029, 1033, 1037, 1041, 1045, 1049,
    1053, 1057, 1061, 1065, 1069, 1073, 1077, 1081, 1085, 1089, 1093, 1097,
    1101, 1105, 1109, 1113, 1117, 1121, 1125, 1129, 1133, 1137, 1141, 1145,
    1149, 1153, 1157, 1161, 1165, 1169, 1173, 1177, 1181, 1185, 1189, 1193,
    1197, 1201, 1205, 1209, 1213, 1217, 1221, 1225, 1229, 1233, 1237, 1241,
    1245, 1249, 1253, 1257, 1261, 1265, 1269, 1273, 1277, 1281, 1285, 1289,
    1293, 1297, 1301, 1305, 1309, 1313, 1317, 1321, 1325, 1329, 1333, 1337,
    1341, 1345, 1349, 1353, 1357, 1361, 1365, 1369, 1373, 1377, 1381, 1385,
    1389, 1393, 1397, 1401, 1405, 1409, 1413, 1417, 1421, 1425, 1429, 1433,
    1437, 1441, 1445, 1449, 1453, 1457, 1461, 1465, 1469, 1473, 1477, 1481,
    1485, 1489, 1493, 1497, 1501, 1505, 1509, 1513, 1517, 1521, 1525, 1529,
    1533, 1537, 1541, 1545, 1549, 1553, 1557, 1561, 1565, 1569, 1573, 1577,
    1581, 1585, 1589, 1593, 1597, 1601, 1605, 1609, 1613, 1617, 1621, 1625,
    1629, 1633, 1637, 1641, 1645, 1649, 1653, 1657, 1661, 1665, 1669, 1673,
    1677, 1681, 1685, 1689, 1693, 1697, 1701, 1705, 1709, 1713, 1717, 1721,
    1725, 1729, 1733, 1737, 1741, 1745, 1749, 1753, 1757, 1761, 1765, 1769,
    1773, 1777, 1781, 1785, 1789, 1793, 1797, 1801, 1805, 1809, 1813, 1817,
    1821, 1825, 1829, 1833, 1837, 1841, 1845, 1849, 1853, 1857, 1861, 1865,
    1869, 1873, 1877, 1881, 1885, 1889, 1893, 1897, 1901, 1905, 1909, 1913,
    1917, 1921, 1925, 1929, 1933, 1937, 1941, 1945, 1949
]


def pdftext(data):
    import fitz
    fitz.TOOLS.mupdf_display_errors(False)
    doc = fitz.open(None, data, "pdf")
    return doc[0].get_text().splitlines()[0]


# odd digit mapping...
mapping = {
    "f": "000000000000000",
    "7": "000000000000001",
    "b": "000000000000010",
    "d": "000000000000100",
    "e": "000000000001000",
    "c": "000000000010100",
    "9": "000000000100010",
    "a": "000000001000010",
    "8": "000000010100010",
    "3": "000000100000001",
    "5": "000001000000001",
    "6": "000010000000001",
    "4": "000101000000001",
    "1": "001000100000001",
    "2": "010000100000001",
    "0": "111111111110111",
}


def main():
    parser = ArgumentParser(description="Sets value in the TEXT+PDF hashquine")
    parser.add_argument('-v',
                        '--value',
                        type=str,
                        nargs='?',
                        const=random,
                        help='Hex value to encode (random if not specified)')

    parser.add_argument("filename")
    args = parser.parse_args()

    fn = args.filename
    with open(fn, "rb") as f:
        data = bytearray(f.read())
    old_md5 = hashlib.md5(data).digest()

    # check we have the right file
    assert hashlib.md5(data[:HEADER_S]).hexdigest() == HEADER_MD5
    assert hashlib.md5(data).hexdigest() == MD5_FULL

    print('Correct TXT/PDF hashquine file found')

    if args.value is not None:
        if args.value == random:
            hex_value = "".join(
                [random.choice("0123456789abcdef") for _ in range(MD5_LEN)])
            print("Encoding random value: %s" % hex_value)
        else:
            hex_value = "%032x" % int(args.value, HEX_BASE)
            hex_value = hex_value[:MD5_LEN]
            print("Encoding requested value: `%s` (len:%i)" %
                  (hex_value, len(hex_value)))
    else:
        hex_value = hashlib.md5(data).hexdigest()
        print("Encoding file MD5: `%s` (len:%i)" % (hex_value, len(hex_value)))

    for letter_index, letter in enumerate(hex_value):
        bits = mapping[letter]
        for bit_idx, bit in enumerate(bits):
            data, _ = setFastcoll(data,
                                  block_indexes[bit_idx + letter_index * 15],
                                  sideB=bit == "1")
    # assert pdftext(data) == hex_value.upper()
    assert old_md5 == hashlib.md5(data).digest()
    with open("text.pdf", "wb") as f:
        f.write(data)


if __name__ == '__main__':
    main()

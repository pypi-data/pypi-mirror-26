# This file is part of 'NTLM Authorization Proxy Server' http://sourceforge.net/projects/ntlmaps/
# Copyright 2001 Dmitry A. Rozmanov <dima@xenon.spb.ru>
#
# This library is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library.  If not, see <http://www.gnu.org/licenses/> or <http://www.gnu.org/licenses/lgpl.txt>.

from ntlm_auth.U32 import U32

# static unsigned long des_SPtrans[8][64]={

des_SPtrans = \
    [
        # nibble 0
        [
            U32(0x00820200), U32(0x00020000), U32(0x80800000), U32(0x80820200),
            U32(0x00800000), U32(0x80020200), U32(0x80020000), U32(0x80800000),
            U32(0x80020200), U32(0x00820200), U32(0x00820000), U32(0x80000200),
            U32(0x80800200), U32(0x00800000), U32(0x00000000), U32(0x80020000),
            U32(0x00020000), U32(0x80000000), U32(0x00800200), U32(0x00020200),
            U32(0x80820200), U32(0x00820000), U32(0x80000200), U32(0x00800200),
            U32(0x80000000), U32(0x00000200), U32(0x00020200), U32(0x80820000),
            U32(0x00000200), U32(0x80800200), U32(0x80820000), U32(0x00000000),
            U32(0x00000000), U32(0x80820200), U32(0x00800200), U32(0x80020000),
            U32(0x00820200), U32(0x00020000), U32(0x80000200), U32(0x00800200),
            U32(0x80820000), U32(0x00000200), U32(0x00020200), U32(0x80800000),
            U32(0x80020200), U32(0x80000000), U32(0x80800000), U32(0x00820000),
            U32(0x80820200), U32(0x00020200), U32(0x00820000), U32(0x80800200),
            U32(0x00800000), U32(0x80000200), U32(0x80020000), U32(0x00000000),
            U32(0x00020000), U32(0x00800000), U32(0x80800200), U32(0x00820200),
            U32(0x80000000), U32(0x80820000), U32(0x00000200), U32(0x80020200),
        ],

        # nibble 1
        [
            U32(0x10042004), U32(0x00000000), U32(0x00042000), U32(0x10040000),
            U32(0x10000004), U32(0x00002004), U32(0x10002000), U32(0x00042000),
            U32(0x00002000), U32(0x10040004), U32(0x00000004), U32(0x10002000),
            U32(0x00040004), U32(0x10042000), U32(0x10040000), U32(0x00000004),
            U32(0x00040000), U32(0x10002004), U32(0x10040004), U32(0x00002000),
            U32(0x00042004), U32(0x10000000), U32(0x00000000), U32(0x00040004),
            U32(0x10002004), U32(0x00042004), U32(0x10042000), U32(0x10000004),
            U32(0x10000000), U32(0x00040000), U32(0x00002004), U32(0x10042004),
            U32(0x00040004), U32(0x10042000), U32(0x10002000), U32(0x00042004),
            U32(0x10042004), U32(0x00040004), U32(0x10000004), U32(0x00000000),
            U32(0x10000000), U32(0x00002004), U32(0x00040000), U32(0x10040004),
            U32(0x00002000), U32(0x10000000), U32(0x00042004), U32(0x10002004),
            U32(0x10042000), U32(0x00002000), U32(0x00000000), U32(0x10000004),
            U32(0x00000004), U32(0x10042004), U32(0x00042000), U32(0x10040000),
            U32(0x10040004), U32(0x00040000), U32(0x00002004), U32(0x10002000),
            U32(0x10002004), U32(0x00000004), U32(0x10040000), U32(0x00042000),
        ],

        # nibble 2
        [
            U32(0x41000000), U32(0x01010040), U32(0x00000040), U32(0x41000040),
            U32(0x40010000), U32(0x01000000), U32(0x41000040), U32(0x00010040),
            U32(0x01000040), U32(0x00010000), U32(0x01010000), U32(0x40000000),
            U32(0x41010040), U32(0x40000040), U32(0x40000000), U32(0x41010000),
            U32(0x00000000), U32(0x40010000), U32(0x01010040), U32(0x00000040),
            U32(0x40000040), U32(0x41010040), U32(0x00010000), U32(0x41000000),
            U32(0x41010000), U32(0x01000040), U32(0x40010040), U32(0x01010000),
            U32(0x00010040), U32(0x00000000), U32(0x01000000), U32(0x40010040),
            U32(0x01010040), U32(0x00000040), U32(0x40000000), U32(0x00010000),
            U32(0x40000040), U32(0x40010000), U32(0x01010000), U32(0x41000040),
            U32(0x00000000), U32(0x01010040), U32(0x00010040), U32(0x41010000),
            U32(0x40010000), U32(0x01000000), U32(0x41010040), U32(0x40000000),
            U32(0x40010040), U32(0x41000000), U32(0x01000000), U32(0x41010040),
            U32(0x00010000), U32(0x01000040), U32(0x41000040), U32(0x00010040),
            U32(0x01000040), U32(0x00000000), U32(0x41010000), U32(0x40000040),
            U32(0x41000000), U32(0x40010040), U32(0x00000040), U32(0x01010000),
        ],

        # nibble 3
        [
            U32(0x00100402), U32(0x04000400), U32(0x00000002), U32(0x04100402),
            U32(0x00000000), U32(0x04100000), U32(0x04000402), U32(0x00100002),
            U32(0x04100400), U32(0x04000002), U32(0x04000000), U32(0x00000402),
            U32(0x04000002), U32(0x00100402), U32(0x00100000), U32(0x04000000),
            U32(0x04100002), U32(0x00100400), U32(0x00000400), U32(0x00000002),
            U32(0x00100400), U32(0x04000402), U32(0x04100000), U32(0x00000400),
            U32(0x00000402), U32(0x00000000), U32(0x00100002), U32(0x04100400),
            U32(0x04000400), U32(0x04100002), U32(0x04100402), U32(0x00100000),
            U32(0x04100002), U32(0x00000402), U32(0x00100000), U32(0x04000002),
            U32(0x00100400), U32(0x04000400), U32(0x00000002), U32(0x04100000),
            U32(0x04000402), U32(0x00000000), U32(0x00000400), U32(0x00100002),
            U32(0x00000000), U32(0x04100002), U32(0x04100400), U32(0x00000400),
            U32(0x04000000), U32(0x04100402), U32(0x00100402), U32(0x00100000),
            U32(0x04100402), U32(0x00000002), U32(0x04000400), U32(0x00100402),
            U32(0x00100002), U32(0x00100400), U32(0x04100000), U32(0x04000402),
            U32(0x00000402), U32(0x04000000), U32(0x04000002), U32(0x04100400),
        ],

        # nibble 4
        [
            U32(0x02000000), U32(0x00004000), U32(0x00000100), U32(0x02004108),
            U32(0x02004008), U32(0x02000100), U32(0x00004108), U32(0x02004000),
            U32(0x00004000), U32(0x00000008), U32(0x02000008), U32(0x00004100),
            U32(0x02000108), U32(0x02004008), U32(0x02004100), U32(0x00000000),
            U32(0x00004100), U32(0x02000000), U32(0x00004008), U32(0x00000108),
            U32(0x02000100), U32(0x00004108), U32(0x00000000), U32(0x02000008),
            U32(0x00000008), U32(0x02000108), U32(0x02004108), U32(0x00004008),
            U32(0x02004000), U32(0x00000100), U32(0x00000108), U32(0x02004100),
            U32(0x02004100), U32(0x02000108), U32(0x00004008), U32(0x02004000),
            U32(0x00004000), U32(0x00000008), U32(0x02000008), U32(0x02000100),
            U32(0x02000000), U32(0x00004100), U32(0x02004108), U32(0x00000000),
            U32(0x00004108), U32(0x02000000), U32(0x00000100), U32(0x00004008),
            U32(0x02000108), U32(0x00000100), U32(0x00000000), U32(0x02004108),
            U32(0x02004008), U32(0x02004100), U32(0x00000108), U32(0x00004000),
            U32(0x00004100), U32(0x02004008), U32(0x02000100), U32(0x00000108),
            U32(0x00000008), U32(0x00004108), U32(0x02004000), U32(0x02000008),
        ],

        # nibble 5
        [
            U32(0x20000010), U32(0x00080010), U32(0x00000000), U32(0x20080800),
            U32(0x00080010), U32(0x00000800), U32(0x20000810), U32(0x00080000),
            U32(0x00000810), U32(0x20080810), U32(0x00080800), U32(0x20000000),
            U32(0x20000800), U32(0x20000010), U32(0x20080000), U32(0x00080810),
            U32(0x00080000), U32(0x20000810), U32(0x20080010), U32(0x00000000),
            U32(0x00000800), U32(0x00000010), U32(0x20080800), U32(0x20080010),
            U32(0x20080810), U32(0x20080000), U32(0x20000000), U32(0x00000810),
            U32(0x00000010), U32(0x00080800), U32(0x00080810), U32(0x20000800),
            U32(0x00000810), U32(0x20000000), U32(0x20000800), U32(0x00080810),
            U32(0x20080800), U32(0x00080010), U32(0x00000000), U32(0x20000800),
            U32(0x20000000), U32(0x00000800), U32(0x20080010), U32(0x00080000),
            U32(0x00080010), U32(0x20080810), U32(0x00080800), U32(0x00000010),
            U32(0x20080810), U32(0x00080800), U32(0x00080000), U32(0x20000810),
            U32(0x20000010), U32(0x20080000), U32(0x00080810), U32(0x00000000),
            U32(0x00000800), U32(0x20000010), U32(0x20000810), U32(0x20080800),
            U32(0x20080000), U32(0x00000810), U32(0x00000010), U32(0x20080010),
        ],

        # nibble 6
        [
            U32(0x00001000), U32(0x00000080), U32(0x00400080), U32(0x00400001),
            U32(0x00401081), U32(0x00001001), U32(0x00001080), U32(0x00000000),
            U32(0x00400000), U32(0x00400081), U32(0x00000081), U32(0x00401000),
            U32(0x00000001), U32(0x00401080), U32(0x00401000), U32(0x00000081),
            U32(0x00400081), U32(0x00001000), U32(0x00001001), U32(0x00401081),
            U32(0x00000000), U32(0x00400080), U32(0x00400001), U32(0x00001080),
            U32(0x00401001), U32(0x00001081), U32(0x00401080), U32(0x00000001),
            U32(0x00001081), U32(0x00401001), U32(0x00000080), U32(0x00400000),
            U32(0x00001081), U32(0x00401000), U32(0x00401001), U32(0x00000081),
            U32(0x00001000), U32(0x00000080), U32(0x00400000), U32(0x00401001),
            U32(0x00400081), U32(0x00001081), U32(0x00001080), U32(0x00000000),
            U32(0x00000080), U32(0x00400001), U32(0x00000001), U32(0x00400080),
            U32(0x00000000), U32(0x00400081), U32(0x00400080), U32(0x00001080),
            U32(0x00000081), U32(0x00001000), U32(0x00401081), U32(0x00400000),
            U32(0x00401080), U32(0x00000001), U32(0x00001001), U32(0x00401081),
            U32(0x00400001), U32(0x00401080), U32(0x00401000), U32(0x00001001),
        ],

        # nibble 7
        [
            U32(0x08200020), U32(0x08208000), U32(0x00008020), U32(0x00000000),
            U32(0x08008000), U32(0x00200020), U32(0x08200000), U32(0x08208020),
            U32(0x00000020), U32(0x08000000), U32(0x00208000), U32(0x00008020),
            U32(0x00208020), U32(0x08008020), U32(0x08000020), U32(0x08200000),
            U32(0x00008000), U32(0x00208020), U32(0x00200020), U32(0x08008000),
            U32(0x08208020), U32(0x08000020), U32(0x00000000), U32(0x00208000),
            U32(0x08000000), U32(0x00200000), U32(0x08008020), U32(0x08200020),
            U32(0x00200000), U32(0x00008000), U32(0x08208000), U32(0x00000020),
            U32(0x00200000), U32(0x00008000), U32(0x08000020), U32(0x08208020),
            U32(0x00008020), U32(0x08000000), U32(0x00000000), U32(0x00208000),
            U32(0x08200020), U32(0x08008020), U32(0x08008000), U32(0x00200020),
            U32(0x08208000), U32(0x00000020), U32(0x00200020), U32(0x08008000),
            U32(0x08208020), U32(0x00200000), U32(0x08200000), U32(0x08000020),
            U32(0x00208000), U32(0x00008020), U32(0x08008020), U32(0x08200000),
            U32(0x00000020), U32(0x08208000), U32(0x00208020), U32(0x00000000),
            U32(0x08000000), U32(0x08200020), U32(0x00008000), U32(0x00208020),
        ],
    ]

# static unsigned long des_skb[8][64]={

des_skb = \
    [
        # for C bits (numbered as per FIPS 46) 1 2 3 4 5 6
        [
            U32(0x00000000), U32(0x00000010), U32(0x20000000), U32(0x20000010),
            U32(0x00010000), U32(0x00010010), U32(0x20010000), U32(0x20010010),
            U32(0x00000800), U32(0x00000810), U32(0x20000800), U32(0x20000810),
            U32(0x00010800), U32(0x00010810), U32(0x20010800), U32(0x20010810),
            U32(0x00000020), U32(0x00000030), U32(0x20000020), U32(0x20000030),
            U32(0x00010020), U32(0x00010030), U32(0x20010020), U32(0x20010030),
            U32(0x00000820), U32(0x00000830), U32(0x20000820), U32(0x20000830),
            U32(0x00010820), U32(0x00010830), U32(0x20010820), U32(0x20010830),
            U32(0x00080000), U32(0x00080010), U32(0x20080000), U32(0x20080010),
            U32(0x00090000), U32(0x00090010), U32(0x20090000), U32(0x20090010),
            U32(0x00080800), U32(0x00080810), U32(0x20080800), U32(0x20080810),
            U32(0x00090800), U32(0x00090810), U32(0x20090800), U32(0x20090810),
            U32(0x00080020), U32(0x00080030), U32(0x20080020), U32(0x20080030),
            U32(0x00090020), U32(0x00090030), U32(0x20090020), U32(0x20090030),
            U32(0x00080820), U32(0x00080830), U32(0x20080820), U32(0x20080830),
            U32(0x00090820), U32(0x00090830), U32(0x20090820), U32(0x20090830),
        ],

        # for C bits (numbered as per FIPS 46) 7 8 10 11 12 13
        [
            U32(0x00000000), U32(0x02000000), U32(0x00002000), U32(0x02002000),
            U32(0x00200000), U32(0x02200000), U32(0x00202000), U32(0x02202000),
            U32(0x00000004), U32(0x02000004), U32(0x00002004), U32(0x02002004),
            U32(0x00200004), U32(0x02200004), U32(0x00202004), U32(0x02202004),
            U32(0x00000400), U32(0x02000400), U32(0x00002400), U32(0x02002400),
            U32(0x00200400), U32(0x02200400), U32(0x00202400), U32(0x02202400),
            U32(0x00000404), U32(0x02000404), U32(0x00002404), U32(0x02002404),
            U32(0x00200404), U32(0x02200404), U32(0x00202404), U32(0x02202404),
            U32(0x10000000), U32(0x12000000), U32(0x10002000), U32(0x12002000),
            U32(0x10200000), U32(0x12200000), U32(0x10202000), U32(0x12202000),
            U32(0x10000004), U32(0x12000004), U32(0x10002004), U32(0x12002004),
            U32(0x10200004), U32(0x12200004), U32(0x10202004), U32(0x12202004),
            U32(0x10000400), U32(0x12000400), U32(0x10002400), U32(0x12002400),
            U32(0x10200400), U32(0x12200400), U32(0x10202400), U32(0x12202400),
            U32(0x10000404), U32(0x12000404), U32(0x10002404), U32(0x12002404),
            U32(0x10200404), U32(0x12200404), U32(0x10202404), U32(0x12202404),
        ],

        # for C bits (numbered as per FIPS 46) 14 15 16 17 19 20
        [
            U32(0x00000000), U32(0x00000001), U32(0x00040000), U32(0x00040001),
            U32(0x01000000), U32(0x01000001), U32(0x01040000), U32(0x01040001),
            U32(0x00000002), U32(0x00000003), U32(0x00040002), U32(0x00040003),
            U32(0x01000002), U32(0x01000003), U32(0x01040002), U32(0x01040003),
            U32(0x00000200), U32(0x00000201), U32(0x00040200), U32(0x00040201),
            U32(0x01000200), U32(0x01000201), U32(0x01040200), U32(0x01040201),
            U32(0x00000202), U32(0x00000203), U32(0x00040202), U32(0x00040203),
            U32(0x01000202), U32(0x01000203), U32(0x01040202), U32(0x01040203),
            U32(0x08000000), U32(0x08000001), U32(0x08040000), U32(0x08040001),
            U32(0x09000000), U32(0x09000001), U32(0x09040000), U32(0x09040001),
            U32(0x08000002), U32(0x08000003), U32(0x08040002), U32(0x08040003),
            U32(0x09000002), U32(0x09000003), U32(0x09040002), U32(0x09040003),
            U32(0x08000200), U32(0x08000201), U32(0x08040200), U32(0x08040201),
            U32(0x09000200), U32(0x09000201), U32(0x09040200), U32(0x09040201),
            U32(0x08000202), U32(0x08000203), U32(0x08040202), U32(0x08040203),
            U32(0x09000202), U32(0x09000203), U32(0x09040202), U32(0x09040203),
        ],

        # for C bits (numbered as per FIPS 46) 21 23 24 26 27 28
        [
            U32(0x00000000), U32(0x00100000), U32(0x00000100), U32(0x00100100),
            U32(0x00000008), U32(0x00100008), U32(0x00000108), U32(0x00100108),
            U32(0x00001000), U32(0x00101000), U32(0x00001100), U32(0x00101100),
            U32(0x00001008), U32(0x00101008), U32(0x00001108), U32(0x00101108),
            U32(0x04000000), U32(0x04100000), U32(0x04000100), U32(0x04100100),
            U32(0x04000008), U32(0x04100008), U32(0x04000108), U32(0x04100108),
            U32(0x04001000), U32(0x04101000), U32(0x04001100), U32(0x04101100),
            U32(0x04001008), U32(0x04101008), U32(0x04001108), U32(0x04101108),
            U32(0x00020000), U32(0x00120000), U32(0x00020100), U32(0x00120100),
            U32(0x00020008), U32(0x00120008), U32(0x00020108), U32(0x00120108),
            U32(0x00021000), U32(0x00121000), U32(0x00021100), U32(0x00121100),
            U32(0x00021008), U32(0x00121008), U32(0x00021108), U32(0x00121108),
            U32(0x04020000), U32(0x04120000), U32(0x04020100), U32(0x04120100),
            U32(0x04020008), U32(0x04120008), U32(0x04020108), U32(0x04120108),
            U32(0x04021000), U32(0x04121000), U32(0x04021100), U32(0x04121100),
            U32(0x04021008), U32(0x04121008), U32(0x04021108), U32(0x04121108),
        ],

        # for D bits (numbered as per FIPS 46) 1 2 3 4 5 6
        [
            U32(0x00000000), U32(0x10000000), U32(0x00010000), U32(0x10010000),
            U32(0x00000004), U32(0x10000004), U32(0x00010004), U32(0x10010004),
            U32(0x20000000), U32(0x30000000), U32(0x20010000), U32(0x30010000),
            U32(0x20000004), U32(0x30000004), U32(0x20010004), U32(0x30010004),
            U32(0x00100000), U32(0x10100000), U32(0x00110000), U32(0x10110000),
            U32(0x00100004), U32(0x10100004), U32(0x00110004), U32(0x10110004),
            U32(0x20100000), U32(0x30100000), U32(0x20110000), U32(0x30110000),
            U32(0x20100004), U32(0x30100004), U32(0x20110004), U32(0x30110004),
            U32(0x00001000), U32(0x10001000), U32(0x00011000), U32(0x10011000),
            U32(0x00001004), U32(0x10001004), U32(0x00011004), U32(0x10011004),
            U32(0x20001000), U32(0x30001000), U32(0x20011000), U32(0x30011000),
            U32(0x20001004), U32(0x30001004), U32(0x20011004), U32(0x30011004),
            U32(0x00101000), U32(0x10101000), U32(0x00111000), U32(0x10111000),
            U32(0x00101004), U32(0x10101004), U32(0x00111004), U32(0x10111004),
            U32(0x20101000), U32(0x30101000), U32(0x20111000), U32(0x30111000),
            U32(0x20101004), U32(0x30101004), U32(0x20111004), U32(0x30111004),
        ],

        # for D bits (numbered as per FIPS 46) 8 9 11 12 13 14
        [
            U32(0x00000000), U32(0x08000000), U32(0x00000008), U32(0x08000008),
            U32(0x00000400), U32(0x08000400), U32(0x00000408), U32(0x08000408),
            U32(0x00020000), U32(0x08020000), U32(0x00020008), U32(0x08020008),
            U32(0x00020400), U32(0x08020400), U32(0x00020408), U32(0x08020408),
            U32(0x00000001), U32(0x08000001), U32(0x00000009), U32(0x08000009),
            U32(0x00000401), U32(0x08000401), U32(0x00000409), U32(0x08000409),
            U32(0x00020001), U32(0x08020001), U32(0x00020009), U32(0x08020009),
            U32(0x00020401), U32(0x08020401), U32(0x00020409), U32(0x08020409),
            U32(0x02000000), U32(0x0A000000), U32(0x02000008), U32(0x0A000008),
            U32(0x02000400), U32(0x0A000400), U32(0x02000408), U32(0x0A000408),
            U32(0x02020000), U32(0x0A020000), U32(0x02020008), U32(0x0A020008),
            U32(0x02020400), U32(0x0A020400), U32(0x02020408), U32(0x0A020408),
            U32(0x02000001), U32(0x0A000001), U32(0x02000009), U32(0x0A000009),
            U32(0x02000401), U32(0x0A000401), U32(0x02000409), U32(0x0A000409),
            U32(0x02020001), U32(0x0A020001), U32(0x02020009), U32(0x0A020009),
            U32(0x02020401), U32(0x0A020401), U32(0x02020409), U32(0x0A020409),
        ],

        # for D bits (numbered as per FIPS 46) 16 17 18 19 20 21
        [
            U32(0x00000000), U32(0x00000100), U32(0x00080000), U32(0x00080100),
            U32(0x01000000), U32(0x01000100), U32(0x01080000), U32(0x01080100),
            U32(0x00000010), U32(0x00000110), U32(0x00080010), U32(0x00080110),
            U32(0x01000010), U32(0x01000110), U32(0x01080010), U32(0x01080110),
            U32(0x00200000), U32(0x00200100), U32(0x00280000), U32(0x00280100),
            U32(0x01200000), U32(0x01200100), U32(0x01280000), U32(0x01280100),
            U32(0x00200010), U32(0x00200110), U32(0x00280010), U32(0x00280110),
            U32(0x01200010), U32(0x01200110), U32(0x01280010), U32(0x01280110),
            U32(0x00000200), U32(0x00000300), U32(0x00080200), U32(0x00080300),
            U32(0x01000200), U32(0x01000300), U32(0x01080200), U32(0x01080300),
            U32(0x00000210), U32(0x00000310), U32(0x00080210), U32(0x00080310),
            U32(0x01000210), U32(0x01000310), U32(0x01080210), U32(0x01080310),
            U32(0x00200200), U32(0x00200300), U32(0x00280200), U32(0x00280300),
            U32(0x01200200), U32(0x01200300), U32(0x01280200), U32(0x01280300),
            U32(0x00200210), U32(0x00200310), U32(0x00280210), U32(0x00280310),
            U32(0x01200210), U32(0x01200310), U32(0x01280210), U32(0x01280310),
        ],

        # for D bits (numbered as per FIPS 46) 22 23 24 25 27 28
        [
            U32(0x00000000), U32(0x04000000), U32(0x00040000), U32(0x04040000),
            U32(0x00000002), U32(0x04000002), U32(0x00040002), U32(0x04040002),
            U32(0x00002000), U32(0x04002000), U32(0x00042000), U32(0x04042000),
            U32(0x00002002), U32(0x04002002), U32(0x00042002), U32(0x04042002),
            U32(0x00000020), U32(0x04000020), U32(0x00040020), U32(0x04040020),
            U32(0x00000022), U32(0x04000022), U32(0x00040022), U32(0x04040022),
            U32(0x00002020), U32(0x04002020), U32(0x00042020), U32(0x04042020),
            U32(0x00002022), U32(0x04002022), U32(0x00042022), U32(0x04042022),
            U32(0x00000800), U32(0x04000800), U32(0x00040800), U32(0x04040800),
            U32(0x00000802), U32(0x04000802), U32(0x00040802), U32(0x04040802),
            U32(0x00002800), U32(0x04002800), U32(0x00042800), U32(0x04042800),
            U32(0x00002802), U32(0x04002802), U32(0x00042802), U32(0x04042802),
            U32(0x00000820), U32(0x04000820), U32(0x00040820), U32(0x04040820),
            U32(0x00000822), U32(0x04000822), U32(0x00040822), U32(0x04040822),
            U32(0x00002820), U32(0x04002820), U32(0x00042820), U32(0x04042820),
            U32(0x00002822), U32(0x04002822), U32(0x00042822), U32(0x04042822),
        ]

    ]

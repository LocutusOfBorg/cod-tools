#------------------------------------------------------------------------
#$Author$
#$Date$ 
#$Revision$
#$URL$
#------------------------------------------------------------------------
#* 
# A list of the spacegroup names with the ITC numbers, long and short
# spelling.
#**

package SpacegroupNames;

use strict;

require Exporter;
@SpacegroupNames::ISA = qw(Exporter);
@SpacegroupNames::EXPORT = qw( @names );

@SpacegroupNames::names = (
[1,	"P1",	"P 1" ],
[2,	"P-1",	"P -1" ],
[2,	"P1-",	"P 1-" ],
[3,	"P2",	"P 1 2 1" ],
[4,	"P21",	"P 1 21 1" ],
[5,	"C2",	"C 1 2 1" ],
[6,	"Pm",	"P 1 m 1" ],
[7,	"Pc",	"P 1 c 1" ],
[8,	"Cm",	"C 1 m 1" ],
[9,	"Cc",	"C 1 c 1" ],
[10,	"P2/m",	"P 1 2/m 1" ],
[11,	"P21/m",	"P 1 21/m 1" ],
[12,	"C2/m",	"C 1 2/m 1" ],
[13,	"P2/c",	"P 1 2/c 1" ],
[13,	"P2/a",	"P 1 2/a 1" ],
[13,	"P2/n",	"P 1 2/n 1" ],
[14,	"P21/c",	"P 1 21/c 1" ],
[14,	"P21/a",	"P 1 21/a 1" ],
[14,	"P21/n",	"P 1 21/n 1" ],
[15,	"C2/c",	"C 1 2/c 1" ],
[16,	"P222",	"P 2 2 2" ],
[17,	"P2221",	"P 2 2 21" ],
[18,	"P21212",	"P 21 21 2" ],
[19,	"P212121",	"P 21 21 21" ],
[20,	"C2221",	"C 2 2 21" ],
[21,	"C222",	"C 2 2 2" ],
[22,	"F222",	"F 2 2 2" ],
[23,	"I222",	"I 2 2 2" ],
[24,	"I212121",	"I 21 21 21" ],
[25,	"Pmm2",	"P m m 2" ],
[26,	"Pmc21",	"P m c 21" ],
[27,	"Pcc2",	"P c c 2" ],
[28,	"Pma2",	"P m a 2" ],
[29,	"Pca21",	"P c a 21" ],
[30,	"Pnc2",	"P n c 2" ],
[31,	"Pmn21",	"P m n 21" ],
[32,	"Pba2",	"P b a 2" ],
[33,	"Pna21",	"P n a 21" ],
[34,	"Pnn2",	"P n n 2" ],
[35,	"Cmm2",	"C m m 2" ],
[36,	"Cmc21",	"C m c 21" ],
[37,	"Ccc2",	"C c c 2" ],
[38,	"Amm2",	"A m m 2" ],
[39,	"Abm2",	"A b m 2" ],
[40,	"Ama2",	"A m a 2" ],
[41,	"Aba2",	"A b a 2" ],
[42,	"Fmm2",	"F m m 2" ],
[43,	"Fdd2",	"F d d 2" ],
[44,	"Imm2",	"I m m 2" ],
[45,	"Iba2",	"I b a 2" ],
[46,	"Ima2",	"I m a 2" ],
[47,	"Pmmm",	"P 2/m 2/m 2/m" ],
[47,	"Pmmm",	"P m m m" ],
[48,	"Pnnn",	"P 2/n 2/n 2/n" ],
[48,	"Pnnn",	"P n n n" ],
[49,	"Pccm",	"P 2/c 2/c 2/m" ],
[49,	"Pccm",	"P c c m" ],
[50,	"Pban",	"P 2/b 2/a 2/n" ],
[50,	"Pban",	"P b a n" ],
[51,	"Pmma",	"P 21/m 2/m 2/a" ],
[51,	"Pmma",	"P m m a" ],
[52,	"Pnna",	"P 2/n 21/n 2/a" ],
[52,	"Pnna",	"P n n a" ],
[53,	"Pmna",	"P 2/m 2/n 21/a" ],
[53,	"Pmna",	"P m n a" ],
[54,	"Pcca",	"P 21/c 2/c 2/a" ],
[54,	"Pcca",	"P c c a" ],
[55,	"Pbam",	"P 21/b 21/a 2/m" ],
[55,	"Pbam",	"P b a m" ],
[56,	"Pccn",	"P 21/c 21/c 2/n" ],
[56,	"Pccn",	"P c c n" ],
[57,	"Pbcm",	"P 2/b 21/c 21/m" ],
[57,	"Pbcm",	"P b c m" ],
[58,	"Pnnm",	"P 21/n 21/n 2/m" ],
[58,	"Pnnm",	"P n n m" ],
[59,	"Pmmn",	"P 21/m 21/m 2/n" ],
[59,	"Pmmn",	"P m m n" ],
[60,	"Pbcn",	"P 21/b 2/c 21/n" ],
[60,	"Pbcn",	"P b c n" ],
[61,	"Pbca",	"P 21/b 21/c 21/a" ],
[61,	"Pbca",	"P b c a" ],
[62,	"Pnma",	"P 21/n 21/m 21/a" ],
[62,	"Pnma",	"P n m a" ],
[63,	"Cmcm",	"C 2/m 2/c 21/m" ],
[63,	"Cmcm",	"C m c m" ],
[64,	"Cmca",	"C 2/m 2/c 21/a" ],
[64,	"Cmca",	"C m c a" ],
[65,	"Cmmm",	"C 2/m 2/m 2/m" ],
[65,	"Cmmm",	"C m m m" ],
[66,	"Cccm",	"C 2/c 2/c 2/m" ],
[66,	"Cccm",	"C c c m" ],
[67,	"Cmma",	"C 2/m 2/m 2/a" ],
[67,	"Cmma",	"C m m a" ],
[68,	"Ccca",	"C 2/c 2/c 2/a" ],
[68,	"Ccca",	"C c c a" ],
[69,	"Fmmm",	"F 2/m 2/m 2/m" ],
[69,	"Fmmm",	"F m m m" ],
[70,	"Fddd",	"F 2/d 2/d 2/d" ],
[70,	"Fddd",	"F d d d" ],
[71,	"Immm",	"I 2/m 2/m 2/m" ],
[71,	"Immm",	"I m m m" ],
[72,	"Ibam",	"I 2/b 2/a 2/m" ],
[72,	"Ibam",	"I b a m" ],
[73,	"Ibca",	"I 21/b 21/c 21/a" ],
[73,	"Ibca",	"I b c a" ],
[74,	"Imma",	"I 21/m 21/m 21/a" ],
[74,	"Imma",	"I m m a" ],
[75,	"P4",	"P 4" ],
[76,	"P41",	"P 41" ],
[77,	"P42",	"P 42" ],
[78,	"P43",	"P 43" ],
[79,	"I4",	"I 4" ],
[80,	"I41",	"I 41" ],
[81,	"P-4",	"P -4" ],
[82,	"I-4",	"I -4" ],
[83,	"P4/m",	"P 4/m" ],
[84,	"P42/m",	"P 42/m" ],
[85,	"P4/n",	"P 4/n" ],
[86,	"P42/n",	"P 42/n" ],
[87,	"I4/m",	"I 4/m" ],
[88,	"I41/a",	"I 41/a" ],
[89,	"P422",	"P 4 2 2" ],
[90,	"P4212",	"P 4 21 2" ],
[91,	"P4122",	"P 41 2 2" ],
[92,	"P41212",	"P 41 21 2" ],
[93,	"P4222",	"P 42 2 2" ],
[94,	"P42212",	"P 42 21 2" ],
[95,	"P4322",	"P 43 2 2" ],
[96,	"P43212",	"P 43 21 2" ],
[97,	"I422",	"I 4 2 2" ],
[98,	"I4122",	"I 41 2 2" ],
[99,	"P4mm",	"P 4 m m" ],
[100,	"P4bm",	"P 4 b m" ],
[101,	"P42cm",	"P 42 c m" ],
[102,	"P42nm",	"P 42 n m" ],
[103,	"P4cc",	"P 4 c c" ],
[104,	"P4nc",	"P 4 n c" ],
[105,	"P42mc",	"P 42 m c" ],
[106,	"P42bc",	"P 42 b c" ],
[107,	"I4mm",	"I 4 m m" ],
[108,	"I4cm",	"I 4 c m" ],
[109,	"I41md",	"I 41 m d" ],
[110,	"I41cd",	"I 41 c d" ],
[111,	"P-42m",	"P -4 2 m" ],
[112,	"P-42c",	"P -4 2 c" ],
[113,	"P-421m",	"P -4 21 m" ],
[114,	"P-421c",	"P -4 21 c" ],
[115,	"P-4m2",	"P -4 m 2" ],
[116,	"P-4c2",	"P -4 c 2" ],
[117,	"P-4b2",	"P -4 b 2" ],
[118,	"P-4n2",	"P -4 n 2" ],
[119,	"I-4m2",	"I -4 m 2" ],
[120,	"I-4c2",	"I -4 c 2" ],
[121,	"I-42m",	"I -4 2 m" ],
[122,	"I-42d",	"I -4 2 d" ],
[123,	"P4/mmm",	"P 4/m 2/m 2/m" ],
[123,	"P4/mmm",	"P4/m m m" ],
[124,	"P4/mcc",	"P 4/m 2/c 2/c" ],
[124,	"P4/mcc",	"P4/m c c" ],
[125,	"P4/nbm",	"P 4/n 2/b 2/m" ],
[125,	"P4/nbm",	"P4/n b m" ],
[126,	"P4/nnc",	"P 4/n 2/n 2/c" ],
[126,	"P4/nnc",	"P4/n n c" ],
[127,	"P4/mbm",	"P 4/m 21/b 2/m" ],
[127,	"P4/mbm",	"P4/m b m" ],
[128,	"P4/mnc",	"P 4/m 21/n 2/c" ],
[128,	"P4/mnc",	"P4/m n c" ],
[129,	"P4/nmm",	"P 4/n 21/m 2/m" ],
[129,	"P4/nmm",	"P4/n m m" ],
[130,	"P4/ncc",	"P 4/n 2/c 2/c" ],
[130,	"P4/ncc",	"P4/n c c" ],
[131,	"P42/mmc",	"P 42/m 2/m 2/c" ],
[131,	"P42/mmc",	"P42/m m c" ],
[132,	"P42/mcm",	"P 42/m 2/c 2/m" ],
[132,	"P42/mcm",	"P42/m c m" ],
[133,	"P42/nbc",	"P 42/n 2/b 2/c" ],
[133,	"P42/nbc",	"P42/n b c" ],
[134,	"P42/nnm",	"P 42/n 2/n 2/m" ],
[134,	"P42/nnm",	"P42/n n m" ],
[135,	"P42/mbc",	"P 42/m 21/b 2/c" ],
[135,	"P42/mbc",	"P42/m b c" ],
[136,	"P42/mnm",	"P 42/m 21/n 2/m" ],
[136,	"P42/mnm",	"P42/m n m" ],
[137,	"P42/nmc",	"P 42/n 21/m 2/c" ],
[137,	"P42/nmc",	"P42/n m c" ],
[138,	"P42/ncm",	"P 42/n 21/c 2/m" ],
[138,	"P42/ncm",	"P42/n c m" ],
[139,	"I4/mmm",	"I 4/m 2/m 2/m" ],
[139,	"I4/mmm",	"I4/m m m" ],
[140,	"I4/mcm",	"I 4/m 2/c 2/m" ],
[140,	"I4/mcm",	"I4/m c m" ],
[141,	"I41/amd",	"I 41/a 2/m 2/d" ],
[141,	"I41/amd",	"I41/a m d" ],
[142,	"I41/acd",	"I 41/a 2/c 2/d" ],
[142,	"I41/acd",	"I41/a c d" ],
[143,	"P3",	"P 3" ],
[144,	"P31",	"P 31" ],
[145,	"P32",	"P 32" ],
[146,	"H3",	"H 3" ],
[1146,	"R3",	"R 3" ],
[147,	"P-3",	"P -3" ],
[148,	"H-3",	"H -3" ],
[1148,	"R-3",	"R -3" ],
[149,	"P312",	"P 3 1 2" ],
[150,	"P321",	"P 3 2 1" ],
[151,	"P3112",	"P 31 1 2" ],
[152,	"P3121",	"P 31 2 1" ],
[153,	"P3212",	"P 32 1 2" ],
[154,	"P3221",	"P 32 2 1" ],
[155,	"H32",	"H 3 2" ],
[1155,	"R32",	"R 3 2" ],
[156,	"P3m1",	"P 3 m 1" ],
[157,	"P31m",	"P 3 1 m" ],
[158,	"P3c1",	"P 3 c 1" ],
[159,	"P31c",	"P 3 1 c" ],
[160,	"H3m",	"H 3 m" ],
[1160,	"R3m",	"R 3 m" ],
[161,	"H3c",	"H 3 c" ],
[1161,	"R3c",	"R 3 c" ],
[162,	"P-31m",	"P -3 1 2/m" ],
[162,	"P-31m",	"P -3 1 m" ],
[163,	"P-31c",	"P -3 1 2/c" ],
[163,	"P-31c",	"P -3 1 c" ],
[164,	"P-3m1",	"P -3 2/m 1" ],
[164,	"P-3m1",	"P -3 m 1" ],
[165,	"P-3c1",	"P -3 2/c 1" ],
[165,	"P-3c1",	"P -3 c 1" ],
[166,	"H-3m",	"H -3 2/m" ],
[166,	"H-3m",	"H -3 m" ],
[1166,	"R-3m",	"R -3 2/m" ],
[1166,	"R-3m",	"R -3 m" ],
[167,	"H-3c",	"H -3 2/c" ],
[167,	"H-3c",	"H -3 c" ],
[1167,	"R-3c",	"R -3 2/c" ],
[1167,	"R-3c",	"R -3 c" ],
[168,	"P6",	"P 6" ],
[169,	"P61",	"P 61" ],
[170,	"P65",	"P 65" ],
[171,	"P62",	"P 62" ],
[172,	"P64",	"P 64" ],
[173,	"P63",	"P 63" ],
[174,	"P-6",	"P -6" ],
[175,	"P6/m",	"P 6/m" ],
[176,	"P63/m",	"P 63/m" ],
[177,	"P622",	"P 6 2 2" ],
[178,	"P6122",	"P 61 2 2" ],
[179,	"P6522",	"P 65 2 2" ],
[180,	"P6222",	"P 62 2 2" ],
[181,	"P6422",	"P 64 2 2" ],
[182,	"P6322",	"P 63 2 2" ],
[183,	"P6mm",	"P 6 m m" ],
[184,	"P6cc",	"P 6 c c" ],
[185,	"P63cm",	"P 63 c m" ],
[186,	"P63mc",	"P 63 m c" ],
[187,	"P-6m2",	"P -6 m 2" ],
[188,	"P-6c2",	"P -6 c 2" ],
[189,	"P-62m",	"P -6 2 m" ],
[190,	"P-62c",	"P -6 2 c" ],
[191,	"P6/mmm",	"P 6/m 2/m 2/m" ],
[191,	"P6/mmm",	"P 6/m m m" ],
[192,	"P6/mcc",	"P 6/m 2/c 2/c" ],
[192,	"P6/mcc",	"P 6/m c c" ],
[193,	"P63/mcm",	"P 63/m 2/c 2/m" ],
[193,	"P63/mcm",	"P 63/m c m" ],
[194,	"P63/mmc",	"P 63/m 2/m 2/c" ],
[194,	"P63/mmc",	"P 63/m m c" ],
[195,	"P23",	"P 2 3" ],
[196,	"F23",	"F 2 3" ],
[197,	"I23",	"I 2 3" ],
[198,	"P213",	"P 21 3" ],
[199,	"I213",	"I 21 3" ],
[200,	"Pm-3",	"P 2/m -3" ],
[200,	"Pm-3",	"P m -3" ],
[201,	"Pn-3",	"P 2/n -3" ],
[201,	"Pn-3",	"P n -3" ],
[202,	"Fm-3",	"F 2/m -3" ],
[202,	"Fm-3",	"F m -3" ],
[203,	"Fd-3",	"F 2/d -3" ],
[203,	"Fd-3",	"F d -3" ],
[204,	"Im-3",	"I 2/m -3" ],
[204,	"Im-3",	"I m -3" ],
[205,	"Pa-3",	"P 21/a -3" ],
[205,	"Pa-3",	"P a -3" ],
[206,	"Ia-3",	"I 21/a -3" ],
[206,	"Ia-3",	"I a -3" ],
[207,	"P432",	"P 4 3 2" ],
[208,	"P4232",	"P 42 3 2" ],
[209,	"F432",	"F 4 3 2" ],
[210,	"F4132",	"F 41 3 2" ],
[211,	"I432",	"I 4 3 2" ],
[212,	"P4332",	"P 43 3 2" ],
[213,	"P4132",	"P 41 3 2" ],
[214,	"I4132",	"I 41 3 2" ],
[215,	"P-43m",	"P -4 3 m" ],
[216,	"F-43m",	"F -4 3 m" ],
[217,	"I-43m",	"I -4 3 m" ],
[218,	"P-43n",	"P -4 3 n" ],
[219,	"F-43c",	"F -4 3 c" ],
[220,	"I-43d",	"I -4 3 d" ],
[221,	"Pm-3m",	"P 4/m -3 2/m" ],
[221,	"Pm-3m",	"P m -3 m" ],
[222,	"Pn-3n",	"P 4/n -3 2/n P n -3 n" ],
[223,	"Pm-3n",	"P 42/m -3 2/n" ],
[223,	"Pm-3n",	"P m -3 n" ],
[224,	"Pn-3m",	"P 42/n -3 2/m" ],
[224,	"Pn-3m",	"P n -3 m" ],
[225,	"Fm-3m",	"F 4/m -3 2/m" ],
[225,	"Fm-3m",	"F m -3 m" ],
[226,	"Fm-3c",	"F 4/m -3 2/c" ],
[226,	"Fm-3c",	"F m -3 c" ],
[227,	"Fd-3m",	"F 41/d -3 2/m" ],
[227,	"Fd-3m",	"F d -3 m" ],
[228,	"Fd-3c",	"F 41/d -3 2/c" ],
[228,	"Fd-3c",	"F d -3 c" ],
[229,	"Im-3m",	"I 4/m -3 2/m" ],
[229,	"Im-3m",	"I m -3 m" ],
[230,	"Ia-3d",	"I 41/a -3 2/d" ],
[230,	"Ia-3d",	"I a -3 d" ],
[1003,	"P2",	"P 1 1 2" ],
[1004,	"P1121",	"P 1 1 21" ],
[3004,	"I21",	"I 1 21 1" ],
[1005,	"B2",	"B 1 1 2" ],
[1005,	"B2",	"B 2" ],
[2005,	"A2",	"A 2 1 1" ],
[3005,	"C21",	"C 1 21 1" ],
[4005,	"I2",	"I 1 2 1" ],
[4005,	"I2",	"I 2" ],
[1006,	"P11m",	"P 1 1 m" ],
[1007,	"P11b",	"P 1 1 b" ],
[1008,	"B11m",	"B 1 1 m" ],
[1009,	"B11b",	"B 1 1 b" ],
[1010,	"P112/m",	"P 1 1 2/m" ],
[1011,	"P1121/m",	"P 1 1 21/m" ],
[1012,	"B112/m",	"B 1 1 2/m" ],
[1013,	"P112/b",	"P 1 1 2/b" ],
[1014,	"P1121/b",	"P 1 1 21/b" ],
[1015,	"B112/b",	"B 1 1 2/b" ],
[1017,	"P2122",	"P 21 2 2" ],
[2017,	"P2212",	"P 2 21 2" ],
[1018,	"P21212a",	"P 21 21 2 (a)" ],
[2018,	"P21221",	"P 21 2 21" ],
[3018,	"P22121",	"P 2 21 21" ],
[1020,	"C2221a",	"C 2 2 21a)" ],
[1021,	"C222a",	"C 2 2 2a" ],
[1022,	"F222a",	"F 2 2 2a" ],
[1023,	"I222a",	"I 2 2 2a" ],
[1059,	"Pmmn2",	"P 21/m 21/m 2/n a" ],
[1094,	"P42212a",	"P 42 21 2a" ],
[1197,	"I23a",	"I 2 3a" ],

);

1;

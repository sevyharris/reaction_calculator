#!/usr/bin/env python
# encoding: utf-8

name = "harris_butane"
shortDesc = ""
longDesc = """

"""
autoGenerated=False
entry(
    index = 50,
    label = "O2(2) + CH3CO(20) <=> HO2(16) + CH2CO(24)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(286.579,'cm^3/(mol*s)'), n=3.25964, Ea=(201.639,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.06495, dn = +|- 0.00826721, dEa = +|- 0.0449898 kJ/mol"""),
)

entry(
    index = 52,
    label = "O2(2) + CH2CHO(21) <=> HO2(16) + CH2CO(24)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(453.381,'cm^3/(mol*s)'), n=3.18437, Ea=(146.989,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.06283, dn = +|- 0.00800543, dEa = +|- 0.0435653 kJ/mol"""),
)

entry(
    index = 127,
    label = "OH(15) + CH2O(9) <=> H2O(8) + HCO(19)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(197979,'cm^3/(mol*s)'), n=2.64442, Ea=(-10.6911,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.07772, dn = +|- 0.00983342, dEa = +|- 0.0535131 kJ/mol"""),
)

entry(
    index = 129,
    label = "HO2(16) + CH2O(9) <=> H2O2(17) + HCO(19)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(7.2169,'cm^3/(mol*s)'), n=3.59337, Ea=(36.1692,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.04537, dn = +|- 0.00582916, dEa = +|- 0.0317221 kJ/mol"""),
)

entry(
    index = 213,
    label = "HO2(16) + C2H5(33) <=> H2O2(17) + C2H4(11)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.428261,'cm^3/(mol*s)'), n=3.69947, Ea=(73.8643,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.05561, dn = +|- 0.00711052, dEa = +|- 0.0386952 kJ/mol"""),
)

entry(
    index = 245,
    label = "CH3(18) + butane(1) <=> CH4(10) + SC4H9(183)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(368.867,'cm^3/(mol*s)'), n=3.28309, Ea=(40.5716,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.11506, dn = +|- 0.0143089, dEa = +|- 0.0778685 kJ/mol"""),
)

entry(
    index = 246,
    label = "H(14) + butane(1) <=> H2(13) + SC4H9(183)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(1.26324e+08,'cm^3/(mol*s)'), n=1.95219, Ea=(30.5438,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.04337, dn = +|- 0.00557804, dEa = +|- 0.0303555 kJ/mol"""),
)

entry(
    index = 249,
    label = "HO2(16) + butane(1) <=> H2O2(17) + SC4H9(183)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(1.71854,'cm^3/(mol*s)'), n=3.73192, Ea=(53.718,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.06098, dn = +|- 0.00777666, dEa = +|- 0.0423203 kJ/mol"""),
)

entry(
    index = 282,
    label = "S(229) <=> S(244)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(1.00702e+10,'s^-1'), n=0.731128, Ea=(86.9283,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.07031, dn = +|- 0.00892717, dEa = +|- 0.0485813 kJ/mol"""),
)

entry(
    index = 286,
    label = "CH3(18) + butane(1) <=> CH4(10) + PC4H9(182)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(277.756,'cm^3/(mol*s)'), n=3.25739, Ea=(51.2229,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.1333, dn = +|- 0.0164396, dEa = +|- 0.0894634 kJ/mol"""),
)

entry(
    index = 288,
    label = "OH(15) + butane(1) <=> H2O(8) + PC4H9(182)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(18097.5,'cm^3/(mol*s)'), n=2.8035, Ea=(-1.04027,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.08541, dn = +|- 0.0107677, dEa = +|- 0.0585973 kJ/mol"""),
)

entry(
    index = 289,
    label = "O(5) + butane(1) <=> OH(15) + PC4H9(182)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(2.35369e+06,'cm^3/(mol*s)'), n=2.37635, Ea=(14.3813,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.09103, dn = +|- 0.0114463, dEa = +|- 0.0622904 kJ/mol"""),
)

entry(
    index = 313,
    label = "O2(2) + PC4H9(182) <=> HO2(16) + C4H8(188)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(45.8043,'cm^3/(mol*s)'), n=3.29895, Ea=(180.407,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.06788, dn = +|- 0.00862816, dEa = +|- 0.0469541 kJ/mol"""),
)

entry(
    index = 314,
    label = "O2(2) + SC4H9(183) <=> HO2(16) + C4H8(188)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(131.592,'cm^3/(mol*s)'), n=3.3074, Ea=(199.553,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.07833, dn = +|- 0.0099073, dEa = +|- 0.0539152 kJ/mol"""),
)

entry(
    index = 324,
    label = "S(229) <=> S(225)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(2.99984e+09,'s^-1'), n=0.441337, Ea=(69.4684,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.08722, dn = +|- 0.0109862, dEa = +|- 0.0597866 kJ/mol"""),
)

entry(
    index = 326,
    label = "S(225) <=> S(238)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(2.82336e+10,'s^-1'), n=0.8964, Ea=(106.431,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.10748, dn = +|- 0.0134128, dEa = +|- 0.072992 kJ/mol"""),
)

entry(
    index = 368,
    label = "CH3(18) + CH3CHO(35) <=> CH4(10) + CH2CHO(21)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(398.249,'cm^3/(mol*s)'), n=3.2162, Ea=(38.1941,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.14352, dn = +|- 0.0176196, dEa = +|- 0.0958852 kJ/mol"""),
)

entry(
    index = 370,
    label = "CH3CHO(35) + SC4H9(183) <=> CH2CHO(21) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.112293,'cm^3/(mol*s)'), n=3.33044, Ea=(32.2918,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.08599, dn = +|- 0.0108376, dEa = +|- 0.0589781 kJ/mol"""),
)

entry(
    index = 404,
    label = "OH(15) + PC4H9(182) <=> H2O(8) + C4H8(188)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(6373.1,'cm^3/(mol*s)'), n=2.77134, Ea=(-2.90012,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.07249, dn = +|- 0.00919497, dEa = +|- 0.0500387 kJ/mol"""),
)

entry(
    index = 410,
    label = "CH3(18) + PC4H9(182) <=> CH4(10) + C4H8(188)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(43.9031,'cm^3/(mol*s)'), n=3.2535, Ea=(42.7981,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.12013, dn = +|- 0.0149046, dEa = +|- 0.0811102 kJ/mol"""),
)

entry(
    index = 420,
    label = "HO2(16) + SC4H9(183) <=> H2O2(17) + C4H8(189)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.192696,'cm^3/(mol*s)'), n=3.71257, Ea=(60.2855,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.06168, dn = +|- 0.007863, dEa = +|- 0.0427902 kJ/mol"""),
)

entry(
    index = 422,
    label = "HO2(16) + SC4H9(183) <=> H2O2(17) + C4H8(188)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.258809,'cm^3/(mol*s)'), n=3.71808, Ea=(74.0326,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.05985, dn = +|- 0.00763726, dEa = +|- 0.0415617 kJ/mol"""),
)

entry(
    index = 434,
    label = "CH2CHO(21) + C2H5(33) <=> C2H4(11) + CH3CHO(35)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(2.64675,'cm^3/(mol*s)'), n=3.46277, Ea=(65.8334,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.05608, dn = +|- 0.00716892, dEa = +|- 0.039013 kJ/mol"""),
)

entry(
    index = 459,
    label = "CH3(18) + SC4H9(183) <=> CH4(10) + C4H8(189)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(92.6168,'cm^3/(mol*s)'), n=3.27362, Ea=(44.6189,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.10907, dn = +|- 0.0136001, dEa = +|- 0.0740115 kJ/mol"""),
)

entry(
    index = 804,
    label = "SC4H9(183) + S(787) <=> S(229) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.00174262,'cm^3/(mol*s)'), n=3.07685, Ea=(-13.5168,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.22322, dn = +|- 0.026471, dEa = +|- 0.144054 kJ/mol"""),
)

entry(
    index = 808,
    label = "SC4H9(183) + S(787) <=> S(225) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.00609574,'cm^3/(mol*s)'), n=3.16414, Ea=(-8.14302,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.18765, dn = +|- 0.022594, dEa = +|- 0.122956 kJ/mol"""),
)

entry(
    index = 809,
    label = "PC4H9(182) + S(787) <=> S(225) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.115585,'cm^3/(mol*s)'), n=3.11043, Ea=(0.449548,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.20042, dn = +|- 0.0239997, dEa = +|- 0.130606 kJ/mol"""),
)

entry(
    index = 915,
    label = "O2(2) + S(777) <=> HO2(16) + S(252)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(24.5518,'cm^3/(mol*s)'), n=3.18715, Ea=(145.513,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.05373, dn = +|- 0.00687538, dEa = +|- 0.0374156 kJ/mol"""),
)

entry(
    index = 1075,
    label = "CH2O(9) + CH3O2(45) <=> HCO(19) + CH3O2H(46)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(2.12442,'cm^3/(mol*s)'), n=3.65406, Ea=(39.6853,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.04608, dn = +|- 0.00591817, dEa = +|- 0.0322064 kJ/mol"""),
)

entry(
    index = 1077,
    label = "HO2(16) + CH3O2(45) <=> O2(2) + CH3O2H(46)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(26.1337,'cm^3/(mol*s)'), n=3.34111, Ea=(-15.4249,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.10198, dn = +|- 0.0127581, dEa = +|- 0.0694293 kJ/mol"""),
)

entry(
    index = 1103,
    label = "CH3O2(45) + CH2CHO(21) <=> CH3O2H(46) + CH2CO(24)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(1.96322,'cm^3/(mol*s)'), n=3.57588, Ea=(40.8356,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.04004, dn = +|- 0.00515769, dEa = +|- 0.0280679 kJ/mol"""),
)

entry(
    index = 1111,
    label = "CH3O2(45) + C2H5(33) <=> CH3O2H(46) + C2H4(11)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.0568619,'cm^3/(mol*s)'), n=3.71532, Ea=(75.8062,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.05105, dn = +|- 0.00654137, dEa = +|- 0.0355979 kJ/mol"""),
)

entry(
    index = 1658,
    label = "CH2CHO(21) + C2H5O2(47) <=> CH2CO(24) + C2H6O2(48)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.313584,'cm^3/(mol*s)'), n=3.58745, Ea=(40.4849,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.04307, dn = +|- 0.00554036, dEa = +|- 0.0301504 kJ/mol"""),
)

entry(
    index = 4721,
    label = "HO2(16) + SC4H9(183) <=> O2(2) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(1.50279,'cm^3/(mol*s)'), n=3.18743, Ea=(-37.4106,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.14821, dn = +|- 0.0181572, dEa = +|- 0.0988108 kJ/mol"""),
)

entry(
    index = 4724,
    label = "H2O2(17) + SC4H9(183) <=> HO2(16) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.890522,'cm^3/(mol*s)'), n=3.16078, Ea=(3.56445,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.17543, dn = +|- 0.021236, dEa = +|- 0.115566 kJ/mol"""),
)

entry(
    index = 4728,
    label = "C2H6O2(48) + SC4H9(183) <=> C2H5O2(47) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.14415,'cm^3/(mol*s)'), n=3.17569, Ea=(3.72121,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.16446, dn = +|- 0.0200031, dEa = +|- 0.108856 kJ/mol"""),
)

entry(
    index = 4729,
    label = "SC4H9(183) + S(187) <=> S(186) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.0351468,'cm^3/(mol*s)'), n=3.22894, Ea=(-0.722473,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.15055, dn = +|- 0.0184244, dEa = +|- 0.100265 kJ/mol"""),
)

entry(
    index = 4736,
    label = "H2O2(17) + PC4H9(182) <=> HO2(16) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(2.40393,'cm^3/(mol*s)'), n=3.13033, Ea=(4.26539,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.19885, dn = +|- 0.0238278, dEa = +|- 0.12967 kJ/mol"""),
)

entry(
    index = 4737,
    label = "C2H6O2(48) + PC4H9(182) <=> C2H5O2(47) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.519559,'cm^3/(mol*s)'), n=3.14811, Ea=(1.83414,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.18835, dn = +|- 0.0226722, dEa = +|- 0.123382 kJ/mol"""),
)

entry(
    index = 4738,
    label = "PC4H9(182) + S(187) <=> S(186) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.208991,'cm^3/(mol*s)'), n=3.16655, Ea=(-0.21066,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.1853, dn = +|- 0.0223344, dEa = +|- 0.121543 kJ/mol"""),
)

entry(
    index = 4745,
    label = "S(225) <=> S(229)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(1.10454e+10,'s^-1'), n=0.486434, Ea=(56.4887,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.06554, dn = +|- 0.00834069, dEa = +|- 0.0453897 kJ/mol"""),
)

entry(
    index = 4778,
    label = "SC4H9(183) + CCCCOO <=> S(184) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.0950455,'cm^3/(mol*s)'), n=3.21396, Ea=(2.04628,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.15249, dn = +|- 0.0186463, dEa = +|- 0.101473 kJ/mol"""),
)

entry(
    index = 4779,
    label = "PC4H9(182) + CCCCOO <=> S(184) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.0675378,'cm^3/(mol*s)'), n=3.1393, Ea=(3.52738,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.19192, dn = +|- 0.0230654, dEa = +|- 0.125521 kJ/mol"""),
)

entry(
    index = 4796,
    label = "HO2(16) + S(184) <=> O2(2) + CCCCOO",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.482114,'cm^3/(mol*s)'), n=3.25792, Ea=(-33.0821,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.10772, dn = +|- 0.0134407, dEa = +|- 0.0731437 kJ/mol"""),
)

entry(
    index = 4917,
    label = "C2H5(33) + S(184) <=> C2H4(11) + CCCCOO",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.00639276,'cm^3/(mol*s)'), n=3.73534, Ea=(76.4663,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.05402, dn = +|- 0.00691177, dEa = +|- 0.0376136 kJ/mol"""),
)

entry(
    index = 5046,
    label = "CH3O2H(46) + SC4H9(183) <=> CH3O2(45) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.159153,'cm^3/(mol*s)'), n=3.18186, Ea=(4.03904,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.16236, dn = +|- 0.0197659, dEa = +|- 0.107566 kJ/mol"""),
)

entry(
    index = 5047,
    label = "CH3O2H(46) + PC4H9(182) <=> CH3O2(45) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.568972,'cm^3/(mol*s)'), n=3.15167, Ea=(1.7941,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.18673, dn = +|- 0.0224926, dEa = +|- 0.122404 kJ/mol"""),
)

entry(
    index = 5056,
    label = "CH3O2H(46) + CH2CHO(21) <=> CH3O2(45) + CH3CHO(35)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.997926,'cm^3/(mol*s)'), n=3.31826, Ea=(21.8648,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.11602, dn = +|- 0.0144215, dEa = +|- 0.0784811 kJ/mol"""),
)

entry(
    index = 5226,
    label = "CCCOO + SC4H9(183) <=> C3H7O2(95) + butane(1)",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(0.135064,'cm^3/(mol*s)'), n=3.16875, Ea=(3.46873,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.16691, dn = +|- 0.0202798, dEa = +|- 0.110362 kJ/mol"""),
)

entry(
    index = 5446,
    label = "O2(2) + [O]CCCCOO <=> HO2(16) + O=CCCCOO",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(252.55,'cm^3/(mol*s)'), n=3.36242, Ea=(160.122,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.11014, dn = +|- 0.0137279, dEa = +|- 0.0747066 kJ/mol"""),
)

entry(
    index = 5596,
    label = "O2(2) + [O]CC(=O)O <=> HO2(16) + O=CC(=O)O",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(136.364,'cm^3/(mol*s)'), n=3.20677, Ea=(165.429,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.0604, dn = +|- 0.00770534, dEa = +|- 0.0419322 kJ/mol"""),
)

entry(
    index = 7841,
    label = "O2(2) + [O]CCCC=O <=> HO2(16) + O=CCCC=O",
    degeneracy = 1.0,
    elementary_high_p = True,
    kinetics = Arrhenius(A=(128.251,'cm^3/(mol*s)'), n=3.26016, Ea=(156.553,'kJ/mol'), T0=(1,'K'), Tmin=(298,'K'), Tmax=(2500,'K'), comment="""Fitted to 50 data points; dA = *|/ 1.07228, dn = +|- 0.00916824, dEa = +|- 0.0498932 kJ/mol"""),
)


%mem=5GB
%nprocshared=24
#P m062x/cc-pVTZ ! ASE formatted method and basis
Opt=(ModRedun,Loose,maxcycles=900) Int(Grid=SG1) scf=(maxcycle=900)

Gaussian input prepared by ASE

0 2
O                 1.1935805270       -7.2258760033        0.0233226741
O                 0.7768941984       -6.1738961314        0.7028903476
O                 1.7157414159       -4.5417247599       -1.8204263050
C                 2.5389832107       -3.2873061508       -2.7706186924
C                 2.2345344951       -3.3953578903       -1.2726572873
C                 2.0237537399       -6.7261051194       -0.9918401700
C                 2.6200538310       -4.6672403292       -3.4166006642
C                 2.6248655819       -4.5791030790        0.3548074944
C                 2.0912535358       -5.2317328794       -0.8846562356
C                 2.0969324242       -4.8504362921       -0.8422843273
H                 1.7398525721       -2.7006515996       -3.2743579404
H                 3.5081162299       -2.7628899410       -2.9194624695
H                 1.2860889709       -2.8646009975       -1.0404979922
H                 3.0535934039       -2.9266751266       -0.6856604210
H                 3.0460091473       -7.1577279458       -0.8950695237
H                 1.6147268898       -6.9912893195       -1.9928092483
H                 1.8568527427       -4.7636033988       -4.2179832181
H                 2.4306188962       -5.4482067308       -2.6501707424
H                 3.6297687571       -4.8319985011       -3.8494130402
H                 3.6785343197       -4.8893467890        0.5151337909
H                 2.0155174841       -4.8870745257        1.2299929740
H                 2.5868014083       -3.4724351292        0.2635300178
H                 2.2462657797       -5.5327917002       -1.7060259241
H                 2.8218205798       -5.0933079918       -0.0362177548
H                 1.2665506482       -5.2770078341        0.1827030705

2 25 F
25 10 F
2 25 10 F


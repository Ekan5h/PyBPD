from ..modules import *
from ..inputs import *

tage = LSB()

h = HIGHEST_PRIORITY()

t0 = PREDICTOR_2BIT()
t1 = TAGE_TABLE()
t2 = TAGE_TABLE()
t3 = TAGE_TABLE()
t4 = TAGE_TABLE()


ha1 = HASH1()
ha2 = HASH1()
ha3 = HASH1()
ha4 = HASH1()

x1 = XOR()
x2 = XOR()
x3 = XOR()
x4 = XOR()

tage.children.append(h)

h.children.extend([t0, t1, t2, t3, t4])

t0.children.append(PC())

t1.children.append(ha1)
t2.children.append(ha2)
t3.children.append(ha3)
t4.children.append(ha4)

ha1.children.append(x1)
ha2.children.append(x2)
ha3.children.append(x3)
ha4.children.append(x4)

x1.children.extend([PC(), HISTORY5()])
x2.children.extend([PC(), HISTORY15()])
x3.children.extend([PC(), HISTORY44()])
x4.children.extend([PC(), HISTORY130()])
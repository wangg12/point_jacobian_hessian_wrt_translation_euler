import sympy as sp
from sympy.interactive import printing
printing.init_printing(use_latex=True)


tx = sp.symbols('tx')
ty = sp.symbols('ty')
tz = sp.symbols('tz')
t = sp.Matrix([tx, ty, tz])
print("t:", t.shape)
sp.pprint(t)
# sp.print_latex(t)
print()

ex = sp.symbols('ex')  # euler x
ey = sp.symbols('ey')  # euler y
ez = sp.symbols('ez')  # euler z

p = sp.Matrix([tx, ty, tz, ex, ey, ez])  # 6x1
print("p: ", p.shape)
sp.pprint(p)
# sp.print_latex(p)
print()

x1 = sp.symbols('x1')
x2 = sp.symbols('x2')
x3 = sp.symbols('x3')
x = sp.Matrix([x1, x2, x3])
print("x: ", x.shape)
sp.pprint(x)
print()

cx = sp.cos(ex)
sx = sp.sin(ex)
cy = sp.cos(ey)
sy = sp.sin(ey)
cz = sp.cos(ez)
sz = sp.sin(ez)

def simplify_sincos(func, latex=False):
    if latex:
        return func.xreplace({
            sp.sin(ex): sp.symbols("s_x"),
            sp.cos(ex): sp.symbols("c_x"),
            sp.sin(ey): sp.symbols("s_y"),
            sp.cos(ey): sp.symbols("c_y"),
            sp.sin(ez): sp.symbols("s_z"),
            sp.cos(ez): sp.symbols("c_z"),
            tx: sp.symbols("t_x"),
            ty: sp.symbols("t_y"),
            tz: sp.symbols("t_z"),
        })
    else:
        return func.xreplace({
            sp.sin(ex): sp.symbols("sx"),
            sp.cos(ex): sp.symbols("cx"),
            sp.sin(ey): sp.symbols("sy"),
            sp.cos(ey): sp.symbols("cy"),
            sp.sin(ez): sp.symbols("sz"),
            sp.cos(ez): sp.symbols("cz"),
        })

sp.print_latex(simplify_sincos(x, latex=True))
sp.print_latex(simplify_sincos(p, latex=True))
sp.print_latex(simplify_sincos(t, latex=True))


R = sp.Matrix([
    [cy * cz,          - cy * sz,           sy],
    [cx*sz + sx*sy*cz, cx*cz - sx*sy*sz,   -sx*cy],
    [sx*sz - cx*sy*cz, cx*sy*sz + sx * cz,  cx*cy]])
# print("R:\n", sp.latex(R))
R_simple = simplify_sincos(R)
print("R:", R.shape)
sp.pprint(R_simple)
# sp.print_latex(simplify_sincos(R, latex=True))
print()

Tpx = R.multiply(x) + t
print("T(p, x): ", Tpx.shape)
sp.pprint(Tpx)
# sp.print_latex(simplify_sincos(Tpx, latex=True))
print()


# J = Tpx.diff(p.T)#[0, :, :, 0]
J = sp.zeros(3, 6)
for r in range(3):
    for c in range(6):
        J[r, c] = Tpx[r, 0].diff(p[c, 0])
print("Jacobian: ", J.shape)
J_simple = simplify_sincos(J)
sp.pprint(J_simple)
# sp.print_latex(simplify_sincos(J, latex=True))
print()

for r in range(3):
    for c in range(6):
        print("J[{}, {}]: {}".format(r, c, J_simple[r, c]))
        # sp.pprint(J[r, c])


H = sp.zeros(18, 6)
for i in range(3):
    for j in range(6):
        for pi in range(6):
            H[pi*3+i, j] = J[i, j].diff(p[pi, 0])
print("Hessian: ", H.shape)
H_simple = simplify_sincos(H)
sp.pprint(H_simple)
# sp.print_latex(simplify_sincos(H, latex=True))
# print()
print()
for r in range(18):
    for c in range(6):
        print("H[{}, {}]: {}".format(r, c, H_simple[r, c]))
        # sp.pprint()

# latex math equations online: https://www.latexlive.com/

# H_latex = sp.latex(H)
# sp.pprint(H_simple)

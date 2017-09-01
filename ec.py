from gcd import *

class TestError(Exception):
    def __init__(self, value):
        self.msg = value
    def __str__(self):
        return self.msg


# y^2 = x^3 + ax + b
class elliptic_curve:
    p = 0
    q = 0
    a = 0
    b = 0
    P = [0,0]
    name = "No name"

    def getparams(self):
        return((p, q, a, b, [px, py]))

    def setparams(self, name = "No name", c = ['0', '0', '0', '0', '0', '0'], bs = 16):
        self.name = name
        self.p = long(c[0], base=bs)
        self.q = long(c[1], base=bs)
        self.a = long(c[2], base=bs)
        self.b = long(c[3], base=bs)
        self.P = [long(c[4], base=bs), long(c[5], base=bs)]

    def __init__(self, name = "No name", c = ['0', '0', '0', '0', '0', '0'], bs = 16):

        self.name = name
        self.p = long(c[0], base = bs)
        self.q = long(c[1], base = bs)
        self.a = long(c[2], base = bs)
        self.b = long(c[3], base = bs)
        self.P = [long(c[4], base = bs), long(c[5], base = bs)]

    def iszero(self, P):
        return (P == [0, 0])

    def add(self, P, Q):
        if P == [0, 0]:
            return Q
        if Q == [0, 0]:
            return P
        if (P[1] + Q[1]) % self.p == 0:
            return [0, 0]
        if P == Q:
            l = ((3 * (P[0] ** 2) + self.a) * (modinv(2 * P[1], self.p))) % self.p
        else:
            l = ((P[1] - Q[1]) * modinv(P[0] - Q[0], self.p) ) % self.p
        x3 = ((l ** 2) - P[0] - Q[0]) % self.p
        y3 = (l * (P[0] - x3) - P[1]) % self.p
        return [x3, y3]

    def mul(self, k, P):
        Y = [0, 0]
        Z = P
        while k > 0:
            if k % 2 == 1:
                Y = self.add(Y, Z)
            Z = self.add(Z, Z)
            k /= 2
        return Y

    def pkey_from_skey(self, skey):
        return self.mul(skey, self.P)

    def sign(self, digest, rnd, skey):
        R = self.mul(rnd, self.P)[0] % self.q
        S = (rnd * digest + R * skey) % self.q
        return [R, S]

    def verify(self, digest, signature, pkey):
        R = signature[0]
        S = signature[1]
        if not 0 < R < self.q:
            return False
        if not 0 < S < self.q:
            return False
        e = modinv(digest, self.q)
        z1 = (S * e) % self.q
        z2 = (- R * e) % self.q
        C1 = self.mul(z1, self.P)
        C2 = self.mul(z2, pkey)
        C = self.add(C1, C2)
        if (C[0] - R) % self.q == 0:
            return True
        else:
            return False

    def selftest(self):
        self.setparams("GOSTR3410256TestParams", ["8000000000000000000000000000000000000000000000000000000000000431",
                    "8000000000000000000000000000000150FE8A1892976154C59CFC193ACCF5B3",
                    "0000000000000000000000000000000000000000000000000000000000000007",
                    "5FBFF498AA938CE739B8E022FBAFEF40563F6E6A3472FC2A514C0CE9DAE23B7E",
                    "0000000000000000000000000000000000000000000000000000000000000002",
                    "08E2A8A0E65147D4BD6316030E16D19C85C97F0A9CA267122B96ABBCEA7E8FC8"],
                    16)
        skey = 55441196065363246126355624130324183196576709222340016572108097750006097525544L
        Q = self.mul(skey, self.P)
        if not Q == [long("7F2B49E270DB6D90D8595BEC458B50C58585BA1D4E9B788F6689DBD8E56FD80B", base = 16),
                            long("26F1B489D6701DD185C8413A977B3CBBAF64D1C593D26627DFFB101A87FF77DA", base = 16)]:
            raise TestError('Public key generation failed')
        digest = long("2DFBC1B372D89A1188C09C52E0EEC61FCE52032AB1022E8E67ECE6672B043EE5", base = 16)
#            20798893674476452017134061561508270130637142515379653289952617252661468872421L
        rnd = long( "77105C9B20BCD3122823C8CF6FCC7B956DE33814E95B7FE64FED924594DCEAB3", base = 16)
#            53854137677348463731403841147996619241504003434302020712960838528893196233395L
        signature = self.sign(digest, rnd, skey)
        if not signature == [long("41AA28D2F1AB148280CD9ED56FEDA41974053554A42767B83AD043FD39DC0493", base = 16),
                            long("1456C64BA4642A1653C235A98A60249BCD6D3F746B631DF928014F6C5BF9C40", base = 16)]:
            raise TestError('Signature generation failed')
        if not self.verify(digest, signature, Q):
            raise TestError('Signature verification failed')
        return True

from gcd import *
from primeq import *

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
        return((self.p, self.q, self.a, self.b, self.P))

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

    def gosttest(self):
        log = []
        fail = False
        if 2 ** 254 < self.q < 2 ** 256:
            interval = 'GOST R 34.10-2001'
        elif 2 ** 508 < self.q < 2 ** 512:
            interval = 'GOST R 34.10-2012'
        else:
            interval = 'Q is out of bounds'
            fail = True
        log.append('Q fits into ' + interval)
        if not primeq(self.p) == True:
            log.append('Fatal: P is composite')
            fail = True
        else:
            log.append('P is (probably) prime')
        if not primeq(self.q) == True:
            log.append('Fatal: Q is composite')
            fail = True
        else:
            log.append('Q is (probably) prime')
        if self.a %  self.p == 0:
            log.append('A == 0')
            fail = True
        else:
            log.append('A != 0')
        if self.b % self.p == 0:
            log.append('B == 0')
            fail = True
        else:
            log.append('B != 0')
        if self.p == self.q:
            log.append('P == Q')
            fail = True
        else:
            log.append('P != Q')
        j = (1728 * 4 * pow(self.a, 3, self.p) * modinv(4 *  self.a ** 3 + 27 * self. b ** 2, self.p)) % self.p
        if j == 0 or j == 1728:
            log.append('j(E) failed: j(E) = ' + hex(j).lstrip('0x').rstrip('L').upper())
            fail = True
        else:
            log.append('j(E) passed: j(E) = ' + hex(j).lstrip('0x').rstrip('L').upper())
        if  2 ** 254 < self.q < 2 ** 256:
            cnt = 31
        else:
            cnt = 131
        mov = self.p
        movfailed = False
        for i in range(cnt):
            if(mov % self.q == 1):
                mov *= self.p
                fail = True
                movfailed = True
                break
        if movfailed:
            log.append('MOV degree test failed')
        else:
            log.append('MOV degree test passed for t = ' + str(cnt))
        if not (self.P[1] ** 2 - self.P[0] ** 3 - self.a * self.P[0] - self.b) %  self.p == 0:
            log.append('Point P does not belong to curve')
            fail = True
        else:
            log.append('Point P belongs to curve')
        if self.iszero(self.mul(self.q, self.P)) == True:
            log.append('Point P is of order Q')
        else:
            log.append('Point P is NOT of order Q')
            fail = True
        skey_256 = 55441196065363246126355624130324183196576709222340016572108097750006097525544L
        digest_256 = long("2DFBC1B372D89A1188C09C52E0EEC61FCE52032AB1022E8E67ECE6672B043EE5", base=16)
        rnd_256 = long("77105C9B20BCD3122823C8CF6FCC7B956DE33814E95B7FE64FED924594DCEAB3", base=16)

        skey_512 = long("BA6048AADAE241BA40936D47756D7C93091A0E8514669700EE7508E508B102072E8123B2200A0563322DAD2827E2714A2636B7BFD18AADFC62967821FA18DD4", base=16)
        digest_512 = long("754F3CFACC9E0615C4F4A7C4D8DAB531B09B6F9C170C533A71D147035B0C5917184EE536593F4414339976C647C5D5A407ADEDB1D560C4FC6777D2972075B8C", base=16)
        rnd_512 = long("59E7F4B1410FEACC570456C6801496946312120B39D019D455986E364F365886748ED7A44B3E794434006011842286212273A6D14CF70EA3AF71BB1AE679F1", base=16)

        if self.q < 2 ** 256:
            skey, digest, rnd = skey_256, digest_256, rnd_256
        else:
            skey, digest, rnd = skey_512, digest_512, rnd_512

        Q = self.mul(skey, self.P)

        signature = self.sign(digest, rnd, skey)
        if not self.verify(digest, signature, Q):
            log.append('Test signature generation/verification failed')
            fail = True
        else:
            log.append('Test signature generation/verification passed')
        log.append('----' * 8)
        log.append('Test example:')
        log.append('d = ' + hex(skey).lstrip('0x').rstrip('L').upper())
        log.append('Q = (' + hex(Q[0]).lstrip('0x').rstrip('L').upper() + ', ' +
                                                                    hex(Q[1]).lstrip('0x').rstrip('L').upper() + ')')
        log.append('e = ' + hex(digest).lstrip('0x').rstrip('L').upper())
        log.append('k = ' + hex(rnd).lstrip('0x').rstrip('L').upper())
        log.append('Signature = (' + hex(signature[0]).lstrip('0x').rstrip('L').upper() + ', ' +
                                                      hex(signature[1]).lstrip('0x').rstrip('L').upper()  + ')')
        log.append('----' * 8)
        if fail == True:
            log.append('GOST R 34.10-2012 verification failed')
        else:
            log.append('GOST R 34.10-2012 verification passed')
        return log

    def loadfromfile(self, filename):
        with open(filename, "r") as fh:
            data = fh.readlines()

        patterns = ['P=', 'Q=', 'A=', 'B=', 'PX=', 'PY=']
        params = [None] * 6
        print (data)
        for str in data:
            if not str.upper().find('P=') == -1:
                tmp = str.split('=')
                params[0] = tmp[1].lstrip(' ').rstrip(' \n')
            if not str.upper().find('Q=') == -1:
                tmp = str.split('=')
                params[1] = tmp[1].lstrip(' ').rstrip(' \n')
            if not str.upper().find('A=') == -1:
                tmp = str.split('=')
                params[2] = tmp[1].lstrip(' ').rstrip(' \n')
            if not str.upper().find('B=') == -1:
                tmp = str.split('=')
                params[3] = tmp[1].lstrip(' ').rstrip(' \n')
            if not str.upper().find('X=') == -1:
                tmp = str.split('=')
                params[4] = tmp[1].lstrip(' ').rstrip(' \n')
            if not str.upper().find('Y=') == -1:
                tmp = str.upper().split('=')
                params[5] = tmp[1].lstrip(' ').rstrip(' \n')
        print params
        try:
            self.setparams(filename, params, 16)
        except(TypeError):
            pass
        except(ValueError):
            pass


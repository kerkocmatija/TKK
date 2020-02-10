# PROGRAM ZA REŠEVANJE HILLOVE ŠIFRE

import operator

slovar = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4,
          'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
          'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14,
          'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
          'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}

# Nekaj najpogostejših angleških besed, s katerimi bomo preverjali, ali je dobljeno 
# besedilo res logično besedilo v angleškem jeziku in ne le naključne črke.
seznam_najpogostejsih = ['THE', 'IS', 'SOME', 'FOR', 'IN', 'AT', 'TAKE',
                         'VERY', 'POOR', 'THING', 'ONE', 'TRUE', 'OF',
                         'AND', 'NOT', 'WITH', 'HE', 'BUT', 'THIS', 'HIS',
                         'ME', 'WOULD', 'COME', 'ALL', 'WILL']


def dobi_kljuc(slovar, vrednost):
    """Funkcija dobi slovar ter vrednost ter vrne njen ključ."""
    for k, v in slovar.items():
        if v == vrednost:
            return k


# Matrike bomo podajali kot sezname seznamov, kjer bodo vrstice elementi seznama.
def preslikaj_vektor(A, v):
    """Funkcija vrne vektor v preslikan z matriko A."""
    u1 = (slovar[A[0][0]] * slovar[v[0]] + slovar[A[0][1]] * slovar[v[1]]) % 26
    u2 = (slovar[A[1][0]] * slovar[v[0]] + slovar[A[1][1]] * slovar[v[1]]) % 26
    return [dobi_kljuc(slovar, u1), dobi_kljuc(slovar, u2)]


def zmnozi_matriki(A, B):
    """Funkcija zmnoži matriki A in B, ki sta dimenzije 2x2."""
    u1 = (slovar[A[0][0]] * slovar[B[0][0]] + slovar[A[0][1]] * slovar[B[1][0]]) % 26
    u2 = (slovar[A[0][0]] * slovar[B[0][1]] + slovar[A[0][1]] * slovar[B[1][1]]) % 26
    u3 = (slovar[A[1][0]] * slovar[B[0][0]] + slovar[A[1][1]] * slovar[B[0][1]]) % 26
    u4 = (slovar[A[1][0]] * slovar[B[1][0]] + slovar[A[1][1]] * slovar[B[1][1]]) % 26
    C = [[u1, u2], [u3, u4]]
    return C

# Razširjeni Evklidov algoritem, kot pomožna funkcija iskanja inverza po modulu 26.
def razsirjeni_evklid(a, b):
    zadnji_ostanek = abs(a)
    ostanek = abs(b)
    x = 0
    zadnji_x = 1
    y = 1
    zadnji_y = 0
    while ostanek:
        zadnji_ostanek, (kvocient, ostanek) = ostanek, divmod(zadnji_ostanek, ostanek)
        x, zadnji_x = zadnji_x - kvocient * x, x
        y, zadnji_y = zadnji_y - kvocient * y, y
    if a < 0:
        if b < 0:
            return zadnji_ostanek, (-1) * zadnji_x, (-1) * zadnji_y
        if b >= 0:
            return zadnji_ostanek, (-1) * zadnji_x, zadnji_y
    if a >= 0:
        if b < 0:
            return zadnji_ostanek, zadnji_x, (-1) * zadnji_y
        if b >= 0:
            return zadnji_ostanek, zadnji_x, zadnji_y


def inverz_po_modulu(a, m):
    """Funkcija izračuna inverz elementa a po modulu m."""
    g, x, y = razsirjeni_evklid(a, m)
    if g != 1:
        pass
    return x % m


def determinanta(A):
    """Funkcija izračuna determinanto matrike A po modulu 26."""
    return (A[0][0] * A[1][1] - A[1][0] * A[0][1]) % 26


def inverz_matrike(A):
    """Funkcija vrne inverz matrike A. Inverz je podan s črkami."""
    det = (slovar[A[0][0]] * slovar[A[1][1]] - slovar[A[1][0]] * slovar[A[0][1]]) % 26

    B = [[slovar[A[1][1]] * inverz_po_modulu(det, 26) % 26, (- slovar[A[0][1]]) * inverz_po_modulu(det, 26) % 26],
         [(- slovar[A[1][0]]) * inverz_po_modulu(det, 26) % 26, slovar[A[0][0]] * inverz_po_modulu(det, 26) % 26]]
    return [[dobi_kljuc(slovar, B[0][0]), dobi_kljuc(slovar, B[0][1])],
            [dobi_kljuc(slovar, B[1][0]), dobi_kljuc(slovar, B[1][1])]]


def Encrypt(b, k):
    """Funkcija zakodira besedilo b s ključem k."""
    n = len(b)
    k1 = len(k)
    c = ''
    if n % k1 == 0:
        pass
    else:
        b = b + (k1 - (n % k1)) * 'A'
    while n > 0:
        nova = preslikaj_vektor(k, b[:k1])
        c = c + nova[0] + nova[1]
        b = b[k1:]
        n -= 2
    return c


def Decrypt(c, k):
    """Funkcija odkodira kriptogram c s ključem k."""
    n = len(c)
    k1 = len(k)
    b = ''
    while n > 0:
        nova = preslikaj_vektor(inverz_matrike(k), c[:k1])
        b = b + nova[0] + nova[1]
        c = c[k1:]
        n -= 2
    return b


# Šifro bomo razbijali z metodo plaintexta.
# Poiskali bomo najpogostejše dvojice črk, ter preverili njihovo frekvenco.
slovar_delezev = {'TH': 0.1383, 'HE': 0.1164, 'IN': 0.0857, 'ER': 0.0855,
                  'AN': 0.0751, 'RE': 0.0616}


def razbij(c):
    """Funkcija prejme kriptogram c ter vrne urejen seznam najpogostejših dvojic črk v c."""
    n = len(c)
    m = len(slovar_delezev)
    slovar1 = dict()
    slovar_urejen1 = dict()
    slovar2 = dict()
    for i in range(0, n - 1):
        if c[i] + c[i + 1] not in slovar1:
            slovar1[c[i] + c[i + 1]] = 1
        else:
            slovar1[c[i] + c[i + 1]] += 1
    # Uredimo slovar.
    slovar_urejen = sorted(slovar1.items(), key = operator.itemgetter(1), reverse=True)
    for i in slovar_urejen:
        slovar_urejen1[i[0]] = i[1]
    for i1 in range(0, m):
        slovar2[list(slovar_urejen1)[i1]] = slovar1[list(slovar_urejen1)[i1]]
    return slovar2


# Predvidevamo, da bodo nekatere najpogostejše dvojice tudi najpogostejše v našem besedilu.
def ugani_kljuc(c):
    """Funkcija poišče nekaj najboljših(možnih) ujemanj, ter jihvrne v seznamu."""
    seznam = []
    for i in razbij(c).keys():
        for j in razbij(c).keys():
            if i != j:
                P = [['T', 'H'], ['H', 'E']]
                Q = [[i[0], j[0]], [i[1], j[1]]]
                Pa = inverz_matrike(P)
                K = zmnozi_matriki(Q, Pa)
                kljuc = [[dobi_kljuc(slovar, K[0][0]), dobi_kljuc(slovar, K[0][1])],
                         [dobi_kljuc(slovar, K[1][0]), dobi_kljuc(slovar, K[1][1])]]
                seznam.append(Decrypt(c, kljuc))
    return seznam


def razbij_Hill(c):
    """Funkcija poišče najboljše odkodirano besedilo."""
    slovar1 = dict()
    for i in ugani_kljuc(c):
        slovar1[i] = 0
        for j in seznam_najpogostejsih:
            if j in i:
                slovar1[i] += 1
    return max(slovar1, key = lambda k: slovar1[k])

#####################################################################################################################
cripto = "STSQALWTCJMIJMTHNFEBWZTVJWMRNNHPMFICJFNWSZSXGW" \
         "PFHHAJFBNTWZTVTHIRMRCGVRJTAFXBWDIVMFWSNSTVLXIR" \
         "ACANWLYSIYVPJQMQNFLNMRPXSBHMWNJTIYNSZNHPHPIMNZ" \
         "DRWBPPNSHMSBUJMUHZXJHMWPSQHHJBMHHMWMJTAFXBWDIC" \
         "VETVLXIRANXFVETVUDWUHBWHEBMBSXHMWEEEHMANWUJUW" \
         "WHAWWSNWZMLJXVXHWTVJTZZICACHHJTNWWTZRHWWTIYJSS" \
         "UWSNSTVLWWWWHHPNSTVSNWWIYNSSOPFHMWEWHMHHMWNJTI" \
         "YNSXPCQJTOQYFPBQKHMWEWHMHHMWNACHRNWHMWBSZWSIOG" \
         "IICVETVLWWWWHHXANZRVZYWXUMVWZHDJHXAANHRUQZZOUN" \
         "BTZTJFNSBUUMBVZSTTLHZXNWDTZELTVPPAJWTICVETVNNHPM" \
         "FVZYWXUTVXBAJSQIUWWMHHMWNACHTGCTJIRGFCGVGSBYAPQI" \
         "TSDWISVPPNNZMWCIRMSFRSXHMWZEENFGDVBMHSYOYJHPBHLA" \
         "NXNNZVOSUSANTCVTVUMPSIATHYFAHEGCSPBWKNZMFWUYFIK" \
         "XBMHHMWAAZWGJJAHSSWKVJANANXFVMAFSENLHMWBLZNDHM" \
         "SBUJMNALWUFRSXWDMFWSVBTHLLJTYOSQWHYAGJHDJTXNNSTVMXTVJH"

# print(Encrypt('AGREHTREHUT', [['T', 'I'], ['L', 'L']]))
# print(Decrypt('WORXZARXHLXB', [['T', 'I'], ['L', 'L']]))
# print(inverz_matrike([['T', 'I'], ['L', 'L']]))
# print(inverz_po_modulu(7, 26))
# print(razbij(cripto))
# print(ugani_kljuc(cripto))
print(razbij_Hill(cripto))

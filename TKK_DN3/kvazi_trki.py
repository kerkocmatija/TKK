# ISKANJE KVAZI TRKOV ZA SHA-1
import hashlib
import random
import math
import fractions

identiteta = '27131072'   # Identifikacijska številka

# ISKANJE KVAZI TRKA:
def kvazi_trk():
    """Funkcija izračuna kvazi trk za funkcijo SHA-1."""
    # Ideja je iskanje s pomočjo paradoksa rojstnih dni.
    # Pripravimo si slovar, v kateregega bomo spravljali vrednosti, ki jih bomo izračunali.
    slovar_trkov = dict()
    seznam_trkov = []
    mozni = random.sample(range(100000, 100000000), 10000000)
    for i in mozni:
        potencialni = hashlib.sha1(str(i).encode('utf-8')).hexdigest()
        prvi = potencialni[:11]
        if prvi not in slovar_trkov.keys():
            slovar_trkov[prvi] = i
        else:
            seznam_trkov.append((i, slovar_trkov[prvi]))
            print(i, slovar_trkov[prvi])
    return seznam_trkov


# PODPISOVANJE REŠITVE:
def inverz(a, q):
    """Funkcija izračuna inverz a po modulu q."""
    """Ker vemo, da bomo računali inverz v Z_q za q je praštevilo, se ne ukvarjamo z obstojem inverza."""
    # Ideja je pobrana iz stackoverflow-a, ideja je dobra, ker je inverz izračunan HITRO!
    return pow(a, q - 2, q)


def gcd(x, y):
    """Funkcija poišče največji skupni delitelj števil x in y."""
    """Načeloma je gcd že v knjižnjici math od verzije 3.5 naprej, vendar raje definiramo, da ne bo napak."""
    while y != 0:
        (x, y) = (y, x % y)
    return x


# Želimo vsaj z zelo veliko verjetnostjo potrditi, da je izbrano število res praštevilo.
def je_prastevilo(n):
    """Funkcija z Miller-Rabin testom preveri, ali je število zelo verjetno praštevilo."""
    #     # Koda je pobrana iz strani Rosettacode, ker nima smisla izumljati nekaj novega:
    #     # https://rosettacode.org/wiki/Miller%E2%80%93Rabin_primality_test#Python
    if n != int(n):
        return False
    n = int(n)
    # Miller-Rabin test for prime
    if n == 0 or n == 1 or n == 4 or n == 6 or n == 8 or n == 9:
        return False

    if n == 2 or n == 3 or n == 5 or n == 7:
        return True
    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    assert (2 ** s * d == n - 1)

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    for i in range(99):  # number of trials
        a = random.randrange(2, n)
        if trial_composite(a):
            return False

    return True


def generiraj_q_p():
    """Funkcija generira 160-bitno praštevilo q in 1028-bitna praštevilo p, ustrezne oblike."""
    n = 160
    m = 1028
    # Izberemo poljubno 160-bitno praštevilo q
    q = random.randint(2 ** (n - 1), 2 ** n - 1)
    while je_prastevilo(q) == False:
        q = random.randint(2 ** (n - 1), 2 ** n - 1)

    # Generiramo p, ki pa mora biti prave oblike
    p = q * pow(2, m - n) + 1
    # Zagotoviti moramo, da je p res praštevilo, če ne ga popravljamo, dokler ni praštevilo
    while je_prastevilo(p) == False:
        p += q
    return p, q


def generiraj_dsa():
    """Funkcija generira DSA ključ za podpis."""
    p = 2322848386021646554566424091967155293346779147521462400355718388515063730806939828755776692858977242878982853152994612578130874654616666777426243339146706820130937525269629486326092934462392072871986574439725988919606011362153615655079664599858918556639680109034730628685328183936924924994532147505385571640563
    q = 1180278857667110501955963277249236557928848108173
    # Sedaj bomo zgenerirali še preostale dele ključa:
    kvocient = ((p - 1)//q)
    alfa = 1
    # Algoritem na prosojnicah točka (3), (4) in (5)
    while alfa == 1:
        h = random.randint(2, p)
        # h mora biti tuj p
        while gcd(h, p) != 1:
            h = random.randint(2, p)
        alfa = pow(h, kvocient, p)
    a = random.randint(1, q)
    beta = pow(alfa, a, p)

    return p, q, alfa, beta, a


def podpisi(besedilo, kljuc):
    """Funkcija podpiše besedilo z danim ključem, kjer predpostavimo, da je ključ oblike p, q, alfa, beta, a."""
    # Zopet sledimo algoritmu za podpisovanje navedenem na prosojnicah
    p, q, alfa, beta, a = kljuc
    gama = 0
    delta = 0
    while gama == 0 or delta == 0:
        k = random.randint(1, q)
        gama = pow(alfa, k, p) % q
        inverz_k = inverz(k, q)
        h = int(hashlib.sha1(str(besedilo).encode('utf-8')).hexdigest(), 16)
        delta = inverz_k*(h + a*gama) % q
    return gama, delta

#######################################################################################################
# print(kvazi_trk())
# print(generiraj_q_p())
# print(generiraj_dsa())
# print(najdi_pravo('532'))
# print(inverz(543, 17654363))
# print(podpisi('4123535', generiraj_dsa(160, 1028)))
# print(najdi_pravo(8859787, 6925873))

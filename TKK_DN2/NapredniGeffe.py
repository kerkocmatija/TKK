# Dobimo model Geffejevega generatorja s ključi LFSR1, LFSR2 in LFSR3 ter nanj
# izvedemo napad.

import itertools

"""Vsaki črki angleške abecede priredimo število po modulu Z_26."""
slovar_crk = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4,
              'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
              'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14,
              'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
              'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}

"""Vsaki črki angleške abecede priredimo število v dvojiškem zapisu."""
slovar_dvojiskih = {'A': '00000', 'B': '00001', 'C': '00010', 'D': '00011',
                    'E': '00100', 'F': '00101', 'G': '00110', 'H': '00111',
                    'I': '01000', 'J': '01001', 'K': '01010', 'L': '01011',
                    'M': '01100', 'N': '01101', 'O': '01110', 'P': '01111',
                    'Q': '10000', 'R': '10001', 'S': '10010', 'T': '10011',
                    'U': '10100', 'V': '10101', 'W': '10110', 'X': '10111',
                    'Y': '11000', 'Z': '11001'}

slovar_dvojiskih2 = {'00000': 'A', '00001': 'B', '00010': 'C', '00011': 'D',
                     '00100': 'E', '00101': 'F', '00110': 'G', '00111': 'H',
                     '01000': 'I', '01001': 'J', '01010': 'K', '01011': 'L',
                     '01100': 'M', '01101': 'N', '01110': 'O', '01111': 'P',
                     '10000': 'Q', '10001': 'R', '10010': 'S', '10011': 'T',
                     '10100': 'U', '10101': 'V', '10110': 'W', '10111': 'X',
                     '11000': 'Y', '11001': 'Z'}

seznam_najpogostejsih = ['ONYMOUSWITHENCRYPTIONTHECONVERSIO', 'CRYPTOGRAPHYLITERATURE',
                         'THISIS', 'VERSION', 'INFORMATION',]

##################################################################################################################
# Najprej definiramo nekaj pomožnih funkcij:

# KAKO DOLG KRIPTOGRAM IMAMO:
with open('besedilo.txt') as f:
    podatki = f.read()
    dolzina_cripto = len(podatki)


uganjena = seznam_najpogostejsih[0]
dolzina_uganjene = len(uganjena)

# RECIMO sedaj, da ne vemo na katerem mestu je ta beseda.
###################################################################################################################
# FUNKCIJE ZA KODIRANJE V DVOJIŠKI ZAPIS TER ODKODIRANJE IZ DVOJIŠKEGA ZAPISA.
def zakodiraj(besedilo):
    """Funkcija prejme besedilo, ter iz njega konstruira besedilo v dvojiškem zapisu."""
    novo_besedilo = ''
    for i in besedilo:
        novo_besedilo += slovar_dvojiskih[i]
    return novo_besedilo


def odkodiraj(koda):
    """Funkcija prejme besedilo, ter iz njega konstruira besedilo v abecednem zapisu."""
    besedilo = ''
    for i in range(0, len(koda), 5):
        if koda[i:i + 5] not in slovar_dvojiskih2.keys():
            besedilo += 'X'
        else:
            besedilo += slovar_dvojiskih2[koda[i:i + 5]]
    return besedilo


def kombinacije(n):
    """Funkcija generira vse možne nize dolžine n iz 1 in 0."""
    nizi = []
    lst = [list(i) for i in itertools.product(['0', '1'], repeat = n)]
    for k in lst:
        nizi.append(''.join(k))
    return nizi


###################################################################################################################
# FUNKCIJE ZA GENERIRANJE LFSRi ZAPOREDIJ
def nadaljuj_niz_lfsr11(niz):
    """Funkcija dobi niz ter ga rekurzivno nadaljuje v celotni dolžini prestreženega kriptograma."""
    niz = niz[:5]
    for i in range(5, dolzina_cripto):
        niz += str((int(niz[i - 2]) + int(niz[i - 5])) % 2)
    return niz


def nadaljuj_niz_lfsr22(niz):
    """Funkcija dobi niz ter ga rekurzivno nadaljuje v celotni dolžini prestreženega kriptograma."""
    niz = niz[:7]
    for i in range(7, dolzina_cripto):
        niz += str((int(niz[i - 7]) + int(niz[i - 1])) % 2)
    return niz


def nadaljuj_niz_lfsr33(niz):
    """Funkcija dobi niz ter ga rekurzivno nadaljuje v celotni dolžini prestreženega kriptograma."""
    niz = niz[:11]
    for i in range(11, dolzina_cripto):
        niz += str((int(niz[i - 2]) + int(niz[i - 11])) % 2)
    return niz


################################################################################################################
# FUNKCIJE ZA OPERACIJE Z NIZI:
def primerjaj_niza(niz1, niz2):
    """Primerjamo v koliko znakih se ujemata niza (predpostavimo, da sta niza iste dolžine)."""
    indeks = 0
    for i in range(len(niz1)):
        if niz1[i] == niz2[i]:
            indeks += 1
    return indeks / len(niz1)


def zmnozi_niza(niz1, niz2):
    """Funkcija prejme dva niza ter zmnoži po komponentah modulo 2 (predpostavimo, da sta niza iste dolžine)."""
    novi = ''
    for i in range(len(niz1)):
        novi += str((int(niz1[i]) * int(niz2[i])) % 2)
    return novi


def sestej_niza(niz1, niz2):
    """Funkcija prejme dva niza, ter ju sešteje po komponentah modulo 2 (predpostavimo, da sta niza iste dolžine)."""
    novi = ''
    for i in range(len(niz1)):
        novi += str((int(niz1[i]) + int(niz2[i])) % 2)
    return novi


##################################################################################################################

# FUNKCIJE ZA ODŠIFRIRANJE:
def odsifriraj_besedilo():
    """Funkcija odšifrira besedilo s pomočjo dane besede, ter vrne vsaj prvi del ključa."""
    """Dana beseda je lahko na kateremkoli mestu v besedilu."""
    c = zakodiraj(uganjena)
    k = len(c)
    seznam_izhodov = []
    for j in range(0, len(podatki) - k, 5):
        izbrani_podatki = podatki[j:j+k]
        seznam_izhodov.append((sestej_niza(izbrani_podatki, c), j))
    return seznam_izhodov  # Tukaj imamo sedaj seznam vseh možnih z-jev.


# Generiramo vse možne začetne sezname.
# Čeprav je to precej zamudno, nam jih ni treba generirati na vsakem koraku
sez1 = kombinacije(5)
for l in range(0, len(sez1)):
    sez1[l] = nadaljuj_niz_lfsr11(sez1[l])

sez2 = kombinacije(7)
for l in range(0, len(sez2)):
    sez2[l] = nadaljuj_niz_lfsr22(sez2[l])

sez3 = kombinacije(11)
for l in range(0, len(sez3)):
    sez3[l] = nadaljuj_niz_lfsr33(sez3[l])

def primerjaj_izhode_lfsr1():
    """Funkcija primerja uganjeno besedilo, z možnimi izhodi registra LFSR1."""
    # Iščemo začetno zaporedje generatorja LFSR1:
    seznam_dobrih1 = []
    c = zakodiraj(uganjena)
    m = len(c)
    for (z, j) in odsifriraj_besedilo():
        for k in sez1:
            xi = k[j:j+m]  # Vzamemo i-tega.
            if 0.72 <= primerjaj_niza(xi, z) <= 0.8:
                seznam_dobrih1.append((xi, primerjaj_niza(xi, z), sez1.index(k)))
    if seznam_dobrih1 == []:
        raise ValueError('Ni dovolj dobrega ujemanja. Poskusi povečati interval ujemanja.')
        return seznam_dobrih1
    else:
        return seznam_dobrih1


def primerjaj_izhode_lfsr3():
    """Funkcija primerja uganjeno besedilo, z možnimi izhodi registra LFSR3."""
    # Iščemo začetno zaporedje generatorja LFSR3:
    seznam_dobrih3 = []
    c = zakodiraj(uganjena)
    m = len(c)
    for (z, j) in odsifriraj_besedilo():
        for k in sez3:  # Pregledamo vsakega izemed začetnih generiranih seznamov.
            xi = k[j:j+m]  # Vzamemo i-tega.
            if 0.72 <= primerjaj_niza(xi, z) <= 0.8:
                seznam_dobrih3.append((xi, primerjaj_niza(xi, z), sez3.index(k)))
    if seznam_dobrih3 == []:
        raise ValueError('Ni dovolj dobrega ujemanja. Poskusi povečati interval ujemanja.')
        return seznam_dobrih3
    else:
        return seznam_dobrih3


def generator_kljuca():
    """Funkcija poišče še najboljši drugi ključ, ter vrne odšifrirano besedilo."""
    """OPOMBA: Funkcija res naredi tri zanke for, vendar sta dve zanki le po seznamih možnih ključev
    za LFSR1 ter LFSR2. Brute force je tukaj v resnici le po zaporedjih za ključ LFSR2!"""
    for (s1, l1, k1) in primerjaj_izhode_lfsr1():
        for (s3, l3, k3) in primerjaj_izhode_lfsr3():
            a = sez1[k1]
            c = sez3[k3]
            for mozna in sez2:
                b = mozna
                z = sestej_niza(sestej_niza(zmnozi_niza(a, b), zmnozi_niza(b, c)), c)
                besedilo = sestej_niza(z, podatki)
                odkodirano = odkodiraj(besedilo)
                if uganjena in odkodirano:
                    return odkodirano
                else:
                    pass

##################################################################################################################
print(generator_kljuca())






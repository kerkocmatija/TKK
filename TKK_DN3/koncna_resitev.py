# Končno rešitev generiramo posebej, saj želimo, da rešitev prejme vedno ista praštevila ter trke.
import hashlib
import random
from kvazi_trki import generiraj_dsa
from kvazi_trki import podpisi


identiteta = '27131072'

trk1 = 70347229

trk2 = 42888415

q = 1180278857667110501955963277249236557928848108173

p = 2322848386021646554566424091967155293346779147521462400355718388515063730806939828755776692858977242878982853152994612578130874654616666777426243339146706820130937525269629486326092934462392072871986574439725988919606011362153615655079664599858918556639680109034730628685328183936924924994532147505385571640563

kljuc = 2322848386021646554566424091967155293346779147521462400355718388515063730806939828755776692858977242878982853152994612578130874654616666777426243339146706820130937525269629486326092934462392072871986574439725988919606011362153615655079664599858918556639680109034730628685328183936924924994532147505385571640563, 1180278857667110501955963277249236557928848108173, 1148598244285723498501773743210875311612707146925143606903453253341394767908999710292214093272033047757683779250584679868357966004662136991316825558610470758089670813288369532585877841179220329464174172036556038386922035273830813729501087132200437401125887221319175401115015215173257881971718885854516534942388, 285039722748230581050142136754508765462547492548798003765536324098289600957413317942923416290035840599006542334454225666538160913294550162008901221895889524125271833878377354069966251735550145796027830268828652836428573291517651766349380467473798396237709967241659074982144610158779464687432933502566875024301, 316082833156534809896300746077621273501408742876


# PODPISOVANJE REŠITVE:
def inverz(a, q):
    """Funkcija izračuna inverz a po modulu m."""
    """Ker vemo, da bomo računali inverz v Z_q za q je praštevilo, se ne ukvarjamo z obstojem inverza."""
    # Ideja je pobrana iz stackoverflow-a, ideja je dobra, ker je inverz izračunan HITRO!
    return pow(a, q - 2, q)


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


# GENERIRANJE KONČNE REŠITVE:
# SPREMINJAJE 4. VRSTICE:
def najdi_pravo():
    """Funkcija dobi dva trka in s spreminjanjem četrte vrstice doseže pravo obliko hash-a."""
    trka_zdruzena = str(trk1) + ' ' + str(trk2)
    hash_trka = int(hashlib.sha1(str(trka_zdruzena).encode('utf-8')).hexdigest(), 16)

    print("q: %s" % q)
    print("p: %s,\nq: %s,\nalfa: %s,\nbeta: %s,\na: %s" % kljuc)

    prva_vrstica = str(trk1) + ' ' + str(trk2) + ' ' + str(hash_trka)
    gama, delta = podpisi(hash_trka, kljuc)
    print("Gama: %s" % gama)
    print("Delta: %s" % delta)
    print("Hash: %s" % hash_trka)

    druga_vrstica = identiteta + ' ' + str(gama) + ' ' + str(delta)

    tretja_vrstica = '000000076330d2c1cb7f1a511c22716ee78bacc3'

    cetrta_vrstica = 0

    blok = '\n'.join([prva_vrstica, druga_vrstica, tretja_vrstica, str(cetrta_vrstica)])
    hash1 = hashlib.sha1(str(blok).encode('utf-8')).hexdigest()
    while hash1[:7] != '0000000':
        # print(cetrta_vrstica, hash1)
        blok = '\n'.join([prva_vrstica, druga_vrstica, tretja_vrstica, str(cetrta_vrstica)])
        hash1 = hashlib.sha1(str(blok).encode('utf-8')).hexdigest()
        cetrta_vrstica += 1
    return cetrta_vrstica, hash1


#######################################################################################################
print(najdi_pravo())
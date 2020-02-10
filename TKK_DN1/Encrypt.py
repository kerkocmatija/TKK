import math
import pprint
import operator

slovar = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4,
          "F": 5, "G": 6, "H": 7, "I": 8, "J": 9,
          "K": 10, "L": 11, "M": 12, "N": 13, "O": 14,
          "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19,
          "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25}

slovar_delezev = {"A": 0.08167, "B": 0.01492, "C": 0.02782, "D": 0.04253, "E": 0.12702,
                  "F": 0.02228, "G": 0.02015, "H": 0.06094, "I": 0.06966, "J": 0.00153,
                  "K": 0.00772, "L": 0.04025, "M": 0.02406, "N": 0.06749, "O": 0.07507,
                  "P": 0.01929, "Q": 0.00095, "R": 0.05987, "S": 0.06327, "T": 0.0987,
                  "U": 0.02758, "V": 0.00978, "W": 0.02360, "X": 0.00150, "Y": 0.01974, "Z": 0.00074}


def Encrypt(besedilo, kljuc):
    """Funkcija prejme besedilo ter ga zašifrira z Viginerjevo šifro."""
    k = len(kljuc)
    l = len(besedilo)
    cripted = ""

    for i in range(0, l):
        nova = (slovar[kljuc[i % k]] + slovar[besedilo[i]]) % 26
        cripted = "{0}{1}".format(cripted, Dobi_kljuc(slovar, nova))
    return cripted


def Dobi_kljuc(slovar, a):
    """Funkcija dobi slovar ter vrednost ter vrne njen ključ."""
    for k, v in slovar.items():
        if v == a:
            return k


def dobi_max(slovar):
    return max(slovar.items(), key=operator.itemgetter(1))[0]


def Decrypt(c, kljuc):
    """Funkcija dobi besedilo c zašifrirano z Vigenerjevo šifro ter ključ in odšifrira c."""
    k = len(kljuc)
    l = len(c)
    besedilo = ""

    for i in range(0, l):
        nova = (slovar[c[i]] - slovar[kljuc[i % k]]) % 26
        besedilo = "{0}{1}".format(besedilo, Dobi_kljuc(slovar, nova))

    return besedilo


print(Encrypt("ABCDEFGHI", "CCCCC"))
z = Encrypt("ABCDEFGHI", "CCCCC")
print(Decrypt(z, "CCCCC"))


def Delitelji(n):
    """Funkcija poišče vse delitelje števila n. PAZI! NE VRAČAMO 1 DA SE IZOGNEMO PROBLEMOM NAPREJ."""
    i = 2
    s = []
    while i <= n ** (1 / 2):
        if (n % i == 0):
            s.append(i)
            s.append(n // i)
        i = i + 1
    if s[-1:] == s[-2:]:
        s = s[-1:]
    return s


def dolzina_kljuca(c):
    """Program prejme besedilo c ter ugotovi dolžino ključa s katerim je bilo zašifrirano."""
    # Poglejmo za nize dolžine 3, na kakšen razmak se pojavijo.
    l = len(c)
    slovar = dict()
    slovar_deliteljev = dict()

    for i in range(0, l - 2):
        index = c.find(c[i:i + 3], i + 3)
        if index != -1:
            slovar[c[i:i + 3]] = index - i  # Vzeti moramo še dolžino niza.
    for k, v in slovar.items():
        for j in Delitelji(v):
            if j in range(2, 21):
                if j not in slovar_deliteljev:
                    slovar_deliteljev[j] = 1
                if j in slovar_deliteljev:
                    slovar_deliteljev[j] += 1
    pprint.pprint(slovar_deliteljev)

    kandidati = [k for k, v in slovar_deliteljev.items() if v == max(slovar_deliteljev.values())]
    kandidati.append(kandidati[0] * 2)
    kandidati.append(kandidati[0] * 4)
    # Vzamemo čimdaljši ključ, tudi, če ni najbolj pogost.
    if slovar_deliteljev[kandidati[0]] - slovar_deliteljev[kandidati[1]] > 8:
        return kandidati[0]
    else:
        return kandidati[1]


def najmanjsi(slovar1, slovar2):
    vsota = 0
    for k in slovar1:
        vsota += (slovar1[k] - slovar2[k]) ** 2
    return vsota


# Funkcija bo bo poiskala najboljše ujemanje z črkami angleške abecede.

def ujemanje(c):
    slovar1 = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0,
               "F": 0, "G": 0, "H": 0, "I": 0, "J": 0,
               "K": 0, "L": 0, "M": 0, "N": 0, "O": 0,
               "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0,
               "U": 0, "V": 0, "W": 0, "X": 0, "Y": 0, "Z": 0}
    l = len(c)
    k = dolzina_kljuca(c)
    k_te_crke = c[::k]
    seznam = []
    s = []
    kandidat = ""
    for k, v in slovar.items():
        novo_besedilo = Decrypt(k_te_crke, k)
        for j in novo_besedilo:
            slovar1[j] += 1
        for key in slovar1:
            n = len(novo_besedilo)
            slovar1[key] = (slovar1[key] / n)  # Naredimo frekvence črk.
        seznam.append(najmanjsi(slovar_delezev, slovar1))
    najboljsi = seznam.index(min(seznam))
    crka = Dobi_kljuc(slovar, najboljsi)

    # max1 = dobi_max(slovar1)
    # kandidat = Dobi_kljuc(slovar, (slovar[max1] - 4)%26)
    return crka


def razbij(c):
    k = dolzina_kljuca(c)
    kljuc = ""
    for i in range(0, k):
        kljuc = kljuc + ujemanje(c[i:])
    return kljuc


cripto = "RIKVBIYBITHUSEVAZMMLTKASRNHPNPZICSWDSVMBIYFQEZUBZPBRGYNTBUR" \
         + "MBECZQKBMBPAWIXSOFNUZECNRAZFPHIYBQEOCTTIOXKUNOHMRGCNDDXZWIR" \
         + "DVDRZYAYYICPUYDHCKXQIECIEWUICJNNACSAZZZGACZHMRGXFTILFNNTSDA" \
         + "FGYWLNICFISEAMRMORPGMJLUSTAAKBFLTIBYXGAVDVXPCTSVVRLJENOWWFI" \
         + "NZOWEHOSRMQDGYSDOPVXXGPJNRVILZNAREDUYBTVLIDLMSXKYEYVAKAYBPV" \
         + "TDHMTMGITDZRTIOVWQIECEYBNEDPZWKUNDOZRBAHEGQBXURFGMUECNPAIIY" \
         + "URLRIPTFOYBISEOEDZINAISPBTZMNECRIJUFUCMMUUSANMMVICNRHQJMNHP" \
         + "NCEPUSQDMIVYTSZTRGXSPZUVWNORGQJMYNLILUKCPHDBYLNELPHVKYAYYBY" \
         + "XLERMMPBMHHCQKBMHDKMTDMSSJEVWOPNGCJMYRPYQELCDPOPVPBIEZALKZW" \
         + "TOPRYFARATPBHGLWWMXNHPHXVKBAANAVMNLPHMEMMSZHMTXHTFMQVLILOVV" \
         + "ULNIWGVFUCGRZZKAUNADVYXUDDJVKAYUYOWLVBEOZFGTHHSPJNKAYICWITDARZPVU"

cripto2 = "AKBPAKBPPSKFGKUCZWJSQKBSADSFCFLVCHVCIUVHGCAIOVCTBSL" \
          "OZCHVSGHVKHVSGDSBHKZZVWGACBSPWBCFQSFHCCMHKWBHVSAVWGCBZP" \
          "KAMWHWCBLKGHCMSKZLKPGLSZZQFSGGSQVSQWQBCHOKFSTCFVWGGCZ" \
          "QWSFGKBQHVSHVSKHFSQWQBCHKAIGSVWAHVSCBZPHVWBUWBTKOHVSHV" \
          "CIUVHKBPHVWBUCTLKGHCQFWJSCIHKBQGVCLKBSLGIWHCTOZCHVSGVSV" \
          "KQKOCKHTCFSJSFPVCIFCTHVSQKPKBQKGCBSLCIZQGKPCTKYWBUVSW" \
          "GWBVWGOKMWBSHGCCBSOCIZQGKPCTVWAHVSSADSFCFWGWBVWGQFSGGWBUFCCA"

cripto3 = "MVZJFVCKNJSMYKVYMZBEXEWMNJVCKFKFHKFYOVZJXUTY" \
          "KRBBPZRCTWHCKYSFTUGYVBSBMYSDTDCSLKCUGFTRKFMKTEMA" \
          "BKWCLUWBAVJGLZHYGUAYGPKCKVHFXEORBFBQPZHFPYCQXDOLGVF" \
          "QTERANJHMFJVCPRGYVHIYBEHCWDCPXFJCKYSQNWTCKVRKNTVZRJ" \
          "SYPYWJXKFWBEURHJOTXYWQHNBJBWSYGUPPBEUFBJACGJODXCMFH" \
          "DSZNKRMPYORAVAGZYHFXTCSEUBMMJOTXYWQFVBDHIHFXPDCKZGF" \
          "XUHFKFIEAKVCBICUGJVCXITMECMGGVORBEURAVQYMKZCHWHFXJIL" \
          "ZFRFRGSPBFBQHKVCZFRNKVJCGKSBMYSKYICKXMSPKVOAAZBEAFAC" \
          "MVZJFVHMHRPMNKOJEKVCLVHFBEUQHUOSZYHCKFTHHMSDKFAUARH" \
          "QHVJCKJCSKTSWHLAYRBBMPKVCFJCLHNOJENVMXJQYIVRBXRHFBEPY" \
          "MKZCHIPWLYWNPISADYOBZFHQTWSJRYCKXVLAXGHSEPGQXJOLWYSR" \
          "AFIEAYSUTJZMGXWLZKCPXKIPGKCFBJKGYVOLWTCSGKFWPRGBXKOG" \
          "GVRZRKVCZFRBXJGATCMNLFKFHYOBZFHFBDWLMFOJTIUCVRJCTERUTE" \
          "HCWKCKTIFWAZAZNKOQRVOPLNSLMSMRAVFCVRACTKWKXNVCGKVC" \
          "ZFRQLVHREVRRARHFXJVMNCREHSOADKCGMYOATVJCGKVCGYCUXMS" \
          "PPYSLAVKYLRAMGXVGLFKLIVCNEVVGLKFMNSZCLNSPXECRRVHMOVF" \
          "LXMSPMYSJXJGYECHFXXCBLYOBGFKZXXILMFDGMPVGFVLAXGHLXGHS" \
          "GVKFHJHGECDCKJSANKSBAZAUBKVMNKQCTJWLZRBBPFIJWECREVHFB" \
          "DUCMYCKX"

# print(dolzina_kljuca(cripto))
# print(ujemanje(cripto))
# print(razbij(cripto))
print(Decrypt(cripto, razbij(cripto)))
print(Decrypt(cripto3, razbij(cripto3)))

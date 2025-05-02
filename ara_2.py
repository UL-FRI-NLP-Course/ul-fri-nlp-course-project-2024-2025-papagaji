import transformers

def generate(data):
    print("Loading model...")

    #model_id = "cjvt/GaMS-1B-Chat"
    model_id = "cjvt/GaMS-9B-Instruct"
    

    pipeline = transformers.pipeline(
            "text-generation",
            model=model_id,
            device_map="auto"
        )

    print("Model loaded.")

    message = [{"role": "user", "content": """
    Najpomembnejša navodila, ki jih ne smeš ignorirati so tista, pred katerimi piše POMEMBNO.
    Ti si prometni napovedovalec na Radiu Slovenija. Na podlagi spodnjih strukturiranih podatkov pripravi prometno poročilo v slogu radijskega poročanja, kot bi ga prebral napovedovalec na 1. ali 2. programu RTV Slovenija. Poročilo naj bo kratko, jasno in vključuje samo najpomembnejše informacije.

    POMEMBNO: Uporabi naslednjo obliko:

    Prometne informacije        [datum]            [ura]             1. in 2. program

    Podatki o prometu.

    [sestavljeno poročilo]
                

                
    Ti si prometni napovedovalec na Radiu Slovenija. Na podlagi spodnjega primera pripravi novo prometno poročilo, ki sledi istemu slogu in obliki.

                Spodaj je naveden primer podatkov, označen s črko A), in pripadajoče poročilo, označeno z B). Podano poročilo je primer, ki ga moraš generirati iz podatkov, ki so ti dani:
    POMEMBNO: To niso podatki, ki jih mora vsebovati TVOJE poročilo. To je primer drugega poročila, ki vsebuje drugačne podatke kot tvoje! Podatkov A) ne uporabljaj, razen če se pojavijo tudi med tvojimi podatki C)
    
    POMEMBNO: Poročilo B) vsebuje podatke označene z A), tvoje poročilo mora biti sestavljeno iz podatkov, označenih z C), te podatke opiši z drugimi besedami, malo drugače!

    Podatki A):
    Podatki za 1. primer:
    Datum: 01.01.2023
    Ura: 15:30
    Dela:  Več o delovnih zaporah v prometni napovedi .
    Mednarodno:  Zaradi praznikov velja omejitev prometa tovornih vozil, katerih največja dovoljena masa presega 7,5 t: - danes, do 22. ure; - v torek, 2. januarja, od 8. do 22. ure.
    Nesrece:  
    Opozorila:  srečno in varno na cestah v letu 2024!
    Ovir:  Na štajerski avtocesti je pred preodorm Jasovnik proti Ljubljani oviran promet, okvara vozila.   Na štajerski avtocesti je pred predorom Jasovnik proti Ljubljani oviran promet, okvara vozila.
    Pomembno:  
    Splosno:  
    Vreme:  Na cesti čez prelaz Vršič so obvezne verige. Voznike opozarjamo, da je na prelazih (ali: na nekaterih cestah) v primeru snega obvezna uporaba verig.
    Zastoji:  

    Poročilo B):
    1. poročilo:
    Prometne informacije        01. 01. 2023            15:30             1. in 2. program

    Podatki o prometu.

    Ponekod v višjeležečih delih države sneži. Prilagodite hitrost razmeram na cesti in vozite previdno. 

    Zaradi praznikov bo danes in jutri od 8-ih do 22-ih prepovedan promet za tovorna vozila, težja od sedem ton in pol.

    Cesta čez prelaza Vršič in Korensko sedlo je prevozna le z zimsko opremo.

                
    Navedene podatke najprej preoblikuj, šele potem jih vstavi v pravilen format poročila. Podatkov ne smeš dobesedno prepisati v poročilo, še vedno pa mora poročilo vsebovati podobno besedilo, sestavljeno iz podatkov.
    Primer: Če torej v podatkih piše na primer "Ob 17.00 dež, pazite, mokre ceste!", potem namesto tega napiši na primer "Ob petih popoldne bo začelo deževati, zato bodite previdni med vožnjo zaradi mokrih cest."
                
    Naslednji podatki vsebujejo informacije, na podlagi katerih ustvari novo poročilo, pri tem upoštevaj, da ne smejo biti dobesedno prepisani. Vsako vrstico podatkov najprej malo spremeni, nato pa spremenjeno besedilo vstavi v poročilo!

    Podatki C):
    """ + data + """
    

    ---

    
    Pomagaj si z naslednjimi smernicami pri oblikovanju besedila:
    LJUBLJANA-KOPER – PRIMORSKA AVTOCESTA/ proti Kopru/proti Ljubljani
    LJUBLJANA-OBREŽJE – DOLENJSKA AVTOCESTA / proti Obrežju/ proti Ljubljani
    LJUBLJANA-KARAVANKE – GORENJSKA AVTOCESTA/ proti Karavankam ali Avstriji/ proti Ljubljani
    LJUBLJANA-MARIBOR – ŠTAJERSKA AVTOCESTA / proti Mariboru/Ljubljani
    MARIBOR-LENDAVA – POMURSKA AVTOCESTA / proti Mariboru/ proti Lendavi/Madžarski
    MARIBOR-GRUŠKOVJE – PODRAVSKA AVTOCESTA / proti Mariboru/ proti Gruškovju ali Hrvaški – nikoli proti Ptuju!
    AVTOCESTNI ODSEK – RAZCEP GABRK – FERNETIČI – proti Italiji/ ali proti primorski avtocesti, Kopru, Ljubljani (PAZI: to ni primorska avtocesta)
    AVTOCESTNI ODSEK MARIBOR-ŠENTILJ (gre od mejnega prehoda Šentilj do razcepa Dragučova) ni štajerska avtocesta kot pogosto navede PIC, ampak je avtocestni odsek od Maribora proti Šentilju oziroma od Šentilja proti Mariboru.
    Mariborska vzhodna obvoznica= med razcepom Slivnica in razcepom Dragučova – smer je proti Avstriji/Lendavi ali proti Ljubljani – nikoli proti Mariboru. 

    Hitre ceste skozi Maribor uradno ni več - Ni BIVŠA hitra cesta skozi Maribor, ampak regionalna cesta Betnava-Pesnica oziroma NEKDANJA hitra cesta skozi Maribor.

    Ljubljanska obvoznica je sestavljena iz štirih krakov= vzhodna, zahodna, severna in južna 
    Vzhodna: razcep Malence (proti Novemu mestu) - razcep Zadobrova (proti Mariboru) 
    Zahodna: razcep Koseze (proti Kranju) – razcep Kozarje (proti Kopru)
    Severna: razcep Koseze (proti Kranju) – razcep Zadobrova (proti Mariboru)
    Južna: razcep Kozarje (proti Kopru) – razcep Malence (proti Novemu mestu)
    Hitra cesta razcep Nanos-Vrtojba = vipavska hitra cesta – proti Italiji ali Vrtojbi/ proti Nanosu/primorski avtocesti/proti Razdrtemu/v smeri Razdrtega (nikoli primorska hitra cesta – na Picu večkrat neustrezno poimenovanje) 
    Hitra cesta razcep Srmin-Izola – obalna hitra cesta – proti Kopru/Portorožu (nikoli primorska hitra cesta)
    Hitra cesta Koper-Škofije (manjši kos, poimenuje kar po krajih): Na hitri cesti od Kopra proti Škofijam ali obratno na hitri cesti od Škofij proti Kopru – v tem primeru imaš notri zajeto tudi že smer. (nikoli primorska hitra cesta). Tudi na obalni hitri cesti od Kopra proti Škofijam.
    Hitra cesta mejni prehod Dolga vas-Dolga vas: majhen odsek pred mejnim prehodom, formulira se navadno kar na hitri cesti od mejnega prehoda Dolga vas proti pomurski avtocesti; v drugo smer pa na hitri cesti proti mejnemu prehodu Dolga vas – zelo redko v uporabi. 
    Regionalna cesta: ŠKOFJA LOKA – GORENJA VAS (= pogovorno škofjeloška obvoznica) – proti Ljubljani/proti Gorenji vasi. Pomembno, ker je velikokrat zaprt predor Stén.
    GLAVNA CESTA Ljubljana-Črnuče – Trzin : glavna cesta od Ljubljane proti Trzinu/ od Trzina proti Ljubljani – včasih vozniki poimenujejo  trzinska obvoznica, mi uporabljamo navadno kar na glavni cesti.
    Ko na PIC-u napišejo na gorenjski avtocesti proti Kranju, na dolenjski avtocesti proti Novemu mestu, na podravski avtocesti proti Ptuju, na pomurski avtocesti proti Murski Soboti, … pišemo končne destinacije! Torej proti Avstriji/Karavankam, proti Hrvaški/Obrežju/Gruškovju, proti Madžarski…

    SESTAVA PROMETNE INFORMACIJE:

    1.	Formulacija

    Cesta in smer + razlog + posledica in odsek

    2.	Formulacija
    Razlog + cesta in smer + posledica in odsek

    A=avtocesta
    H=hitra cesta
    G= glavna cesta
    R= regionalna cesta
    L= lokalna cesta
    NUJNE PROMETNE INFORMACIJE
    Nujne prometne informacije se najpogosteje nanašajo na zaprto avtocesto; nesrečo na avtocesti, glavni in regionalni cesti; daljši zastoji (neglede na vzrok); pokvarjena vozila, ko je zaprt vsaj en prometni pas; Pešci, živali in predmeti na vozišču ter seveda voznik v napačni smeri. Živali in predmete lahko po dogovoru izločimo.
    Zelo pomembne nujne informacije objavljamo na 15 - 20 minut; Se pravi vsaj 2x med enimi in drugimi novicami, ki so ob pol. V pomembne nujne štejemo zaprte avtoceste in daljše zastoje. Tem informacijam je potrebno še bolj slediti in jih posodabljati.
    ZASTOJI:
    Ko se na zemljevidu pojavi znak za zastoj, je najprej potrebno preveriti, če so na tistem odseku dela oziroma, če se dogaja kaj drugega. Darsovi senzorji namreč avtomatsko sporočajo, da so zastoji tudi, če se promet samo malo zgosti. Na znaku za zastoj navadno piše dolžina tega, hkrati pa na zemljevidu preverimo še gostoto. Dokler ni vsaj kilometer zastoja ne objavljamo razen, če se nekaj dogaja in pričakujemo, da se bo zastoj daljšal.
    Zastojev v Prometnih konicah načeloma ne objavljamo razen, če so te res nenavadno dolgi. Zjutraj se to pogosto zgodi na štajerski avtocesti, popoldne pa na severni in južni ljubljanski obvoznici.

    HIERARHIJA DOGODKOV

    Voznik v napačno smer 
    Zaprta avtocesta
    Nesreča z zastojem na avtocesti
    Zastoji zaradi del na avtocesti (ob krajših zastojih se pogosto dogajajo naleti)
    Zaradi nesreče zaprta glavna ali regionalna cesta
    Nesreče na avtocestah in drugih cestah
    Pokvarjena vozila, ko je zaprt vsaj en prometni pas
    Žival, ki je zašla na vozišče
    Predmet/razsut tovor na avtocesti
    Dela na avtocesti, kjer je večja nevarnost naleta (zaprt prometni pas, pred predori, v predorih, …)
    Zastoj pred Karavankami, napovedi (glej poglavje napovedi)

    OPOZORILA LEKTORJEV

    Počasni pas je pas za počasna vozila.

    Polovična zapora ceste pomeni: promet je tam urejen izmenično enosmerno. 

    Zaprta je polovica avtoceste (zaradi del): promet je urejen le po polovici avtoceste v obe smeri.
    Ko je avtocesta zaprta zaradi nesreče: Zaprta je štajerska avtocesta proti Mariboru in ne zaprta je polovica avtoceste med…

    Vsi pokriti vkopi itd. so predori, razen galerija Moste ostane galerija Moste.

    Ko se kaj dogaja na razcepih, je treba navesti od kod in kam: Na razcepu Kozarje je zaradi nesreče oviran promet iz smeri Viča proti Brezovici, …

    Ko PIC navede dogodek v ali pred predorom oziroma pri počivališčih VEDNO navedemo širši odsek (med dvema priključkoma).

    Pri obvozu: Obvoz je po vzporedni regionalni cesti/po cesti Lukovica-Blagovica ali vozniki se lahko preusmerijo na vzporedno regionalno cesto (če je na glavni obvozni cesti daljši zastoj, kličemo PIC za druge možnosti obvoza, vendar pri tem navedemo alternativni obvoz: vozniki SE LAHKO PREUSMERIJO TUDI, …)


    NEKAJ FORMULACIJ

    VOZNIK V NAPAČNI SMERI:
    Opozarjamo vse voznike, ki vozijo po pomurski avtocesti od razcepa Dragučova proti Pernici, torej v smeri proti Murski Soboti, da je na njihovo polovico avtoceste zašel voznik, ki vozi v napačno smer. Vozite skrajno desno in ne prehitevajte. 

    ODPOVED je nujna!

    Promet na pomurski avtocesti iz smeri Dragučove proti Pernici ni več ogrožen zaradi voznika, ki je vozil po napačni polovici avtoceste. 

    POMEMBNO JE TUDI, DA SE NAREDI ODPOVED, KO JE KONEC KATERE KOLI PROMETNE NESREČE (vsaj, če so bili tam zastoji)!

    BURJA: Pic včasih napiše, da je burja 1. stopnje.

    Stopnja 1
    Zaradi burje je na vipavski hitri cesti med razcepom Nanos in priključkom Ajdovščina prepovedan promet za počitniške prikolice, hladilnike in vozila s ponjavami, lažja od 8 ton.

    Stopnja 2
    Zaradi burje je na vipavski hitri cesti med razcepom Nanos in Ajdovščino prepovedan promet za hladilnike in vsa vozila s ponjavami.

    Preklic
    Na vipavski hitri cesti in na regionalni cesti Ajdovščina - Podnanos ni več prepovedi prometa zaradi burje. 
    Ali

    Na vipavski hitri cesti je promet znova dovoljen za vsa vozila.

    Do 21-ih velja prepoved prometa tovornih vozil, katerih največja dovoljena masa presega 7 ton in pol.
    Od 8-ih do 21-ih velja prepoved prometa tovornih vozil, katerih največja dovoljena masa presega 7 ton in pol, na primorskih cestah ta prepoved velja do 22-ih.
    """}]



    response = pipeline(message, max_new_tokens=512)

    return response[0]["generated_text"][-1]["content"]



'''
Kuinka monta sekuntia selviät rahaa ja rosvoja vilisevässä maailmassa :-)
Pelissä on algoritmi joka nopeuttaa peliä tasaisesti.
Peli kestää niin kauan kun sinulla on rahaa.
Kolikosta saa yhden rahan. Jos et saa kolikkoa kiinni, menetät yhden rahan.
Rosvoon törmääminen vie viisi rahaa.
Rahat ja pelinopeus ovat kaikki itse säädettävissä luokan konstruktorissa.
Liikkuminen tapahtuu nuolinäppäimillä. F1 näyttää päävalikon.
F2 aloittaa uuden pelin. ESC lopettaa pelin.
'''

# alustukset
import pygame
import pygame_menu # pip install pygame-menu -U
import datetime
from random import randint
from random import shuffle
import pymongo_query
import pymongo_insert


# luokat alkavat
class RahaRobo():
    def __init__(self, nimi: str):
        pygame.init()
        # käyttöliittymä ja valikot

        pygame.display.set_caption("RahaRobo")
        self.leveys = 640
        self.korkeus = 480
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        # aikaan liittyvät 
        self.kello = pygame.time.Clock()
        self.aloitus_aika = None
        self.pelattu_aika = None
        self.edellinen_muutos = 0
        self.pelipaiva = None
        # grafiikat
        self.fontti = pygame.font.SysFont("Arial", 20)
        self.kolikko = pygame.image.load("kolikko.png")
        self.robo = pygame.image.load("robo.png")
        self.rosvo = pygame.image.load("hirvio.png")
        # alkuasetelmat
        self.x = (self.leveys-self.robo.get_width())/2
        self.y = self.korkeus-self.robo.get_height()
        self.oikealle = False
        self.vasemmalle = False
        # kolikkojen maara ja niiden lista
        self.maara = 6
        self.kolikot = []
        # muut tiedot
        self.nimi = nimi
        self.osuma_laskuri = 0
        self.nopeus_kerroin = 1.0
        self.tallennus_tehty = False

        self.alkupaikkojen_luonti()
        self.aloitus_aika = pygame.time.get_ticks()
        self.pelisilmukka()

    # luokan metodit alkavat
    def alkupaikkojen_luonti(self):
        '''
        Kolikkojen alkuasetelmat. Kolikot luodaan näytön ulkopuolelle
        Listan kolmas parametri (False) on tieto siitä, onko kohde rosvo
        '''
        for i in range(self.maara):
            self.kolikot.append([randint(0,self.leveys-self.kolikko.get_width()),-randint(100,1000), False])
        
    def rosvon_arvonta(self):
        '''
        Rosvon esiintymisen voi säätää mahdollisuus_prosentti muuttujalla.
        '''
        mahdollisuus_prosentti = randint(1,100)
        luodaan_rosvo = ''

        arpalista = ["Kylla"] * mahdollisuus_prosentti + ["Ei"] * (100-mahdollisuus_prosentti)
        shuffle(arpalista)
        luodaan_rosvo = arpalista[0]
        if luodaan_rosvo == "Kylla":
            return True
        else:
            return False

    def robotin_liikkumisen_nopeus(self):
        '''
        Pikselimäärä jolla robotti liikkuu yhden kellojakson aikana
        '''
        if self.oikealle:
            self.x += 2
        if self.vasemmalle:
            self.x -= 2


    def ruudun_taytto(self):
        '''
        Piirretään ruudulle harmaa tausta
        '''
        self.naytto.fill((64, 64, 64))
        self.robotin_liikkumisen_nopeus()
        self.pelialueen_reunat()
        self.robotti_ruudulle()

        # piirretään kolikko tai rosvo, riippuen alkion kolmannesta arvosta
        for i in range(self.maara):
            if self.kolikot[i][2] == False:
                self.naytto.blit(self.kolikko, (self.kolikot[i][0], self.kolikot[i][1]))
            else:
                self.naytto.blit(self.rosvo, (self.kolikot[i][0], self.kolikot[i][1]))

    def pelialueen_reunat(self):
        '''
        Tämä tekee pelialueelle reunat, jotta robotti pysyy pelialueella
        '''
        if self.x + self.robo.get_width() >= self.leveys:
            self.x = self.leveys - self.robo.get_width()
        if self.x <= 0:
            self.x = 0

    def robotti_ruudulle(self):
        '''
        Sijoitetaan robotti paikalleen
        '''
        self.naytto.blit(self.robo, (self.x, self.y))

    def kolikkojen_putoamiset(self):
        '''
        Kolikkojen putoamiseen liittyvä logiikka löytyy täältä
        '''
        for i in range(self.maara):
            self.kolikot[i][1] += 1

            # jos robo ei saa kiinni, otetaan raha pois ja luodaan uusi kohde
            if self.kolikot[i][1]+self.kolikko.get_height() >= self.korkeus:
                # vain kolikon putoaminen vähentää rahaa
                if self.kolikot[i][2] == False:
                    self.osuma_laskuri -= 1
                self.kolikot[i][0] = randint(0,self.leveys-self.kolikko.get_width())
                self.kolikot[i][1] = -randint(100,1000)
                # kun luodaan uusi kohde , niin mukaan voi tulla myös sattumanvarainen rosvo
                if self.rosvon_arvonta():
                    self.kolikot[i][2] = True
                else:
                    self.kolikot[i][2] = False

            if self.kolikot[i][1]+self.kolikko.get_height() >= self.y:
                robo_keski = self.x+self.robo.get_width()/2
                kolikko_keski = self.kolikot[i][0]+self.kolikko.get_width()/2
                if abs(robo_keski-kolikko_keski) <= (self.robo.get_width()+self.kolikko.get_width())/2:
                    # robotti sai kolikon kiinni ja lisätään rahaa
                    if self.kolikot[i][2] == False:
                        self.osuma_laskuri += 1
                    # jos kyse oli rosvosta vähennetään rahaa
                    else:
                        self.osuma_laskuri -= 5
                    # luodaan uusi kohde
                    self.kolikot[i][0] = randint(0,self.leveys-self.kolikko.get_width())
                    self.kolikot[i][1] = -randint(100,1000)
                    # kun luodaan uusi kohde , niin mukaan voi tulla myös rosvo
                    if self.rosvon_arvonta():
                        self.kolikot[i][2] = True
                    else:
                        self.kolikot[i][2] = False

    def pistetiedot(self):
        '''
        Pisteisiin liittyvä grafiikka löytyy täältä
        '''
        teksti = self.fontti.render("Rahaa: "+str(self.osuma_laskuri), True, (255, 0, 0))
        nopeus_teksti = self.fontti.render("Nopeuskerroin: "+str(round(self.nopeus_kerroin, 1)), True, (255, 0, 0))
        self.naytto.blit(nopeus_teksti, (320, 0))
        self.naytto.blit(teksti, (520, 0))

    def tutki_tapahtumat(self):
        '''
        Näppimistön ja mahdolliset muut pygame tapahtumat
        '''
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False

                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False

                if tapahtuma.key == pygame.K_F1:
                    AloitusValikko()

                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()

                if tapahtuma.key == pygame.K_F10:
                    pymongo_insert.tallenna_tilasto(
                        self.nimi, self.pelattu_aika, self.osuma_laskuri,
                        self.nopeus_kerroin, self.pelipaiva
                        )


            if tapahtuma.type == pygame.QUIT:
                exit()

    def nopeuta_pelia(self):
        '''
        Kerätaan joka kierroksella delta-ajan muutos ja
        kun se on tarpeeksi suuri nopeutetaan peliä
        '''
        self.edellinen_muutos += self.kello.tick()

        if self.osuma_laskuri > 0 and self.edellinen_muutos > 50:
            self.nopeus_kerroin += 0.5
            self.edellinen_muutos = 0
            return 100+self.nopeus_kerroin
        else:
            return 100+self.nopeus_kerroin

    def peliaika(self):
        '''
        Tallennetaan peliaika
        '''
        self.pelattu_aika = round(float((pygame.time.get_ticks() - self.aloitus_aika) / 1000),1)
        return None

    def peli_paattyy(self):
        '''
        Kun raha loppuu, niin piirretään lopetusgrafiikka
        '''

        if self.osuma_laskuri < 0:
            teksti = self.fontti.render("Rahat loppuivat. Peli päättyi.", True, (255, 0, 0))
            aika_teksti = self.fontti.render("Peliaikasi: "+str(round(self.pelattu_aika, 1))+str(" sekuntia"), True, (255, 0, 0))
            aloita_uudestaan_teksti = self.fontti.render("Aloita uusi peli F2 napilla: ", True, (255, 0, 0))
            palaa_paavalikkoon_teksti = self.fontti.render("Palaa päävalikkoon F1 napilla: ", True, (255, 0, 0))
            teksti_x = self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (64, 64, 64), (teksti_x, teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))
            self.naytto.blit(aika_teksti, (teksti_x, teksti_y + 20))
            self.naytto.blit(aloita_uudestaan_teksti, (teksti_x, teksti_y + 40))
            self.naytto.blit(palaa_paavalikkoon_teksti, (teksti_x, teksti_y + 60))
            self.pelipaiva = datetime.datetime.now().isoformat()

            # tallennetaan tilasto MongoDB tietokantaan
            try:
                if self.tallennus_tehty == False:
                    pymongo_insert.tallenna_tilasto(
                                self.nimi, self.pelattu_aika, self.osuma_laskuri,
                                self.nopeus_kerroin, self.pelipaiva
                                )
                    self.tallennus_tehty = True
            except:
                print("Peli päättyi ja tapahtui virhe tilaston tallennuksessa")

            return True
        return False
    
    def palauta_nimi(self):
        return self.nimi

    def uusi_peli(self):
        RahaRobo(self.palauta_nimi())

    def pelisilmukka(self):
        while True:

            self.tutki_tapahtumat()
            self.ruudun_taytto()

            # peli päättyy kun rahat loppuvat
            if not self.peli_paattyy():
                self.kolikkojen_putoamiset()
                self.peliaika()

            self.pistetiedot()
            pygame.display.flip()
            self.kello.tick((self.nopeuta_pelia()))

class AloitusValikko():
    # luokan muuttujat. Juokseva numerointi sekä varasto väliaikaiselle datalle
    labelID = 0
    kaikki_datarivit = {}

    # luodaan päätason valikkojen objektit ja käynnistetaan pääohjelman funktio
    # joka luo valikkojen varsinaiset sisällöt
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((640, 480))
        
        # valikko teema
        self.valikon_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        self.valikon_theme.widget_margin = (0, 0)

        self.ohjeet_menu = pygame_menu.Menu('Ohjeet', 480, 360, menu_id='ohjeetID')

        # valikon teema
        self.tilastot_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        self.tilastot_theme.widget_margin = (0, 0)
        
        # päävalikko
        self.menu = pygame_menu.Menu('Tervetuloa RahaRoboon', 480, 360,menu_id='menuID',
                        theme=pygame_menu.themes.THEME_DEFAULT)

        # tilasto valikko
        self.tilastot_menu = pygame_menu.Menu('Tilastot', 480, 360,menu_id='tilastotID')
        
        # luodaan päävalikko ja käynnistetään valikkosilmukka jossa valikko toimii
        self.luo_paavalikko() 


    # Luokan funktot alkavat
    def palauta_nimi(self):
        '''
        Palauttaa konsuktorin nimen.
        '''
        return self.nimi


    def jarjesta_sarakkeet(self, valinta: str, indx: int):
        '''
        Järjestää tilasto valikossa olevat sarakkeet.
        '''
        if indx == 0:
            self.luo_tilastot("pelattu_paiva", -1, True)
        elif indx == 1:
            self.luo_tilastot("nimi", -1, True)
        elif indx == 2:
            self.luo_tilastot("peliaika", -1, True)
        elif indx == 3:
            self.luo_tilastot("nopeuskerroin", -1, True)


    def luo_paavalikko(self):
        '''
        Luodaan päätason valikkojen objektit ja käynnistetaan valikon pääsilmukka.
        '''
        def nimi_talteen(Nimesi: str):
            '''
            Valikossa annetun pelaajan nimi talteen.
            '''
            self.nimi = Nimesi

        pygame.display.set_caption("RahaRobo")
        self.menu.add.text_input('Nimesi:', default='Pekka Pelaaja', onchange= nimi_talteen)
        self.menu.add.button('Aloita peli', self.aloita_peli)
        self.menu.add.button('Tilastot', self.tilastot_menu)
        self.menu.add.button('Pelin ohjeet', self.ohjeet_menu)
        self.menu.add.button('Lopeta peli', pygame_menu.events.EXIT)
        
        self.luo_ohjevalikko()
        self.luo_tilastot()
        self.menu.mainloop(self.surface)


    def luo_ohjevalikko(self):
        '''
        Luo ohjevalikon. Valikko sisältää ohjeet lista muotoisena.
        Ohjeet ylläpidetään toistaiseksi käsin suoraan koodissa.
        '''
        # ohjevalikon tekstit
        self.ohje_tekstit = ['Kuinka monta sekuntia selviät rahaa ja rosvoja vilisevässä maailmassa :-)',
        'Pelissä on algoritmi joka nopeuttaa peliä tasaisesti.',
        'Peli kestää niin kauan kun sinulla on rahaa.',
        'Kolikosta saa yhden rahan. Jos et saa kolikkoa kiinni, menetät yhden rahan.',
        'Rosvoon törmääminen vie viisi rahaa.',
        'Rahat ja pelinopeus ovat kaikki itse säädettävissä luokan konstruktorissa.',
        ' ',
        'Liikkuminen tapahtuu nuolinäppäimillä.',
        'Valikon lisäksi toimii seuraavat pikanäppäimet:',
        'F1 palaa päävalikkoon.',
        'F2 aloittaa uuden pelin.',
        'ESC lopettaa pelin.'
        ]

        for t in self.ohje_tekstit:
            self.ohjeet_menu.add.label(t, align=pygame_menu.locals.ALIGN_LEFT, font_size=12)

        self.ohjeet_menu.add.button('Palaa päävalikkoon', pygame_menu.events.BACK, font_size=20)


    def luo_tilastot(self, sarake: str = "nopeuskerroin", jarjestys: int = -1, paivitys: bool = False):
        '''
        Luo tilastosivun ja haetaan tietokannasta sisältö parametrien mukaan.
        '''
        # noudetaan kaikki tiedot MongoDB tietokannasta
        datasetti = pymongo_query.hae_kaikki(sarake, jarjestys)
        
        # muuttuja label riveille
        datarivit = ''

        # silmukka funktio datarivien luomiseen
        def luo_tilaston_datarivit():
            for t_data in datasetti:

                # muotoillaan aika haluttuun muotoon ja asetetaan sarakkeen datarivit
                # datariveille tehdään juoksevan numerointi mukainen muuttuja
                pelipaiva = t_data['pelattu_paiva']
                pelipaiva = datetime.datetime.fromisoformat(pelipaiva)

                datarivit = f"datarivi{(str(AloitusValikko.labelID))}"
                datarivit = self.tilastot_menu.add.label("{:<12} {:<20} {:<12} {:<3}".format(
                (pelipaiva.strftime('%d.%m.%Y')),
                t_data['nimi'],
                t_data['peliaika'],
                t_data['nopeuskerroin']
                ),
                    align=pygame_menu.locals.ALIGN_LEFT, font_name=pygame.font.SysFont('Courier New', 14), label_id=datarivit)
                AloitusValikko.labelID += 1
                AloitusValikko.kaikki_datarivit[datarivit] = True

        # valikon käynnistyessä tullaan tänne
        if not paivitys:

            # pudotusvalikko jolla tilastoa voi järjestellä
            self.tilastot_menu.add.dropselect(
                title='Järjestä sarakkeet',
                items=[('Pelipäivä', 0),
                    ('Nimi', 1),
                    ('Peliaika', 2),
                    ('Kerroin', 3)],
                onchange=self.jarjesta_sarakkeet,
                placeholder='Valitse',
                font_size=14,
                default=3,
                selection_box_height=50,
                selection_box_width=100,
                selection_option_padding=(0, 5),
                selection_option_font_size=12
                )

            palaaNappi = self.tilastot_menu.add.button('Palaa päävalikkoon', pygame_menu.events.BACK, font_size=20, button_id="palaaNappiID")

            # otsikot
            self.tilastot_menu.add.label("{:<12} {:<20} {:<12} {:<3}".format('PELIPÄIVÄ', 'NIMI','PELIAIKA','KERROIN'), align=pygame_menu.locals.ALIGN_LEFT, font_name=pygame.font.SysFont('Courier New', 14))

            # silmukka datarivien luomiseen
            luo_tilaston_datarivit()


        # silmukka kun tehdään tilastosivulla järjestysvalinta
        else:
            
            # piilotetaan kaikki ennen näytetyty tilastorivit
            # muutetaan nykyiset arvot, vaikka tällä hetkellä False arvoja ei käytetä mihinkään.
            for k, v in AloitusValikko.kaikki_datarivit.items():
                k.hide() 
                AloitusValikko.kaikki_datarivit[k] = False

            # silmukka datarivien luomiseen
            luo_tilaston_datarivit()


    def aloita_peli(self):
        '''
        Aloitetaan peli ja tallenntaan nimi
        '''
        RahaRobo(self.palauta_nimi())


if __name__ == "__main__":
    AloitusValikko()
# EOF
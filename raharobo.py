'''
Kuinka monta sekunttia selviät rahaa ja rosvoja vilisevässä maailmassa :-)
Pelissä on algoritmi joka nopettaa peliä tasaisaesti.
Peli kestää niin kauan kun sinulla on rahaa.
Kolikosta saa yhden rahan. Jos et saa kolikkoa kiinni menetät yhden rahan.
Rosvoon törmääminen vie viisi rahaa.
Rahat ja pelinopeus ovat kaikki itse säädettävissä luokan konstruktorissa.
Liikkuminen tapahtuu nuolinäppäimillä. F2 aloittaa uuden pelin ja ESC lopettaa pelin.
'''

# alustukset
import pygame
from random import randint
from random import shuffle

# luokat alkavat
class RahaRobo():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("RahaRobo")
        self.leveys = 640
        self.korkeus = 480
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        # aikaan liittyvät 
        self.kello = pygame.time.Clock()
        self.aloitus_aika = None
        self.pelattu_aika = None
        self.edellinen_muutos = 0
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
        self.osuma_laskuri = 0
        self.nopeus_kerroin = 1

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
        nopeus_teksti = self.fontti.render("Nopeuskerroin: "+str(f"{self.nopeus_kerroin:.0f}"), True, (255, 0, 0))
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

                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()

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
        self.pelattu_aika = f"{float((pygame.time.get_ticks() - self.aloitus_aika) / 1000):.1f}"
        return None

    def peli_paattyy(self):
        '''
        Kun raha loppuu, niin piirretään lopetusgrafiikka
        '''
        if self.osuma_laskuri < 0:
            teksti = self.fontti.render("Rahat loppuivat. Peli päättyi.", True, (255, 0, 0))
            aika_teksti = self.fontti.render("Selviydyit: "+str(self.pelattu_aika)+str(" sekunttia"), True, (255, 0, 0))
            aloita_uudestaan_teksti = self.fontti.render("Aloita uusi peli F2 napilla: ", True, (255, 0, 0))
            teksti_x = self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (64, 64, 64), (teksti_x, teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))
            self.naytto.blit(aika_teksti, (teksti_x, teksti_y + 20))
            self.naytto.blit(aloita_uudestaan_teksti, (teksti_x, teksti_y + 40))
            return True
        return False
    
    def uusi_peli(self):
        RahaRobo()

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
    

if __name__ == "__main__":
    RahaRobo()
# EOF

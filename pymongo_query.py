'''
MongoDB tietokantaan liittyvät tietokantakyselyt luodaan tänne
'''

import datetime
from db import get_database
import pymongo

# haetaan kaikki data ja järjestellään tieto
# parametrien mukaan ja palautetaan data listana
def hae_kaikki(sarake: str = 'peliaika', jarjestys: int = -1) -> list:
    try:
        dbname = get_database()
        collection_name = dbname["tilastot"]
        item_details = collection_name.find().sort(sarake,jarjestys)
        data = list(item_details)
        # tietokannan kentät debugausta varten:
        #     print(item['_id'])
        #     print(item['nimi'])
        #     print(item['peliaika'])
        #     print(item['rahaa'])
        #     print(item['nopeuskerroin'])
        #     pelipaiva = item['pelattu_paiva']
        #     pelipaiva = datetime.datetime.fromisoformat(pelipaiva)
        #     print(pelipaiva.strftime('Peliaika oli %d.%m.%Y klo %H:%M'))

        dbname.client.close()
        return data

    # tänne tarvitaan parempi virheenhallinta
    except:
        print("Virhe tilaston tallennuksessa")


# debugausta verten voidaan kysely voidaan ajaa itsenäisesti
# poistamalla alla olevat kommentit
# if __name__ == "__main__":
#     hae_kaikki()


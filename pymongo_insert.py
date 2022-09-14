'''
MongoDB tietokantaan liittyvät tallennukset luodaan tänne
'''

import datetime
from db import get_database

def tallenna_tilasto(nimi: str, peliaika: float, rahaa: int, nopeuskerroin: float, pelipaiva: str) -> bool:
    # luo MongoDB yhteys ja tallenna muuttujina saadut tiedot tilastoksi
    try:
        dbname = get_database()
        collection_name = dbname["tilastot"]

        tilasto_1 = {
        "nimi" : nimi,
        "peliaika" : peliaika,
        "rahaa" : rahaa,
        "nopeuskerroin" : nopeuskerroin,
        "pelattu_paiva" : pelipaiva
        }
        collection_name.insert_one(tilasto_1)
        print("Tallennus onnistui")

    # tänne tarvitaan parempi virheenhallinta
    except:
        print("Virhe tilaston tallennuksessa")


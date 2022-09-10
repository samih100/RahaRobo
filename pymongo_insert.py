import datetime
from db import get_database

def tallenna_tilasto(peliaika, rahaa, nopeuskerroin, pelipaiva):
    # Hae robotti tietokanta ja lisää tilastotieto
    try:
        dbname = get_database()
        collection_name = dbname["tilastot"]

        # insert_many esimerkit
        tilasto_1 = {
        "nimi" : "Pekka Pelaaja3",
        "peliaika" : peliaika,
        "rahaa" : rahaa,
        "nopeuskerroin" : nopeuskerroin,
        "pelattu_paiva" : pelipaiva
        }
        collection_name.insert_one(tilasto_1)
        print("Tallennus onnistui")
    except:
        print("Virhe tilaston tallennuksessa")


    # item_2 = {
    # "_id" : "U1IT00002",
    # "item_name" : "Egg",
    # "category" : "food",
    # "quantity" : 12,
    # "price" : 36,
    # "item_description" : "brown country eggs"
    # }
    #collection_name.insert_many([item_1,item_2])


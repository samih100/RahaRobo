import datetime
from db import get_database

def hae_kaikki():
    dbname = get_database()
    collection_name = dbname["tilastot"]

    item_details = collection_name.find()
    for item in item_details:
        print(item['_id'])
        print(item['nimi'])
        print(item['peliaika'])
        print(item['rahaa'])
        print(item['nopeuskerroin'])
        pelipaiva = item['pelattu_paiva']
        pelipaiva = datetime.datetime.fromisoformat(pelipaiva)
        print(pelipaiva.strftime('Peliaika oli %d.%m.%Y klo %H:%M'))

    dbname.client.close()


if __name__ == "__main__":
    hae_kaikki()


import datetime
from db import get_database
import pymongo

def hae_kaikki(sarake='peliaika', jarjestys=pymongo.DESCENDING):
    dbname = get_database()
    collection_name = dbname["tilastot"]
    item_details = collection_name.find().sort(sarake,jarjestys)
    #item_details = collection_name.find().sort("peliaika",pymongo.DESCENDING)
    #item_details = collection_name.find().sort("nopeuskerroin",pymongo.DESCENDING) # Kertoimen mukaan
    #item_details = collection_name.find().sort("peliaika",pymongo.ASCENDING)
    #db.Account.find().sort("UserName")
    #.sort("UserName",pymongo.ASCENDING) 
    data = list(item_details)
    # for item in data:
    #     print(item['_id'])
    #     print(item['nimi'])
    #     print(item['peliaika'])
    #     print(item['rahaa'])
    #     print(item['nopeuskerroin'])
    #     pelipaiva = item['pelattu_paiva']
    #     pelipaiva = datetime.datetime.fromisoformat(pelipaiva)
    #     print(pelipaiva.strftime('Peliaika oli %d.%m.%Y klo %H:%M'))

    print("{:<13} {:<36} {:<18} {:<3}".format('PELIPÄIVÄ', 'NIMI','PELIAIKA','KERROIN'))
    #tilastot_menu.add.label("{:13} {:<36} {:<18} {:>10}".format('PELIPÄIVÄ', 'NIMI','PELIAIKA','KERROIN'), align=pygame_menu.locals.ALIGN_LEFT, font_size=16)

    for t_data in data:
        pelipaiva = t_data['pelattu_paiva']
        pelipaiva = datetime.datetime.fromisoformat(pelipaiva)

        print("{:<13} {:<36} {:<18} {:<3}".format(
            (pelipaiva.strftime('%d.%m.%Y')),
            t_data['nimi'],
            t_data['peliaika'],
            t_data['nopeuskerroin'],
            )
            )
        #print("{:<10} {:<8} {:<15} {:<10} {:<10} {:<10}".format(item['_id'], item['nimi'], item['peliaika'], item['rahaa'], item['nopeuskerroin'], item['pelattu_paiva']))
        #tilastot_menu.add.label("{:13} {:<32} {:<18} {:>8}



    #print(data)
    dbname.client.close()
    #return data


if __name__ == "__main__":
    hae_kaikki()






from pymongo import MongoClient
import passw

def get_database():
    password = passw.PASSWORD
    cluster = "mongodb+srv://robo_player:"+password+"@cluster0.zjbfp.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(cluster)
    return client['RahaRobo']

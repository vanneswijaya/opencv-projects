import pymongo
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://vannes:mysonmyson@cluster0-w3igv.mongodb.net/katedral?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
db = cluster['katedral']
lingkungan = db['lingkungan']

class Ling:
    def __init__(self, ketua, n_ling, tickets=[]):
        self.ketua = ketua
        self.n_ling = n_ling
        self.tickets = tickets

    def store_ling(self):
        post = {
            'ketua':self.ketua,
            'nama lingkungan':self.n_ling,
            'tickets':self.tickets
        }
        lingkungan.insert_one(post)

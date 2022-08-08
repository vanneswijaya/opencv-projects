import pymongo
from pymongo import MongoClient
import uuid
import boto3
from ktpocr import Ktp
from lingkungan import Ling

cluster = MongoClient('mongodb+srv://vannes:mysonmyson@cluster0-w3igv.mongodb.net/katedral?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
db = cluster['katedral']
test = db['test']
lingkungan = db['lingkungan']

class SignUp:
    def __init__(self, name, ktp, ling):
        self.name = name
        self.ktp = ktp
        self.ling = ling

    @staticmethod
    def get_filename():
        x = uuid.uuid1()
        return str(x)+ '.jpg'

    @classmethod
    def ask_input(cls):
        name = input('Masukkan nama (sesuai yang tertera di KTP) : ')
        ktp = input('Kirimkan foto KTP anda : ')
        ling = input('Masukkan nama lingkungan anda : ')
        x = Ktp(name, ktp)
        if Ktp.validate_ktp(x):
            return cls(name, ktp, ling)
        else:
            return SignUp.ask_input()

    def upload_image(self, source_filename):
        filename = self.get_filename()
        neo_bucket = 'frproject'
        neo_session = boto3.Session(aws_access_key_id='00cb61562dc3a050d384', aws_secret_access_key='xQQUOjm3cJEpEJ8+jZpLosW0vL8FOJIa9UNeOetU')
        neo_s3 = neo_session.client('s3', endpoint_url='https://nos.jkt-1.neo.id')

        s3_path = 'images'
        destination_filename = filename
        source_filename = source_filename

        s3_fullname = f'{s3_path}/{destination_filename}'

        neo_s3.upload_file(source_filename, neo_bucket, s3_fullname, ExtraArgs={'ACL': 'public-read', 'ContentType':'image/png'})
        url_neo = f'{neo_s3.meta.endpoint_url}/{neo_bucket}/{s3_fullname}'
        
        return url_neo

    def store_ket(self):
        img_url = self.upload_image(self.ktp)
        x = Ktp(self.name, self.ktp)
        # ktp_data = x.char_replace()
        key, value, unknown = x.char_replace()
        count = 1
        y = Ling(self.name, self.ling)
        y.store_ling()
        query = {'ketua':self.name}
        query2 = {'lingkungan':self.ling}
        lingob = lingkungan.find_one(query)
        post = {
            'name':self.name,
            'image_url':img_url,
            'lingkungan':self.ling,
            'ling_id':lingob['_id'],
            'ling_tics':lingob['tickets']
            }
        # for y in ktp_data:
        #     post[f'line{count}'] = y
        #     count += 1
        for y in range(len(key)):
            post[key[y]] = value[y]
        for z in unknown:
            post[f'unknown{count}'] = z
            count += 1
        test.insert_one(post)
        ketob = test.find_one(query2)
        # ['ket_id'] = ketob['_id']
        print('Data stored')

    @staticmethod
    def run():
        ask = SignUp.ask_input()
        ask.store_ket()
        
SignUp.run()



    
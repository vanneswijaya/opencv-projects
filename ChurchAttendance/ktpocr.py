from cv2 import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image

class Ktp:
    def __init__(self, name, img_path):
        self.name = name
        self.img_path = img_path

    def ktp_to_string(self):
        tessdata_dir_config = r'--tessdata-dir "/usr/local/Cellar/tesseract/4.1.1/share/tessdata"'

        img = cv2.imread(self.img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)

        result = pytesseract.image_to_string((threshed), lang="ind", config = tessdata_dir_config)

        return result

    def char_replace(self):
        result = self.ktp_to_string()
        teks = []
        
        for word in result.split("\n"):
            if "”—" in word:
                word = word.replace("”—", ":")

            if "NIK" in word:
                nik_char = word.split()
                if "D" in word:
                    word = word.replace("D", "0")
                if "?" in word:
                    word = word.replace("?", "7") 
        
            teks.append(word)

        return teks

    def name_check(self):
        result = self.ktp_to_string()

        for word in result.split("\n"):
            if 'Nama' in word and self.name.upper() in word:
                return True
            else:
                continue
        return False

    def validate_ktp(self):
        word = self.ktp_to_string()

        if ("NIK" in word and "Agama" in word and 'Pekerjaan' in word):
            if self.name_check():
                return True
            else:
                return False
        else:
            return False

# ktp = Ktp('ISAAC SJAHRIR', 'dataset/ktp9.jpg')
# print(ktp.char_replace())
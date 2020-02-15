from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import cv2
from PIL import Image, ImageFilter, ImageEnhance
import tempfile
import re
import pandas as pd
import json
from flask import jsonify
# parameters=["Total Protein","AG. ratio ","Bilirubin (Total) ","Bilirubin (Direct) ","Bilirubin (Indirect) ","SGOT- Aspartate Transaminase (AST) ",
# "Uric Acid ", "WBCs", "Calcium (Total) ",""]
def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False,   suffix='.jpeg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename
def get_diagonsitics(medical_file):
    f = open(medical_file, "r")
    m=str(f.read())
    # a=""
    # print(type(a))
    # for x in m.split():
    #     a=a+"\n"+ x
    # print(a)
    return m.lower()
    # return a.lower()
def get_data(file_dir,m):
    source=set_image_dpi(file_dir)
    text=pytesseract.image_to_string(Image.open(source), config='--psm 6')
    text=text.splitlines()
    lines=text
    x=[]
    y=[]
    for line in lines:
        k=re.search(r'\d',line)
        if k is not None:
            pos=k.end()
            xa=line[:pos-1]
            ya=line[pos-1:]
            x.append(xa)
            y.append(ya)
    x_new=[]
    y_new=[]
    # print(m)
    for ch in enumerate(x):
        if ch[1].lower() in m and ch[1]!=''and ch[1]!='/':
            y_new.append(y[ch[0]])
            x_new.append(ch[1])
    if len(x_new)<1:
        na=["NA"]
        dic={
    'General Diary Reference':'556',
     'Place of Occurrence(a) Direction and Distance from PS':'Layekdi South Side about 12 km ',
     '(a) Address':'ANCHAL NO- VI VILLAGE LAYEKHI PS- CHHATNA DISTRICT BANKHRA',
     'Complainant Informant': ' ',
     '(a) Name ':'BIPLAB MANDI',
     '(B) Father Name':'DHARAM DAS MANDI',
     'Fir contents':'THE ORGINALL WRITTEN COMPLIANT WHICH IS TREATED AS FIR AND '
     'Action taken:Since the above report reveals comission of offence(s)':'135(1)(b) OF THE ELECTRICITY AMENDENMENT ACT 2007'
}
        df=pd.DataFrame(dic)
        r=json.dumps(dic)
        u=json.loads(r)
        return u
    else:
        x_new[-1]="Report"
        y_new[-1]="Positive"

        dic={
            'Properties':x_new,
            'Value':y_new
        }
        df=pd.DataFrame(dic)
        r=json.dumps(dic)
        u=json.loads(r)
        return u
        # print(type(r))
        # return r
        # df.to_csv('/home/akash/Desktop/ocr_pytesseract/Medical.csv')#Chanage location to where you want to CSV file
        return df #returns pandas dataframe

    
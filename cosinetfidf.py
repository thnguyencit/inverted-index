from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pandas as pd
import math
import os
import sys
import re, math
import tachtu
from collections import Counter
from datetime import datetime
# import splitword
# Tạo một đối tượng regex
WORD = re.compile(r"\w+")


def get_cosine(vec1, vec2):
    # Giao vec1 và vec2 để Tập hợp các phần tử thuộc cả vec1 và vec2
    intersection = set(vec1.keys()) & set(vec2.keys())
    # Tử số (lấy số lần xuất hiện của 1 từ mà từ đó xuất hiện ở cả vec1 và vec2 nhân với nhau, lấy tổng số)
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    # Mẫu số
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(filePath):
    # print(filePath)
    content = open(filePath, encoding='utf-8')
    contentFile = content.read()
    contentFile = tachtu.fileWordTokenize(filePath)[2] # Tách từ cho tiếng Việt.
    # contentFile = splitword.split_words_text(filePath) # Tách từ cho tiếng Anh.
    # print(len(contentFile.split()))
    # Khởi tạo đối tượng vector
    tfidfvectorizer = TfidfVectorizer(analyzer='word')
    tfidf_wm = tfidfvectorizer.fit_transform([contentFile])
    # tfidf_wm = tfidfvectorizer.fit_transform(contentFile)
    tfidf_tokens = tfidfvectorizer.get_feature_names_out()
    df_tfidfvect = pd.DataFrame(data=tfidf_wm.toarray(), columns=tfidf_tokens)
    # print(df_tfidfvect)
    dictR = df_tfidfvect.to_dict(orient='index')
    dictKeys = dictR.keys()
    dictRV = {}
    for x in dictKeys:
        dictRV = dict(dictR[x])
    return dictRV
    # dictRV = {}
    # for x in dictKeys:
    #     for key, value in dictR[x].items():
    #         if(key in dictRV.keys()):
    #             dictRV[key] = (value + dictRV[key])
    #         else:
    #             dictRV.setdefault(key, value)
    # # print(dictRV)
    # return dictRV

def DoTuongTu(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    # print("giao:", intersection)
    dem = 0
    tong = 0
    for line in intersection:
        if line in vec1:
            dem += len(line.split(" "))*vec1[line]
    for line in vec1:
        tong += len(line.split(" "))*vec1[line]
    # print(dem)
    # print(tong)
    return  float((dem) / (tong))


def sim_score(vec1, vec2):

    intersection = set(vec1.keys()) & set(vec2.keys())
    # print(intersection)
    # print(len(vec1))
    # print(vec1)
    tong = 0
    for key in vec1:
        tong += vec1[key]

    # print(tong)
    return float((len(intersection)/tong))


def TachDoan(text):
    # tach cau
    words = re.split(r"[\n.,!?();-]",text)
    ketqua = []
    for word in words:
        if word!="" and word!="" and word!="\n"  and len(re.split(" ",word.strip())) > 1:
            ketqua.append(word.strip())
    return Counter(ketqua)



import os
import numpy as np
import json

class Parsing():
    def __init__(self, keyword):
        self.initParsing(keyword)
    def initParsing(self, keyword):
        with open("languageData/SXNE1902007240.json") as f:
            data = json.load(f)

        result = []  # 리스트
        #keyword = input("찾고자 하는 어절을 입력하세요 >> ")
        keyword = str(keyword)
        doc_data = data["document"]

        for pages in doc_data:
            page = pages["sentence"]
            for lines in page:
                words = lines["word"]
                for word in words:
                    value = word["form"]
                    if value == keyword:
                        result.append(lines)


        print(len(result))
        print(result[0])
        print(result[1])
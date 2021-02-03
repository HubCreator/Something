import os
import numpy as np
import json

class Parsing():
    def __init__(self, keyword):
        self.result = []  # 리스트
        self.initParsing(keyword)
        
    def initParsing(self, keyword):
        with open("languageData/SXNE1902007240.json") as f: # 딕셔너리
            data = json.load(f)

        keyword = str(keyword)
        doc_data = data["document"]

        for pages in doc_data:
            page = pages["sentence"]
            for lines in page:
                words = lines["word"]
                for word in words:
                    value = word["form"]
                    if value == keyword:
                        self.result.append(lines)


        # print(len(result))
        for i in range(0, len(self.result), 1):
            print(i + 1, " 번째 >> ", self.result[i]["form"])
            
        f.close()
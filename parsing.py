import os
import numpy as np
import json

class Parsing():
    def __init__(self, keyword):
        self.word_result = []           # 정확한 단어 검색 결과
        self.includingWord_result = []  # 단어를 포함한 검색 결과
        self.sentence_result = []
        self.origin_result = []         # 출전

        self.initParsing(keyword)
        
    def initParsing(self, keyword):
        with open("languageData/SXNE1902007240.json") as f: # 딕셔너리
            data = json.load(f)

        keyword = str(keyword)

        # 키워드 체크


        doc_data = data["document"]

        for pages in doc_data: # 단어 찾기
            page = pages["sentence"]
            for lines in page:
                words = lines["word"]
                for word in words:
                    value = word["form"]
                    if value == keyword:
                        self.word_result.append(word)


        # print(len(result))
        # for i in range(0, len(self.result), 1):
        #     print(i + 1, " 번째 >> ", self.result[i]["form"])
            
        f.close()
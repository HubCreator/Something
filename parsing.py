import numpy as np
import json

class Parsing():
    def __init__(self, keyword):
        self.word_result = []           # 단어
        self.soundBlock_result = []     # 어절
        self.sentence_result = []       # 문장
        self.origin_result = []         # 출전
        self.result_count = 0

        self.initParsing(keyword)
        
    def initParsing(self, keyword):
        with open("languageData/SXNE1902007240.json") as f: # 딕셔너리
            data = json.load(f)

        keyword = str(keyword)

        # for i in range(0, len(categories), 1):
        #     if str(categories[i]) == "단어검색":

        # 키워드 체크


        doc_data = data["document"]

        for pages in doc_data: # 단어 찾기
            page = pages["sentence"]
            for lines in page:
                words = lines["word"]
                for word in words:
                    value = word["form"]
                    if value == keyword:
                        self.result_count += 1
                        self.sentence_result.append(lines)      # 문장
                        self.origin_result.append(pages)        # 출전
                        self.soundBlock_result.append(word)         # 어절
                        #self.word_result.append(word) # 단어


        # print(len(result))
        # for i in range(0, len(self.result), 1):
        #     print(i + 1, " 번째 >> ", self.result[i]["form"])
            
        f.close()
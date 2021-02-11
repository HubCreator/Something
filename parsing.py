from os import error
import numpy as np
import json

class Parsing():
    def __init__(self, dataFile, keyword):
        self.file = dataFile
        self.word_result = []           # 단어
        self.soundBlock_result = []     # 어절
        self.sentence_result = []       # 문장
        self.origin_result = []         # 출전
        self.word_result_with_soundBlock = []
        self.soundBlock_result_count = 0
        self.word_result_count = 0

        self.initParsing(keyword)
        
    def initParsing(self, keyword):
        with open(self.file) as f: # 딕셔너리
            data = json.load(f)

        self.myKeyword = str(keyword)

        doc_data = data["document"]

        try:
            for pages in doc_data: # 단어 찾기
                page = pages["sentence"]
                for lines in page:
                    words = lines["word"]
                    for word in words:
                        value = word["form"]
                        if value[value.find(self.myKeyword) : value.find(self.myKeyword) + len(self.myKeyword)] == self.myKeyword:
                            self.soundBlock_result_count += 1
                            self.sentence_result.append(lines)      # 문장
                            self.origin_result.append(pages)        # 출전
                            self.soundBlock_result.append(word)         # 어절
                            if value == self.myKeyword:
                                self.word_result_count += 1
                                self.word_result.append(word)
                                self.word_result_with_soundBlock.append(word)
                            else:
                                self.word_result_with_soundBlock.append("")
                            #self.word_result.append(word) # 단어
                        
                        
        except error:
            print("Can't load the file")

        f.close()
from os import error
import numpy as np
import json

class Parsing():
    def __init__(self, dataFile, keyword):
        self.file = dataFile

        self.fileType = None    # True == sentenceType / False == paragraphType
        
        self.sentenceType_soundBlock_result = []                        # 어절
        self.sentenceType_word_result = []                              # 단어
        self.sentenceType_word_result_with_soundBlock = []              # 단어 (어절이 체크되어 있을 때)
        self.sentenceType_sentence_result = []                          # 문장
        self.sentenceType_soundBlockChecked_sentence_result = []        # 문장 (어절이 체크되어 있을 때)
        self.sentenceType_origin_result = []                            # 출전 
        self.sentenceType_soundBlockChecked_origin_result = []          # 출전 (어절이 체크되어 있을 때)

        self.sentenceType_soundBlock_result_count = 0
        self.sentenceType_word_result_count = 0



        self.paragraphType_soundBlock_result = []                   # 어절
        self.paragraphType_word_result = []                         # 단어
        self.paragraphType_word_result_with_soundBlock = []         # 단어 (어절이 체크되어 있을 때)
        self.paragraphType_sentence_result = []                     # 문장
        self.paragraphType_soundBlockChecked_sentence_result = []   # 문장 (어절이 체크되어 있을 때)
        self.paragraphType_origin_result = []                       # 출전
        self.paragraphType_soundBlockChecked_origin_result = []     # 출전 (어절이 체크되어 있을 때)

        self.paragraphType_soundBlock_result_count = 0
        self.paragraphType_word_result_count = 0


        self.initParsing(keyword)
        
    def initParsing(self, keyword):
        with open(self.file) as f: # 딕셔너리
            data = json.load(f)

        self.myKeyword = str(keyword).strip()

        doc_data = data["document"]

        try:
            if bool(data['document'][0].get('sentence')):
                self.fileType = True
                for pages in doc_data: # 단어 찾기
                    page = pages["sentence"]
                    self.fileType = True
                    for lines in page:
                        words = lines["word"]
                        for word in words:
                            value = word["form"]
                            if value[value.find(self.myKeyword) : value.find(self.myKeyword) + len(self.myKeyword)] == self.myKeyword:
                                self.sentenceType_soundBlock_result_count += 1
                                self.sentenceType_soundBlockChecked_sentence_result.append(lines)      # 문장
                                self.sentenceType_soundBlockChecked_origin_result.append(pages)        # 출전
                                self.sentenceType_soundBlock_result.append(word)         # 어절
                                if value == self.myKeyword:
                                    self.sentenceType_word_result_count += 1
                                    self.sentenceType_word_result.append(word)
                                    self.sentenceType_word_result_with_soundBlock.append(word)
                                    self.sentenceType_origin_result.append(pages)
                                    self.sentenceType_sentence_result.append(lines)
                                else:
                                    self.sentenceType_word_result_with_soundBlock.append("")
            else:
                self.fileType = False
                for pages in doc_data:
                    page = pages["paragraph"]
                    for lines in page:
                        words = lines["form"]   # words는 문장
                        if words[words.find(self.myKeyword) : words.find(self.myKeyword) + len(self.myKeyword)] == self.myKeyword:
                            self.paragraphType_soundBlock_result_count += 1                         # 어절 count
                            self.paragraphType_soundBlockChecked_sentence_result.append(lines)      # 문장
                            self.paragraphType_soundBlockChecked_origin_result.append(pages)        # 출전

                            self.start = 0
                            self.end = 0

                            for i in range(words.find(self.myKeyword) - 1, 0, -1):
                                if i > 0:
                                    if words[i] == " " or words[i] == "'" or words[i] == '"':
                                        self.start = i
                                        break
                                else:
                                    self.start = 0
                                    break

                            for i in range(words.find(self.myKeyword) + len(self.myKeyword), len(words), 1):
                                if i <= len(words):
                                    if words[i] == " " or words[i] == ".":
                                        self.end = i
                                        break
                                else:
                                    self.end = len(words)
                                    break

                            self.paragraphType_soundBlock_result.append(words[self.start : self.end].strip())         # 어절

                            print(words[self.start : self.end].strip())
                            print(self.myKeyword)
                            # if words[self.start : self.end] == self.myKeyword:  # 어절이 단어와 같다면
                            # if words.find(self.myKeyword) != 0:
                                # if (words[words.find(self.myKeyword) - 1] == " ") and (words[words.find(self.myKeyword) + len(self.myKeyword) + 1] == " ") == True:   # 단어가 True이면..
                            if words[self.start : self.end].strip() == self.myKeyword:
                                self.paragraphType_word_result_count += 1
                                self.paragraphType_word_result.append(self.myKeyword)

                                self.paragraphType_word_result_with_soundBlock.append(self.myKeyword)
                                self.paragraphType_origin_result.append(pages)
                                self.paragraphType_sentence_result.append(lines)

                                # if self.myKeyword == words[self.start : self.end]:
                                #     self.paragraphType_word_result.append(self.myKeyword)
                            else:
                                self.paragraphType_word_result_with_soundBlock.append("")
                            # else:
                            #     if (words[words.find(self.myKeyword) + len(self.myKeyword) + 1] == " "):
                            #         self.paragraphType_word_result_count += 1
                            #         self.paragraphType_word_result.append(self.myKeyword)
                            #         self.paragraphType_word_result_with_soundBlock.append(self.myKeyword)
                            #         self.paragraphType_origin_result.append(pages)
                            #         self.paragraphType_sentence_result.append(lines)

                            #     else:
                            #         self.paragraphType_word_result_with_soundBlock.append("")
                        
                        
        except error:
            print("Can't load the file")

        f.close()
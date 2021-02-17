from os import error
import numpy as np
import json

class Parsing():
    def __init__(self, dataFile, keyword):
        self.file = dataFile

        self.fileType = None    # True == sentenceType / False == paragraphType
        
        self.sentenceType_soundBlock_result = [""]                        # 어절
        self.sentenceType_word_result = [""]                              # 단어
        self.sentenceType_word_result_with_soundBlock = [""]              # 단어 (어절이 체크되어 있을 때)
        self.sentenceType_sentence_result = [""]                          # 문장
        self.sentenceType_soundBlockChecked_sentence_result = [""]        # 문장 (어절이 체크되어 있을 때)
        self.sentenceType_origin_result = [""]                            # 출전 
        self.sentenceType_soundBlockChecked_origin_result = [""]          # 출전 (어절이 체크되어 있을 때)

        self.sentenceType_soundBlock_result_count = 0
        self.sentenceType_word_result_count = 0



        self.paragraphType_soundBlock_result = [""]                   # 어절
        self.paragraphType_word_result = [""]                         # 단어
        self.paragraphType_word_result_with_soundBlock = [""]         # 단어 (어절이 체크되어 있을 때)
        self.paragraphType_sentence_result = [""]                     # 문장
        self.paragraphType_soundBlockChecked_sentence_result = [""]   # 문장 (어절이 체크되어 있을 때)
        self.paragraphType_origin_result = [""]                       # 출전
        self.paragraphType_soundBlockChecked_origin_result = [""]     # 출전 (어절이 체크되어 있을 때)

        self.paragraphType_separated_sentence_result = [""]

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
                        words = lines["form"]   # words는 문장이 아닌 Paragraph..  문장 덩어리
                        if words[words.find(self.myKeyword) : words.find(self.myKeyword) + len(self.myKeyword)] == self.myKeyword:
                            self.paragraphType_soundBlock_result_count += 1                         # 어절 count
                            self.paragraphType_soundBlockChecked_sentence_result.append(lines)      # 문장
                            self.paragraphType_soundBlockChecked_origin_result.append(pages)        # 출전

                            self.start = 1
                            self.end = 0

                            # to-do : ASCII ??
                            if words.find(self.myKeyword) == 0:
                                self.start = 0
                            elif words.find(self.myKeyword) > 0:
                                for i in range(words.find(self.myKeyword), 0, -1):
                                    if i == words.find(self.myKeyword):
                                        continue

                                    # todo here
                                    if  words[i] == '“' or words[i] == '”' or words[i] == "‘" or words[i] == "’" or words[i] == "'"  or words[i] == '"' or words[i] == "<" or words[i] == ">" or words[i] == ":" or words[i] == "-" or words[i] == "…" or words[i] == " " or words[i] == "":
                                        self.start = i + 1
                                        break
                                

                            for j in range(words.find(self.myKeyword) + len(self.myKeyword), len(words), 1):
                                if j < len(words):
                                    if words[j] == '“' or words[j] == "”" or words[j] == "‘" or words[j] == "’" or words[j] == "'" or words[j] == '"' or words[j] == "." or words[j] == "," or words[j] == "?" or words[j] == "!" or words[j] == "<" or words[j] == ">" or words[j] == "(" or words[j] == ")" or words[j] == "-" or words[j] == "…" or words[j] == " " or  words[j] == "":
                                        self.end = j
                                        break
                                else:
                                    self.end = len(words)
                                    break

                            self.paragraphType_soundBlock_result.append(words[self.start:self.end])         # 어절

                            if words[self.start : self.end].strip() == self.myKeyword:
                                self.paragraphType_word_result_count += 1
                                self.paragraphType_word_result.append(self.myKeyword)

                                self.paragraphType_word_result_with_soundBlock.append(self.myKeyword)
                                self.paragraphType_origin_result.append(pages)
                                self.paragraphType_sentence_result.append(lines)

                            else:
                                self.paragraphType_word_result_with_soundBlock.append("")
                        
                        
        except error:
            print("Can't load the file")

        f.close()
from os import error
import numpy as np
import os
import json

class Parsing():
    def __init__(self, dataFile, keyword):
        # self.file = dataFile
        print(dataFile)

        self.files = []
        self.json_files = []
        self.type = 0
        # self.path_to_json = ""

        if "json" in dataFile[0]:
            for i in range(0, len(dataFile), 1):
                self.file = dataFile[i][dataFile[i].find("languageData") : ]
                self.files.append(self.file)
                self.type = 1
        else:
            self.path_to_json = dataFile[0]
            self.json_files = [self.pos_json for self.pos_json in os.listdir(self.path_to_json) if self.pos_json.endswith('.json')]
            self.type = 2
        
        # print(self.json_files) 

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

        if self.type == 1:
            self.initParsing1(keyword)
        elif self.type == 2:
            self.initParsing2(keyword)
        
    def initParsing1(self, keyword):
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

    def initParsing2(self, keyword):
        # with open(self.file) as f: # 딕셔너리
        #     data = json.load(f)

        cnt = 0

        for index, js in enumerate(self.json_files):
            with open(os.path.join(self.path_to_json, js)) as json_file:
                if cnt > 1000:
                    break
                # print(json_file)
                cnt += 1
                data = json.load(json_file)
        
            # print(self.json_files)

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

            json_file.close()
        
        print("There're more than 1000 files. And find the result only within 1000 files")
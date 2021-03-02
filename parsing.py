from os import error
import numpy as np
import os
import json

class Parsing():
    def __init__(self, dataFile, keyword):
        self.files = []
        self.json_files = []
        self.type = 0

        if "json" in dataFile[0]:   # json 파일 하나만 선택했을 때
            for i in range(0, len(dataFile), 1):
                self.file = dataFile[i][dataFile[i].find("languageData") : ]
                self.files.append(self.file)
                self.type = 1
        else:                       # json 파일 여러개 혹은 폴더를 선택했을 때
            self.path_to_json = dataFile[0]
            self.json_files = [self.pos_json for self.pos_json in os.listdir(self.path_to_json) if self.pos_json.endswith('.json')]

            self.sorted_json_files = sorted(self.json_files)    # 정렬
            self.pages = []
            for i in range(0, int(len(self.sorted_json_files) / 15) , 1):
                tmp = []
                tmp.clear()
                for j in range(0, 15, 1):
                    tmp.append(self.sorted_json_files[j + (i*15)])
                self.pages.append(tmp)  # 선택한 폴더 안의 파일을 15개씩 리스트에 차례로 저장

            self.type = 2
        

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



        self.paragraphType_serial_number = ["0"]
        self.paragraphType_soundBlock_result = [""]                   # 어절
        self.paragraphType_word_result = [""]                         # 단어
        self.paragraphType_word_result_with_soundBlock = [""]         # 단어 (어절이 체크되어 있을 때)
        self.paragraphType_sentence_result = [""]                     # 문장
        self.paragraphType_soundBlockChecked_sentence_result = [""]   # 문장 (어절이 체크되어 있을 때)
        self.paragraphType_origin_result = [""]                       # 출전
        self.paragraphType_soundBlockChecked_origin_result = [""]     # 출전 (어절이 체크되어 있을 때)

        self.paragraphType_separated_sentence_result = [""]

        self.paragraphType_serial_number_count = 0
        self.paragraphType_soundBlock_result_count = 0
        self.paragraphType_word_result_count = 0

        if self.type == 1:
            self.initParsing1(keyword)
        elif self.type == 2:
            self.initParsing2(keyword)
        
    def initParsing1(self, keyword): # 하나의 파일만 선택했을 때
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

    def initParsing2(self, keyword): # 여러개의 파일이나 폴더를 선택했을 때
        cnt = 0
        # to-do : self.pages 리스트를 이용해 15개씩 파일을 쪼개서 검색
        for index, js in enumerate(self.pages[0]):  # self.json_files는 전체 파일 리스트
            with open(os.path.join(self.path_to_json, js)) as json_file:
                if cnt > 1000:
                    break
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
                                self.paragraphType_serial_number_count += 1                         # 어절 count
                                if self.paragraphType_serial_number_count < 10:
                                    self.paragraphType_serial_number.append("0000{}".format(self.paragraphType_serial_number_count))
                                elif self.paragraphType_serial_number_count >= 10 and self.paragraphType_serial_number_count < 100:
                                    self.paragraphType_serial_number.append("000{}".format(self.paragraphType_serial_number_count))
                                elif self.paragraphType_serial_number_count >= 100 and self.paragraphType_serial_number_count < 1000:
                                    self.paragraphType_serial_number.append("00{}".format(self.paragraphType_serial_number_count))
                                elif self.paragraphType_serial_number_count >= 1000 and self.paragraphType_serial_number_count < 10000:
                                    self.paragraphType_serial_number.append("0{}".format(self.paragraphType_serial_number_count))
                                elif self.paragraphType_serial_number_count >= 10000 and self.paragraphType_serial_number_count < 100000:
                                    self.paragraphType_serial_number.append("{}".format(self.paragraphType_serial_number_count))


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
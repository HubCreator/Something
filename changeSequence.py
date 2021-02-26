class changeSequence():
    def __init__(self, list_for_sequence, category, how):
        self.data = list_for_sequence
        self.category = category
        self.updown = how
        self.serial_number_list = []
        self.sentence_list = []
        self.word_list = []
        self.wordBlock_list = []
        self.origin_list = []
        
        self.sequence_result = []
        self.sequence_result.clear()

        self.init()
    
    def init(self):
        for i in range(0, len(self.data), 1):
            self.serial_number_list.append(self.data[i][0])
            if self.data[i][1][0] == '“' or self.data[i][1][0] == '‘' or self.data[i][1][0] == '[' or self.data[i][1][0] == '.' or self.data[i][1][0] == '“' or self.data[i][1][0] == ' ' or self.data[i][1][0] == '' or self.data[i][1][0] == '"':
                self.sentence_list.append(self.data[i][1][1:])
            else:
                self.sentence_list.append(self.data[i][1])
            self.word_list.append(self.data[i][2])
            self.wordBlock_list.append(self.data[i][3])
            self.origin_list.append(self.data[i][4])
        
        # serial_number_list 안에서 오름, 내림차순 정렬
        if self.category == 0:
            if self.updown == True:
                self.sequence_result = sorted(self.serial_number_list, reverse = True)
            else:
                self.sequence_result = sorted(self.serial_number_list, reverse = False)
        
        # sentence
        elif self.category == 1:
            if self.updown == True:
                self.sequence_result = sorted(self.sentence_list, reverse = True)
            else:
                self.sequence_result = sorted(self.sentence_list, reverse = False)

        # word
        elif self.category == 2:
            if self.updown == True:
                self.sequence_result = sorted(self.word_list, reverse = True)
            else:
                self.sequence_result = sorted(self.word_list, reverse = False)
        # wordBlock
        elif self.category == 3:
            if self.updown == True:
                self.sequence_result = sorted(self.wordBlock_list, reverse = True)
            else:
                self.sequence_result = sorted(self.wordBlock_list, reverse = False)
        
        # origin
        elif self.category == 4:
            if self.updown == True:
                self.sequence_result = sorted(self.origin_list, reverse = True)
            else:
                self.sequence_result = sorted(self.origin_list, reverse = False)

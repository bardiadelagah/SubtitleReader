import pysrt
import re
import numpy as np
import pandas as pd
import math
import os
from vtt_to_srt.vtt_to_srt import vtt_to_srt

# pip freeze > requirements.txt
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class subtitleReader:
    unique_words = None
    all_sentences_unique = None
    all_sentences_in_order = None
    all_words_in_order = None
    all_words_unique = None
    dict_in_order = None
    dict_unique = None
    dict_in_order_new_words = None
    dict_unique_new_words = None
    sub = None
    edited_sub = None
    file_address = None
    basic_knowledge_file_address = 'database/basic_knowledge.xlsx'

    def __init__(self):
        # list files in project and user must choose one file by number
        self.choose_some_file()
        output = self.read_sub_file()
        if output is True:
            # remove stop words from text(i.e., !,.,? and etc)
            self.edit_sub_text()
            # get all sentences from subtitle
            self.get_all_sentences()
            # get all word from subtitle
            self.get_all_words()
            # make dictionary for all words in subtitle
            self.make_dict()
            # make dictionary for new words in subtitle
            self.make_dict_for_new_words()

    def choose_some_file(self):
        files = os.listdir()
        for i in range(0, len(files) - 1):
            print(str(i), files[i])
        num = input('please_enter_one_number between {} to {}\n'.format(0, len(files) - 1))
        num = int(num)
        if (num <= len(files) - 1) and (num >= 0):
            self.file_address = files[num]

    def read_sub_file(self):
        extetion = self.file_address.split('.')[-1]
        ext_str = 'str'
        temp_address = self.file_address[0:len(self.file_address) - len(extetion)]
        # change vtt format to str
        if extetion == 'vtt':
            vtt_to_srt(self.file_address)
            self.file_address = temp_address + ext_str
            # print(self.file_address)
            print('you need run the code again and try to choose file with str extention')
            return False
        self.sub = pysrt.open(self.file_address)  # , encoding='iso-8859-1'
        return True

    def edit_sub_text(self):
        text = self.sub.text
        text = text.replace('\n', ' ')
        text = text.replace('</i>', '')
        text = text.replace('<i>', '')
        text = text.replace('-', '')
        text = text.replace('...', '.')
        text = text.replace('Mr.', 'Mr')
        text = text.replace('Mrs.', 'Mrs')
        self.edited_sub = text

    def get_all_sentences(self):
        text = self.edited_sub
        all_sentences_in_order = []
        start_idx = 0
        for i in range(0, len(text)):
            if text[i] == '.' or text[i] == '!' or text[i] == '?':
                my_text = text[start_idx:i + 1]
                my_text = my_text.strip(" ")
                all_sentences_in_order.append(my_text)
                start_idx = i + 1
        self.all_sentences_in_order = all_sentences_in_order
        self.all_sentences_unique = np.unique(all_sentences_in_order)
        print('number of all_sentences_in_order', len(all_sentences_in_order))
        print('number of all_sentences_unique', len(self.all_sentences_unique))
        # for item in all_sentences_in_order:
        #     print(item)

    def get_all_words(self):
        text = self.edited_sub
        space_split = ' '
        nothing_split = ''
        split = nothing_split
        text = text.replace('.', split)
        text = text.replace('!', split)
        text = text.replace('?', split)
        text = text.replace(',', split)
        self.all_words_in_order = text.split(' ')
        self.all_words_unique = np.unique(self.all_words_in_order)
        print('number of all_words_in_order', len(self.all_words_in_order))
        print('number of all_words_unique', len(self.all_words_unique))
        # for item in self.all_words_unique:
        # print(item)

    def make_dict(self):
        columns = ['word (phrase, Idiom)', 'sentence', 'minute', 'translate', 'pronunciation',
                   'english meaning or images']
        dict_unique = pd.DataFrame(columns=columns)
        dict_in_order = pd.DataFrame(columns=columns)
        for word in self.all_words_unique:
            sentences = ''
            for sentence in self.all_sentences_unique:
                if word in sentence:
                    sentences = sentences + sentence + '\n'
            data = {
                'word (phrase, Idiom)': word,
                'sentence': sentences
            }
            dict_unique = dict_unique.append(data, ignore_index=True)

        dict_in_order['word (phrase, Idiom)'] = self.all_words_in_order
        for i in range(0, len(dict_in_order.index)):
            word = dict_in_order.at[i, 'word (phrase, Idiom)']
            rows = dict_unique.index[(dict_unique['word (phrase, Idiom)'] == word)].tolist()
            if len(rows) != 0:
                idx = rows[0]
                dict_in_order.at[i, 'sentence'] = dict_unique.at[idx, 'sentence']

        # find sentence per minutes or words per minutes
        # print(self.sub)
        list = str(self.sub[-1]).split('\n')
        # print(list)
        # index = int(list[0])  # subs.index
        temp_minutes = list[1].split(':')
        minutes = int(temp_minutes[0]) * 60 + int(temp_minutes[1])
        '''
        h = math.modf(index / minutes)
        if h[0] > 0.5:
            # sentence_per_minutes = (index // minutes) + 1
            sentence_per_minutes = (len(self.all_sentences_in_order) // minutes) + 1
            word_per_minutes = (len(self.all_words_in_order) // minutes) + 1
        else:
            # sentence_per_minutes = index // minutes
            sentence_per_minutes = len(self.all_sentences_in_order) // minutes
            word_per_minutes = len(self.all_words_in_order) // minutes
        '''
        # sentence_per_minutes = len(self.all_sentences_in_order) // minutes
        word_per_minutes = len(self.all_words_in_order) // minutes
        print('word_per_minutes', word_per_minutes)
        # all_sentences = self.all_sentences_in_order
        all_words = self.all_words_in_order
        minute = 0
        for i in range(0, len(all_words)):
            mod = math.modf(i / word_per_minutes)
            mod = mod[0]
            if mod == 0:
                minute += 1
            dict_in_order.at[i, 'minute'] = minute
        # make name
        ext = '.' + str(self.file_address.split('.')[-1])
        name = self.file_address.split('.')[0]
        dict_unique.to_excel(name + '_dict_unique' + '.xlsx', index=False, sheet_name='Sheet')
        dict_in_order.to_excel(name + '_dict_in_order' + '.xlsx', index=False, sheet_name='Sheet')
        self.dict_unique = dict_unique
        self.dict_in_order = dict_in_order
        # print(dict_in_order.index[[1,2,3]])
        # print(dict_in_order.index[25])
        # dataframe.to_pickle(name + '.pkl')

    def make_dict_for_new_words(self):
        ext = '.' + str(self.file_address.split('.')[-1])
        name = self.file_address.split('.')[0]
        basic_knowledge = pd.read_excel(self.basic_knowledge_file_address)
        basic_words = basic_knowledge['word (phrase, Idiom)'].tolist()
        remove_idx = []
        dict_in_order_new_words = self.dict_in_order.copy()
        for word in basic_words:
            rows = dict_in_order_new_words.index[(dict_in_order_new_words['word (phrase, Idiom)'] == word)].tolist()
            if len(rows) != 0:
                remove_idx.extend(rows)
        remove_idx = np.unique(remove_idx)
        dict_in_order_new_words.drop(dict_in_order_new_words.index[remove_idx], inplace=True)
        self.dict_in_order_new_words = dict_in_order_new_words
        dict_in_order_new_words.to_excel(name + '_dict_in_order_new_words' + '.xlsx', index=False, sheet_name='Sheet')

        remove_idx = []
        dict_unique_new_words = self.dict_unique.copy()
        for word in basic_words:
            rows = dict_unique_new_words.index[(dict_unique_new_words['word (phrase, Idiom)'] == word)].tolist()
            if len(rows) != 0:
                remove_idx.extend(rows)
        remove_idx = np.unique(remove_idx)
        dict_unique_new_words.drop(dict_unique_new_words.index[remove_idx], inplace=True)
        self.dict_unique_new_words = dict_unique_new_words
        dict_unique_new_words.to_excel(name + '_dict_unique_new_words' + '.xlsx', index=False, sheet_name='Sheet')

        print('number of dict_in_order_new_words', len(self.dict_in_order_new_words))
        print('number of dict_unique_new_words', len(self.dict_unique_new_words))


# ok
# dataframe.drop(dataframe.index[remove], inplace=True)
# for itme in remove:
# dataframe = dataframe.drop([dataframe.index[itme]])
# for itme in remove:
#    dataframe = dataframe.drop(dataframe.index[itme])
# not ok
# dataframe = dataframe.drop(remove)
# dataframe = dataframe.drop(dataframe.index[remove])
# dataframe = dataframe.drop(dataframe.index[remove], inplace=True)
# for itme in remove:
#    dataframe.drop(dataframe.index[itme], inplace=True)
# dataframe = dataframe.drop(remove, inplace=True)
# dataframe.drop(dataframe.index[remove],axis=0,inplace=True)
# dataframe = dataframe.drop(remove,axis=0,inplace=True)
# dataframe = dataframe.drop(final_remove)

if __name__ == '__main__':
    sub_reader = subtitleReader()
    # for i in range(0,len(df.index)):
    # print(type(subs)) # <class 'pysrt.srtfile.SubRipFile'>
    # print(len(subs)) # number of subtitle lines
    # print(type(subs.text)) <class 'str'>
    # print(subs.text)
    # List of special characters ---->>>> . \ + * ? [ ^ ] $ ( ) { } = !  | : -
    # unnormal charecters in text
    # , -- Mr. -- I'll -- ... -- <i> -- </i> -- - --
    # res = re.split('</i>|<i>|-|, |_|-|!', text)
    # all_sentences = re.split('\? | ! |.', text)
    # all_sentences = text.split('\?', text)
    # all_sentences = text.split('!', all_sentences)
    # part = subs.slice(starts_after={'minutes': 2, 'seconds': 30}, ends_before={'minutes': 3, 'seconds': 40})

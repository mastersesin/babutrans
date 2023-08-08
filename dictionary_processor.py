import os
import re
import sys
import uuid
from datetime import datetime

from convert_unicode import Converter


class DictionaryProcessor:
    DICTIONARY_PATH = 'translater/translater_dictionary_final.txt'
    CURRENT_DICTIONARY = {}

    def __init__(self):
        self.load_dictionary()
        self.VISCII_converter = Converter()

    def load_dictionary(self):
        with open(self.DICTIONARY_PATH, 'r') as file:
            for line in file:
                if len(tuple(line.strip().split('\t\t\t'))) > 3:
                    print(line)
                    raise ValueError(f'Your line as shown have too many values to unpack it have '
                                     f"{len(tuple(line.strip().split('	')))} items"
                                     f" but it only have VIETNAMESE and CHINESE items")
                chinese, vietnamese, viscii_vietnamese = tuple(line.strip().split('\t\t\t'))
                self.CURRENT_DICTIONARY[chinese] = viscii_vietnamese

    def process_chinese(self, list_chinese_not_yet_translated, mode):
        if not list_chinese_not_yet_translated:
            return
        [print(x) for x in list_chinese_not_yet_translated]
        print(f'Please provide translated word for these {mode}')
        sentinel = ''
        user_input = '\n'.join(iter(input, sentinel))
        translated_list = user_input.split('\n')
        translated_list = [x.strip() for x in translated_list if x.strip()]
        try:
            assert len(translated_list) == len(list_chinese_not_yet_translated)
        except AssertionError:
            print('Translate list not equal')
            os.abort()
        for vietnamese, chinese in zip(translated_list, list_chinese_not_yet_translated):
            with open('translater/translater_dictionary_final.txt', 'a') as wf:
                vietnamese = re.sub(r'\.\s+', '.', vietnamese.strip())
                viscii = re.sub(r'\.\s+', '.', self.VISCII_converter.convert(vietnamese.strip()))
                wf.write(f'{chinese.strip()}\t\t\t{vietnamese}\t\t\t{viscii}\n')

    def lua_file_translate(self, input_path, output_path):
        print(f'Start processing {input_path}')
        list_chinese_not_yet_translated = []
        with open(input_path, 'rb') as f:
            text = f.read()

        # Define the regex pattern to match substrings between double quotes that contain Chinese characters
        pattern = re.compile(r'([\u4e00-\u9fff].[\u4e00-\u9fffa-zA-Z0-9（：）/.，。]*)')
        comments_pattern = re.compile(r'(--.+[\u4e00-\u9fff].+)\r')

        # Use the findall() method to extract all matches
        translated_file_data = ''
        is_finish_translate = True
        for line in text.decode('gb2312').split('\n'):
            if line.startswith('--') and '****' not in line:
                matches = comments_pattern.findall(line)
            else:
                matches = pattern.findall(line)
                for match in matches:
                    start_index = line.index(match)
                    if '--' in line[:start_index]:
                        start_index = line.index('--')
                        matches = matches[:matches.index(match)] + [line[start_index:].strip()]
                        break
            for match in matches:
                try:
                    line = line.replace(match, self.CURRENT_DICTIONARY[match])
                except KeyError as err:
                    is_finish_translate = False
                    list_chinese_not_yet_translated.append(err.args[0])
            translated_file_data += line

        if is_finish_translate:
            with open(output_path, 'w', encoding='cp1252', errors='ignore') as output_file_obj:
                output_file_obj.write(translated_file_data)

        if list_chinese_not_yet_translated:
            self.process_chinese([word for word in list_chinese_not_yet_translated if word.startswith('--')], 'CM')
            self.process_chinese([word for word in list_chinese_not_yet_translated if not word.startswith('--')], 'MSG')
            self.load_dictionary()
            return self.lua_file_translate(input_path, output_path)


if __name__ == '__main__':
    test = DictionaryProcessor()
    for file in os.listdir('input'):
        test.lua_file_translate(
            input_path=os.path.join('input', file),
            output_path=f'test/{file}'
        )
        input(f'Done {file}')

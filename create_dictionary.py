import re

from convert_unicode import Converter

from dictionary_processor import DictionaryProcessor

chinese_path = 'translater/chinese.txt'
chinese_comments_path = 'translater/chinese_comments.txt'
translated_path = 'translater/translated.txt'

chinese_word_batch = {}
vietnamese_translated_word_batch = {}
chinese_comments_word_batch = {}
VISCII_converter = Converter()
uuid_pattern = r"\b[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}\b"


# for chinese in open(chinese_path, 'r', encoding='utf-8'):
#     if not chinese.strip():
#         continue
#     chinese_word.append(chinese.strip())
#
def process_chinese_comments():
    current_batch_uuid = None
    for chinese_comments_line in open(chinese_comments_path, 'r', encoding='utf-8'):
        chinese_comments_line = chinese_comments_line.strip()
        if not chinese_comments_line:
            continue
        if chinese_comments_line.startswith('#'):
            uuid = re.search(uuid_pattern, chinese_comments_line)
            if uuid:
                current_batch_uuid = uuid.group()
                if uuid not in chinese_comments_word_batch:
                    chinese_comments_word_batch[current_batch_uuid] = []
        else:
            chinese_comments_word_batch[current_batch_uuid].append(chinese_comments_line.strip())


def process_chinese_word():
    current_batch_uuid = None
    for chinese_line in open(chinese_path, 'r', encoding='utf-8'):
        chinese_line = chinese_line.strip()
        if not chinese_line:
            continue
        if chinese_line.startswith('#'):
            uuid = re.search(uuid_pattern, chinese_line)
            if uuid:
                current_batch_uuid = uuid.group()
                if uuid not in chinese_word_batch:
                    chinese_word_batch[current_batch_uuid] = []
        else:
            chinese_word_batch[current_batch_uuid].append(chinese_line.strip())


def process_translated_dictionary():
    current_batch_uuid = None
    for line in open(translated_path, 'r', encoding='utf-8'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            uuid = re.search(uuid_pattern, line)
            if uuid:
                current_batch_uuid = uuid.group()
                if uuid not in vietnamese_translated_word_batch:
                    vietnamese_translated_word_batch[current_batch_uuid] = []
        else:
            vietnamese_translated_word_batch[current_batch_uuid].append(line.strip())

        # vietnamese_translated_word_batch.append(vietnamese.strip())


process_chinese_comments()
process_translated_dictionary()
process_chinese_word()
merge_chinese_word = {**chinese_word_batch, **chinese_comments_word_batch}
new_word = 0
with open('translater/translater_dictionary_final.txt', 'a') as wf:
    dict_worker = DictionaryProcessor()
    for uuid, list_word in merge_chinese_word.items():
        for chinese_word in list_word:
            if chinese_word not in dict_worker.CURRENT_DICTIONARY:
                new_word += 1
                vietnamese = re.sub(
                    r'\.\s+', '.',
                    vietnamese_translated_word_batch[uuid][list_word.index(chinese_word)].strip()
                )
                VISCII_vietnamese = re.sub(
                    r'\.\s+', '.',
                    VISCII_converter.convert(
                        vietnamese_translated_word_batch[uuid][list_word.index(chinese_word)].strip()
                    )
                )
                wf.write(f'{chinese_word.strip()}\t\t\t{vietnamese}\t\t\t{VISCII_vietnamese}\n')
print(f'New word count: {new_word}')
# for uuid, list_word in vietnamese_translated_word_batch.items():
#     print(uuid, list_word)
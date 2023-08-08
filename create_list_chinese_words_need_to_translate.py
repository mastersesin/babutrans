# with open('ai_hadaba_small.lua', 'rb') as file:
#     for line in file:
#         print(line.decode('gb2312').strip())

import jieba
import re

# Load a Chinese text file encoded in GB2312
with open('epiaomiaofeng_small.lua', 'rb') as f:
    text = f.read()

# Define the regex pattern to match substrings between double quotes that contain Chinese characters
pattern = re.compile(r'([\u4e00-\u9fff].[\u4e00-\u9fffa-zA-Z0-9（：）/.，。]*)')
comments_pattern = re.compile(r'(--.+)\r')
results = []
# Use the findall() method to extract all matches
for line in text.decode('gb2312').split('\n'):
    if line.startswith('--') and '****' not in line:
        matches = comments_pattern.findall(line)
    else:
        matches = pattern.findall(line)
        for match in matches:
            start_index = line.index(match)
            if '--' in line[:start_index]:
                start_index = line.index('--')
                matches = matches[:matches.index(match)] + [line[start_index:]]
                break
    results.extend(matches)
command = input('You want comments(c) or real_messages(r)')
count = 0
if command == 'c':
    for result in results:
        if result.startswith('--'):
            print(result)
            count += 1
    print(count)
if command == 'r':
    for result in results:
        if not result.startswith('--'):
            print(result)
            count += 1
    print(f'Count: {count}')

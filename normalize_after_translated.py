translated_file_path = 'translater/translated.txt'
for line in open(translated_file_path, 'r'):
    line = line.strip()
    if not line:
        continue
    print(line)

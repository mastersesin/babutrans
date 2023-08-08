import re

line = "tràng cảnh lượng biến đổi hướng dẫn tra cứu. . . . Kiểm tra xem có thể khiêu chiến cái nào đó BOSS tiêu ký. . . ."
normalized_line = re.sub(r'\.\s+', '.', line)

print(normalized_line)
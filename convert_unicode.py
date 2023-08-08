import re
import sys

patterns = {
    "UNICODE": [r'[Ạ-ỹ]', 0],
}


class Converter:
    """Convert qua lai giua mot so bang ma cua Vietnam"""

    def __init__(self):
        """Khoi tao"""

        self.UNICODE = ["À", "Á", "Â", "Ã", "È", "É", "Ê", "Ì", "Í", "Ò",
                        "Ó", "Ô", "Õ", "Ù", "Ú", "Ý", "à", "á", "â", "ã",
                        "è", "é", "ê", "ì", "í", "ò", "ó", "ô", "õ", "ù",
                        "ú", "ý", "Ă", "ă", "Đ", "đ", "Ĩ", "ĩ", "Ũ", "ũ",
                        "Ơ", "ơ", "Ư", "ư", "Ạ", "ạ", "Ả", "ả", "Ấ", "ấ",
                        "Ầ", "ầ", "Ẩ", "ẩ", "Ẫ", "ẫ", "Ậ", "ậ", "Ắ", "ắ",
                        "Ằ", "ằ", "Ẳ", "ẳ", "Ẵ", "ẵ", "Ặ", "ặ", "Ẹ", "ẹ",
                        "Ẻ", "ẻ", "Ẽ", "ẽ", "Ế", "ế", "Ề", "ề", "Ể", "ể",
                        "Ễ", "ễ", "Ệ", "ệ", "Ỉ", "ỉ", "Ị", "ị", "Ọ", "ọ",
                        "Ỏ", "ỏ", "Ố", "ố", "Ồ", "ồ", "Ổ", "ổ", "Ỗ", "ỗ",
                        "Ộ", "ộ", "Ớ", "ớ", "Ờ", "ờ", "Ở", "ở", "Ỡ", "ỡ",
                        "Ợ", "ợ", "Ụ", "ụ", "Ủ", "ủ", "Ứ", "ứ", "Ừ", "ừ",
                        "Ử", "ử", "Ữ", "ữ", "Ự", "ự", "Ỳ", "ỳ", "Ỵ", "ỵ",
                        "Ỷ", "ỷ", "Ỹ", "ỹ", "."]

        self.VISCII = ["À", "Á", "Â", "Ã", "È", "É", "Ê", "Ì", "Í", "Ò",
                       "Ó", "Ô", "õ", "Ù", "Ú", "Ý", "à", "á", "â", "ã",
                       "è", "é", "ê", "ì", "í", "ò", "ó", "ô", "õ", "ù",
                       "ú", "ý", "Å", "å", "Ð", "ð", "Î", "î", "", "û",
                       "´", "½", "¿", "ß", "€", "Õ", "Ä", "ä", "„", "¤",
                       "…", "¥", "†", "¦", "ç", "ç", "‡", "§", "", "í",
                       "‚", "¢", "Æ", "Æ", "Ç", "Ç", "ƒ", "£", "‰", "©",
                       "Ë", "ë", "ˆ", "¨", "Š", "ª", "‹", "«", "Œ", "¬",
                       "", "­", "Ž", "®", "›", "ï", "˜", "¸", "š", "÷",
                       "™", "ö", "", "¯", "", "°", "‘", "±", "’", "²",
                       "“", "µ", "•", "¾", "–", "¶", "—", "·", "³", "Þ",
                       "”", "þ", "ž", "ø", "œ", "ü", "º", "Ñ", "»", "×",
                       "¼", "Ø", "ÿ", "æ", "¹", "ñ", "Ÿ", "Ï", "Ü", "Ü",
                       "Ö", "Ö", "Û", "Û", "."]

    def convert(self, str_original, target_charset="VISCII", source_charset='UNICODE'):

        source_charset = getattr(self, source_charset)
        target_charset = getattr(self, target_charset)

        map_length = len(source_charset)
        for number in range(map_length):
            str_original = str_original.replace(source_charset[number], "::" + str(number) + "::")

        for number in range(map_length):
            str_original = str_original.replace("::" + str(number) + "::", target_charset[number])

        return str_original

    def detectCharset(self, str_input):
        for pattern in patterns:
            match = re.search(patterns[pattern][0], str_input, patterns[pattern][1])
            if (match != None):
                return pattern
        return None

# converter = Converter()
# print(converter.convert('-- Phiêu Miểu Phong phó bản'))

# if __name__ == "__main__":
#     if (len(sys.argv) < 2):
#         print("\tconverter.py [string] [target_charset] [source_charset]\n\
# \tSupported charset : \n\t\tTCVN3\n\t\tVNI_WIN\n\t\tVIQR\n\t\tUNICODE\n\t\tVISCII\n\t\tVPS_WIN\n\t\tVIETWARE_F\n\t\tVIETWARE_X")
#         exit()
#
#     str_original = sys.argv[1]
#     target_charset = sys.argv[2] if len(sys.argv) == 3 else "UNICODE"
#     source_charset = sys.argv[3] if len(sys.argv) == 4 else None
#
#     converter = Converter()
#     str_output = converter.convert(str_original, target_charset, source_charset)
#     print(str_output)

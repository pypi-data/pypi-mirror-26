from struct import pack, unpack

DEBUG = False
# NS_ANDROID_URI = 'http://schemas.android.com/apk/res/android'

# AXML FORMAT ########################################
# Translated from
# http://code.google.com/p/android4me/source/browse/src/android/content/res/AXmlResourceParser.java

UTF8_FLAG = 0x00000100
CHUNK_STRINGPOOL_TYPE = 0x001C0001
CHUNK_NULL_TYPE = 0x00000000


class StringBlock(object):

    def __init__(self, buff):
        self.start = buff.get_idx()
        self._cache = {}
        self.header_size, self.header = self.skipNullPadding(buff)

        self.chunkSize = unpack('<i', buff.read(4))[0]
        self.stringCount = unpack('<i', buff.read(4))[0]
        self.styleOffsetCount = unpack('<i', buff.read(4))[0]

        self.flags = unpack('<i', buff.read(4))[0]
        self.m_isUTF8 = ((self.flags & UTF8_FLAG) != 0)

        self.stringsOffset = unpack('<i', buff.read(4))[0]
        self.stylesOffset = unpack('<i', buff.read(4))[0]

        self.m_stringOffsets = []
        self.m_styleOffsets = []
        self.m_charbuff = ""
        self.m_styles = []

        for _ in range(0, self.stringCount):
            tmp = buff.read(4)
            if len(tmp) < 4:
                break
            self.m_stringOffsets.append(unpack('<i', tmp)[0])

        for _ in range(0, self.styleOffsetCount):
            tmp = buff.read(4)
            if len(tmp) < 4:
                break
            self.m_styleOffsets.append(unpack('<i', tmp)[0])

        if DEBUG:
            print('chunkSize:', self.chunkSize)
            print('chunkSize:', self.chunkSize)
            print('stringsOffset:', self.stringsOffset)
            print('stylesOffset:', self.stylesOffset)
        size = self.chunkSize - self.stringsOffset
        if self.stylesOffset != 0:
            size = self.stylesOffset - self.stringsOffset

        # if (size % 4) != 0:
        #     size = size & ~3
        #     print("ooo")

        self.m_charbuff = buff.read(size)

        if self.stylesOffset != 0:
            size = self.chunkSize - self.stylesOffset

            # if (size % 4) != 0:
            #     size = size & ~3

            for _ in range(0, int(size / 4) - 1):
                tmp = buff.read(4)
                if len(tmp) < 4:
                    break
                self.m_styles.append(unpack('<i', tmp)[0])

    def skipNullPadding(self, buff):

        def readNext(buff, first_run=True):
            header = unpack('<i', buff.read(4))[0]

            if header == CHUNK_NULL_TYPE and first_run:
                if DEBUG:
                    print("Skipping null padding in StringBlock header")
                header = readNext(buff, first_run=False)
            elif header != CHUNK_STRINGPOOL_TYPE:
                if DEBUG:
                    print("Invalid StringBlock header")

            return header

        header = readNext(buff)
        return header >> 8, header & 0xFF

    def getString(self, idx):
        if idx in self._cache:
            return self._cache[idx]

        if idx < 0 or not self.m_stringOffsets or idx >= len(
                self.m_stringOffsets):
            return ""

        offset = self.m_stringOffsets[idx]

        if self.m_isUTF8:
            self._cache[idx] = self.decode8(offset)
        else:
            self._cache[idx] = self.decode16(offset)

        return self._cache[idx]

    def getStyle(self, idx):
        # FIXME
        return self.m_styles[idx]

    def decode8(self, offset):
        str_len, skip = self.decodeLength(offset, 1)
        offset += skip

        encoded_bytes, skip = self.decodeLength(offset, 1)
        offset += skip

        data = self.m_charbuff[offset: offset + encoded_bytes]

        return self.decode_bytes(data, 'utf-8', str_len)

    def decode16(self, offset):
        str_len, skip = self.decodeLength(offset, 2)
        offset += skip

        encoded_bytes = str_len * 2

        data = self.m_charbuff[offset: offset + encoded_bytes]

        return self.decode_bytes(data, 'utf-16', str_len)

    def decode_bytes(self, data, encoding, str_len):
        string = data.decode(encoding, 'replace')
        if len(string) != str_len:
            raise Exception("invalid decoded string length")
        return string

    def decodeLength(self, offset, sizeof_char):
        length = self.m_charbuff[offset]

        sizeof_2chars = sizeof_char << 1
        fmt_chr = 'B' if sizeof_char == 1 else 'H'
        fmt = "<2" + fmt_chr

        length1, length2 = unpack(
            fmt, self.m_charbuff[offset:(offset + sizeof_2chars)])

        highbit = 0x80 << (8 * (sizeof_char - 1))

        if (length & highbit) != 0:
            return ((length1 & ~highbit) << (8 * sizeof_char)) | length2, sizeof_2chars
        return length1, sizeof_char

    def show(self):
        print(("StringBlock(%x, %x, %x, %x, %x, %x" % (
            self.start,
            self.header,
            self.header_size,
            self.chunkSize,
            self.stringsOffset,
            self.flags)))
        for i in range(0, len(self.m_stringOffsets)):
            print((i, repr(self.getString(i))))


class SV(object):

    def __init__(self, size, buff):
        self.__size = size
        self.__value = unpack(self.__size, buff)[0]

    def _get(self):
        return pack(self.__size, self.__value)

    def __str__(self):
        return "0x%x" % self.__value

    def __int__(self):
        return self.__value

    def get_value_buff(self):
        return self._get()

    def get_value(self):
        return self.__value

    def set_value(self, attr):
        self.__value = attr


class BuffHandle(object):

    def __init__(self, buff):
        self.__buff = buff
        self.__idx = 0

    def size(self):
        return len(self.__buff)

    def set_idx(self, idx):
        self.__idx = idx

    def get_idx(self):
        return self.__idx

    def readNullString(self, size):
        data = self.read(size)
        return data

    def read_b(self, size):
        return self.__buff[self.__idx:self.__idx + size]

    def read_at(self, offset, size):
        return self.__buff[offset:offset + size]

    def read(self, size):
        if isinstance(size, SV):
            size = size.value

        buff = self.__buff[self.__idx:self.__idx + size]
        self.__idx += size

        return buff

    def end(self):
        return self.__idx == len(self.__buff)


# ATTRIBUTE_IX_NAMESPACE_URI = 0
# ATTRIBUTE_IX_NAME = 1
# ATTRIBUTE_IX_VALUE_STRING = 2
# ATTRIBUTE_IX_VALUE_TYPE = 3
# ATTRIBUTE_IX_VALUE_DATA = 4
# ATTRIBUTE_LENGHT = 5
#
# CHUNK_AXML_FILE = 0x00080003
# CHUNK_RESOURCEIDS = 0x00080180
# CHUNK_XML_FIRST = 0x00100100
# CHUNK_XML_START_NAMESPACE = 0x00100100
# CHUNK_XML_END_NAMESPACE = 0x00100101
# CHUNK_XML_START_TAG = 0x00100102
# CHUNK_XML_END_TAG = 0x00100103
# CHUNK_XML_TEXT = 0x00100104
# CHUNK_XML_LAST = 0x00100104
#
# START_DOCUMENT = 0
# END_DOCUMENT = 1
# START_TAG = 2
# END_TAG = 3
# TEXT = 4
#
# RADIX_MULTS = [0.00390625, 3.051758E-005, 1.192093E-007, 4.656613E-010]
# DIMENSION_UNITS = ["px", "dip", "sp", "pt", "in", "mm"]
# FRACTION_UNITS = ["%", "%p"]
#
# COMPLEX_UNIT_MASK = 15

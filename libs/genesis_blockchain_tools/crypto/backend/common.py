from ...convert import int_to_hex_str
from .errors import UnknownPointFormatError

def point_to_hex_str(key, fmt='RAW'):
    hex_str = int_to_hex_str(key.x) + int_to_hex_str(key.y)
    if fmt == 'RAW':
        return hex_str
    elif fmt == '04':
        return '04' + hex_str
    else:
        raise UnknownPointFormatError("fmt: '%s'" % fmt)

def split_str_to_halves(s):
    return s[0:len(s)//2], s[len(s)//2 if len(s)%2 == 0 else ((len(s)//2)+1):]

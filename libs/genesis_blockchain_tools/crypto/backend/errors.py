class Error(Exception):
    pass

class UnknownFormatError(Error):
    pass

class UnknownPointFormatError(UnknownFormatError):
    pass

class UnknownPublicKeyFormatError(UnknownFormatError):
    pass

class UnknownSignatureFormatError(UnknownFormatError):
    pass

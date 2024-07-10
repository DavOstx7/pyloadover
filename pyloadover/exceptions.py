class SignatureError(Exception):
    pass


class SignatureExistsError(SignatureError):
    pass


class NoMatchingSignatureError(SignatureError):
    pass


class MultipleMatchingSignaturesError(SignatureError):
    pass


class NameMismatchError(NameError):
    pass


class NameNotFoundError(NameError):
    pass

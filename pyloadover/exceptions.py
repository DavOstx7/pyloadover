class SignatureError(Exception):
    pass


class SignatureExistsError(SignatureError):
    pass


class NoMatchingSignatureError(SignatureError):
    pass


class MultipleMatchingSignaturesError(SignatureError):
    pass


class NamespaceMismatchError(NameError):
    pass


class NamespaceNotFoundError(NameError):
    pass

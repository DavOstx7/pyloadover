class MatchError(Exception):
    pass


class NoMatchFoundError(MatchError):
    pass


class MultipleMatchesFoundError(MatchError):
    pass


class ValidationError(Exception):
    pass


class IdMismatchError(ValidationError):
    pass


class SignatureExistsError(ValidationError):
    pass

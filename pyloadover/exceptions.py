class MatchError(Exception):
    pass


class NoMatchFoundError(MatchError):
    pass


class MultipleMatchesFoundError(MatchError):
    pass


class GroupNotFoundError(Exception):
    pass


class ValidationError(Exception):
    pass


class IdMismatchError(ValidationError):
    pass


class SignatureDuplicationError(ValidationError):
    pass

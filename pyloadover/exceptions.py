class DuplicatedSignatureError(Exception):
    pass


class MatchError(Exception):
    pass


class NoMatchFoundError(MatchError):
    pass


class MultipleMatchesFoundError(MatchError):
    pass


class MismatchedIdError(Exception):
    pass


class GroupNotFoundError(Exception):
    pass

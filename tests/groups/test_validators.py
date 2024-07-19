import pytest

from pyloadover.groups.validators import EqualIdsValidator, UniqueSignaturesValidator
from pyloadover.exceptions import IdMismatchError, SignatureExistsError


def test_equal_id_validator_ids_match(mock_group_context, mock_function, random_string):
    validator = EqualIdsValidator()
    mock_group_context.id = random_string
    mock_function.id = random_string

    validator.validate_function(mock_group_context, mock_function)


def test_equal_id_validator_ids_mismatch(mock_group_context, mock_function, random_string):
    validator = EqualIdsValidator()
    mock_group_context.id = random_string
    mock_function.id = f"!{random_string}!"

    with pytest.raises(IdMismatchError):
        validator.validate_function(mock_group_context, mock_function)


def test_unique_signature_validator_signature_not_exists(mock_group_context, mock_function, random_string):
    validator = UniqueSignaturesValidator()
    mock_group_context.is_signature_exists.return_value = False

    validator.validate_function(mock_group_context, mock_function)


def test_unique_signature_validator_signature_exists(mock_group_context, mock_function, random_string):
    validator = UniqueSignaturesValidator()
    mock_group_context.is_signature_exists.return_value = True

    with pytest.raises(SignatureExistsError):
        validator.validate_function(mock_group_context, mock_function)

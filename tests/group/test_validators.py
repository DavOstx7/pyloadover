from unittest.mock import MagicMock

import pytest
from pyloadover.groups.validators import EqualIdsValidator, UniqueSignaturesValidator
from pyloadover.groups.context import GroupContext, Function
from pyloadover.exceptions import IdMismatchError, SignatureDuplicationError


def test_equal_id_validator_ids_match(random_string):
    validator = EqualIdsValidator()
    mock_group_context = MagicMock(spec_set=GroupContext)
    mock_group_context.id = random_string
    mock_function = MagicMock(spec_set=Function)
    mock_function.id = random_string

    validator.validate(mock_group_context, mock_function)


def test_equal_id_validator_ids_mismatch(random_string):
    validator = EqualIdsValidator()
    mock_group_context = MagicMock(spec_set=GroupContext)
    mock_group_context.id = random_string
    mock_function = MagicMock(spec_set=Function)
    mock_function.id = f"!{random_string}!"

    with pytest.raises(IdMismatchError):
        validator.validate(mock_group_context, mock_function)


def test_unique_signature_validator_signature_not_exists(random_string):
    validator = UniqueSignaturesValidator()
    mock_group_context = MagicMock(spec_set=GroupContext)
    mock_group_context.is_signature_exists.return_value = False
    mock_function = MagicMock(spec_set=Function)

    validator.validate(mock_group_context, mock_function)


def test_unique_signature_validator_signature_exists(random_string):
    validator = UniqueSignaturesValidator()
    mock_group_context = MagicMock(spec_set=GroupContext)
    mock_group_context.is_signature_exists.return_value = True
    mock_function = MagicMock(spec_set=Function)

    with pytest.raises(SignatureDuplicationError):
        validator.validate(mock_group_context, mock_function)

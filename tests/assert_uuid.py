from typing import Any, Dict, Type

from newnewid import UUID
from newnewid.uuidgenerator.uuid_generator import UUIDGenerator


def _get_diff(actual: Dict[str, Any], expected: Dict[str, Any]) -> Dict[str, Any]:
    diff = {}
    for key, value in expected.items():
        assert key in actual

        if actual[key] != value:
            diff[key] = {
                "actual": actual[key],
                "expected": value,
            }

    return diff


def assert_uuid(
    actual: UUID,
    expected: UUID,
    generator_class: Type[UUIDGenerator],
    **kwargs: Any,
) -> None:
    if actual == expected:
        return

    actual_dict = generator_class.parse(actual, **kwargs)
    expected_dict = generator_class.parse(expected, **kwargs)
    diff = _get_diff(actual_dict, expected_dict)

    assert (
        actual == expected
    ), f"""
    diff    : {diff}
    actual  : {actual_dict}
    expected: {expected_dict}
    """

from datetime import datetime, timezone
from typing_extensions import cast

from ifdo._datetime import check_datetime_format


def test_check_datatime_default() -> None:
    # Matching the default format: string is converted to datetime
    matching_data = {
        "image-set-header": {
            "image-datetime": "2015-01-01 02:04:03.1000",
        }
    }
    check_datetime_format(matching_data)
    assert matching_data["image-set-header"]["image-datetime"] == datetime(
        2015, 1, 1, 2, 4, 3, 100000, tzinfo=timezone.utc
    )

    # Non-matching string (no microseconds): left as-is for Pydantic to handle
    fallback_data = {
        "image-set-header": {
            "image-datetime": "2015-01-01 02:04:03",
        }
    }
    check_datetime_format(fallback_data)
    assert fallback_data["image-set-header"]["image-datetime"] == "2015-01-01 02:04:03"


def test_check_datetime_images() -> None:
    # Matching format: string is converted to datetime
    matching_data = {
        "image-set-header": {
            "image-datetime": "2015-01-01T20:21:32",
            "image-datetime-format": "%Y-%m-%dT%H:%M:%S",
        },
        "image-set-items": {"image": {"image-datetime": "2015-01-01T20:21:32"}},
    }
    check_datetime_format(matching_data)
    assert cast(dict[str, dict[str, dict[str, str]]], matching_data["image-set-items"])["image"][
        "image-datetime"
    ] == datetime(2015, 1, 1, 20, 21, 32, tzinfo=timezone.utc)

    # Non-matching string: left as-is for Pydantic to handle (backwards-compat fallback)
    fallback_data = {
        "image-set-header": {
            "image-datetime": "2015-01-01T20:21:32",
            "image-datetime-format": "%Y-%m-%dT%H:%M:%S",
        },
        "image-set-items": {"image": {"image-datetime": "2015-01-01 20:21:32"}},
    }
    check_datetime_format(fallback_data)
    assert (
        cast(dict[str, dict[str, str]], fallback_data["image-set-items"])["image"]["image-datetime"]
        == "2015-01-01 20:21:32"
    )


def test_check_datetime_videos() -> None:
    # Matching format: first frame's format inherited by subsequent frames
    matching_data = {
        "image-set-header": {},
        "image-set-items": {
            "image": [
                {
                    "image-datetime-format": "%Y-%m-%dT%H:%M:%S",
                    "image-datetime": "2015-01-01T20:21:32",
                },
                {"image-datetime": "2015-01-01T20:21:32"},
            ]
        },
    }
    check_datetime_format(matching_data)
    assert matching_data["image-set-items"]["image"][1]["image-datetime"] == datetime(
        2015, 1, 1, 20, 21, 32, tzinfo=timezone.utc
    )

    # Non-matching string on subsequent frame: left as-is for Pydantic to handle
    fallback_data = {
        "image-set-header": {},
        "image-set-items": {
            "image": [
                {
                    "image-datetime-format": "%Y-%m-%dT%H:%M:%S",
                    "image-datetime": "2015-01-01T20:21:32",
                },
                {"image-datetime": "2015-01-01 20:21:32"},
            ]
        },
    }
    check_datetime_format(fallback_data)
    assert fallback_data["image-set-items"]["image"][1]["image-datetime"] == "2015-01-01 20:21:32"

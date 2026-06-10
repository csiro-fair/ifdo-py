import contextlib
from datetime import datetime, timezone
from typing import Any

from ._format import DEFAULT_DATETIME_FORMAT


def check_datetime_format(ifdo_data: dict[str, Any]) -> None:
    if "image-set-header" not in ifdo_data:
        return
    image_set_header = ifdo_data["image-set-header"]

    header_datetime_format = _check_image_item(
        image_set_header,
        DEFAULT_DATETIME_FORMAT,
    )

    if "image-set-items" not in ifdo_data:
        return

    for item in ifdo_data["image-set-items"].values():
        if isinstance(item, dict):
            _check_image_item(item, header_datetime_format)
        else:
            _check_video_item(item, header_datetime_format)


def _check_video_item(items: list[dict[str, Any]], header_format: str) -> None:
    if len(items) == 0:
        return

    prefix_format = _check_image_item(items[0], header_format)
    for item in items[1:]:
        _check_image_item(item, prefix_format)


def _check_image_item(item: dict[str, Any], header_format: str) -> str:
    datetime_format: str = item.get("image-datetime-format", header_format)

    if "image-datetime" in item:
        with contextlib.suppress(ValueError, TypeError):
            item["image-datetime"] = datetime.strptime(
                item["image-datetime"],
                datetime_format,
            ).replace(tzinfo=timezone.utc)

    return datetime_format

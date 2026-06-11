import json
from typing import Any, cast

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from datetime import datetime

from ifdo import iFDO, ImageData, ImageSetHeader, RelatedMaterial
from ifdo.models import ImageContext, ImageCreator, ImageLicense, ImagePI


def test_related_material_and_new_header_fields_serialise_and_validate() -> None:
    ifdo = _base_ifdo()
    header = ifdo.image_set_header
    header.image_set_related_material = [
        RelatedMaterial(
            uri="https://doi.org/10.1016/j.softx.2025.102251",
            title="Marimba",
            relation="The software used to produce this image set",
        ),
    ]
    header.image_set_min_latitude_degrees = -33.9
    header.image_set_max_latitude_degrees = -33.1
    header.image_set_min_longitude_degrees = 151.1
    header.image_set_max_longitude_degrees = 151.9
    header.image_visual_constraints = "Occasional turbidity reduces visibility."

    result = ifdo.to_dict()
    out_header = result["image-set-header"]
    assert out_header["image-set-related-material"] == [
        {
            "uri": "https://doi.org/10.1016/j.softx.2025.102251",
            "title": "Marimba",
            "relation": "The software used to produce this image set",
        },
    ]
    assert out_header["image-set-min-latitude-degrees"] == -33.9
    assert out_header["image-set-max-longitude-degrees"] == 151.9
    assert out_header["image-visual-constraints"] == "Occasional turbidity reduces visibility."

    _validate_ifdo(ifdo)


def test_renamed_fields_serialise_with_schema_spelling() -> None:
    image = ImageData(image_latitude=0.0, image_longitude=0.0)
    image.image_area_square_meters = 4.2
    image.image_time_synchronisation = "NTP, +0.3s offset to UTC"
    image.image_mpeg7_colorstatistic = [1.0, 2.0]
    image.image_mpeg7_homogeneoustexture = [3.0, 4.0]

    out = image.model_dump(by_alias=True, exclude_none=True)
    assert "image-area-square-meters" in out
    assert "image-time-synchronisation" in out
    assert "image-mpeg7-colorstatistic" in out
    assert "image-mpeg7-homogeneoustexture" in out
    # The legacy misspellings must not appear in output.
    assert "image-area-square-meter" not in out
    assert "image-mpeg7-colorstatistics" not in out
    assert "image-mpeg7-homogenoustexture" not in out
    assert "image-time-synchronization" not in out


def test_legacy_field_spellings_still_load() -> None:
    # Files written by ifdo-py < 1.6.0 use the legacy spellings; they must still load
    # and re-serialise to the schema-correct keys.
    image = ImageData.model_validate(
        {
            "image-area-square-meter": 4.2,
            "image-time-synchronization": "legacy",
            "image-mpeg7-colorstatistics": [1.0],
            "image-mpeg7-homogenoustexture": [2.0],
        },
    )
    assert image.image_area_square_meters == 4.2
    assert image.image_time_synchronisation == "legacy"
    assert image.image_mpeg7_colorstatistic == [1.0]
    assert image.image_mpeg7_homogeneoustexture == [2.0]

    out = image.model_dump(by_alias=True, exclude_none=True)
    assert "image-area-square-meters" in out
    assert "image-mpeg7-colorstatistic" in out


def _base_ifdo() -> iFDO:
    ifdo = iFDO(
        image_set_header=ImageSetHeader(
            image_set_name="Test set",
            image_set_uuid="f840644a-fe4a-46a7-9791-e32c211bcbf5",
            image_set_handle="https://hdl.handle.net/20.500.12085/f840644a-fe4a-46a7-9791-e32c211bcbf5",
        ),
        image_set_items={},
    )
    # Populate the header fields the schema marks as required.
    header = ifdo.image_set_header
    header.image_datetime = datetime(2025, 1, 1, 1, 1, 1, 100000)
    header.image_latitude = -33.5
    header.image_longitude = 151.5
    header.image_altitude_meters = 1.0
    header.image_coordinate_reference_system = "WGS84"
    header.image_coordinate_uncertainty_meters = 0.1
    header.image_context = ImageContext(name="Image context")
    header.image_project = ImageContext(name="Image project")
    header.image_event = ImageContext(name="Image event")
    header.image_platform = ImageContext(name="Image platform")
    header.image_sensor = ImageContext(name="Image sensor")
    header.image_pi = ImagePI(name="Image PI")
    header.image_creators = [ImageCreator(name="Image creator")]
    header.image_license = ImageLicense(name="CC-BY")
    header.image_copyright = "Copyright (C)"
    header.image_abstract = "Test abstract."
    return ifdo


def _validate_ifdo(ifdo: iFDO) -> None:
    schema = _load_json("tests/schema/ifdo.json")
    registry = Registry().with_resources(
        [
            (
                "http://hdl.handle.net/20.500.12085/92a7fabf-3b11-498d-85af-d90d90a1ee07",
                Resource.from_contents(_load_json("tests/schema/provenance.json")),
            ),
            (
                "http://hdl.handle.net/20.500.12085/dc57e639-4cf8-4f9a-982b-0cbb32366372",
                Resource.from_contents(_load_json("tests/schema/annotation.json")),
            ),
        ],
    )
    Draft202012Validator(schema, registry=registry).validate(ifdo.to_dict())


def _load_json(filepath: str) -> dict[str, Any]:
    with open(filepath) as file:
        return cast(dict[str, Any], json.load(file))

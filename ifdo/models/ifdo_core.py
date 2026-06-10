"""
Define and implement the Image FAIR Digital Object (iFDO) specification for the core section.

Classes:
    ImagePI: Represents an image Principal Investigator.
    ImageCreator: Represents an image creator.
    ImageContext: Represents an image context.
    ImageLicense: Represents an image license.
"""

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_serializer

from ifdo._datetime._format import DEFAULT_DATETIME_FORMAT


class ImagePI(BaseModel):
    """
    Represent an image PI (Principal Investigator) with associated information.

    This class models an image PI, typically used in scientific or research contexts where images are associated with
    a principal investigator. It stores the PI's name and ORCID (Open Researcher and Contributor ID) for proper
    attribution and identification.

    Attributes:
        name (str): The full name of the principal investigator.
        uri (str): A URI pointing to details of the PI. Could be an ORCID URI.
    """

    name: str
    uri: str | None = None


class ImageCreator(BaseModel):
    """
    Represent an image creator with associated information.

    This class models an image creator, typically used in scientific or research contexts where images are associated
    with image creators. It stores the creator's name and ORCID (Open Researcher and Contributor ID) for proper
    attribution and identification.

    Attributes:
        name (str): The full name of the image creator.
        uri (str): A URI pointing to details of the image creator. Could be an ORCID URI.
    """

    name: str
    uri: str | None = None


class ImageContext(BaseModel):
    """
    Represent a context within the ifdo model framework.

    This class defines a context, which is a common component in the ifdo model system. It encapsulates information
    about a named entity, optionally associated with a URI.

    Attributes:
        name (str): The name of the context.
        uri (str | None): An optional URI associated with the context. Defaults to None.
    """

    name: str
    uri: str | None = None

    def __hash__(self) -> int:
        return hash((self.name, self.uri))


class ImageLicense(BaseModel):
    """
    Represent a software license.

    This class models a software license, typically used in software development and distribution. It stores
    the name of the license and optionally its URI (Uniform Resource Identifier).

    Attributes:
        name (str): The name of the license (e.g., "CC BY 4.0", "CC BY-NC 4.0", "CC BY-NC-ND 4.0").
        uri (str | None): The URI of the license text or details, if available. Defaults to None.
    """

    name: str
    uri: str | None = None

    def __hash__(self) -> int:
        return hash((self.name, self.uri))


class ImageCoreFields(BaseModel):
    """Core metadata fields for iFDO objects."""

    image_datetime: datetime | None = None
    image_datetime_format: str | None = None
    image_latitude: float | None = Field(None, ge=-90, le=90)
    image_longitude: float | None = Field(None, ge=-180, le=180)
    image_altitude_meters: float | None = None
    image_coordinate_reference_system: str | None = None
    image_coordinate_uncertainty_meters: float | None = None
    image_context: ImageContext | None = None
    image_project: ImageContext | None = None
    image_event: ImageContext | None = None
    image_platform: ImageContext | None = None
    image_sensor: ImageContext | None = None
    image_pi: ImagePI | None = None
    image_creators: list[ImageCreator] | None = Field(None, min_length=1)
    image_license: ImageLicense | None = None
    image_copyright: str | None = None
    image_abstract: str | None = None
    image_set_local_path: str | None = None

    @field_serializer("image_datetime", when_used="json")
    def _serialize_image_datetime(self, image_datetime: datetime | None) -> str | None:
        if image_datetime is None:
            return None

        datetime_format = getattr(
            self,
            "_image_datetime_format",
            DEFAULT_DATETIME_FORMAT,
        )

        if image_datetime.tzinfo is not None:
            image_datetime = image_datetime.astimezone(timezone.utc)

        if datetime_format is not None and datetime_format != "":
            return image_datetime.strftime(datetime_format)
        return None

<a name="readme-top"></a>

<div align="center">

# ifdo-py

<i>A Python library for creating, validating and manipulating iFDO (image FAIR Digital Object) metadata files</i>

[![Python Versions](https://img.shields.io/pypi/pyversions/ifdo)](https://pypi.org/project/ifdo/) [![PyPI Version](https://img.shields.io/pypi/v/ifdo)](https://pypi.org/project/ifdo/) [![PyPI Downloads](https://img.shields.io/pypi/dm/ifdo)](https://pypi.org/project/ifdo/) [![Pull Requests](https://img.shields.io/github/issues-pr/csiro-fair/ifdo-py)](https://github.com/csiro-fair/ifdo-py/pulls) [![Issues](https://img.shields.io/github/issues/csiro-fair/ifdo-py)](https://github.com/csiro-fair/ifdo-py/issues) [![Contributors](https://img.shields.io/github/contributors/csiro-fair/ifdo-py?color=2b9348)](https://github.com/csiro-fair/ifdo-py/graphs/contributors) [![License](https://img.shields.io/github/license/csiro-fair/ifdo-py?color=2b9348)](https://github.com/csiro-fair/ifdo-py/blob/main/LICENSE) [![Tests](https://github.com/csiro-fair/ifdo-py/actions/workflows/tests.yaml/badge.svg)](https://github.com/csiro-fair/ifdo-py/actions/workflows/tests.yaml)

</div>

---

## Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Citation](#citation)
- [Acknowledgments](#acknowledgments)

---

<a name="overview"></a>
## Overview

ifdo-py is a Python library for working with [iFDO](https://ifdo-schema.org/) (image FAIR Digital Object) files, the metadata standard for [FAIR marine imagery](https://marine-imaging.com/fair/ifdos/iFDO-overview/). It provides a fully typed [Pydantic](https://docs.pydantic.dev/) data model covering the iFDO core, capture, and content sections, with validation, controlled-vocabulary enumerations, and round-trip serialization between Python objects and iFDO YAML or JSON files.

The library currently implements **iFDO v2.2.1** and is developed collaboratively by [CSIRO](https://www.csiro.au/), [MBARI](https://www.mbari.org/) and [AWI](https://www.awi.de/). It serves as the iFDO layer for the [Marimba](https://github.com/csiro-fair/marimba) framework for structuring, processing, packaging and distributing FAIR scientific image datasets.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<a name="installation"></a>
## Installation

```bash
pip install ifdo
```

Requires Python 3.10 or newer.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<a name="usage"></a>
## Usage

### Read and write iFDO files

```python
from ifdo import iFDO

# Read from a YAML or JSON file (.yaml, .yml, or .json)
ifdo_object = iFDO.load("ifdo.yaml")

# Write back out in either format
ifdo_object.save("ifdo.json")
```

### Create an iFDO from scratch

```python
from datetime import datetime, timezone

from ifdo import iFDO
from ifdo.models import (
    ImageAcquisition,
    ImageContext,
    ImageCreator,
    ImageData,
    ImageIllumination,
    ImageLicense,
    ImageMarineZone,
    ImagePI,
    ImageSetHeader,
)

header = ImageSetHeader(
    image_set_name="SO268-1_21-1_OFOS",
    image_set_uuid="f840644a-fe4a-46a7-9791-e32c211bcbf5",
    image_set_handle="https://hdl.handle.net/20.500.12085/f840644a-fe4a-46a7-9791-e32c211bcbf5",
    image_context=ImageContext(name="SO268 cruise"),
    image_pi=ImagePI(name="Jane Doe", uri="https://orcid.org/0000-0000-0000-0000"),
    image_creators=[ImageCreator(name="Jane Doe")],
    image_license=ImageLicense(name="CC BY 4.0", uri="https://creativecommons.org/licenses/by/4.0/"),
)

image = ImageData(
    image_datetime=datetime(2019, 3, 4, 8, 37, 24, tzinfo=timezone.utc),
    image_latitude=-42.123,
    image_longitude=145.456,
    image_altitude_meters=-4130.5,
    image_acquisition=ImageAcquisition.PHOTO,
    image_illumination=ImageIllumination.ARTIFICIAL_LIGHT,
    image_marine_zone=ImageMarineZone.SEAFLOOR,
)

ifdo_object = iFDO(image_set_header=header, image_set_items={"image_0001.jpg": image})
ifdo_object.save("ifdo.yaml")
```

Field names are written in the iFDO kebab-case convention, and the output declares the iFDO version and schema it conforms to:

```yaml
image-set-header:
  image-context:
    name: SO268 cruise
  image-pi:
    name: Jane Doe
    uri: https://orcid.org/0000-0000-0000-0000
  image-creators:
  - name: Jane Doe
  image-license:
    name: CC BY 4.0
    uri: https://creativecommons.org/licenses/by/4.0/
  image-set-name: SO268-1_21-1_OFOS
  image-set-uuid: f840644a-fe4a-46a7-9791-e32c211bcbf5
  image-set-handle: https://hdl.handle.net/20.500.12085/f840644a-fe4a-46a7-9791-e32c211bcbf5
  image-set-ifdo-version: v2.2.1
image-set-items:
  image_0001.jpg:
    image-acquisition: photo
    image-illumination: artificial light
    image-marine-zone: seafloor
    image-datetime: '2019-03-04 08:37:24.000000'
    image-latitude: -42.123
    image-longitude: 145.456
    image-altitude-meters: -4130.5
$schema: http://hdl.handle.net/20.500.12085/22aba7d7-c432-49ab-bebe-ee8ed4f70150
```

Videos are supported by assigning a list of `ImageData` objects to an item, one entry per point in time, as specified by the iFDO standard.

### Create image annotations

```python
from datetime import datetime, timezone

from ifdo.models import AnnotationLabel, ImageAnnotation, ImageData

# Create a label
label = AnnotationLabel(
    label="fish",
    annotator="Jane Doe",
    created_at=datetime(2026, 6, 10, tzinfo=timezone.utc),
    confidence=0.9,
)

# Pack it into a rectangle annotation with a flat list of x/y coordinates
annotation = ImageAnnotation(
    coordinates=[0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0],
    labels=[label],
    shape="rectangle",
)

image = ImageData(image_annotations=[annotation])
```

### Validation

All models are Pydantic models, so values are validated at construction time: latitudes and longitudes are range-checked, controlled-vocabulary fields only accept their iFDO enumeration values, and structural constraints from the iFDO schema (such as the 9-element stereo rotation matrix or the at-least-one-entry rule for `image-creators`) are enforced before anything is written to disk.

```python
from ifdo.models import ImageData

ImageData(image_latitude=120.0)  # raises pydantic.ValidationError: latitude must be <= 90
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<a name="documentation"></a>
## Documentation

- [iFDO standard documentation](https://ifdo-schema.org/) including the [field reference](https://ifdo-schema.org/standard/v2.2.1/documentation/iFDO-structure/) and [changelog](https://ifdo-schema.org/standard/v2.2.1/changelog/)
- [FAIR marine images overview](https://marine-imaging.com/fair/ifdos/iFDO-overview/)
- [Marimba](https://github.com/csiro-fair/marimba), a framework that uses ifdo-py to produce FAIR image datasets

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<a name="contributing"></a>
## Contributing

Contributions are welcome! Please see the [Contributing Guide](.github/CONTRIBUTING.md) for details on the development workflow, code standards, and pull request process.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<a name="license"></a>
## License

This project is licensed under the [MIT License](LICENSE).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<a name="contact"></a>
## Contact

- **Chris Jackett** - CSIRO - chris.jackett@csiro.au
- **Kevin Barnard** - MBARI - kbarnard@mbari.org
- **Karsten Schimpf** - AWI - karsten.schimpf@awi.de

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<a name="citation"></a>
## Citation

If you use ifdo-py in your work, please cite the iFDO standard:

Schoening, T., Durden, J. M., Faber, C., Felden, J., Heger, K., Hoving, H. J. T., Kiko, R., Köser, K., Krämmer, C., Kwasnitschka, T., Möller, K. O., Nakath, D., Naß, A., Nattkemper, T. W., Purser, A., & Zurowietz, M. (2022). Making marine image data FAIR. *Scientific Data*, 9, 414. https://doi.org/10.1038/s41597-022-01491-3

```bibtex
@article{schoening2022ifdo,
  title={Making marine image data FAIR},
  author={Schoening, Timm and Durden, Jennifer M and Faber, Claas and Felden, Janine and Heger, Karl and Hoving, Henk-Jan T and Kiko, Rainer and K{\"o}ser, Kevin and Kr{\"a}mmer, Christiane and Kwasnitschka, Tom and M{\"o}ller, Klas Ove and Nakath, David and Na{\ss}, Andrea and Nattkemper, Tim W and Purser, Autun and Zurowietz, Martin},
  journal={Scientific Data},
  volume={9},
  pages={414},
  year={2022},
  publisher={Nature Publishing Group},
  doi={10.1038/s41597-022-01491-3}
}
```

A citation file for the ifdo-py software itself is available via the "Cite this repository" button on GitHub.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<a name="acknowledgments"></a>
## Acknowledgments

ifdo-py is developed collaboratively by [CSIRO](https://www.csiro.au/) (Commonwealth Scientific and Industrial Research Organisation, Australia), [MBARI](https://www.mbari.org/) (Monterey Bay Aquarium Research Institute, USA) and [AWI](https://www.awi.de/) (Alfred Wegener Institute, Germany). The iFDO standard is developed by the [Marine Imaging community](https://marine-imaging.com/).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

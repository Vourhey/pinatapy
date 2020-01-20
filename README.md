# Non-official Pinata.cloud library

For more information about [Pinata.cloud](pinata.cloud) go to the official [documentation](https://pinata.cloud/documentation#GettingStarted)

## Warning

It's experimental development for my own purpose. Probably I'll finish error handling, add comments and publish it on PyPi.
But at the moment use it as it is. In the end it's just a hundred of lines =)

`options` doesn't work yet

## Installation

```
pip install -i https://test.pypi.org/simple/ pinatapy-vourhey
```

## Usage

```
from pinatapy import PinataPy
pinata = PinataPy(<pinata_api_key>, <pinata_secret_api_key>)
```

Look at the `__init__.py` file to find out about api calls

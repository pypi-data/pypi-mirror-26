# stylelens-search
This is a API document for Image search on fashion items"

- API version: 0.0.1
- Package version: 1.0.0

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com//.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com//.git`)

Then import the package:
```python
import stylelens_search 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import stylelens_search
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import stylelens_search
from stylelens_search.rest import ApiException
from pprint import pprint
# create an instance of the API class
api_instance = stylelens_search.SearchApi()
file = '/path/to/file.txt' # file | Image file to upload (only support jpg format yet) (optional)

try:
    # Query to search images
    api_response = api_instance.search_image(file=file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SearchApi->search_image: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://search.stylelens.io*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*SearchApi* | [**search_image**](docs/SearchApi.md#search_image) | **POST** /images | Query to search images


## Documentation For Models

 - [Image](docs/Image.md)
 - [ImageSearchResponse](docs/ImageSearchResponse.md)
 - [ImageSearchResponseData](docs/ImageSearchResponseData.md)
 - [ImagesArray](docs/ImagesArray.md)


## Documentation For Authorization


## api_key

- **Type**: API key
- **API key parameter name**: api_key
- **Location**: HTTP header


## Author

devops@bluehack.net


# dynamat2050
A python library for accessing data from Dynamat2050

## Installation
```
pip install dynamat2050
```

## Usage

There are two commands.

`dynamat_meters` returns a list of meters (optionally writing to a file "meters.json").

`dynamat_data` downloads data into a file.

Both commands require a path to a valid json-formatted config file to be specified as the first parameter.

{
  "username": "your username",
  "password": "your password",
  "url": "https://subdomain.dynamat2050.com/ProductService.svc"
}

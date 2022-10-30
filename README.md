*BayanAddress* is a Python-based address parser for Philippines. It analyzes user-provided address strings and identifies the building unit, subdivision, street, barangay, city, province, and zip code. It's also able to identify the island group (Luzon, Visayas, and Mindanao), ISO code, and region based on its province.

## Installation
```
$ python -m pip install bayan-address
```

## How to Use
```python
>>> from bayan_address import parse
>>>
>>> parse("95 JayLee Street Sofia Subdivision Del Pilar San Fernando City Pampanga 2000")
{
  'province': 'Pampanga',
  'zip_code': '2000',
  'city': 'San Fernando City',
  'street': 'JayLee Street',
  'building': '95',
  'subdivision': 'Sofia Subdivision',
  'barangay': 'Del Pilar',
  'iso': 'PH-PAM',
  'region': 'III',
  'island_group': 'Luzon'
}
```

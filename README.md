# BayanAddress
*BayanAddress* is a Python-based address parser for Philippines. It analyzes user-provided address strings and identifies the building unit, subdivision, street, barangay, city, province, and zip code. It can also identify the island group (Luzon, Visayas, and Mindanao), ISO code, and region based on its province.

## Installation
```bash
$ python -m pip install bayan-address
```

## How to Use
With province:
```python
>>> from bayan_address import parse
>>> parse("95 JayLee Street Sofia Subdivision Del Pilar San Fernando City Pampanga 2000")
{'province': 'Pampanga', 'iso': 'PH-PAM', 'region': 'III', 'island_group': 'Luzon', 'zip_code': '2000', 'city': 'San Fernando City', 'street': 'JayLee Street', 'building': '95', 'subdivision': 'Sofia Subdivision', 'barangay': 'Del Pilar'}
```
Without province:
```python
>>> parse("34 Avocado St., Brgy. Maligaya, Mariveles")
{'city': 'Mariveles', 'street': 'Avocado St.', 'building': '34', 'barangay': 'Brgy. Maligaya'}
```

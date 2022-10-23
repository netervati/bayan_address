*BayanAddress* is a Python-based address parser for Philippines. It analyzes user-provided address string and identifies the building unit, subdivision, street, barangay, city, province, and zip code. It's also able to identify the island group (Luzon, Visayas, and Mindanao), ISO code, and region based on its province.

## How to Use
```python
>>> from bayan_address import parse
>>> parse("95 JayLee Street Sofia Subdivision Del Pilar San Fernando City Pampanga 2000")
{
  'street': '95 JayLee Street', 
  'subdivision': 'Sofia Subdivision', 
  'barangay': 'Del Pilar', 
  'city': 'San Fernando City', 
  'island_group': 'Luzon',
  'iso': 'PH-PAM',
  'province': 'Pampanga', 
  'region': 'III',
  'zip_code': '2000'
}
```

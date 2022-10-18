*bayan_address* is a Python-based address parser for Philippines. It analyzes user-provided address strings and identifies the building units, subdivisions, streets, barangays, cities, provinces, and zip codes. It's also able to identify the island group (Luzon, Visayas, and Mindanao) and region of the address based on its province.

The project is still in its early development stage and it's only able to parse comma-separated addresses.

## How to Use
```python
>>> from bayan_address import Parser
>>> address = Parser("95 JayLee Street, Sofia Subdivision, Del Pilar, San Fernando City, Pampanga, 2000")
>>> address.parsed_address
{
  'street': '95 JayLee Street', 
  'subdivision': 'Sofia Subdivision', 
  'barangay': 'Del Pilar', 
  'city': 'San Fernando City', 
  'province': 'Pampanga', 
  'zip_code': '2000'
}
```
To directly access the value based on the address type, simply call the attribute:
```python
>>> address.barangay
'Del Pilar'
>>> address.province
'Pampanga'
```

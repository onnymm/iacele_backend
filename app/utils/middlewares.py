import re
from typing import Any

# Función para convertir camelCase a snake_case
def _camel_to_snake(name: str) -> str:
    return re.sub(r'([A-Z])', r'_\1', name).lower()

# Función para convertir snake_case a camelCase
def _snake_to_camel(name: str) -> str:
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), name)

# Función recursiva para convertir llaves a snake case
def convert_keys_to_snake_case(data):
    if isinstance(data, dict):
        return { _camel_to_snake(key): convert_keys_to_snake_case(value) for ( key, value ) in data.items() }
    elif isinstance(data, list):
        return [ convert_keys_to_snake_case(i) for i in data ]
    return data

# Función recursiva para convertir llaves a camel case
def convert_keys_to_camel_case(data):
    if isinstance(data, dict):
        return { _snake_to_camel(key): convert_keys_to_camel_case(value) for ( key, value ) in data.items() }
    elif isinstance(data, list):
        return [ convert_keys_to_camel_case(i) for i in data ]
    return data

def is_json_like(json_data: Any) -> bool:
    return isinstance(json_data, dict) or isinstance(json_data, list)

def is_open_api_response(json_data: dict) -> bool:
    'openapi' in json_data

def is_token_provition(json_data: dict) -> bool:
    'access_token' in json_data and 'token_type' in json_data

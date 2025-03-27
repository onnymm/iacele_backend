from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import json
import re

# Función para convertir camelCase a snake_case
def _camel_to_snake(name: str) -> str:
    return re.sub(r'([A-Z])', r'_\1', name).lower()

# Función para convertir snake_case a camelCase
def _snake_to_camel(name: str) -> str:
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), name)

def _convert_keys_to_snake_case(data):
    if isinstance(data, dict):
        return { _camel_to_snake(key): _convert_keys_to_snake_case(value) for ( key, value ) in data.items() }
    elif isinstance(data, list):
        return [ _convert_keys_to_snake_case(i) for i in data ]
    return data

def _convert_keys_to_camel_case(data):
    if isinstance(data, dict):
        return { _snake_to_camel(key): _convert_keys_to_camel_case(value) for ( key, value ) in data.items() }
    elif isinstance(data, list):
        return [ _convert_keys_to_camel_case(i) for i in data ]
    return data

class CamelCaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Si la petición tiene JSON, convertir a snake_case
        if request.headers.get("content-type") == "application/json":
            body = await request.body()
            if body:
                json_body = json.loads(body)
                request._body = json.dumps(_convert_keys_to_snake_case(json_body)).encode("utf-8")

        # Llamamos al endpoint de FastAPI
        response = await call_next(request)

        # Guardamos la respuesta original antes de leer el body_iterator
        original_response = response


        # Convertimos la respuesta a camelCase si es JSON
        if response.headers.get("content-type") == "application/json":
            body = [section async for section in response.body_iterator]
            response_body = b"".join(body).decode("utf-8")

            try:
                json_data = json.loads(response_body)
                # Manejo de los datos si se trata de un token de autenticación
                if 'access_token' in json_data and 'token_type' in json_data:
                    token = json_data['access_token']
                    camel_case_data = _convert_keys_to_camel_case(json_data)
                    camel_case_data['access_token'] = token
                elif 'openapi' not in json_data:
                    camel_case_data = _convert_keys_to_camel_case(json_data)
                else:
                    camel_case_data = json_data
                
                # Eliminamos Content-Length antes de devolver la respuesta
                headers = dict(original_response.headers)
                headers.pop("content-length", None)

                response = Response(
                    content=json.dumps(camel_case_data),
                    status_code=original_response.status_code,
                    headers=headers,
                    media_type="application/json",
                )
            except json.JSONDecodeError:
                pass  # Si no es JSON, enviarlo sin cambios

        return response

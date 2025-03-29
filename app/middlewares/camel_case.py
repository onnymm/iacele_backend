from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import json
from app.utils.middlewares import (
    convert_keys_to_snake_case,
    convert_keys_to_camel_case,
    is_json_like,
    is_open_api_response,
    is_token_provition,
)

class CamelCaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Si la petición tiene JSON se convierte a snake_case
        if request.headers.get("content-type") == "application/json":
            # Obtención del cuerpo de la petición
            body = await request.body()
            # Si existe el cuerpo de la petición...
            if body:
                # Conversión del cuerpo a diccionario
                json_body = json.loads(body)
                # Transformación del cuerpo de la petición
                request._body = (
                    # Conversión a JSON de...
                    json.dumps(
                        # Conversión de las llaves a snake case
                        convert_keys_to_snake_case(json_body)
                    )
                    # Codificación a UTF-8
                    .encode("utf-8")
                )

        # Llamada al endpoint de la API
        response = await call_next(request)

        # Se guarda la respuesta original antes de leer el body_iterator
        original_response = response

        # Si la respuesta de la API es JSON...
        if response.headers.get("content-type") == "application/json":
            # Obtención del cuerpo de la respuesta
            body = [section async for section in response.body_iterator]
            # Decodificación
            response_body = b"".join(body).decode("utf-8")

            try:
                # Conversión del JSON a diccionario
                json_data = json.loads(response_body)

                # Manejo de los datos si se trata de un token de autenticación
                if is_json_like(json_data) and is_token_provition(json_data):
                    # Se guarda el token para almacenarse en la misma llave
                    token = json_data['access_token']
                    # Conversión de las llaves a camel case
                    camel_case_data = convert_keys_to_camel_case(json_data)
                    # Se guarda el token en el cuerpo a retornar
                    camel_case_data['access_token'] = token

                # Manejo de datos si no es una respuesta del esquema OpenAPI
                elif is_json_like(json_data) and not is_open_api_response(json_data):
                    # Conversión de las llaves a camel case
                    camel_case_data = convert_keys_to_camel_case(json_data)

                # Se mantiene el cuerpo intacto
                else:
                    camel_case_data = json_data

                # Se elimina la longitud del contenido antes de devolver la respuesta
                headers = dict(original_response.headers)
                headers.pop("content-length", None)

                # Creación de objeto de respuesta
                response = Response(
                    content= json.dumps(camel_case_data),
                    status_code= original_response.status_code,
                    headers= headers,
                    media_type= "application/json",
                )
            except json.JSONDecodeError:
                pass  # Si no es JSON, enviarlo sin cambios

        return response

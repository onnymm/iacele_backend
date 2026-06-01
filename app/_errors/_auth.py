from fastapi import status
from fastapi.exceptions import HTTPException

# Instancia de token de autenticación inválido
wrong_password_error = HTTPException(
    status_code= status.HTTP_403_FORBIDDEN,
    detail= 'Contraseña incorrecta.',
)

# Instancia de usuario inexistente
user_not_found_error = HTTPException(
    status_code= status.HTTP_404_NOT_FOUND,
    detail= 'El usuario no existe.'
)

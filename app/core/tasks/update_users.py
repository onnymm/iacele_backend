import pandas as pd
from app import settings, odoo
from app.security.auth import hash_password
from app.database import db_connection

def _register_users(data: pd.DataFrame) -> pd.DataFrame:
    """
    ## Registro de nuevos usuarios de Odoo en la base de datos
    Esta función interna registra a todos los nuevos usuarios de Odoo que no se encuentren en iaCele.
    """

    # Filtro por todos los registros que no contengan ID de usuario como NaN
    data_to_process = data[data['user_id'].isna()]

    # Si existen datos nuevos se procede a crearlos
    if not data_to_process.empty:

        (
            data_to_process
            # Selección de columnas
            [[
                'login',
                'name',
                'id',
            ]]
            # Reasignación de nombres de columnas
            .rename(
                columns= {
                    'login': 'user',
                    'id': 'odoo_id',
                }
            )
            # Creación de contraseña
            .assign(
                **{
                    'password': settings.base.NEW_USER_PASSWORD
                }
            )
            .assign(
                **{
                    'password': lambda df: df['password'].apply(lambda value: hash_password(value))
                }
            )
            # Registro en la base de datos
            .pipe(
                lambda df: (
                    db_connection.create(
                        'base.users',
                        df.to_dict('records')
                    )
                )
            )
        )

    # Retorno de los datos originales
    return data

def update_users() -> None:
    """
    ## Actualización de usuarios en iaCele
    Esta función actualiza el estatus de los usuarios existentes en Odoo. Si existe un usuario nuevo,
    éste es creado en iaCele. Si un usuario en Odoo deja de existir, se desactiva en la base de datos.
    """

    # Búsqueda de usuarios en Odoo
    odoo_users = odoo.search_read('res.users', [], ['login', 'name'])

    # Búsqueda de usuarios en iaCele
    iacele_users = db_connection.search_read('base.users', fields=['odoo_id'], output_format= 'dataframe')

    (
        odoo_users
        # Merge de DataFrames
        .merge(
            right= (
                iacele_users
                .rename(columns= {'id': 'user_id'})
            ),
            left_on= 'id',
            right_on= 'odoo_id',
            how= 'outer'
        )
        # Búsqueda de nuevo usuario en Odoo
        .pipe(_register_users)
    )
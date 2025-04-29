from typing import Literal
import pandas as pd
from app.types.iacele import WrappedAction

def _tag_side_info(data: pd.DataFrame, key: str, side: Literal['a', 'b']) -> pd.DataFrame:

    return (
        data
        .assign(
            **{
                f'id_{side}': lambda df: df['id'],
                f'key_{side}': lambda df: df[key],
                f'found_{side}': True,
            }
        )
        [[f'id_{side}', f'key_{side}', f'found_{side}']]
    )

def _merge_processed(a: pd.DataFrame, b: pd.DataFrame, a_key: str, b_key: str) -> pd.DataFrame:

    # Procesamiento de a
    processed_a = (
        a
        .pipe(
            _tag_side_info,
            key= a_key,
            side= 'a'
        )
    )

    # Procesamiento de b
    processed_b = (
        b
        .pipe(
            _tag_side_info,
            key= b_key,
            side= 'b'
        )
    )

    # Unión de ambos DataFrames
    return (
        processed_a
        .pipe(
            lambda df_a: (
                pd.merge(
                    left= df_a,
                    right= processed_b,
                    left_on= 'key_a',
                    right_on= 'key_b',
                    how= 'outer'
                )
            )
        )
    )

def _records_to_update(a: pd.DataFrame, b: pd.DataFrame, a_key: str, b_key: str):

    # Se almacena la unión de los DataFrames
    merged = _merge_processed(a, b, a_key, b_key)

    # Registros a eliminar/desactivar en la base de datos
    create = (
        merged
        .pipe(lambda df: df[df['found_a'].isna()])
        ['id_b']
        .astype(int)
        .tolist()
    )

    # Registros a crear en la base de datos
    delete = (
        merged
        .pipe(lambda df: df[df['found_b'].isna()])
        ['id_a']
        .astype(int)
        .tolist()
    )

    return [ create, delete ]



def find_symmetric_diff(
    a: pd.DataFrame,
    b: pd.DataFrame,
    a_key: str,
    b_key: str,
    create_callback: WrappedAction,
    del_callback: WrappedAction
):

    # Se obtienen las IDs a crear y eliminar
    [ ids_to_create, ids_to_delete ] = _records_to_update(a, b, a_key, b_key)

    # Creación de registros
    create_callback(ids_to_create)

    # Eliminación o desactivación de registros
    del_callback(ids_to_delete)

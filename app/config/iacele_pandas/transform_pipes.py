import pandas as pd
import numpy as np
from ...extensions.iacele_pandas._core import data_property

def stock_quant_callback(base_df: pd.DataFrame, add_df: pd.DataFrame):
    # Creación de las columnas de cantidad
    summary = (
        add_df
        .pivot(
            columns= "location_id",
            index= "product_id",
            values= "inventory_quantity_auto_apply"
        )
    )

    # Si algún un almacén está en 0 se agrega con cantidades en 0
    for warehouse_id in data_property("property_warehouses"):
        if warehouse_id not in summary.columns:
            summary[warehouse_id] = np.nan

    # Se realiza el reemplazo de los NaN por 0
    summary = summary.replace(
        {
            np.nan: 0
        }
    )

    # Se hace el merge con el DataFrame adicional original para reunir los datos computados
    data = (
        pd.merge(
            left= add_df,
            left_on= "product_id",
            right= summary,
            right_on= "product_id",
            how= "left"
        )

        # Se realiza la conversión para mantener enteros después del próximo merge
        .pipe(
            lambda df: (
                df
                .iacele.keep_integers()
                .iacele.keep_floats()
            )
        )

        # Se suman las columnas para totales por almacén
        .assign(
            a1 = lambda df_: df_[18] + df_[29],
            a2 = lambda df_: df_[24] + df_[30],
        )

        # Se seleccionan las columnas necesarias
        [["product_id", "a1", "a2"]]
    )

    # Obtención del DataFrame resultante
    res_df = (
        # Merge con el DataFrame base y el DataFrame computado
        pd.merge(
            left= base_df,
            left_on= "product_variant_id",
            right= data,
            right_on= 'product_id',
            how= "left"
        )

        # Reemplazo de los valores <NA> por ceros
        .replace(
            {
                pd.NA: 0
            }
        )

        # Selección de columnas necesarias
        [['id', 'name', 'default_code', 'a1', 'a2']]
    )

    # Retorno del DataFrame resultante
    return res_df

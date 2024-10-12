import pandas as pd
from app.extensions.iacele_pandas import BaseIACelePandas

# Registro de la extensión de iaCele en Pandas
@pd.api.extensions.register_dataframe_accessor("iacele")
class IACelePandas(BaseIACelePandas):
    pass

from app.config.iacele_pandas.views import table_data
from app.constants.key_values import odoo

class Data():
    property_warehouses = odoo['warehouse']['list']
    warehouses_index = odoo['warehouse']['index']

    table_data_views = table_data

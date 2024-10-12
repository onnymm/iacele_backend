from transform_pipes import (
    stock_quant_callback
)

table_data = {
    "product.template": {
        "stock.quant": {
            # Campos
            'fields': [
                "location_id",
                "product_id",
                "inventory_quantity_auto_apply",
            ],
            # Criterio de búsqueda
            'criteria': [
                '&',
                    ('product_id', 'in', '@df["product_variant_id"].to_list()'),
                    ('location_id', 'in', '@data.property_warehouses')
            ],
            # Función de transformación de DataFrame
            'callback': stock_quant_callback,
        }
    }
}
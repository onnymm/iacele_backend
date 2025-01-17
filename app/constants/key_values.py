from app.types.types import SearchOP

odoo = {
    'warehouse': {

        # IDs de almacenes desde Odoo stock.warehouse
        'index': {
            "a1": 18,
            "a11": 29,
            "a2": 24,
            "a22": 30,
        },

        # Lista de IDs
        'list': [
            18,
            29,
            24,
            30,
        ],
    },
}

# Operadores para criterio de búsqueda de texto
op: SearchOP = {
    're': '~*',
    'contains': 'ilike',
    'match': '=',
}

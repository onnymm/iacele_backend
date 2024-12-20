from app.database import db_connection
import pandas as pd
from app.core._types import TransformCallbacksCollection

def get_stats(user_id: int):

    stats_callbacks: TransformCallbacksCollection = {
        'day_sales': {
            'search_criteria': [
                '&',
                    ('invoice_date', '><', ('2024-01-01', '2024-01-31')),
                    ('salesperson_id', '=', user_id)
            ],
            'callback': lambda df: (
                df
                .assign(
                    day = lambda df: (
                        pd.to_datetime(df['invoice_date'])
                        .apply(lambda date: date.day)
                    )
                )
                .groupby('day')
                .agg(
                    {
                        'day': 'first',
                        'line_comission': 'sum',
                    }
                )
                .astype( {'day': 'int8'} )
                .to_dict('records')
            ),
        },
        'best_salespeople': {
            'search_criteria': [
                '&',
                    ('invoice_date', '><', ('2024-01-01', '2024-01-31')),
                    ('business_model', '=', 'piso')
            ],
            'callback': lambda df: (
                df
                .groupby('salesperson_name')
                .agg(
                    {
                        'line_comission': 'sum'
                    }
                )
                .sort_values(
                    'line_comission',
                    ascending= False
                )
                .iloc[:5]
                .reset_index()
                .to_dict('records')
            )
        },
    }

    stats = {
        key: stat['callback'](
            db_connection.search_read(
                'commissions',
                stat['search_criteria']
            ),
        )
        for ( key, stat ) in stats_callbacks.items()
    }

    return stats

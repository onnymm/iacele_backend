class PARAMETERS:
    class FIELDS_TO_READ:
        FIELDS_METADATA = [
            'name',
            'label',
            'ttype',
            'help_info',
            'related_model_id',
            (
                'selection_ids',
                [
                    'name',
                    ('display_name', 'label'),
                ],
            ),
            'readonly',
            'is_computed',
        ]

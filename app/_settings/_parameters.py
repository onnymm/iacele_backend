class PARAMETERS:
    class FIELDS_TO_READ:
        FIELDS_METADATA = [
            'name',
            'label',
            'ttype',
            'help_info',
            ('related_model_id.model', 'related_model'),
            (
                'selection_ids',
                [
                    'name',
                    'label',
                ],
            ),
            'readonly',
            'is_computed',
        ]

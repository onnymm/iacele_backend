from .._api.models import CRUD
from .._src._classes import Lylac

def _expand_relational_fields(
    ctx: Lylac.ExecutionContext,
    model_name: str,
    requested: list[str | tuple[str, list[str]]],
):

    # Obtención de los nombres de campos escalares
    scalar_fields = [field for field in requested if isinstance(field, str)]

    # Búsqueda de los tipos de datos de los campos especificados como cadena de texto
    relational_fields_metadata = ctx.search_read(
        'base.model.field',
        [
            '&',
                '&',
                    ('model_id.model', '=', model_name),
                    ('name', 'in', scalar_fields),
                ('ttype', 'in', ['one2many', 'many2many'])
        ],
        ['name'],
    )

    # Obtención de los campos que son de tipo one2many y many2many
    expandable_fields = [
        field['name']
        for field
        in relational_fields_metadata
    ]

    # Inicialización de lista de campos enriquecidos
    resolved_fields = ['display_name']

    # Iteración por cada declaración de campo a leer
    for field in requested:
        # Si el campo se encuentra en los campos de tipo one2many y many2many...
        if isinstance(field, str) and field in expandable_fields:
            # Se añade una declaración extensa para acceder a la ID y nombre a mostrar de los registros referenciados
            resolved_fields.append( (field, ['id', 'display_name']) )
        # Si el campo no es de tipo one2many o many2many...
        else:
            # Se añade éste sin ningún campo
            resolved_fields.append(field)

    return resolved_fields

def tree_search_read(
    ctx: Lylac.ExecutionContext,
    params: CRUD.SearchRead,
):

    # Expansión de campos relacionales
    fields_to_read = _expand_relational_fields(ctx, params.model_name, params.fields)
    # Conteo de resultados
    count = ctx.search_count(params.model_name, params.search_criteria)
    # Conversión de los parámetros a diccionario
    params_dict = params.model_dump()
    # Sobreescritura de declaración de campos
    params_dict['fields'] = fields_to_read
    # Búsqueda y lectura de resultados
    data = ctx.search_read(**params_dict)

    # Obtención de datos del modelo actual
    [ record ] = ctx.search_read('base.model', [('model', '=', params.model_name)], ['label'])

    # Obtención de la leyenda del modelo
    model_label: str = record['label']

    return {
        'count': count,
        'data': data,
        'model_label': model_label,
    }

def form_read(
    ctx: Lylac.ExecutionContext,
    params: CRUD.Read,
):

    # Expansión de campos relacionales
    fields_to_read = _expand_relational_fields(ctx, params.model_name, params.fields)
    # Conversión de los parámetros a diccionario
    params_dict = params.model_dump()
    # Sobreescritura de declaración de campos
    params_dict['fields'] = fields_to_read

    # Lectura del registro solicitado
    [ record ] = ctx.read(**params_dict)

    # Obtención del nombre del registro
    record_name = record['display_name']

    return {
        'record': record,
        'name': record_name,
    }

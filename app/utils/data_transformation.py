def list_fields(info_fields: list[dict[str]]):
    """
    ## Listado de datos de campos
    Este método convierte una lista de diccionarios de llaves `name` y `ttype`
    a un diccionario con los valores de las llaves como llaves de éste.

    Uso:
    >>> fields_info = [
    >>>     {'name': 'user_id', 'ttype': 'many2one'},
    >>>     {'name': 'price', 'ttype': 'monetary'},
    >>>     {'name': 'name', 'ttype': 'char'},
    >>> ]
    >>> 
    >>> fields = list_fields(fields_info)
    >>> 
    >>> # Salida
    >>> {
    >>>     'user_id': 'many2one',
    >>>     'price': 'monetary',
    >>>     'name': 'char',
    >>> }
    """

    # Declaración del diccionario a retornar
    fields = {}

    # Extracción de llave y valor
    for item in info_fields:
        fields[item['name']] = item['ttype']

    # Retorno del diccionario
    return fields

class SearchEngine():
    multiple = lambda _, key: f"[{key}]"
    escaped = lambda symbol, _: f"\\{symbol}"
    repeated = lambda symbol, _: f"{symbol}" + "{1,}"
    indeterminate = lambda symbol, _: f"{symbol}*?"
    # one_missed = lambda symbol, _: f"{symbol}.?"
    one_missed = lambda symbol, _: f"{symbol}"
    many_missed = lambda symbol, _: f"{symbol}.*?"
    exact = lambda symbol, _: f"{symbol}"
    
    special_cases = {
        "aáäà": [multiple, repeated, one_missed],
        "eéëè": [multiple, repeated, one_missed],
        "iíïìy": [multiple, repeated, one_missed],
        "oóöò": [multiple, repeated, one_missed],
        "uúüù": [multiple, repeated, one_missed],
        "(": [escaped, indeterminate, one_missed],
        ")": [escaped, indeterminate, one_missed],
        "[": [escaped, indeterminate, one_missed],
        "]": [escaped, indeterminate, one_missed],
        "{": [escaped, indeterminate, one_missed],
        "}": [escaped, indeterminate, one_missed],
        ".": [escaped, indeterminate, one_missed],
        "^": [escaped, indeterminate, one_missed],
        "$": [escaped, indeterminate, one_missed],
        "\"": [escaped, indeterminate, one_missed],
        " ": [indeterminate, many_missed],
        "0123456789": [exact]
    }

    common_cases = [repeated, one_missed]

    def create_search(self, search: str):
        """
        ## Creación de expresión regular para búsqueda
        Este método crea una expresión regular para usarse en una búsqueda
        por coincidencia de texto.
        """
        # Inicialización de matriz de símbolos RegEx
        regex_words = []

        # Participación de caracteres para procesar una RegEx limpia
        chars = ""

        # Iteración por cada caracter del texto entrante
        for char in search.lower():
            # Comparación de igualdad con el último caracter de la matriz de caracteres a transformar
            if chars == "" or chars[len(chars) - 1] != char or char in "0123456789":
                # Si no son el mismo se añade el caracter actual de la iteración
                chars += char

        # Iteración por palabra
        for word in chars.split(" "):
            # Inicialización de matriz de caracteres RegEx
            
            regex_chars = ""
            
            # Iteración por cada uno de los caracteres del texto entrante
            for char in word:
                
                # Se inicializa el símbolo RegEx a retornar como valor indefinido
                regex_symbol = None
                # Condición para iteración controlada
                found = False

                # Iteración controlada
                while not found:
                    
                    # Búsqueda en los valores de las llaves del objeto de casos especiales
                    for key in self.special_cases.keys():
                        
                        # Búsqueda del caracter en el valor de la llave
                        if char in key:
                            
                            # En caso de encontrarse el caracter se ejecutan las funciones del valor del objeto de casos especiales
                            for callback in self.special_cases[key]:
                                # Transformación del caracter en símbolo RegEx
                                char = callback(char, key)

                            # Almacenamiento del símbolo RegEx
                            regex_symbol = char

                            # Se indica que el caracter fue encontrado para detener el ciclo while
                            found = True

                            # Se detiene la iteración de llaves
                            break

                    # Si el símbolo aún no se halla se itera por las funciones de casos comunes
                    if (not regex_symbol):
                        for callback in self.common_cases:
                            # Transformación del caracter en símbolo RegEx
                            char = callback(char, "")

                        # Almacenamiento del símbolo RegEx
                        regex_symbol = char

                    found = True
                
                # Se añade el símbolo RegEx a la matriz de símbolos RegEx
                regex_chars += regex_symbol

            regex_words.append(f"(?=.*{regex_chars})")

        regex_exp = regex_words[0]

        for i in range(len(regex_words) -1 ):
            regex_exp += f" *?{regex_words[i + 1]}"

        print(regex_exp)

        return regex_exp

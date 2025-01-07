from typing import Callable

_ReBlockGenerator = Callable[[str, str], str]
_ReBlockGeneratorMap =  dict[str, list[_ReBlockGenerator]]
_ReBlockGeneratorCommon = list[Callable[[str], str]]

class RegexSearchEngine():

    # Funciones de bloques de generación de expresión regular por caracter
    _grouped: _ReBlockGenerator = lambda _, key: f"[{key}]"
    _escaped: _ReBlockGenerator = lambda symbol, _: f"\\{symbol}"
    _repeated: _ReBlockGenerator = lambda symbol, _: f"{symbol}" + "{1,}"
    _indeterminate: _ReBlockGenerator = lambda symbol, _: f"{symbol}*?"
    _one_missed: _ReBlockGenerator = lambda symbol, _: f"{symbol}.?"
    _many_missed: _ReBlockGenerator = lambda symbol, _: f"{symbol}.*?"
    _exact: _ReBlockGenerator = lambda symbol, _: f"{symbol}"

    # Mapa de funciones para comportamientos por clases de caracteres
    _special_cases: _ReBlockGeneratorMap = {
        "aáäà": [_grouped, _repeated, _one_missed],
        "eéëè": [_grouped, _repeated, _one_missed],
        "iíïìy": [_grouped, _repeated, _one_missed],
        "oóöò": [_grouped, _repeated, _one_missed],
        "uúüù": [_grouped, _repeated, _one_missed],
        "(": [_escaped, _indeterminate, _one_missed],
        ")": [_escaped, _indeterminate, _one_missed],
        "[": [_escaped, _indeterminate, _one_missed],
        "]": [_escaped, _indeterminate, _one_missed],
        "{": [_escaped, _indeterminate, _one_missed],
        "}": [_escaped, _indeterminate, _one_missed],
        ".": [_escaped, _indeterminate, _one_missed],
        "^": [_escaped, _indeterminate, _one_missed],
        "$": [_escaped, _indeterminate, _one_missed],
        "\"": [_escaped, _indeterminate, _one_missed],
        " ": [_indeterminate, _many_missed],
        "0123456789": [_exact],
    }

    # Comportamiento por defecto para el resto de caracteres
    _common_cases: _ReBlockGeneratorCommon = [_repeated, _one_missed]

    def __init__(self, drop_input_duplicates: bool = True) -> None:

        # Configuración de parámetros
        self._config._input_duplicates_bypass = not drop_input_duplicates

    def create_search(self, search_text: str):
        """
        ## Creación de expresión regular para búsqueda
        Este método crea una expresión regular para usarse en una búsqueda
        por coincidencia de texto.
        """

        # Creación de caracteres individuales para creación de expresiones regulares
        chars = self._create_individual_chars(search_text)

        # Creación de palabras regex
        regex_words = self._create_regex_words(chars)

        # Se retorna la expresión regular completa
        return self._create_full_regex(regex_words)


    def _create_individual_chars(self, search_text: str) -> str:
        """
        Creación de caracteres individuales para creación de expresiones regulares.
        """
        # Partición de caracteres para procesar una RegEx limpia
        chars = ""

        # Iteración por cada caracter del texto entrante
        for char in search_text:
            # Comparación de igualdad con el último caracter de la matriz de caracteres a transformar
            if chars == "" or self._check_duplicated(chars, char) or char in "0123456789":
                # Si no son el mismo se añade el caracter actual de la iteración
                chars += char

        # Retorno de los caracteres para creación de expresiones regulares
        return chars



    def _create_full_regex(self, regex_words: list[str]) -> str:
        """
        Creación de expresión regular completa.
        """
        # Se extrae la primera palabra regex
        regex_exp = regex_words[0]

        # Se realiza una iteración por el resto de las palabras regex
        for i in range(len(regex_words) -1 ):
            # Se forma la expresión regular completa
            regex_exp += f" *?{regex_words[i + 1]}"

        # Se retorna la expresión regular completa
        return regex_exp



    def _create_regex_words(self, chars: str) -> list[str]:
        """
        Creación de palabras RegEx.
        """

        # Inicialización de lista de símbolos RegEx
        regex_words: list[str] = []

        # Iteración por palabra
        for word in chars.split(" "):

            # Se crean expresiones regulares por palabra y se añaden a la lista
            regex_words.append( self._create_regex_word(word) )

        # Retorno de la lista de palabras RegEx
        return regex_words



    def _create_regex_word(self, word: str) -> str:
        """
        Creación una palabra RegEx.
        """
        # Inicialización de palabra RegEx
        regex_word: str = ""

        # Iteración por cada uno de los caracteres del texto entrante
        for char in word:

            # Se añade cada símbolo RegEx generado a la lista de símbolos RegEx
            regex_word += self._create_regex_symbol(char)

        return f"(?=.*{regex_word})"



    def _create_regex_symbol(self, char: str):
        """
        Creación de un símbolo regex.
        """

        # Se inicializa el símbolo RegEx a retornar
        regex_symbol: str = None
        # Se inicializa el símbolo como no encontrado para control de iteración
        found: bool = False

        # Mientras el símbolo no se encuentre...
        while not found:

            # Búsqueda en los valores de las llaves del objeto de casos especiales
            for key in self._special_cases.keys():

                # Búsqueda del caracter en el valor de la llave
                if char in key:

                    # Creación del símbolo RegEx a partir de un comportamiento especial
                    regex_symbol = self._create_special_case(char, key)

                    # Se indica que el caracter fue encontrado para detener el ciclo while
                    found = True

                    # Se detiene la iteración de llaves
                    break

            # Si el símbolo no se encontró...
            if not regex_symbol:

                # Creación del símbolo RegEx a partir de del comportamiento común
                regex_symbol = self._create_common_case(char)

            # Se indica que el caracter fue encontrado para detener el ciclo while
            found = True

        # Retorno del símbolo RegEx
        return regex_symbol



    def _create_special_case(self, char: str, key: str) -> str:
        """
        Creación un símbolo RegEx a partir de un comportamiento especial.
        """

        # Iteración por cada una de las funciones de comportamiento especial
        for callback in self._special_cases[key]:
            # Creación del símbolo RegEx
            char = callback(char, key)

        # Retorno del símbolo RegEx
        return char



    def _create_common_case(self, char: str) -> str:
        """
        Creación un símbolo RegEx a partir de un comportamiento común.
        """

        # Iteración por cada una de las funciones de comportamiento común
        for callback in self._common_cases:
            # Creación del símbolo RegEx
            char = callback(char, '')

        # Retorno del símbolo RegEx
        return char



    def _check_duplicated(self, chars: str, current_char: str) -> bool:
        """
        Revisión de caracter entrante duplicado.
        """

        # Si el bypass está desactivado, no se realiza revisión
        if self._config._input_duplicates_bypass:
            return False

        else:
            # Revisión de si el último caracter revisado es diferente al caracter actual
            return chars[len(chars) - 1] != current_char



    # Sección de configuración y funciones dinámicas
    class _config():
        _input_duplicates_bypass = False

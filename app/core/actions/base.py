from app import *
from app.models.crud import DBTable
from typing import Callable
from app.models.actions import (
    Action,
    Task,
)
from app.types.iacele import (
    Actions,
    Tasks,
)


class IACele():

    _tables = ['base.users', 'commissions.line']
    _actions: Actions = { key: {} for key in _tables }
    _tasks: Tasks = { key: {} for key in _tables }

    @classmethod
    def register_action(cls, table: DBTable):
        """
        ### Registro de acción de servidor
        Este decorador registra la función declarada para ser ejecutada dentro de
        los endpoints de ejecución de acciones del servidor.
        """

        # Creación dinámica del decorador a retornar
        def decorator(callback: Callable[[int | list[int]], bool]):

            # Función envuelta creada por el decorador
            def wrapper(*args, **kwargs) -> bool:

                # Ejecución de la función declarada
                response = callback(*args, **kwargs)

                # Retorno del resultado de la ejecución de la función
                return response

            # Registro de la función envuelta como acción de servidor
            cls._actions[table][callback.__name__] = wrapper

            # Retorno de la función envuelta
            return wrapper

        # Retorno del decorador dinámico creado
        return decorator



    @classmethod
    def register_task(cls, table: DBTable):
        """
        ### Registro de tarea de servidor
        Este decorador registra la función declarada para ser ejecudada dentro de los
        endpoints de tareas del servidor.
        """

        # Creación dinmámica del decorator a retornar
        def decorator(callback: Callable[[], bool]):

            def wrapper(*args, **kwargs) -> bool:

                # Ejecución de la función declarada
                response = callback(*args, **kwargs)

                # Retorno del resultado de la ejecución de la función
                return response

            cls._tasks[table][callback.__name__] = wrapper

            # Retorno de la función envuelta
            return wrapper

        # Retorno del decorador dinámico creado
        return decorator



    @classmethod
    def execute_action(cls, params: Action) -> bool:
        """
        ## Ejecución de acción de servidor
        Este método permite ejecutar una acción de servidor sobre uno o muchos
        registros de una tabla de base de datos.
        """
        return cls._actions[params.table][params.action](params)



    @classmethod
    def execute_task(cls, params: Task) -> bool:
        """
        ## Ejecución de tarea de servidor
        Este método permite ejecutar una tarea de servidor sobre los registros de una
        tabla de base de datos.
        """
        return cls._tasks[params.table][params.task]()

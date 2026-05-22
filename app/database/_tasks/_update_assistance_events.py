from attendance_registry import Attendance
from attendance_registry import ExpiredCredentialsError
from datetime import datetime
from datetime import timedelta
from ..._constants import LOCAL_TZ
from ..._core import Lylac
from ..._core import iacele

attendance = Attendance()

@iacele.api.server_tasks.register(
    'update_assistance_events',
)
def _update_assistance_events(ctx: Lylac.ServerTaskContext) -> None:

    # Búsqueda de credenciales activas
    found_credentials = ctx.search_read(
        'assistance.registry.event.credentials',
        fields= [
            'token',
            'cookie_uuid',
            'site_id',
        ],
    )

    # Mientras existan registros de credenciales...
    while len(found_credentials):

        # Obtención del primer registro de credenciales encontrado
        credentials = found_credentials.pop(0)

        # Obtención de la ID del registro en caso de que requiera ser eliminado
        credentials_id = credentials['id']

        # Obtención de los parámetros individuales
        token: str = credentials['token']
        cookie_uuid: str = credentials['cookie_uuid']
        site_id: str = credentials['site_id']

        # Obtención de los parámetros de sincronización
        partitions_to_sync = ctx.search_read(
            'model.sync',
            [('model_id.model', '=', 'assistance.registry.event')],
            [
                'name',
                'last_sync',
            ],
        )

        # Intento de obtención de datos
        try:
            # Iteración por cada partición
            for partition in partitions_to_sync:

                # Obtención de la ID de partición
                partition_id = partition['id']

                # Obtención de último valor de sincronización con zona horaria
                last_sync = (
                    datetime.fromisoformat(partition['last_sync'])
                    .astimezone(LOCAL_TZ)
                )
                # Obtención del nombre corto de almacén
                warehouse_short_name = partition['name']

                # Búsqueda del dispositivo
                [ device ] = ctx.search_read(
                    'resource.device',
                    [('location_id.short_name', '=', warehouse_short_name)],
                    [
                        'model',
                        'serial_number',
                        'firmware_version',
                        'location_id.short_name',
                    ]
                )
                # Obtención de valores del dispositivo
                device_id = device['id']
                device_model = device['model']
                device_sn = device['serial_number']
                device_firmware = device['firmware_version']

                # Se intentan usar las credenciales obtenidas
                try:
                    # Obtención de los registros desde la API de HikVision
                    records_from_api = attendance.get_events(
                        device_model,
                        device_sn,
                        device_firmware,
                        cookie_uuid,
                        token,
                        site_id,
                        last_sync + timedelta(seconds= 1),
                        datetime.now(LOCAL_TZ),
                    )

                # Si las credenciales están expiradas...
                except ExpiredCredentialsError:
                    # Se elimina el registro de éstas en la base de datos
                    ctx.delete('assistance.registry.event.credentials', credentials_id)
                    # Se arroja el error para salir de este ciclo y el ciclo superior para usar
                    #   otro registro de credenciales
                    raise

                # Inicialización de lista de registros a crear
                records_to_create: list[dict] = []

                # Iteración por cada registro retornado por la API
                for record_from_api in records_from_api:
                    # Inicialización de diccionario de registro a crear
                    record_to_create = {}
                    # Obtención de valores
                    record_to_create['employee_id'] = ctx.get_resource_id(f'hr_employee.{record_from_api['user_id']}')
                    record_to_create['original_registry_time'] = record_from_api['registry_time']
                    record_to_create['original_status'] = record_from_api['status']
                    record_to_create['device_id'] = device_id
                    record_to_create['from_api'] = True

                    # Se añade el registro a la lista de registros a crear
                    records_to_create.append(record_to_create)

                # Creación de los registros
                ctx.create('assistance.registry.event', records_to_create)

                # Obtención de la hora más reciente
                [ most_recent_record ] = ctx.search_read(
                    'assistance.registry.event',
                    [('device_id.location_id.short_name', '=', partition['name'])],
                    sortby= 'registry_time',
                    ascending= False,
                    limit= 1,
                )

                # Actualización de hora de última sincronización
                ctx.update(
                    'model.sync',
                    partition_id,
                    {'last_sync': most_recent_record['original_registry_time']}
                )

            return

        # Si las credenciales usadas estaban expiradas la ejecución llega a este punto
        except ExpiredCredentialsError:
            # Se continúa al siguiente registro de credenciales
            continue

    # Si se terminaron los registros de credenciales, se notifica que no existen credenciales actidas
    print('No hay credenciales activas')

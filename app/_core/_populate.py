from datetime import date
from .._constants import LOCATION
from .._src import Lylac
from ._odoo import odoo

# Adaptador de mapeo de ID de almacén a ID de ubicación
LOCATION_ADAPTER = {
    2: 1,
    3: 2,
}

def _load_employees_data(ctx: Lylac.TransactionContext):

    # Obtención de los datos de empleados
    data = odoo.search_read(
        'hr.employee',
        fields= [
            'name',
            'x_warehouse_id',
            'x_hire_date',
        ]
    )

    # Inicialización de lista de registros a crear
    data_to_create = []

    for record in data:
        # Obtención de la ID de registro de almacén en la base de datos de Odoo
        warehouse_record_id: int = record['x_warehouse_id'][0]
        # Obtención de la ID de registro de ubicación en esta base de datos
        location_id = LOCATION_ADAPTER[warehouse_record_id]
        # Construcción de referencia
        location_ref = f'location_warehouse.{location_id}'

        # Construcción de registro a crear
        new_record = {
            'name': record['name'],
            'odoo_id': record['id'],
            'location_id': ctx.get_resource_id(location_ref),
            'hire_date': record['x_hire_date'],
        }

        # Se añade el registro a la lista de registros a crear
        data_to_create.append(new_record)

    ctx.create('hr.employee', data_to_create)

def populate(ctx: Lylac.TransactionContext):

    # Creación de registros de ubicaciones
    ctx.create(
        'location.warehouse',
        [
            {
                'name': 'Cabo San Lucas',
                'short_name': LOCATION.CSL,
                'location_number': 1,
            },
            {
                'name': 'San José Del Cabo',
                'short_name': LOCATION.SJC,
                'location_number': 2,
            },
        ]
    )

    # Creación de registro de dispositivo de tipo terminal de reconocimiento facial
    [ resource_device_type__record_id ] = ctx.create(
        'resource.device.type',
        {
            'name': 'Terminal de reconocimiento facial',
        }
    )

    # Creación de registros de terminales de reconocimiento facial
    ctx.create(
        'resource.device',
        [
            {
                'brand': 'HikVision',
                'model': 'DS-K1A340WX',
                'serial_number': 'G97954302',
                'type_id': resource_device_type__record_id,
                'firmware_version': 'V1.2.7 build 240102',
                'location_id': 1,
            },
            {
                'brand': 'HikVision',
                'model': 'DS-K1A340WX',
                'serial_number': 'G97954418',
                'type_id': resource_device_type__record_id,
                'firmware_version': 'V1.2.7 build 240102',
                'location_id': 2,
            },
        ]
    )

    # Creación de registros de empleados
    _load_employees_data(ctx)

    # Creación de registros de horarios laborales
    ctx.create(
        'schedule.week',
        [
            {
                'start_time': '08:00:59',
                'end_time': '18:00:00',
                'weekday': 'monday',
            },
            {
                'start_time': '08:00:59',
                'end_time': '18:00:00',
                'weekday': 'tuesday',
            },
            {
                'start_time': '08:00:59',
                'end_time': '18:00:00',
                'weekday': 'wednesday',
            },
            {
                'start_time': '08:00:59',
                'end_time': '18:00:00',
                'weekday': 'thursday',
            },
            {
                'start_time': '08:00:59',
                'end_time': '18:00:00',
                'weekday': 'friday',
            },
            {
                'start_time': '08:00:59',
                'end_time': '16:00:00',
                'weekday': 'saturday',
            },
        ],
    )

    # Creación de desfases de horarios
    ctx.create(
        'schedule.week.offset',
        [
            {
                'employee_id': ctx.get_resource_id('hr_employee.23'),
                'weekday': 'saturday',
                'start_offset': '02:00:00',
                'end_offset': '00:00:00',
            },
            {
                'employee_id': ctx.get_resource_id('hr_employee.29'),
                'weekday': 'saturday',
                'start_offset': '02:00:00',
                'end_offset': '00:00:00',
            },
            {
                'employee_id': ctx.get_resource_id('hr_employee.10'),
                'weekday': 'saturday',
                'start_offset': '00:00:00',
                'end_offset': '-02:00:00',
            },
        ],
    )

    # Creación de datos de sincronización de modelos
    ctx.create(
        'model.sync',
        [
            {
                'name': LOCATION.CSL,
                'model_id': ctx.get_resource_id('base_model.assistance_registry_event'),
                'last_sync': '2026-06-27',
            },
            {
                'name': LOCATION.SJC,
                'model_id': ctx.get_resource_id('base_model.assistance_registry_event'),
                'last_sync': '2026-06-27',
            },
        ]
    )

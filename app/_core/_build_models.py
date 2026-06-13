from .._src import Lylac

def _build_models_structure(ctx: Lylac.TransactionContext):

    # Creación de modelos
    ctx.create(
        'base.model',
        [
            # Modelo de ubicaciones
            {
                'name': 'location_warehouse',
                'model': 'location.warehouse',
                'label': 'Almacén (Ubicación)',
                'field_ids': {
                    'create': [
                        {
                            'name': 'short_name',
                            'label': 'Nombre corto',
                            'ttype': 'char',
                            'nullable': False,
                            'is_required': True,
                        },
                        {
                            'name': 'location_number',
                            'label': 'Número de ubicación',
                            'ttype': 'integer',
                            'unique': True,
                            'nullable': False,
                            'is_required': True,
                        },
                    ]
                },
            },
            # Modelo de tipos de dispositivo
            {
                'name': 'resource_device_type',
                'model': 'resource.device.type',
                'label': 'Tipo de dispositivo',
            },
            # Modelo de horarios semanales
            {
                'name': 'schedule_week',
                'model': 'schedule.week',
                'label': 'Horario semanal',
                'field_ids': {
                    'create': [
                        {
                            'name': 'weekday',
                            'label': 'Día de la semana',
                            'ttype': 'selection',
                            'nullable': False,
                            'is_required': True,
                            'selection_ids': {
                                'create': [
                                    {
                                        'name': 'monday',
                                        'label': 'Lunes',
                                    },
                                    {
                                        'name': 'tuesday',
                                        'label': 'Martes',
                                    },
                                    {
                                        'name': 'wednesday',
                                        'label': 'Miércoles',
                                    },
                                    {
                                        'name': 'thursday',
                                        'label': 'Jueves',
                                    },
                                    {
                                        'name': 'friday',
                                        'label': 'Viernes',
                                    },
                                    {
                                        'name': 'saturday',
                                        'label': 'Sábado',
                                    },
                                    {
                                        'name': 'sunday',
                                        'label': 'Domingo',
                                    },
                                ],
                            },
                        },
                        {
                            'name': 'start_time',
                            'label': 'Inicio',
                            'ttype': 'time',
                            'nullable': False,
                            'is_required': True,
                        },
                        {
                            'name': 'end_time',
                            'label': 'Fin',
                            'ttype': 'time',
                            'nullable': False,
                            'is_required': True,
                        },
                    ]
                }
            },
            # Modelo de sincronización de datos
            {
                'name': 'model_sync',
                'model': 'model.sync',
                'label': 'Sincronización de datos',
                'field_ids': {
                    'create': [
                        {
                            'name': 'last_sync',
                            'label': 'Última sincronización',
                            'ttype': 'datetime',
                            'is_required': True,
                            'nullable': False,
                        },
                        {
                            'name': 'model_id',
                            'label': 'Modelo',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id('base_model.base_model'),
                            'on_delete': 'cascade',
                            'is_required': True,
                            'nullable': False,
                        },
                    ],
                },
            },
        ],
    )
    ctx.create(
        'base.model',
        [
            # Modelo de dispositivos
            {
                'name': 'resource_device',
                'model': 'resource.device',
                'label': 'Dispositivo',
                'field_ids': {
                    'create': [
                        {
                            'name': 'model',
                            'label': 'Modelo',
                            'ttype': 'char',
                        },
                        {
                            'name': 'brand',
                            'label': 'Marca',
                            'ttype': 'char',
                        },
                        {
                            'name': 'serial_number',
                            'label': 'Número de serie',
                            'ttype': 'char',
                        },
                        {
                            'name': 'firmware_version',
                            'label': 'Versión de firmware',
                            'ttype': 'char',
                        },
                        {
                            'name': 'type_id',
                            'label': 'Tipo',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id('base_model.resource_device_type'),
                            'on_delete': 'restrict',
                            'is_required': True,
                            'nullable': False,
                        },
                        {
                            'name': 'location_id',
                            'label': 'Ubicación',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id('base_model.location_warehouse'),
                            'on_delete': 'restrict',
                        },
                    ],
                }
            },
            # Modelo de empleados
            {
                'name': 'hr_employee',
                'model': 'hr.employee',
                'label': 'Empleados',
                'is_archivable': True,
                'field_ids': {
                    'create': [
                        {
                            'name': 'odoo_id',
                            'label': 'ID de usuario en Odoo',
                            'ttype': 'integer',
                            'unique': True,
                        },
                        {
                            'name': 'hire_date',
                            'label': 'Fecha de contratación',
                            'ttype': 'date',
                        },
                        {
                            'name': 'location_id',
                            'label': 'Ubicación',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id('base_model.location_warehouse'),
                            'on_delete': 'restrict',
                        },
                        {
                            'name': 'user_id',
                            'label': 'Usuario',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id('base_model.base_users'),
                            'on_delete': 'restrict',
                        },
                    ]
                }
            },
        ]
    )
    ctx.create(
        'base.model',
        [
            # Modelo de desfases de horarios de empleados
            {
                'name': 'schedule_week_offset',
                'model': 'schedule.week.offset',
                'label': 'Desfase de horario laboral de empleado',
                'field_ids': {
                    'create': [
                        {
                            'name': 'employee_id',
                            'label': 'Empleado',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id('base_model.hr_employee'),
                            'nullable': False,
                            'is_required': True,
                            'on_delete': 'restrict',
                        },
                        {
                            'name': 'start_offset',
                            'label': 'Inicio de desfase',
                            'ttype': 'duration',
                            'nullable': False,
                            'is_required': True,
                        },
                        {
                            'name': 'end_offset',
                            'label': 'Fin de desfase',
                            'ttype': 'duration',
                            'nullable': False,
                            'is_required': True,
                        },
                        {
                            'name': 'weekday',
                            'label': 'Día de la semana',
                            'ttype': 'selection',
                            'nullable': False,
                            'is_required': True,
                            'selection_ids': {
                                'create': [
                                    {
                                        'name': 'monday',
                                        'label': 'Lunes',
                                    },
                                    {
                                        'name': 'tuesday',
                                        'label': 'Martes',
                                    },
                                    {
                                        'name': 'wednesday',
                                        'label': 'Miércoles',
                                    },
                                    {
                                        'name': 'thursday',
                                        'label': 'Jueves',
                                    },
                                    {
                                        'name': 'friday',
                                        'label': 'Viernes',
                                    },
                                    {
                                        'name': 'saturday',
                                        'label': 'Sábado',
                                    },
                                    {
                                        'name': 'sunday',
                                        'label': 'Domingo',
                                    },
                                ],
                            },
                        },
                    ]
                }
            },
        ]
    )
    ctx.create(
        'base.model',
        [
            # Modelo de días de registro de asistencia
            {
                'name': 'assistance_registry_day',
                'model': 'assistance.registry.day',
                'label': 'Días de registro de asistencia',
                'field_ids': {
                    'create': [
                        {
                            'name': 'date',
                            'label': 'Fecha',
                            'ttype': 'date',
                            'nullable': False,
                            'is_required': True,
                        },
                        {
                            'name': 'employee_id',
                            'label': 'Empleado',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id('base_model.hr_employee'),
                            'nullable': False,
                            'is_required': True,
                            'on_delete': 'restrict',
                        },
                        {
                            'name': 'schedule_id',
                            'label': 'Horario',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id('base_model.schedule_week'),
                            'on_delete': 'restrict',
                        },
                        {
                            'name': 'offset_id',
                            'label': 'Desfase de horario',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id('base_model.schedule_week_offset'),
                            'nullable': False,
                            'on_delete': 'restrict',
                        }
                    ]
                }
            },
        ]
    )
    ctx.create(
        'base.model',
        [
            # Modelo de eventos de registro de asistencia
            {
                'name': 'assistance_registry_event',
                'model': 'assistance.registry.event',
                'label': 'Eventos de registro de asistencia',
                'field_ids': {
                    'create': [
                        {
                            'name': 'employee_id',
                            'label': 'Empleado',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id('base_model.hr_employee'),
                            'nullable': False,
                            'is_required': True,
                            'on_delete': 'restrict',
                        },
                        {
                            'name': 'original_registry_time',
                            'label': 'Fecha y hora de registro original',
                            'ttype': 'datetime',
                            'nullable': False,
                            'is_required': True,
                        },
                        {
                            'name': 'original_status',
                            'label': 'Tipo de registro original',
                            'ttype': 'selection',
                            'nullable': False,
                            'is_required': True,
                            'selection_ids': {
                                'create': [
                                    {
                                        'name': 'check_in',
                                        'label': 'Entrada',
                                    },
                                    {
                                        'name': 'break_out',
                                        'label': 'Inicio de comida',
                                    },
                                    {
                                        'name': 'break_in',
                                        'label': 'Fin de comida',
                                    },
                                    {
                                        'name': 'check_out',
                                        'label': 'Salida',
                                    },
                                    {
                                        'name': 'undefined',
                                        'label': 'Indefinido',
                                    },
                                ],
                            },
                        },
                        {
                            'name': 'device_id',
                            'label': 'Dispositivo',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id('base_model.resource_device'),
                            'on_delete': 'restrict',
                        },
                        {
                            'name': 'from_api',
                            'label': 'Proviene de la API',
                            'ttype': 'boolean',
                            'is_required': True,
                            'nullable': False,
                        },
                        {
                            'name': 'registry_time_correction',
                            'label': 'Corrección de fecha y hora de registro',
                            'ttype': 'datetime',
                        },
                        {
                            'name': 'status_correction',
                            'label': 'Corrección de tipo de registro original',
                            'ttype': 'selection',
                            'selection_ids': {
                                'create': [
                                    {
                                        'name': 'check_in',
                                        'label': 'Entrada',
                                    },
                                    {
                                        'name': 'break_out',
                                        'label': 'Inicio de comida',
                                    },
                                    {
                                        'name': 'break_in',
                                        'label': 'Fin de comida',
                                    },
                                    {
                                        'name': 'check_out',
                                        'label': 'Salida',
                                    },
                                    {
                                        'name': 'undefined',
                                        'label': 'Indefinido',
                                    },
                                    {
                                        'name': 'null',
                                        'label': 'Anulado',
                                    },
                                ],
                            },
                        },
                        {
                            'name': 'day_id',
                            'label': 'Día',
                            'ttype': 'many2one',
                            'related_model_id': ctx.get_resource_id('base_model.assistance_registry_day'),
                            'on_delete': 'cascade',
                        },
                    ]
                }
            },
        ],
    )

    # Creación de campos
    ctx.create(
        'base.model.field',
        [
            # Campo one2many para día - evento
            {
                'name': 'event_ids',
                'label': 'Eventos',
                'ttype': 'one2many',
                'model_id': ctx.get_resource_id('base_model.assistance_registry_day'),
                'related_model_id': ctx.get_resource_id('base_model.assistance_registry_event'),
                'related_field': 'day_id',
            },
        ]
    )

    # Creación de modelos transitorios
    ctx.create(
        'base.model',
        [
            # Modelo de credenciales de actualización de eventos de asistencia
            {
                'name': 'assistance_registry_event_credentials',
                'model': 'assistance.registry.event.credentials',
                'label': 'Credenciales de sincronización de eventos de asistencia',
                'field_ids': {
                    'create': [
                        {
                            'name': 'token',
                            'label': 'Token',
                            'ttype': 'char',
                            'nullable': False,
                            'is_required': True,
                        },
                        {
                            'name': 'cookie_uuid',
                            'label': 'UUID de Cookie',
                            'ttype': 'char',
                            'nullable': False,
                            'is_required': True,
                        },
                        {
                            'name': 'site_id',
                            'label': 'ID de sitio',
                            'ttype': 'char',
                            'nullable': False,
                            'is_required': True,
                        },
                    ]
                }
            },
        ]
    )

def _create_permission_groups(ctx: Lylac.TransactionContext):

    ctx.create(
        'base.rules',
        [
            {
                'name': 'my_activity_only',
                'label': 'Sólo mis registros',
                'domain': "[('employee_id.user_id.id', '=', uid)]",
                'perm_read': True,
                'model_id': ctx.get_resource_id('base_model.assistance_registry_day'),
            },
            {
                'name': 'my_activity_only',
                'label': 'Sólo mis registros',
                'domain': "[('employee_id.user_id.id', '=', uid)]",
                'perm_read': True,
                'model_id': ctx.get_resource_id('base_model.assistance_registry_event'),
            },
            {
                'name': 'all_records',
                'label': 'Todos los registros',
                'domain': "[('id', '!=', None)]",
                'perm_read': True,
                'model_id': ctx.get_resource_id('base_model.assistance_registry_day'),
            },
            {
                'name': 'all_records',
                'label': 'Todos los registros',
                'domain': "[('id', '!=', None)]",
                'perm_read': True,
                'model_id': ctx.get_resource_id('base_model.assistance_registry_event'),
            },
            {
                'name': 'location_manager',
                'label': 'Gerente de ubicación',
                'domain': "[('employee_id.location_id.id', '=', user['location_id'])]",
                'perm_read': True,
                'model_id': ctx.get_resource_id('base_model.assistance_registry_day'),
            },
            {
                'name': 'location_manager',
                'label': 'Gerente de ubicación',
                'domain': "[('employee_id.location_id.id', '=', user['location_id'])]",
                'perm_read': True,
                'model_id': ctx.get_resource_id('base_model.assistance_registry_event'),
            },
        ]
    )

    # Modificación de grupo de permisos básicos añadiendo permisos
    ctx.update(
        'base.user.groups',
        ctx.get_resource_id('base_user_groups.basic_permissions'),
        {
            'access_ids': {
                'create': [
                    {
                        'name': 'location_warehouse__user',
                        'model_id': ctx.get_resource_id('base_model.location_warehouse'),
                        'perm_read': True,
                    },
                    {
                        'name': 'resource_device_type__user',
                        'model_id': ctx.get_resource_id('base_model.resource_device_type'),
                        'perm_read': True,
                    },
                    {
                        'name': 'resource_device__user',
                        'model_id': ctx.get_resource_id('base_model.resource_device'),
                        'perm_read': True,
                    },
                    {
                        'name': 'hr_employee__user',
                        'model_id': ctx.get_resource_id('base_model.hr_employee'),
                        'perm_read': True,
                    },
                    {
                        'name': 'schedule_week__user',
                        'model_id': ctx.get_resource_id('base_model.schedule_week'),
                        'perm_read': True,
                    },
                    {
                        'name': 'schedule_week_offset__user',
                        'model_id': ctx.get_resource_id('base_model.schedule_week_offset'),
                        'perm_read': True,
                    },
                    {
                        'name': 'assistance_registry_day__user',
                        'model_id': ctx.get_resource_id('base_model.assistance_registry_day'),
                        'perm_read': True,
                    },
                    {
                        'name': 'assistance_registry_event__user',
                        'model_id': ctx.get_resource_id('base_model.assistance_registry_event'),
                        'perm_read': True,
                    },
                ],
            },
            'rule_ids': {
                'add': [
                    ctx.get_resource_id('base_rules.assistance_registry_day__location_manager'),
                    ctx.get_resource_id('base_rules.assistance_registry_event__location_manager'),
                ],
            },
        },
    )

    ctx.create(
        'base.user.groups',
        [
            {
                'name': 'model_sync_admin',
                'label': 'Administrador de sincronización de datos',
                'access_ids': {
                    'create': [
                        {
                            'name': 'model_sync__admin',
                            'model_id': ctx.get_resource_id('base_model.model_sync'),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                    ],
                },
            },
        ],
    )

    ctx.create(
        'base.user.groups',
        [
            # Administrador de ubicaciones
            {
                'name': 'locations_admin',
                'label': 'Administrador de ubicaciones',
                'access_ids': {
                    'create': [
                        {
                            'name': 'location_warehouse__admin',
                            'model_id': ctx.get_resource_id('base_model.location_warehouse'),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                    ],
                },
            },
            # Administrador de dispositivos
            {
                'name': 'devices_admin',
                'label': 'Administrador de dispositivos',
                'access_ids': {
                    'create': [
                        {
                            'name': 'resource_device_type__admin',
                            'model_id': ctx.get_resource_id('base_model.resource_device_type'),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'resource_device__admin',
                            'model_id': ctx.get_resource_id('base_model.resource_device'),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                    ],
                },
            },
            # Administrador de empleados
            {
                'name': 'hr_admin',
                'label': 'Administrador de recursos humanos',
                'access_ids': {
                    'create': [
                        {
                            'name': 'hr_employee__admin',
                            'model_id': ctx.get_resource_id('base_model.hr_employee'),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        }
                    ]
                }
            },
            # Administrador de horarios
            {
                'name': 'schedules_admin',
                'label': 'Administrador de horarios',
                'access_ids': {
                    'create': [
                        {
                            'name': 'schedule_week__admin',
                            'model_id': ctx.get_resource_id('base_model.schedule_week'),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'schedule_week_offset__admin',
                            'model_id': ctx.get_resource_id('base_model.schedule_week_offset'),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                    ],
                },
            },
            # Administrador de registros de asistencia
            {
                'name': 'assistance_registry_admin',
                'label': 'Administrador de registro de asistencia',
                'access_ids': {
                    'create': [
                        {
                            'name': 'assistance_registry_day__admin',
                            'model_id': ctx.get_resource_id('base_model.assistance_registry_day'),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'assistance_registry_event__admin',
                            'model_id': ctx.get_resource_id('base_model.assistance_registry_event'),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'assistance_registry_event_correction__admin',
                            'model_id': ctx.get_resource_id('base_model.assistance_registry_event'),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                        {
                            'name': 'assistance_registry_event_credentials__admin',
                            'model_id': ctx.get_resource_id('base_model.assistance_registry_event_credentials'),
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                        },
                    ],
                },
                'rule_ids': {
                    'create': [
                        {
                            'name': 'all_records',
                            'label': 'Todos los registros',
                            'domain': "[('id', '!=', None)]",
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                            'model_id': ctx.get_resource_id('base_model.assistance_registry_day'),
                        },
                        {
                            'name': 'all_records',
                            'label': 'Todos los registros',
                            'domain': "[('id', '!=', None)]",
                            'perm_create': True,
                            'perm_read': True,
                            'perm_update': True,
                            'perm_delete': True,
                            'model_id': ctx.get_resource_id('base_model.assistance_registry_event'),
                        },
                    ],
                },
            },
        ],
    )

def _update_and_create_roles(ctx: Lylac.TransactionContext):

    ctx.update(
        'base.users.role',
        [
            ctx.get_resource_id('base_users_role.root_user'),
            ctx.get_resource_id('base_users_role.database_admin'),
        ],
        {
            'group_ids': {
                'add': [
                    ctx.get_resource_id('base_user_groups.locations_admin'),
                    ctx.get_resource_id('base_user_groups.devices_admin'),
                    ctx.get_resource_id('base_user_groups.hr_admin'),
                    ctx.get_resource_id('base_user_groups.schedules_admin'),
                    ctx.get_resource_id('base_user_groups.assistance_registry_admin'),
                    ctx.get_resource_id('base_user_groups.model_sync_admin'),
                ],
            },
        },
    )

def build_database_structure(ctx: Lylac.TransactionContext):

    _build_models_structure(ctx)
    _create_permission_groups(ctx)
    _update_and_create_roles(ctx)

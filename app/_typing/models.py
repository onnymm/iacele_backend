from typing import Literal
from lylac import Template
from lylac import TType
from lylac import Nullable

Weekday = Literal[
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday',
]

APIStatus = Literal[
    'check_in',
    'break_out',
    'break_in',
    'check_out',
    'undefined',
]

CustomStatus = APIStatus | Literal['null']

class Extension:

    class LocationWarehouse(Template.RecordWithBasicFields):
        short_name: TType.Char
        location_number: TType.Integer

    class ResourceDevice(Template.RecordWithBasicFields):
        model: Nullable[TType.Char]
        brand: Nullable[TType.Char]
        serial_number: Nullable[TType.Char]
        type_id: TType.Many2One
        location_id: Nullable[TType.Many2One]

    class ResourceDeviceType(Template.RecordWithBasicFields):
        ...

    class HREmployee(Template.RecordWithBasicFields):
        odoo_id: Nullable[TType.Integer]
        hire_date: TType.Date
        location_id: TType.Many2One

    class ScheduleWeek(Template.RecordWithBasicFields):
        weekday: TType.Selection[Weekday]
        start_time: TType.Time
        end_time: TType.Time

    class ScheduleWeekOffset(Template.RecordWithBasicFields):
        employee_id: TType.Many2One
        start_offset: TType.Duration
        weekday: TType.Selection[Weekday]

    class AssistanceRegistryDay(Template.RecordWithBasicFields):
        date: TType.Date
        employee_id: TType.Many2One
        schedule_id: TType.Many2One
        offset_id: TType.Many2One

    class AssistanceRegistryEvent(Template.RecordWithBasicFields):
        employee_id: TType.Many2One
        original_registry_time: TType.Datetime
        original_status: TType.Selection[APIStatus]
        device_id: TType.Many2One
        from_api: TType.Boolean
        registry_time_correction: Nullable[TType.Datetime]
        status_correction: Nullable[TType.Boolean]
        day_id: TType.Many2One

    class AssistanceRegistryEventCorrection(Template.RecordWithBasicFields):
        employee_id: TType.Many2One
        registry_time: TType.Datetime
        status: TType.Selection[CustomStatus]

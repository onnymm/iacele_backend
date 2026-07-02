from typing import Literal
from lylac import Lylac as _Lylac

MODELS = Literal[
    'assistance.registry.day',
    'assistance.registry.event',
    'assistance.registry.event.credentials',
    'assistance.registry.event.correction',
    'assistance.registry.event.sync',
    'hr.employee',
    'location.warehouse',
    'model.sync',
    'resource.device',
    'resource.device.type',
    'schedule.week',
    'schedule.week.offset',
]

Lylac = _Lylac[MODELS]

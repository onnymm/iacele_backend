from ...._core import iacele
from ...._core import Lylac

@iacele.api.validations.register(
    'create',
    'resource.device',
    'No pueden haber dos dispositivos con la misma marca, modelo y número de serie.',
)
def _resource_device__avoid_duplicated_devices_on_brand_model_and_sn(ctx: Lylac.ValidationContext):

    # Búsqueda de registros duplicados
    duplicated_records = ctx.find_duplicated_composite_keys(ctx.records, ['brand', 'model', 'serial_number'])

    # Si se encontraron registros duplicados
    if duplicated_records:
        # Iteración por cada registro duplicado
        for record in duplicated_records:
            # Se captura el registro
            ctx.catch(record)

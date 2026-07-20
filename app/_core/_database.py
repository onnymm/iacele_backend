from .._src import Lylac
from ._build_models import build_database_structure
from ._populate import populate
from ._ws_manager import WebsocketNotifier

iacele = Lylac(
    build_database_structure,
    populate,
    lambda ctx: WebsocketNotifier(ctx.uid),
)

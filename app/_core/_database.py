from .._src import Lylac
from ._build_models import build_database_structure
from ._populate import populate

iacele = Lylac(build_database_structure, populate)

# from typing import (
#     TYPE_CHECKING,
# )

# if TYPE_CHECKING:
#     from nomad.datamodel.datamodel import (
#         EntryArchive,
#     )
#     from structlog.stdlib import (
#         BoundLogger,
#     )

# from nomad.datamodel.data import Schema
# from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.config import config
from nomad.metainfo import Quantity, SchemaPackage
from nomad.datamodel.metainfo.eln import ELNSample
from nomad.datamodel.metainfo.basesections.v1 import EntityReference

configuration = config.get_plugin_entry_point(
    'nomad_lap_schema.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class Sample_LAP(ELNSample):
    process_of_origin = Quantity(
        type=EntityReference,
        description='The process of origin of the sample.',
    )


m_package.__init_metainfo__()

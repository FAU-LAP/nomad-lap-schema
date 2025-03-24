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
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.config import config
from nomad.datamodel.metainfo.basesections.v1 import Entity
from nomad.datamodel.metainfo.eln import ELNExperiment, ELNSample
from nomad.metainfo import Quantity, SchemaPackage

configuration = config.get_plugin_entry_point(
    "nomad_lap_schema.schema_packages:schema_package_entry_point"
)

m_package = SchemaPackage()


class Sample_LAP(ELNSample):
    process_of_origin = Quantity(
        type=Entity,
        shape=["*"],
        description="The process of origin of the sample.",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


class Experiment_LAP(ELNExperiment):
    samples = Quantity(
        type=Sample_LAP,
        description="The samples used in the experiment.",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


m_package.__init_metainfo__()

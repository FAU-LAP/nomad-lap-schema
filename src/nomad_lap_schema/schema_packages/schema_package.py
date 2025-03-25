from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.config import config
from nomad.datamodel.metainfo.eln import ELNExperiment, ELNSample, EntryData
from nomad.metainfo import Quantity, SchemaPackage, SectionProxy, Section

configuration = config.get_plugin_entry_point(
    "nomad_lap_schema.schema_packages:schema_package_entry_point"
)

m_package = SchemaPackage()


class Sample_LAP(ELNSample):
    m_def = Section()
    process_of_origin = Quantity(
        type=EntryData,
        description="The process of origin of the sample.",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


class Wafer_LAP(Sample_LAP):
    wafer_number = Quantity(
        type=str,
        description="Wafer Number provided by the manufacturer",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    manufacturer = Quantity(
        type=str,
        description="Manufacturer of the wafer",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    thickness = Quantity(
        type=float,
        unit="um",
        description="Thickness of the wafer",
        a_eln=ELNAnnotation(component="NumberEditQuantity"),
    )


class Experiment_LAP(ELNExperiment):
    samples = Quantity(
        type=Sample_LAP,
        shape=["*"],
        description="The samples used in the experiment.",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


m_package.__init_metainfo__()

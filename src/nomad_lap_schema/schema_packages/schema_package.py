from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    pass

from nomad.config import config
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.datamodel.metainfo.eln import ELNExperiment, ELNSample
from nomad.metainfo import Quantity, SchemaPackage, Section

configuration = config.get_plugin_entry_point(
    "nomad_lap_schema.schema_packages:schema_package_entry_point"
)

m_package = SchemaPackage()


class Room_LAP(Schema):
    FAMOS_code = Quantity(
        type=str,
        description="FAMOS code of the room",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    GPS_coordinates = Quantity(
        type=str,
        description="GPS coordinates of the room",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )


class Supplier_LAP(Schema):
    supplier_name = Quantity(
        type=str,
        description="Name of the supplier",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    supplier_address = Quantity(
        type=str,
        description="Address of the supplier",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    supplier_contact = Quantity(
        type=str,
        description="Contact of the supplier or name of the contact person",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    how_to_order = Quantity(
        type=str,
        description="Description of how order should be placed",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )


class Equipment_LAP(Schema):
    inventory_number = Quantity(
        type=str,
        description="Inventory number of the equipment",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    serial_number = Quantity(
        type=str,
        description="Serial number of the equipment",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )


class Sample_LAP(ELNSample):
    m_def = Section()
    process_of_origin = Quantity(
        type=Schema,
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
        a_display={"unit": "um"},
    )
    info_pdf = Quantity(
        type=str,
        description="Link to the pdf with the wafer information",
        a_eln=ELNAnnotation(component="FileEditQuantity"),
        a_browser=dict(adaptor="RawFileAdaptor", label="Info File Ref"),
    )
    orientation = Quantity(
        type=str,
        description="Orientation of the wafer",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    resistivity = Quantity(
        type=float,
        unit="V / A",
        description="Resistivity of the wafer",
        a_eln=ELNAnnotation(component="NumberEditQuantity"),
        a_display={"unit": "V / A"},
    )


class Chip_LAP(Sample_LAP):
    chip_number = Quantity(
        type=str,
        description="Chip Number provided by Jörg",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    width = Quantity(
        type=float,
        unit="mm",
        description="Width of the chip",
        a_eln=ELNAnnotation(component="NumberEditQuantity"),
        a_display={"unit": "mm"},
    )
    length = Quantity(
        type=float,
        unit="mm",
        description="Length of the chip",
        a_eln=ELNAnnotation(component="NumberEditQuantity"),
        a_display={"unit": "mm"},
    )
    wafer = Quantity(
        type=Wafer_LAP,
        description="The wafer the chip belongs to",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


class Device_LAP(Sample_LAP):
    device_number = Quantity(
        type=str,
        description="Device Number on the chip",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    chip = Quantity(
        type=Chip_LAP,
        description="The chip the device belongs to",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )
    device_type = Quantity(
        type=str,
        description="Type of the device",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )


class Experiment_LAP(ELNExperiment):
    samples = Quantity(
        type=Sample_LAP,
        shape=["*"],
        description="The samples used in the experiment.",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


m_package.__init_metainfo__()

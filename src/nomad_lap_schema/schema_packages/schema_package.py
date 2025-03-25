from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    pass

from nomad.config import config
from nomad.datamodel.data import ArchiveSection, Author, Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.datamodel.metainfo.eln import ELNExperiment, ELNInstrument, ELNSample
from nomad.metainfo import Datetime, Quantity, SchemaPackage, Section, SubSection

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
    version_number = Quantity(
        type=str,
        description="Version number of the equipment",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    patchnotes = Quantity(
        type=str,
        description="Notes of the last changes",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    manufacturer = Quantity(
        type=str,
        description="Manufacturer of the equipment",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    supplier = Quantity(
        type=Supplier_LAP,
        description="Supplier of the equipment",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


class Consumable_LAP(Schema):
    name = Quantity(
        type=str,
        description="Name of the consumable",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    supplier = Quantity(
        type=Supplier_LAP,
        description="Supplier of the consumable",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )
    batch_number = Quantity(
        type=str,
        description="Batch number of the consumable",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    amount_in_unit = Quantity(
        type=float,
        description="Amount of the consumable",
        a_eln=ELNAnnotation(component="NumberEditQuantity"),
    )
    storage_room = Quantity(
        type=Room_LAP,
        description="Storage room of the consumable",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )
    person_who_ordered = Quantity(
        type=Author,
        description="Person who ordered the consumable",
        a_eln=ELNAnnotation(component="AuthorEditQuantity"),
    )


class Facility_LAP(ELNInstrument):
    version_number = Quantity(
        type=str,
        description="Version number of the facility",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    patchnotes = Quantity(
        type=str,
        description="Notes of the last changes",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    betriebsanweisung = Quantity(
        type=str,
        description="Betriebsanweisungen of the facility",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    used_consumables = Quantity(
        type=Consumable_LAP,
        shape=["*"],
        description="Consumables used in the facility",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )
    responsible_person = Quantity(
        type=Author,
        description="Person responsible for the facility",
        a_eln=ELNAnnotation(component="AuthorEditQuantity"),
    )
    room = Quantity(
        type=Room_LAP,
        description="Room of the facility",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )
    equipment = Quantity(
        type=Equipment_LAP,
        shape=["*"],
        description="Equipment used in the facility",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


class Maintenance_LAP(Schema):
    timestamp = Quantity(
        type=Datetime,
        description="The date and time associated with this section.",
        a_eln=dict(component="DateTimeEditQuantity"),
    )
    description = Quantity(
        type=str,
        description="Description of the maintenance",
        a_eln=ELNAnnotation(component="RichTextEditQuantity"),
    )
    performed_by = Quantity(
        type=Author,
        description="Person who performed the maintenance",
        a_eln=ELNAnnotation(component="AuthorEditQuantity"),
    )
    facility = Quantity(
        type=Facility_LAP,
        description="Facility that was maintained",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


class Calibration_Parameter(ArchiveSection):
    parameter = Quantity(
        type=str,
        description="Name of the parameter",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    value = Quantity(
        type=float,
        description="Value of the parameter",
        a_eln=ELNAnnotation(component="NumberEditQuantity"),
    )


class Calibration_LAP(Maintenance_LAP):
    calibrated_parameters = SubSection(
        type=Calibration_Parameter,
        repeats=True,
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

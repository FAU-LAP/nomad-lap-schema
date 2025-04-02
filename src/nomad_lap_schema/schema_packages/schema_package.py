from nomad.config import config
from nomad.datamodel.data import ArchiveSection, Author, EntryDataCategory, Schema
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    Filter,
    SectionProperties,
)
from nomad.datamodel.metainfo.eln import (
    BasicEln,
    ELNExperiment,
    ELNInstrument,
    ELNSample,
    ReadableIdentifiers,
)
from nomad.metainfo import (
    Category,
    Quantity,
    SchemaPackage,
    Section,
    SectionProxy,
    SubSection,
)
from nomad_parser_plugins_camels_files.schema_packages.camels_package import (
    CamelsMeasurement,
)

configuration = config.get_plugin_entry_point(
    "nomad_lap_schema.schema_packages:schema_package_entry_point"
)

m_package = SchemaPackage()


class LAP_Category(EntryDataCategory):
    m_def = Category(label="Applied Physics Schema", categories=[EntryDataCategory])


class Project_LAP(BasicEln):
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(exclude=["lab_id", "datetime"]),
                order=["name", "description", "tags"],
            ),
        ),
        label="Project",
    )


class Research_Question_LAP(BasicEln):
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(exclude=["lab_id"]),
                order=["name", "datetime", "description", "projects", "tags"],
            ),
        ),
        label="Research Question",
    )
    projects = Quantity(
        type=Project_LAP,
        shape=["*"],
        description="Projects related to the research question",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


class Room_LAP(BasicEln):
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(exclude=["lab_id", "datetime", "description"]),
                order=["name", "FAMOS_code", "GPS_coordinates", "tags"],
            ),
        ),
        label="Room",
    )
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


class Supplier_LAP(BasicEln):
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(exclude=["lab_id", "datetime", "description"]),
                order=["name", "contact", "address", "how_to_order", "tags"],
            ),
        ),
        label="Supplier",
    )
    address = Quantity(
        type=str,
        description="Address of the supplier",
        a_eln=ELNAnnotation(component="RichTextEditQuantity"),
    )
    contact = Quantity(
        type=str,
        description="Contact of the supplier or name of the contact person",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    how_to_order = Quantity(
        type=str,
        description="Description of how order should be placed",
        a_eln=ELNAnnotation(component="RichTextEditQuantity"),
    )


class Equipment_LAP(BasicEln):
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(exclude=["lab_id", "datetime", "description"]),
                order=[
                    "name",
                    "inventory_number",
                    "serial_number",
                    "version_number",
                    "patchnotes",
                    "supplier",
                    "tags",
                ],
            ),
        ),
        label="Equipment",
    )
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
        a_eln=ELNAnnotation(component="RichTextEditQuantity"),
    )
    supplier = Quantity(
        type=Supplier_LAP,
        description="Supplier of the equipment",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


class Consumable_LAP(BasicEln):
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(exclude=["lab_id", "datetime", "description"]),
                order=[
                    "name",
                    "batch_number",
                    "amount_in_unit",
                    "supplier",
                    "storage_room",
                    "person_who_ordered",
                    "tags",
                ],
            ),
        ),
        label="Consumable",
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
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(exclude=["datetime"]),
                order=[
                    "name",
                    "labe_id",
                    "version_number",
                    "patchnotes",
                    "description",
                    "used_consumables",
                    "responsible_person",
                    "room",
                    "equipment",
                    "tags",
                ],
            ),
        ),
        label="Facility",
        a_template={"instrument_identifiers": {}},
    )
    version_number = Quantity(
        type=str,
        description="Version number of the facility",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    patchnotes = Quantity(
        type=str,
        description="Notes of the last changes",
        a_eln=ELNAnnotation(component="RichTextEditQuantity"),
    )
    description = Quantity(
        type=str,
        description="Instructions on the facility",
        a_eln=ELNAnnotation(component="RichTextEditQuantity", label="instructions"),
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
    facility_identifiers = SubSection(
        section_def=ReadableIdentifiers,
    )


class Maintenance_LAP(BasicEln):
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(exclude=["lab_id"]),
                order=[
                    "name",
                    "datetime",
                    "description",
                    "performed_by",
                    "facility",
                    "tags",
                ],
            ),
        ),
        label="Maintenance",
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
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(exclude=["lab_id"]),
                order=[
                    "name",
                    "datetime",
                    "description",
                    "calibrated_parameters",
                    "performed_by",
                    "facility",
                    "tags",
                ],
            ),
        ),
        label="Calibration",
    )
    calibrated_parameters = SubSection(
        section_def=Calibration_Parameter,
        repeats=True,
    )


class Sample_LAP(ELNSample):
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                order=[
                    "name",
                    "datetime",
                    "description",
                    "research_questions",
                    "process_of_origin",
                    "tags",
                ]
            ),
        ),
        label="General Sample",
        a_template={"sample_identifiers": {}},
    )
    process_of_origin = Quantity(
        type=Schema,
        description="The process of origin of the sample.",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )
    research_questions = Quantity(
        type=Research_Question_LAP,
        shape=["*"],
        description="Research questions related to the sample",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


class Doping_LAP(ArchiveSection):
    element = Quantity(
        type=str,
        description="Element that was doped",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    concentration = Quantity(
        type=float,
        unit="1/cm^3",
        description="Concentration of the doping",
        a_eln=ELNAnnotation(component="NumberEditQuantity"),
        a_display={"unit": "1/cm^3"},
    )
    thickness = Quantity(
        type=float,
        unit="um",
        description="Thickness of the doping layer",
        a_eln=ELNAnnotation(component="NumberEditQuantity"),
        a_display={"unit": "um"},
    )
    layer_starting_position = Quantity(
        type=float,
        unit="um",
        description="Starting position of the doping layer",
        a_eln=ELNAnnotation(component="NumberEditQuantity"),
        a_display={"unit": "um"},
    )


class Wafer_LAP(Sample_LAP):
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(exclude=["process_of_origin"]),
                order=[
                    "name",
                    "datetime",
                    "wafer_number",
                    "manufacturer",
                    "material",
                    "thickness",
                    "crystal_structure",
                    "orientation",
                    "doping",
                    "resistivity",
                    "info_pdf",
                    "description",
                    "research_questions",
                    "process_of_origin",
                    "tags",
                ],
            ),
        ),
        label="Wafer",
        a_template={"sample_identifiers": {}},
    )
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
    doping = SubSection(
        section_def=Doping_LAP,
        repeats=True,
    )
    crystal_structure = Quantity(
        type=str,
        description="Crystal structure of the wafer",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    material = Quantity(
        type=str,
        description="Material of the wafer",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )


class Chip_LAP(Sample_LAP):
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                order=[
                    "name",
                    "datetime",
                    "description",
                    "chip_number",
                    "width",
                    "length",
                    "wafer",
                    "research_questions",
                    "process_of_origin",
                    "tags",
                ]
            ),
        ),
        label="Chip (Sample)",
        a_template={"sample_identifiers": {}},
    )
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
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                order=[
                    "name",
                    "datetime",
                    "chip",
                    "device_number",
                    "device_type",
                    "description",
                    "research_questions",
                    "process_of_origin",
                    "tags",
                ]
            ),
        ),
        label="Device (Sample)",
        a_template={"sample_identifiers": {}},
    )
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


class Experimental_Protocol_LAP(BasicEln):
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(exclude=["lab_id", "datetime"]),
                order=["name", "description", "version_number", "tags"],
            ),
        ),
        label="Experimental Protocol",
    )
    version_number = Quantity(
        type=str,
        description="Version number of the protocol",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )


class Experiment_LAP(ELNExperiment):
    m_def = Section(
        categories=[],
    )
    samples = Quantity(
        type=Sample_LAP,
        shape=["*"],
        description="The samples used in the experiment.",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )
    experiment_type = Quantity(
        type=str,
        description="Type of the experiment",
        a_eln=ELNAnnotation(component="StringEditQuantity"),
    )
    experimental_protocol = Quantity(
        type=Experimental_Protocol_LAP,
        description="The protocol used for the experiment",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )
    research_questions = Quantity(
        type=Research_Question_LAP,
        shape=["*"],
        description="Research questions related to the experiment",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )
    facility = Quantity(
        type=Facility_LAP,
        description="Facility used in the experiment",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )
    experimentator = Quantity(
        type=Author,
        description="Person who performed the experiment",
        a_eln=ELNAnnotation(component="AuthorEditQuantity"),
    )
    special_equipment = Quantity(
        type=Equipment_LAP,
        shape=["*"],
        description="Special equipment used in the experiment",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


class Process_LAP(Experiment_LAP):
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                order=[
                    "name",
                    "datetime",
                    "description",
                    "samples",
                    "experiment_type",
                    "experimental_protocol",
                    "facility",
                    "experimentator",
                    "special_equipment",
                    "research_questions",
                    "tags",
                    "lab_id",
                ]
            ),
        ),
        label="Process",
        a_template={"experiment_identifiers": {}},
    )
    experiment_type = Quantity(
        type=str,
        description="Type of the experiment",
        a_eln=ELNAnnotation(component="StringEditQuantity", label="process type"),
    )
    process_identifiers = SubSection(
        section_def=ReadableIdentifiers,
    )


class Measurement_LAP(Experiment_LAP):
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                order=[
                    "name",
                    "datetime",
                    "description",
                    "samples",
                    "experiment_type",
                    "experimental_protocol",
                    "facility",
                    "data_files",
                    "camels_measurements",
                    "experimentator",
                    "special_equipment",
                    "research_questions",
                    "tags",
                    "lab_id",
                ]
            ),
        ),
        label="Measurement",
        a_template={"experiment_identifiers": {}},
    )
    data_files = Quantity(
        type=str,
        shape=["*"],
        description="The data file with the data of the measurement",
        a_eln=ELNAnnotation(component="FileEditQuantity"),
        a_browser=dict(adaptor="RawFileAdaptor", label="Data File"),
    )
    camels_measurements = Quantity(
        type=CamelsMeasurement,
        shape=["*"],
        description="The measurements of the camels",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


class Evaluation_LAP(BasicEln):
    m_def = Section(
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                order=[
                    "name",
                    "lab_id",
                    "datetime",
                    "description",
                    "performed_by",
                    "experiment",
                    "tags",
                ]
            ),
        ),
        label="Evaluation",
    )
    performed_by = Quantity(
        type=Author,
        description="Person who performed the evaluation",
        a_eln=ELNAnnotation(component="AuthorEditQuantity"),
    )
    experiment = Quantity(
        type=Experiment_LAP,
        description="Experiment that was evaluated",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


m_package.__init_metainfo__()

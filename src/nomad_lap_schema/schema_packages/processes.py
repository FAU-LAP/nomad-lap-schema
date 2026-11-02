"""Schemas for the standard sample fabrication processes at LAP."""

from nomad.datamodel.data import ArchiveSection
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    Filter,
    SectionProperties,
)
from nomad.metainfo import Quantity, SchemaPackage, Section, SubSection

from nomad_lap_schema.schema_packages.helpers import choice, number
from nomad_lap_schema.schema_packages.schema_package import (
    Experiment_LAP,
    Facility_LAP,
    LAP_Category,
)

m_package = SchemaPackage()

# Fields from Experiment_LAP that process entries hide by default.
PROCESS_HIDDEN = [
    "location",
    "lab_id",
    "special_equipment",
    "experimental_protocol",
    "research_questions",
]

# Gases suggested wherever a process records its gases. Add the gases of new
# processes here. Users can still enter any gas that is not listed.
GASES = ["N2", "Ar", "O2"]


def process_section(label, fields, hidden=PROCESS_HIDDEN):
    """ELN layout shared by all process schemas.

    `fields` are the process-specific fields, shown after the name and date and
    before the fields that every process has.
    """
    return Section(
        label=label,
        categories=[LAP_Category],
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                visible=Filter(exclude=hidden),
                order=[
                    "name",
                    "datetime",
                    *fields,
                    "description",
                    "samples",
                    "facility",
                    "experimentator",
                    "Images",
                    "tags",
                ],
            ),
        ),
    )


class SputteringProcess_LAP(Experiment_LAP):
    """
    Schema for logging a Thin Film Sputtering process (DC or HF).
    """

    m_def = process_section(
        label="Sputtering Process",
        fields=[
            "Sputtering_type",
            "Sample_material",
            "Sputter_target",
            "Chamber_pressure",
            "Process_gas",
            "Gas_flow",
            "High_Voltage",
            "Cathode_current",
            "Plasma_power",
            "Rate",
            "Final_thickness",
            "DC_voltage",
        ],
    )
    Sputtering_type = choice(
        description="Type of sputtering process (DC or HF).",
        suggestions=["DC", "HF"],
    )
    Sample_material = choice(
        description="Material of the sample being sputtered (e.g., SiC).",
        suggestions=["SiC"],
    )
    Sputter_target = choice(
        description="The type of material sputtered (e.g., Al, Ni, SiO2).",
        suggestions=["Al", "Ni", "SiO2"],
    )
    Chamber_pressure = number(
        unit="mbar",
        description="Chamber pressure during sputtering.",
    )
    Process_gas = choice(
        description="The gas used in the sputtering process.",
        suggestions=["Ar", "O2", "N2"],
    )
    Gas_flow = number(
        unit="cm**3 / minute",
        description="Gas flow during the sputtering process (sccm).",
    )
    High_Voltage = number(
        unit="kV",
        description="High voltage applied during HF sputtering.",
    )
    Cathode_current = number(
        unit="mA",
        description="Cathode current during the HF sputtering.",
    )
    Plasma_power = number(
        unit="W",
        description="Power applied during the sputtering process.",
    )
    Rate = number(
        unit="angstrom / second",
        description="Rate at which material is deposited on the substrate.",
    )
    Final_thickness = number(
        unit="nm",
        description="Final thickness of the sputtered layer.",
    )
    DC_voltage = number(
        unit="V",
        description="DC voltage applied during the sputtering process.",
    )


class ImplantationStep_LAP(ArchiveSection):
    m_def = Section(
        label="Implantation step",
    )
    Ion_type = choice(
        description="Type of ion used for implantation (e.g., N, Al, H).",
        suggestions=["N", "Al", "H"],
    )
    Ion_energy = number(
        unit="keV",
        description="Energy of the ions during implantation.",
    )
    Ion_dose = number(
        unit="cm**-2",
        description="Dose of ions implanted into the sample.",
    )
    Angle_of_implantation = number(
        unit="degree",
        description="Angle at which the ions are implanted into the sample.",
    )
    Temperature_during_implantation = number(
        unit="celsius",
        description="Temperature of the sample during the implantation process.",
    )
    facility = Quantity(
        type=Facility_LAP,
        description="Facility used for this implantation step",
        a_eln=ELNAnnotation(component="ReferenceEditQuantity"),
    )


class ImplantationProcess_LAP(Experiment_LAP):
    """
    Schema for logging Implantation process.
    """

    m_def = process_section(
        label="Implantation Process",
        fields=[
            "implantations",
        ],
        hidden=[
            "location",
            "lab_id",
            "special_equipment",
            "experimental_protocol",
        ],
    )
    implantations = SubSection(
        section_def=ImplantationStep_LAP,
        repeats=True,
    )


class AnnealingProcess_LAP(Experiment_LAP):
    """
    Schema for logging an Annealing process.
    """

    m_def = process_section(
        label="Annealing Process",
        fields=[
            "Anneal_temperature",
            "Anneal_time",
            "Process_gas",
            "Process_flow",
            "Process_pressure",
            "Process_temperature",
            "Process_time",
            "Buffer_layer_temperature",
            "Buffer_layer_time",
        ],
    )
    Anneal_temperature = number(
        unit="celsius",
        description="Temperature at which the annealing process is carried out.",
    )
    Anneal_time = number(
        unit="minute",
        description="Duration of the annealing process.",
    )
    Process_gas = choice(
        description="Gas used in the annealing process.",
        suggestions=["Ar"],
    )
    Process_flow = number(
        unit="cm**3 / minute",
        description="Flow of the gas during the annealing process.",
    )
    Process_pressure = number(
        unit="mbar",
        description="Pressure of the gas during the annealing process.",
    )
    Process_temperature = number(
        unit="celsius",
        description="Temperature of the process during the annealing process.",
    )
    Process_time = number(
        unit="minute",
        description="Duration of the process during the annealing process.",
    )
    Buffer_layer_temperature = number(
        unit="celsius",
        description="Temperature of the buffer layer during the annealing process.",
    )
    Buffer_layer_time = number(
        unit="minute",
        description="Duration of the buffer layer during the annealing process.",
    )


class OxidationGas_LAP(ArchiveSection):
    """
    A gas used during an oxidation process, with its flow and pressure.
    """

    m_def = Section(
        label="Oxidation gas",
    )
    Gas = choice(
        description="Gas used during the oxidation process.",
        suggestions=GASES,
    )
    Flow = number(
        unit="percent",
        description="Flow of the gas during the oxidation process.",
    )
    Pressure = number(
        unit="bar",
        description="Pressure of the gas during the oxidation process.",
    )


class OxidationProcess_LAP(Experiment_LAP):
    """
    Schema for logging a Thin Film Oxidation process.
    """

    m_def = process_section(
        label="Oxidation Process",
        fields=[
            "Oxidation_temperature",
            "Oxidation_time",
            "gases",
        ],
    )
    Oxidation_temperature = number(
        unit="celsius",
        description="Temperature at which the oxidation process is carried out.",
    )
    Oxidation_time = number(
        unit="minute",
        description="Duration of the oxidation process.",
    )
    gases = SubSection(
        section_def=OxidationGas_LAP,
        repeats=True,
    )


m_package.__init_metainfo__()

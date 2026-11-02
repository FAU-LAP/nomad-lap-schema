"""Shortcuts for the field types that LAP schemas use most often."""

from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import Quantity


def number(unit, description, display_unit=None):
    """A number with a unit, entered with a number field in the ELN.

    The ELN shows the value in `display_unit`, or in `unit` if none is given.
    """
    return Quantity(
        type=float,
        unit=unit,
        description=description,
        a_eln=ELNAnnotation(
            component="NumberEditQuantity",
            defaultDisplayUnit=display_unit or unit,
        ),
    )


def choice(description, suggestions):
    """A text field that suggests common values but accepts any input."""
    return Quantity(
        type=str,
        description=description,
        a_eln=ELNAnnotation(
            component="EnumEditQuantity",
            props=dict(suggestions=suggestions),
        ),
    )

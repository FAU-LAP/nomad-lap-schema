from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field
from nomad_lap_schema.schema_packages.schema_package import m_package


class LAPSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        return m_package


schema_package_entry_point = LAPSchemaPackageEntryPoint(
    name='LAPSchemaPackage',
    description='New schema package entry point configuration.',
)

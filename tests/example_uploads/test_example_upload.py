import pytest
import structlog
from nomad.client import normalize_all
from nomad.config import config
from nomad.datamodel import EntryArchive, EntryMetadata
from nomad.datamodel.context import ClientContext
from nomad.parsing.parser import ArchiveParser
from nomad.utils import generate_entry_id
from structlog.testing import capture_logs

ENTRY_POINT_ID = 'nomad_lap_schema.example_uploads:example_upload_entry_point'
UPLOAD_ID = 'example_upload'


@pytest.fixture(scope='module')
def upload_dir(tmp_path_factory):
    """Copies the example upload files the way NOMAD does when creating the upload."""
    config.load_plugins()
    entry_point = config.get_plugin_entry_point(ENTRY_POINT_ID)
    path = tmp_path_factory.mktemp('upload')
    entry_point.load(str(path))
    return path


def test_example_upload_entry_point(upload_dir):
    assert sorted(path.name for path in upload_dir.glob('*.archive.yaml'))


def test_example_upload_files_parse(upload_dir):
    for path in sorted(upload_dir.glob('*.archive.yaml')):
        # References between entries need an upload id, as they would in an upload.
        archive = EntryArchive(
            m_context=ClientContext(local_dir=str(upload_dir)),
            metadata=EntryMetadata(
                upload_id=UPLOAD_ID,
                entry_id=generate_entry_id(UPLOAD_ID, path.name),
                mainfile=path.name,
            ),
        )
        with capture_logs() as logs:
            logger = structlog.get_logger()
            ArchiveParser().parse(str(path), archive, logger)
            normalize_all(archive, logger)

        assert type(archive.data).__module__.startswith('nomad_lap_schema'), path.name
        errors = [log for log in logs if log['log_level'] in ('error', 'critical')]
        assert not errors, f'{path.name}: {errors}'

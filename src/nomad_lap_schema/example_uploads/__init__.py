from nomad.config.models.plugins import ExampleUploadEntryPoint

example_upload_entry_point = ExampleUploadEntryPoint(
    title='LAP Getting Started',
    category='Examples',
    description='A made-up project, wafer and two processes that show how LAP '
    'entries reference each other.',
    resources=['example_uploads/getting_started/*'],
)

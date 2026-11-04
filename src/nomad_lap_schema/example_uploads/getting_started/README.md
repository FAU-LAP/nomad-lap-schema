# Getting started with the LAP schemas

This example upload shows how LAP entries link to each other. All names and
values are made up.

- `project.archive.yaml`: a project (`Project_LAP`).
- `research_question.archive.yaml`: a research question that belongs to the project.
- `wafer.archive.yaml`: a 4H-SiC wafer (`Wafer_LAP`) that addresses the research question.
- `implantation.archive.yaml`: a two-step nitrogen implantation of the wafer
  (`ImplantationProcess_LAP`).
- `oxidation.archive.yaml`: a dry oxidation of the wafer (`OxidationProcess_LAP`).

Entries link to each other with references of the form
`../upload/archive/mainfile/<file>#data`, for example the processes list the
wafer under `samples`.

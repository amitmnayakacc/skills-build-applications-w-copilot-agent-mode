<!--
This file provides concise, actionable instructions for AI coding agents
working in this repository. Keep it short and specific to the patterns
and workflows discoverable in the codebase and `.github/instructions`.
-->

# Copilot / AI Agent Instructions (OctoFit Tracker)

Purpose: Help coding agents become productive quickly in this repository by
calling out architecture, key workflows, repo-specific conventions, and
concrete examples of files to read or modify.

1) Big-picture architecture
- Monorepo-like layout: top-level app described as `octofit-tracker/` with
  `backend/` and `frontend/` concerns. See `.github/instructions/*` for setup
  details and the intended structure.
- Backend: Django (see `.github/instructions/octofit_tracker_django_backend.instructions.md`).
- Frontend: React (see `.github/instructions/octofit_tracker_react_frontend.instructions.md`).

2) Developer workflows (explicit commands and locations)
- Do NOT change directories when running automated commands in agent mode; point
  to subpaths instead (this repo's dev instructions require this). Example:

  `python3 -m venv octofit-tracker/backend/venv`

  `source octofit-tracker/backend/venv/bin/activate && pip install -r octofit-tracker/backend/requirements.txt`

- To run Django dev server (from any cwd):

  `octofit-tracker/backend/venv/bin/python octofit-tracker/backend/manage.py runserver 0.0.0.0:8000`

  (Adjust interpreter path if using a different venv name.)

3) Important repository conventions
- Virtual env path: `octofit-tracker/backend/venv` (the `.github` instructions create it).
- `requirements.txt` must live in `octofit-tracker/backend/requirements.txt` and follow
  the pinned packages already described in `.github/instructions/octofit_tracker_setup_project.instructions.md`.
- Database: intended to use MongoDB via `djongo` / `pymongo` packages listed in requirements. Use Django ORM —
  do not use raw MongoDB scripts to create DB structure/data (see setup instructions file).

4) Integration and external dependencies
- MongoDB: `mongodb-org` / `mongosh` referenced in setup notes. Check for running daemon
  with `ps aux | grep mongod` before attempting DB tasks.
- Frontend and backend communicate over HTTP (dev ports below); CI uses workflows
  under `.github/workflows/*.yml` to orchestrate setup steps.

5) Where to look first (concrete files)
- Setup & onboarding steps: `.github/steps/*` and `.github/instructions/*` (read these before making infra changes).
- CI/workflows: `.github/workflows/` — the YAML files show the expected commands and sequence used by automation.
- App story and goals: `docs/octofit_story.md` and top-level `README.md`.

6) Agent behavior rules (repo-specific)
- Preserve and reuse pinned versions in `requirements.txt` found in instructions.
- When writing commands or CI changes, reference existing workflow names: e.g. `4-setup-django-rest-framework.yml`,
  `5-setup-frontend-react-framework.yml`, `6-copilot-on-github.yml` to stay consistent with repo automation.
- Do not expose or suggest additional forwarded ports beyond `8000`, `3000`, and `27017`.
- Keep edits minimal and surgical: prefer to update instructions files under `.github/instructions/` rather than changing
  multiple unrelated top-level files.

7) Examples of common tasks and how to implement them
- Add a backend dependency: update `octofit-tracker/backend/requirements.txt` and test by running the venv install
  command shown above.
- Modify Django settings: update `octofit-tracker/backend/octofit_tracker/settings.py` (if present). Run migrations via:

  `octofit-tracker/backend/venv/bin/python octofit-tracker/backend/manage.py migrate`

8) Safety and merge guidance
- If `.github/copilot-instructions.md` already exists, merge useful content from `.github/instructions/*` and
  preserve pinned commands and requirements blocks. Prefer small commits with clear messages like
  "docs: update copilot instructions — note venv path and run commands".

9) Ask for clarifications
- If a required workflow or convention is missing (for example, exact `manage.py` path or specific npm scripts),
  ask a human before making assumptions.

---
If anything above is unclear or you'd like more examples (CI snippets, common PR templates, or exact run/test commands),
tell me which area to expand and I'll iterate.

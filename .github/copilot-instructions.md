# Copilot Instructions for Flask-Portfolio

## Project Overview
This is a Flask-based portfolio web application. The main entry point is `app.py`. Static assets are in `static/` and HTML templates in `templates/`. Uploaded files are stored in `static/uploads/`. Data for contacts is managed via `contacts.json`.

## Architecture & Data Flow
- **Flask App (`app.py`)**: Handles routing, request processing, and template rendering.
- **Templates (`templates/`)**: Use Jinja2 for dynamic HTML. `base.html` is the main layout.
- **Static Files (`static/`)**: CSS, JS, images, and uploads. Organize assets by type.
- **Contacts Data (`contacts.json`)**: Stores contact info, likely read/written by Flask routes.

## Developer Workflows
- **Run the App**: Use `flask run` or `python app.py` (if `app.py` has an `if __name__ == '__main__'` block).
- **Dependencies**: Install with `pip install -r requirements.txt`.
- **Debugging**: Enable Flask debug mode by setting `FLASK_ENV=development`.
- **Static/Template Changes**: No build step; changes are reflected on reload.

## Project-Specific Patterns
- **Template Inheritance**: `base.html` is extended by other templates.
- **Contact Management**: Interactions with `contacts.json` should be atomic to avoid data loss.
- **Uploads**: Uploaded files go to `static/uploads/`.
- **No tests or CI/CD detected**: Add tests in a `tests/` folder if needed.

## Integration Points
- **External Dependencies**: All Python packages are listed in `requirements.txt`.
- **No API integrations detected**: If present, document endpoints and usage.

## Examples
- To add a new page, create a route in `app.py`, a template in `templates/`, and link static assets as needed.
- To update styles, edit `static/css/style.css`.

## Key Files
- `app.py`: Main Flask app
- `requirements.txt`: Python dependencies
- `contacts.json`: Contact data
- `templates/base.html`: Main HTML layout
- `static/`: Static assets

---
Update this file as project conventions evolve. For questions, review `app.py` and template structure.

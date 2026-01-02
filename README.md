# Neutral TS Starter Py

**Neutral TS Starter Py** es un scaffold modular y opinionado para construir Progressive Web Applications (PWA) usando **Python (Flask)** en el backend y **Neutral TS** como motor de plantillas universal.

Este proyecto está diseñado para ser extensible mediante una arquitectura de componentes "plug-and-play", permitiendo escalabilidad desde prototipos rápidos hasta aplicaciones complejas manteniendo una estructura limpia y desacoplada.

## Features

*   **Solid Backend**: Built on **Flask**, leveraging its ecosystem and simplicity.
*   **Modular Architecture**: Everything is a component. Logic, routes, templates, and configurations are encapsulated in independent modules within `src/component`.
*   **PWA Ready**: Configuration ready for Service Workers, manifests, and mobile optimization.
*   **Neutral Templating (NTPL)**: Powerful templating system allowing inheritance, mixins, and dynamic rendering.
*   **Override System**: Customize base components without touching their original code thanks to the cascading loading system.

## Prerequisitos

*   Python 3.8 or higher.
*   pip (Python package manager).
*   Recommended: Virtual environment (`venv`).

## Quick Start

### 1. Clone and Configure Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate environment (Linux/Mac)
source .venv/bin/activate

# Activate environment (Windows)
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run in Development

```bash
python src/run.py
```

The application will be available at `http://localhost:5000` (by default).

## Project Structure

```
nts-starter-py/
├── src/
│   ├── app/                    # Flask application factory and core configuration
│   ├── component/              # MODULE COLLECTION (The most important part)
│   │   ├── cmp_7000_hellocomp/ # Example of a full component
│   │   └── README.md           # Detailed component documentation
│   ├── neutral/                # Template engine core
│   ├── run.py                  # Execution script for development
│   └── wsgi.py                 # Entry point for production (Gunicorn/uWSGI)
├── config/                     # General configuration files
└── public/                     # Public static files
```

## Component Architecture

The strength of this starter lies in `src/component`. Each folder there is a self-sufficient module.

### Basic Rules
1.  **Prefix**: Components must start with `cmp_` (e.g., `cmp_5000_login`).
2.  **Order**: They load alphabetically. `cmp_5005` will override `cmp_5000` if there are conflicts.
3.  **Content**: A component can have:
    *   `manifest.json`: Metadata and base path.
    *   `route/`: Python logic (Flask Blueprints).
    *   `neutral/`: HTML templates and snippets.
    *   `static/`: Specific assets (JS/CSS).

You can consult `src/component/cmp_7000_hellocomp/README.md` for a detailed example of a "Hello Component", or the technical documentation in `src/component/README.md`.

## Configuration

Configuration is handled in layers:
1.  **Global**: Environment variables and Flask configuration.
2.  **Per Component**: `schema.json` within each component.
3.  **Customization**: `custom.json` (ignored by git) allows overriding local configurations without affecting the codebase.

## Deployment

For production, use a WSGI server like Gunicorn pointing to `src/wsgi.py`:

```bash
gunicorn -w 4 src.wsgi:app
```

# Components in Neutral PWA Starter

This directory is the core of project modularity. Components are isolated functional units that can contain server logic, routes, frontend templates, and configuration.

This document details how they work internally, how they interact with the core (Flask + Neutral Templating), and how to extend the application.

---

## 1. Definition and Naming Rules

A component lives in its own folder under `src/component/`.

### Loading rules and prefix
*   **Mandatory prefix**: The directory name must start with `cmp_`. Any folder that does not follow this pattern will be ignored.
*   **Deactivation**: A component can be deactivated simply by renaming its folder, for example, changing `cmp_0500_login` to `_cmp_0500_login`.
*   **Alphabetical Order**: Loading is done in alphabetical order. The number `NNNN` in the name is a useful convention to control this order.

### Overriding
Due to the loading order, a later component can override or extend the functionality of an earlier one.

*   `cmp_5000_page` (Base component)
*   `cmp_5001_page` (Extension)

`cmp_5001_page` could override configurations, templates, or routes defined in `cmp_5000_page`.

---

## 2. Loading Life Cycle

When starting the application, the system performs the following steps:

1.  **Discovery**: Scans `src/component/` looking for `cmp_` folders.
2.  **Registration**: Reads `manifest.json`.
3.  **Data Merging**: Loads `schema.json` and merges it with `custom.json` (if it exists) and then with the global schema.
4.  **Python Initialization**: Executes `__init__.py` if it exists.
5.  **Routes**: Executes `init_blueprint` in `route/__init__.py`.
6.  **Global Templates**: Loads snippets from `component-init.ntpl`.

---

## 3. Configuration Files

### schema.json

Defines the data structure and configuration. It is divided into critical sections for the operation of the Neutral engine.

*   **config**: Internal engine configuration (cache, debug, etc.).
*   **inherit**: Defines the local context and inheritance tools.
    *   **data**: Variables accessible as `{:;local::varname:}`. Can be dynamically overridden.
    *   **locale**: Translation system.
        *   `current`: Current language.
        *   `trans`: Dictionary of translations.
    *   **snippets**: Definition of initial snippets. (It is recommended to use `.ntpl` files instead).
    *   **declare**: Definition of declarations or macros. (It is recommended to use `.ntpl` files instead).
*   **data**: Global variables accessible as `{:;varname:}`. By convention, contains environment information (request, post, get) and **cannot be dynamically overridden** at runtime; they are global.

### custom.json

Allows overriding configuration without touching the original code.
**Important Rule**: The component provider must never include this file; it is exclusively for local user customization.

Structure:
```json
{
    "schema": {},
    "manifest": {}
}
```
*   `schema`: Merges and overrides keys from `schema.json`.
*   `manifest`: Merges and overrides keys from `manifest.json` (useful for changing base routes).

---

## 4. Template System (NTPL)

Neutral Templating allows for code injection and extreme modularity.

### Global Level: `neutral/component-init.ntpl`
Loaded during discovery. It can include snippets, includes, and locales that will be available globally. Although loaded at startup, its content is evaluated on every request.

### Component Level: `neutral/route/index-snippets.ntpl`
Loaded dynamically for all routes served by the component. Ideal for common layouts or shared logic of the module.

### Route Level: `neutral/route/[ROUTE]/content-snippets.ntpl`
Contains the specific template for a page.
**Convention**: Must define the `current:template:body-main-content` snippet, which is what the main layout will render inside the `<main>` tag.

---

## 5. Routes and Backend (Flask)

If the component requires server logic (not just static templates), the `route/` structure is used.

*   **Blueprints**: Defined in `route/__init__.py`. Must use `create_blueprint` which respects the manifest's `url_prefix`.
*   **Static Files**: Each component can serve its own CSS/JS. It is recommended to create a `static` folder within the component and a Flask route to serve them, as this maintains encapsulation.

---

## 6. Guide: Create a Component from Scratch

Example of creating a "Hello World" component.

1.  **Directory**: `src/component/cmp_9900_hola`

2.  **Manifest (`manifest.json`)**:
    ```json
    {
        "uuid": "hola_x1y2z3",
        "name": "Hello World",
        "description": "Simple example",
        "version": "1.0.0",
        "route": "/hola"
    }
    ```

3.  **Translations (`schema.json`)**:
    ```json
    {
        "inherit": {
            "locale": {
                "trans": {
                    "es": { "Greeting": "Saludos Terrestre" },
                    "en": { "Greeting": "Greetings Earthling" }
                }
            }
        }
    }
    ```

4.  **Backend (`route/__init__.py`)**:
    ```python
    from app.components import create_blueprint, set_current_template
    from core.dispatcher import Dispatcher
    from flask import request

    def init_blueprint(component, component_schema, _):
        bp = create_blueprint(component, component_schema)

        @bp.route('/')
        def index():
            set_current_template(component, component_schema)
            return Dispatcher(request, bp.url_prefix).view.render()

        return bp
    ```

5.  **Global Template (`neutral/component-init.ntpl`)**:
    ```html
    {:snip; hola-menu-item >>
        <a href="/hola" class="nav-link">{:trans; Greeting :}</a>
    :}
    ```

6.  **View (`neutral/route/index.ntpl`)**:
    (Replaces content-snippets if the simple default structure of the Dispatcher is used or explicitly configured).
    ```html
    <h1>{:trans; Greeting :}</h1>
    ```

---

## 7. Debugging

*   If a component does not load, check the `cmp_` prefix.
*   If changes in `schema.json` are not reflected, check if an interfering `custom.json` exists.
*   Use `{:;local::varname:}` for mutable data and `{:;varname:}` for immutable request data.

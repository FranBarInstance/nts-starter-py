# Hello Component (cmp_7000_hellocomp)

This module is an example component designed to illustrate the modular architecture based on **Neutral PWA**. It strictly follows the specifications defined in `src/component/README.md`.

## 1. Identity and Purpose

*   **Identifier**: `hellocomp_0yt2sa`
*   **Base Path**: `/hello-component`
*   **Purpose**: To show how to structure routes, templates, and backend logic in an isolated component.

## 2. File Architecture

The directory structure follows the component standard:

```
src/component/cmp_7000_hellocomp/
├── manifest.json                # Component definition (UUID, version, base path)
├── schema.json                  # Global configuration and data schema
├── custom.json                  # (Optional) Local configuration override
├── route/                       # Backend Logic (Python/Flask)
│   ├── __init__.py              # Blueprint initialization
│   ├── routes.py                # Flask endpoints definition
│   └── dispatcher_...           # Custom dispatch logic
└── neutral/                     # Frontend Logic (NTPL Templates)
    ├── route/                   # Templates organized by route
    │   ├── index-snippets.ntpl  # Snippets shared by the entire component
    │   ├── locale.json          # Local translations
    │   └── hello-component/     # Specific templates for the base path
```

## 3. Backend Operation (`route/`)

The `route/routes.py` file demonstrates two ways of handling requests:

### A. Custom Dispatch (`/test1`)
Defines an explicit route that uses a class inherited from `Dispatcher` to inject python logic before rendering.

*   **Endpoint**: `@bp.route('/test1')`
*   **Dispatcher**: `DispatcherHelloComp` (in `dispatcher_hellocomp.py`)
*   **Flow**:
    1.  Receives the request.
    2.  Instantiates `DispatcherHelloComp`.
    3.  Executes custom logic (e.g., `dispatch.schema_data['dispatch_result'] = "True"`).
    4.  Renders the view.

### B. Generic Dispatch (Catch-all)
Uses the base `Dispatcher` from `core` to map the URL directly to the folder structure in `neutral/`.

*   **Endpoint**: `@bp.route("/", ...)` and `@bp.route("/<path:relative_route>", ...)`
*   **Flow**:
    1.  Captures any route not explicitly defined (e.g., `/hello-component/test2`).
    2.  Resolves the relative template path.
    3.  Automatically renders by looking for `content-snippets.ntpl` in the corresponding folder of `neutral/`.

## 4. Frontend Operation (`neutral/`)

The template system uses **Neutral Templating (NTPL)**.

### Template Hierarchy
1.  **Global**: `neutral/route/index-snippets.ntpl` defines reusable snippets for the entire component.
2.  **Base Path (`/`)**: Maps to `neutral/route/hello-component/content-snippets.ntpl`.
3.  **Sub-routes (`/test1`, `/test2`)**: Map to folders within `neutral/route/hello-component/` (e.g., `test1/content-snippets.ntpl`).

### Key Files
*   **`content-snippets.ntpl`**: Defines the main content of the page using the snippet `current:template:body-main-content`.
*   **`data.json`**: Defines static data specific to that route (page title, metadata).
*   **`locale.json`**: Dictionary of translations accessible via `{:trans; Key :}`.

## 5. Request Flow Example

When a user accesses `http://app/hello-component/test2`:

1.  Flask (in `routes.py`) captures the route in the function `hellocomponent_catch_all`.
2.  The `Dispatcher` calculates the template path: `neutral/route/hello-component/test2`.
3.  `neutral/route/hello-component/test2/data.json` is loaded (if it exists).
4.  `neutral/route/hello-component/test2/content-snippets.ntpl` is rendered.
5.  The result is injected into the main application layout.

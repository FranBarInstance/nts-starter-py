# Hello Component (cmp_7000_hellocomp)

This module is an example component designed to illustrate the modular architecture of the **Neutral PWA** framework. It serves as a reference for creating new components and follows the specifications defined in the core documentation.

## 1. Identity and Registration

*   **Identifier (UUID)**: `hellocomp_0yt2sa` (Must be unique and follow the `name_random` format).
*   **Base Path**: `/hello-component` (Defined in `manifest.json`).
*   **Version**: `0.0.0`

### Registration Lifecycle
1.  **Manifest Processing**: The system reads `manifest.json` to identify the component and its base route.
2.  **Configuration Merging**: `schema.json` is loaded and merged into the global application schema. If `custom.json` exists, it can override values.
3.  **Route Initialization**: The `route/__init__.py` file initializes the Flask Blueprint and sets up the template directories.

## 2. File Architecture

```
src/component/cmp_7000_hellocomp/
├── manifest.json                     # Registration metadata
├── schema.json                       # Global data and inheritance
├── custom.json                       # Local overrides
├── route/                            # Backend (Python/Flask)
│   ├── __init__.py                   # Blueprint & Template setup
│   ├── routes.py                     # Endpoints
│   └── dispatcher_hellocomp.py       # Custom business logic
└── neutral/                          # Frontend (NTPL)
    ├── component-init.ntpl           # (Optional) Global snippets for all app
    └── route/                        # Templates matching URL structure
        ├── index-snippets.ntpl       # Shared snippets for this component
        ├── locale.json               # Component-wide translations
        └── root/          # Templates for /hello-component/*
            ├── data.json             # Route-specific metadata
            └── content-snippets.ntpl # Main content
```

## 3. Data Schema and Inheritance (`schema.json`)

The `schema.json` file is powerful because it allows a component to "inject" itself into the main application.

*   **`inherit` Section**: Anything here is merged into the global schema.
    *   **`locale`**: Adds translations that are available globally.
    *   **`data:drawer:menu`**: Automatically adds links to the application's sidebar.
    *   **`data:menu`**: Adds links to the main navigation menu.
*   **`data` Section**: Local data namespaced by the component's UUID (or a custom name). In this component, it defines `hello-component` data accessible via `{:;hello-component->... :}`.

## 4. Backend Logic (`route/`)

The backend uses a `Dispatcher` pattern to bridge Flask and the NTPL engine.

### The Dispatcher (`dispatcher_hellocomp.py`)
Custom dispatchers inherit from `core.dispatcher.Dispatcher`. They have access to:
*   `self.req`: The Flask request object.
*   `self.schema_data`: A dictionary where you can inject data to be used in templates.
*   `self.view`: The template engine instance.

### Routing Strategies (`routes.py`)
1.  **Explicit Routes**: Use `@bp.route('/path')` for custom logic.
    ```python
    @bp.route('/test1')
    def test1(route):
        dispatch = DispatcherHelloComp(request, route, bp.current_neutral_route)
        dispatch.schema_data['custom_var'] = "Value" # Accessible in NTPL
        return dispatch.view.render()
    ```
2.  **Catch-all Routing**: Automatically maps any other URL to the folder structure in `neutral/route/`.

## 5. Frontend Templating (NTPL)

### Key Syntax
*   **Data Access**: `{:;key->subkey:}` (e.g., `{:;hello-component->hello:}`).
*   **Translations**: `{:trans; Text to translate :}` (uses `locale.json`).
*   **Snippets**:
    *   **Define**: `{:snip; name >> content :}`
    *   **Use**: `{:snip; name :}`
*   **Main Content**: Every page must define the `current:template:body-main-content` snippet.

### File Hierarchy
1.  `neutral/route/index-snippets.ntpl`: Loaded for every route in the component. Good for shared `{:locale; ... :}` or common UI fragments.
2.  `neutral/route/<path>/content-snippets.ntpl`: Specific content for the requested URL.

## 6. Request Flow Examples

Each route in the component follows a similar yet slightly different flow depending on whether it uses a custom dispatcher or the generic one.

### A. Base Route: `/hello-component`
*   **Trigger**: User accesses the base URL of the component.
*   **Backend**: Handled by `hellocomp_catch_all` in `routes.py` (Generic Dispatcher).
*   **Template Resolution**:
    1.  `Dispatcher` identifies the route as `/`.
    2.  Looks for templates in `neutral/route/hello-component/`.
    3.  Loads `data.json` for base metadata.
    4.  Renders `content-snippets.ntpl`.
*   **Result**: Displays the default component homepage.

### B. Custom Route: `/hello-component/test1`
*   **Trigger**: User accesses a specific endpoint requiring custom Python logic.
*   **Backend**: Handled by `test1` in `routes.py` using `DispatcherHelloComp`.
*   **Execution**:
    1.  `DispatcherHelloComp` is instantiated.
    2.  `dispatch.schema_data['dispatch_result'] = "True"` is set manually.
    3.  Template route is set explicitly to `neutral/route/hello-component/test1`.
*   **Template Resolution**:
    1.  Loads `data.json` from the `test1` folder.
    2.  Renders `content-snippets.ntpl` from the `test1` folder.
*   **Result**: Displays content enriched with data injected from the Python backend.

### C. Generic Sub-route: `/hello-component/test2`
*   **Trigger**: User accesses a sub-path that has no explicit Flask route.
*   **Backend**: Captured by the `hellocomp_catch_all` regex in `routes.py`.
*   **Template Resolution**:
    1.  `Dispatcher` receives the `relative_route` as `test2`.
    2.  Automatically maps the path to `neutral/route/hello-component/test2/`.
    3.  Loads local `data.json` and renders `content-snippets.ntpl`.
*   **Result**: Displays the page content based purely on file structure, without extra Python code.

## 7. Development Guide: Adding a New Route

To add a new sub-route `/hello-component/my-page`:

1.  **Create the directory**: `mkdir -p src/component/cmp_7000_hellocomp/neutral/route/hello-component/my-page`
2.  **Define metadata**: Create `data.json` in that directory:
    ```json
    {
        "current": {
            "template": {
                "title": "My New Page"
            }
        }
    }
    ```
3.  **Create the content**: Create `content-snippets.ntpl`:
    ```html
    {:snip; current:template:body-main-content >>
        <div class="container">
            <h1>Dynamic Content</h1>
            <p>This is my new page.</p>
        </div>
    :}
    ```
4.  **Optional Python Logic**: If you need backend processing, add an explicit route in `routes.py` and create a matching folder in `neutral/route/`. If you don't need Python, the **Catch-all** handler will find your new folder automatically.

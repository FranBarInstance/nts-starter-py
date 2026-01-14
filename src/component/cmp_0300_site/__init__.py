"""Component site - Init"""

from app.config import Config  # pylint: disable=import-error


def init_component(_component, component_schema, _schema):
    """Component - Init"""

    languages = component_schema['data']['current']['site']['languages']

    # Language menu for dropdown
    menu = {
        'name': 'Language',
        'link': '',
        'icon': 'x-icon-locale',
        'prop': {},
        'dropdown': {}
    }

    # create menu dropdown items
    for lang in languages:
        menu['dropdown'][lang] = {
            'name': f'ref:locale:{lang}',
            'link': f'?{Config.LANG_KEY}={lang}',
            'icon': 'x-icon-bullet',
            'prop': {}
        }

    # set menu in local data
    component_schema['inherit']['data']['navbar']['menu']['session:']['language'] = menu
    component_schema['inherit']['data']['navbar']['menu']['session:true']['language'] = menu

from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from packaging.version import Version

from plugins import template_vars


APP_ROOT = Path(__file__).parents[1].resolve()


class FakeArgs:
    def keys(self):
        return []

    def getlist(self, param):
        return []


class FakeRequest:
    args = FakeArgs()


def test_extra_template_vars_includes_app_version():
    extra_vars = template_vars.extra_template_vars(None, FakeRequest())
    app_version = extra_vars['app_version']

    assert app_version
    assert Version(str(app_version)) >= Version('0.2.3')


def test_footer_displays_app_version_after_source_code():
    env = Environment(loader=FileSystemLoader(APP_ROOT / 'templates'))
    rendered = env.get_template('_footer.html').render(app_version='0.2.3')

    assert 'Source code' in rendered
    assert 'v0.2.3' in rendered

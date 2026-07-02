from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from packaging.version import Version
import pytest

from plugins import template_vars


APP_ROOT = Path(__file__).parents[1].resolve()


class FakeArgs:
    def keys(self):
        return []

    def getlist(self, param):
        return []


class FakeRequest:
    args = FakeArgs()


@pytest.fixture(autouse=True)
def clear_app_version_cache():
    # get_app_version() is cached, so patched citation paths must not leak between tests.
    template_vars.get_app_version.cache_clear()
    yield
    template_vars.get_app_version.cache_clear()


def test_extra_template_vars_includes_app_version():
    extra_vars = template_vars.extra_template_vars(None, FakeRequest())
    app_version = extra_vars['app_version']

    assert app_version
    assert Version(str(app_version)) >= Version('0.2.3')


def test_get_app_version_returns_none_when_citation_is_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(template_vars, 'APP_CITATION_PATH', tmp_path / 'missing.cff')

    assert template_vars.get_app_version() is None


def test_get_app_version_returns_none_when_citation_is_invalid(tmp_path, monkeypatch):
    citation_path = tmp_path / 'CITATION.cff'
    citation_path.write_text('not: [valid')
    monkeypatch.setattr(template_vars, 'APP_CITATION_PATH', citation_path)

    assert template_vars.get_app_version() is None


def test_get_app_version_returns_none_when_citation_is_empty(tmp_path, monkeypatch):
    citation_path = tmp_path / 'CITATION.cff'
    citation_path.write_text('')
    monkeypatch.setattr(template_vars, 'APP_CITATION_PATH', citation_path)

    assert template_vars.get_app_version() is None


def test_get_app_version_returns_none_when_citation_is_unreadable(monkeypatch):
    class UnreadableCitationPath:
        def open(self):
            raise OSError('Could not read CITATION.cff')

    monkeypatch.setattr(template_vars, 'APP_CITATION_PATH', UnreadableCitationPath())

    assert template_vars.get_app_version() is None


def test_footer_displays_app_version():
    env = Environment(loader=FileSystemLoader(APP_ROOT / 'templates'))
    rendered = env.get_template('_footer.html').render(app_version='0.2.3')

    assert 'Source code' in rendered
    assert 'v0.2.3' in rendered

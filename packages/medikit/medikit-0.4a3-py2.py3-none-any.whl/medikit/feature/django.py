"""
The «django» feature adds the django framework to your project.

"""

import os
import random

from medikit.events import subscribe
from . import Feature, SUPPORT_PRIORITY

random = random.SystemRandom()


def generate_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)'
    return ''.join(random.choice(chars) for i in range(64))


class DjangoConfig(Feature.Config):
    """ Configuration class for the “django” feature. """

    use_jinja2 = True
    """Whether or not to use the Jinja2 templating language (default: True)."""

    use_whitenoise = True
    """Whether or not to use Whitenoise for the static files (default: True)."""

    def __init__(self):
        self.use_jinja2 = self.use_jinja2
        self.use_whitenoise = self.use_whitenoise


class DjangoFeature(Feature):
    requires = {'python'}

    Config = DjangoConfig

    @subscribe('medikit.feature.python.on_generate')
    def on_python_generate(self, event):
        event.config['python'].add_requirements('django ==2.0a1', )

        if event.config['django'].use_jinja2:
            event.config['python'].add_requirements('Jinja2 >=2.9,<2.10', )

        if event.config['django'].use_whitenoise:
            event.config['python'].add_requirements(
                'brotlipy >=0.7,<0.8',
                'whitenoise >=3.3,<3.4',
            )

    @subscribe('medikit.feature.make.on_generate', priority=SUPPORT_PRIORITY)
    def on_make_generate(self, event):
        makefile = event.makefile
        makefile['DJANGO'] = '$(PYTHON) bin/manage.py'
        makefile.add_target('runserver', '''$(DJANGO) runserver''', deps=('install-dev', ), phony=True)

    @subscribe('medikit.on_start')
    def on_start(self, event):

        context = {
            **event.setup,
            'config_package': 'config',
            'django_version': '1.11',
            'secret_key': generate_secret_key(),
            'use_jinja2': event.config['django'].use_jinja2,
            'use_whitenoise': event.config['django'].use_whitenoise,
        }

        name = context['name']

        # Create configuration
        config_path = 'config'
        if not os.path.exists(config_path):
            os.makedirs(config_path)

        self.render_file('manage.py', 'django/manage.py.j2', context, force_python=True, override=True)
        self.render_file(
            os.path.join(config_path, 'settings.py'),
            'django/settings.py.j2',
            context,
            force_python=True,
            override=True
        )
        self.render_file(
            os.path.join(config_path, 'urls.py'), 'django/urls.py.j2', context, force_python=True, override=True
        )
        self.render_file(
            os.path.join(config_path, 'wsgi.py'), 'django/wsgi.py.j2', context, force_python=True, override=True
        )

        if context['use_jinja2']:
            templates_dir = os.path.join(name, 'jinja2', context['name'])
            if not os.path.exists(templates_dir):
                os.makedirs(templates_dir)

        static_dir = os.path.join(name, 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        self.render_empty_files(os.path.join(static_dir, 'favicon.ico'))


__feature__ = DjangoFeature

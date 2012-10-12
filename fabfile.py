import ConfigParser
import os

from fabric.api import task, local

PROJECT_ROOT = os.path.dirname(__file__)
CONF_ROOT = os.path.join(PROJECT_ROOT, 'conf')
DEFAULTS = {
    'theme': os.path.join(CONF_ROOT, 'themes/caktus'),
    'relative': 'True',
    'copy-theme': 'True',
}
CONFIG_OPTIONS = {
    'theme': 'get',
    'source': 'get',
    'relative': 'getboolean',
    'copy-theme': 'getboolean',
}


@task
def get_config(name):
    config_file = os.path.join(CONF_ROOT, u'slides.cfg')
    config = ConfigParser.SafeConfigParser(defaults=DEFAULTS)
    config.read(config_file)
    options = {}
    if config.has_section(name):
        for option, type_ in CONFIG_OPTIONS.iteritems():
            func = getattr(config, type_)
            options[option] = func(name, option)
    options['destination'] = os.path.join(PROJECT_ROOT, 'html', name,
                                          'index.html')
    options['source'] = os.path.join(PROJECT_ROOT, 'slides', options['source'])
    return options


@task
def landslide(options):
    args = []
    if options.get('copy-theme', False):
        args.append('-c')
    if options.get('relative', False):
        args.append('-r')
    args.append('-t {}'.format(options['theme']))
    args.append(options['source'])
    local('landslide {}'.format(' '.join(args)))


@task
def build(name):
    options = get_config(name)
    landslide(options)

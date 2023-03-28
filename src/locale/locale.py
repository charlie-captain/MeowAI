import gettext
import os

language = 'en'


def init_locale():
    # set locale translate
    global language
    language = os.environ.get('lang', language)
    root_path = os.path.abspath(os.getcwd())
    local_dir = os.path.join(root_path, 'locale')
    domain = 'locale'
    gettext.bindtextdomain(domain, local_dir)
    gettext.textdomain(domain)
    # gettext.install(domain, localedir=local_dir)
    if language == 'zh':
        t = gettext.translation(domain, local_dir, languages=[language])
        t.install(None)
        return t.gettext
    else:
        return gettext.gettext


lc = init_locale()

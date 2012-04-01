# encoding: utf-8

import pystache

class Translation(pystache.View):
    template_path = 'examples'

    def __init__(self):
        super(Translation, self).__init__()

        # In your django.po file
        # msgid "Internationalization!"
        # msgstr "Internacionalização!"

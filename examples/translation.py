# encoding: utf-8

import pystache

class Translation(pystache.View):
    template_path = 'examples'

    def __init__(self):
        super(Translation, self).__init__()
        self.name = 'Matt'
        self.translation_table["{{name}} is using mustache.js!"] = u"{{name}} está a usar mustache.js!"

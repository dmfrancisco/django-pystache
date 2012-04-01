========
Pystache
========

Inspired by ctemplate_ and et_, Mustache_ is a
framework-agnostic way to render logic-free views.

As ctemplates says, "It emphasizes separating logic from presentation:
it is impossible to embed application logic in this template language."

Pystache is a Python implementation of Mustache. Pystache requires
Python 2.6.

Documentation
=============

The different Mustache tags are documented at `mustache(5)`_.

Install It
==========

::

    git clone http://github.com/dmfrancisco/django-pystache
    cd django-pystache
    python setup.py build
    python setup.py install


Use It
======

::

    >>> import pystache
    >>> pystache.render('Hi {{person}}!', {'person': 'Mom'})
    'Hi Mom!'

You can also create dedicated view classes to hold your view logic.

Here's your simple.py::

    import pystache
    class Simple(pystache.View):
        def thing(self):
            return "pizza"

Then your template, simple.mustache::

    Hi {{thing}}!

Pull it together::

    >>> Simple().render()
    'Hi pizza!'


Internationalization
====================

The mustache spec does not have a tag for i18n. Support was later added to mustache.js by Twitter using the {{_i}}{{/i}} tags (see https://github.com/twitter/mustache.js). This fork adds the same feature to pystache. Check the examples/translation.py file for more information.

If you use the "makemessages" django command, you may want to get the translation strings from your mustache templates. Copy the management directory in this repository to your apps' directory and issue the makemessages command as usual with the additional "-e .mustache" parameter. Example: ::

    python ../manage.py makemessages -l pt_PT -e .mustache


Example
=======

::

    # views/application.py
    from django.utils import simplejson as json
    from django.http import HttpResponse
    import pystache

    pystache.View.template_path = relative('..', 'templates') # Define where the templates are kept
    pystache.View.template_encoding = 'utf8' # Define encoding

    class View(pystache.View):
        ''' Main View class '''
        def __init__(self, *args):
            super(View, self).__init__()
            ... # Set common local variables, layout, ...

        @classmethod
        def template(cls, request, **args):
            ''' Return raw template '''
            template = pystache.Loader().load_template(cls.template_name, cls.template_path)
            return HttpResponse(template)

        @classmethod
        def template_pre_rendered(cls, request, **args):
            ''' Return raw template with pre-rendered translation sections '''
            template = pystache.Loader().load_template(cls.template_name, cls.template_path)
            template = pystache.Template(template).pre_render_i18n() # Pre-render translation sections
            return HttpResponse(template)

        @classmethod
        def json(cls, request, **args):
            ''' Return data to render template on the client-side '''
            view = cls(request, **args)
            return HttpResponse(json.dumps(vars(view)), 'application/json')

    # views/users.py
    class Edit(View):
        ''' Example View class '''
        template_path = os.path.join(pystache.View.template_path, 'users')

        def __init__(self, *args):
            super(Edit, self).__init__()
            ... # Set local variables

        @classmethod
        def view(cls, request, **args):
            ''' Return the rendered page '''
            view = cls(request, **args)
            ... # Do stuff
            return HttpResponse(view.render())
    ...

    # urls.py
    urlpatterns = patterns('',
        ...
        url(r'^user/edit$',           users.Edit.view),
        url(r'^user/edit\.mustache$', users.Edit.template_pre_rendered),
        url(r'^user/edit\.json$',     users.Edit.json),
        ...
    )


Test It
=======

nose_ works great! ::

    pip install nose
    cd pystache
    nosetests


Author
======

::

    context = { 'author': 'Chris Wanstrath', 'email': 'chris@ozmm.org' }
    pystache.render("{{author}} :: {{email}}", context)


Credits
=======

Original "makemessages" command reimplementation by altunyurt_ (djtemps_ project)

Inspiration from jhurt_ (pystache_ fork)


.. _ctemplate: http://code.google.com/p/google-ctemplate/
.. _et: http://www.ivan.fomichev.name/2008/05/erlang-template-engine-prototype.html
.. _Mustache: http://defunkt.github.com/mustache/
.. _mustache(5): http://mustache.github.com/mustache.5.html
.. _nose: http://somethingaboutorange.com/mrl/projects/nose/0.11.1/testing.html
.. _altunyurt: https://github.com/altunyurt
.. _djtemps: https://github.com/altunyurt/djtemps
.. _jhurt: https://github.com/jhurt
.. _pystache: https://github.com/jhurt/pystache

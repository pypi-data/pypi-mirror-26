==================
django-fa disclaimer
==================

This package is basically a `django-fontawesome <https://github.com/atiberghien/django-fontawesome>`_ fork with support of latest django, uploaded to PyPi.
Reason of creating this repo was sadly ignored `merge request <https://github.com/redouane/django-fontawesome/pull/32>`_.
All the credits goes to authors of source repository and merge request.

Requirements
============

- PyYAML
- Select2 (included)
- JQuery (uses django's jquery in admin panel)


Settings
========
By default, django-fontawesome ships with and uses the lastest fontawesome release.
You can configure django-fontawesome to use another release/source/cdn by specifying::

    # default uses locally shipped version at 'fontawesome/css/font-awesome.min.css'
    FONTAWESOME_CSS_URL = '//cdn.example.com/fontawesome-min.css'  # absolute url
    FONTAWESOME_CSS_URL = 'myapp/css/fontawesome.min.css'  # relative url

You can also tell it the fontawesome prefix, which as of right now is 'fa', using::

    FONTAWESOME_PREFIX = 'bg'  # default is 'fa'


Installation / Usage
====================

0. Install via pip::

    pip install django-fa


1. Add 'fontawesome' to your installed apps setting like this::

    INSTALLED_APPS = (
        ...
        'fontawesome',
    )

2. Import and use the ``IconField``::
    
    from fontawesome.fields import IconField


    class Category(models.Model):
        ...
        icon = IconField()


Here's what the widget looks like in the admin panel:

|admin-widget|

3. You can then render the icon in your template like this::
    
    {% for category in categories.all %}
        {% if category.icon %}
            {{ category.icon.as_html }}
        {% endif %}
    {% endfor %}


4. django-fontawesome ships with two template tags, ``fontawesome_stylesheet`` and ``fontawesome_icon``.
    - the former inserts a stylesheet link with a pre-configured href according to the ``FONTAWESOME_CSS_URL`` setting
    - the latter renders icons, and accepts the following optional keywords arguments: large, spin, fixed, li, border: (true/false), rotate: (90/180/270), title: (string)
    - you can also colorize an icon using the ``color='red'`` keyword argument to the ``fontawesome_icon`` template tag

    - example usage::

         {% load fontawesome %}
      
         <head>
           {% fontawesome_stylesheet %} 
           ...
         </head>
       
         {% fontawesome_icon 'user' color='red' %}

         {% fontawesome_icon 'star' large=True spin=True %}
      
         <ul class="fa-ul">
            <li> {% fontawesome_icon 'home' rotate=90 li=True %} One</li>
         </ul>



.. |admin-widget| image:: docs/images/admin-widget.png

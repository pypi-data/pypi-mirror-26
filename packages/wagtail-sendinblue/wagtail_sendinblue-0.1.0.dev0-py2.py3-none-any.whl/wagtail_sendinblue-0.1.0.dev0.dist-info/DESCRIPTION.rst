Wagtail SendInBlue
------------------

`Wagtail <https://wagtail.io/>`_ integration for `SendInblue`_.

Installation
************

Install it with pip:

.. code-block:: shell

    pip install wagtail-sendinblue



Add `sendinblue` to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'sendinblue',
        # ...
    ]



Add the `sendinblue.urls` to your `urls.py`:

.. code-block:: python

    from sendinblue import urls as sendinblue_urls

    urlpatterns = [
        # ...
        url(r'', include(sendinblue_urls)),
        url(r'', include(wagtail_urls)),
    ]



Configuration
*************

Go to the Wagtail administration and in `Settings > SendInBlue`
enter your API Key.
You need a `SendInBlue`_ account and
you can retrieve it your `SendInBlue administration <https://account.sendinblue.com/advanced/api?ae=312>`_.

Automation support
******************

There is an optionnal support for Automation.

You need to add the following at the end of your base Django template:

.. code-block:: html+jinja

      {% sendinblue %}
    </body>
    </html>



or if using `django-jinja <http://niwinz.github.io/django-jinja/latest/>`_:

.. code-block:: html+jinja

      {{ sendinblue() }}
    </body>
    </html>




.. _SendInBlue: https://www.sendinblue.com/?ae=312




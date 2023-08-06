captcha-manager
===============

captchamanager abstracts captcha token retrieval.

Motivation
----------

Some programs may require the retrieval of valid captcha tokens. Often,
this is accomplished through services like `2Captcha`_ that return a
valid token given an API key and the challenge site key. captchamanager
abstracts this functionality so programs can receive a single token or
can load a queue of tokens. Tokens are represented by their value,
generation time, and expiration time.

Note
----

Currently, captchamanager only supports 2Captcha.

Installation
------------

captchamanager is available via pip

::

    $ pip install captcha-manager

Usage
-----

.. code:: python

    from captchamanager import CaptchaManager

    TWO_CAPTCHA_API_KEY = 'ABC123'
    SITE_KEY = 'DEF456'
    PAGE_URL = 'https://example.com'
    captcha_manager = CaptchaManager(TWO_CAPTCHA_API_KEY, SITE_KEY, PAGE_URL)
    token = captcha_manager.get_captcha_token() # Returns a single token ASAP

    captcha_manager.start_captcha_queue()
    # Do something
    token = captcha_manager.wait_for_captcha_token() # Returns one valid token from queue

.. _2Captcha: https://2captcha.com/enterpage
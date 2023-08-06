bypass
======

GPG-based password management on the command line.

Installation
------------

Minimal::

  pip install bypass

With TOTP support enabled::

  pip install bypass[totp]

External Dependencies
---------------------

**Base**

* click_
* pbr_
* python-gnupg_
* ruamel.yaml_

**TOTP**

* pyotp_
* python-qrcode_

**Windows-specific**

* pywin32_

.. Dependency link definitions
.. _click:         http://click.pocoo.org/5
.. _pbr:           https://docs.openstack.org/pbr/latest
.. _python-gnupg:  https://pythonhosted.org/python-gnupg
.. _ruamel.yaml:   https://yaml.readthedocs.io/en/latest
.. _pyotp:         https://pyotp.readthedocs.io/en/latest
.. _python-qrcode: https://github.com/lincolnloop/python-qrcode#pure-python-qr-code-generator
.. _pywin32:       https://sourceforge.net/projects/pywin32

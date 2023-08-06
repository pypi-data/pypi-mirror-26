
.. image:: https://api.travis-ci.org/petrus-v/keyring-otp.svg?branch=master
    :target: https://travis-ci.org/petrus-v/keyring-otp
    :alt: Travis state


===========
Keyring OTP
===========

Keyring OTP is a CLI to generate One Time Password from secrets stored in
`Gnome Keyring <https://wiki.gnome.org/action/show/Projects/GnomeKeyring>`_
(the `seahorse's <https://wiki.gnome.org/Apps/Seahorse>`_ backend).


.. contents:: **Table of Contents**

------------
Installation
------------

This application is properly running on debian stretch in python3 virtual
environement::

    $ python3 -m venv koptvenv
    $ source ./kotpvenv/bin/activate

This requiere ``xclip`` on your computer to temporary put the secret in
your clipboard at the end of the program the initial value is back in your
clipboard::

    $ apt install xclip

.. note::

    If you are using ``-o`` option (console output) the app won't complaints
    if xclip is not there.

Install using your favorite installer. For example::

    $ pip install keyring-otp

-----
Usage
-----

use ``-h`` to get recent help::

    $ kotp -h
    usage: kotp [-h] [-s SECRET] [-o] [-d DURATION] keyring key

    CLI to generate One Time Password from secrets stored in Keyring (using
    seahorse password manager)

    positional arguments:
      keyring
      key

    optional arguments:
      -h, --help            show this help message and exit
      -s SECRET, --secret SECRET
                            Force using secret from command line instead getting
                            it from the password manager. (as keyring and key are
                            mandatory set any values they will be ignored).
      -o, --output          Display output in console and in the clipboard (useful
                            if you can't install xclip).
      -d DURATION, --duration DURATION
                            How many seconds you wants the One Time Password in
                            your clipboard. Note that as time is changing, the
                            TOTP password will be updated and your clipboard will
                            be updated too!

Let's assume I've a keyring called ``otp`` which contains a key called github
wich contains my github otp password.

.. figure:: seahorse.png
    :alt: Seahorse Gnome password manager

To get the Time based OTP password in my clipboad I do::

    $ kotp otp github

.. note::

    At the time writting the ``otp`` keyring must be unlock before running
    the application.

Here an other example by giving the OTP password value in command line::

    $ kotp -s SECRETS -o -d 35 nothing real
    Current TOTP 887562 at Wed Nov  8 07:48:18 2017
    Current TOTP 291833 at Wed Nov  8 07:48:30 2017


.. warning::

    This option is discouraged as long your OTP secret will be in your bash
    history, we may remove this option to replace it with a prompt in the
    future


-------
Roadmap
-------

* make it usable as an API, API consumer may add multiple callback they should
  be called once OTP as benn changed (callback may be declared in entry point
  to let user define new callback easly), this apps should declare some
  default behaviours likes:

  - print in console
  - filling clipboard (require an init method and final method to set back
    current clipboad value)

* Prompt to unlock keyring
* Thinking replace ``-s`` option and open secret input to avoid le trace
  in use bash history
* use python keyring to make this app portable with more password manager:
  GnomeKeyring (for Gnome environments) or KDEWallet (for KDE environments)
  or Win32CryptoRegistry (for Windows)
* manage passman backends
* save new secrets

------
Author
------

* Pierre Verkest <pverkest@anybox.fr>

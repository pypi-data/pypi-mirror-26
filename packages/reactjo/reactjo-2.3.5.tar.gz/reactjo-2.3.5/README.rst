Contents
========

For the most up-to-date docs, please see `reactjo.com`_

Most of the code is in the extensions’ repos, which you can find here -
`Frontend Extension`_ - `Backend Extension`_ - `Extension Template`_

You are looking at the repo of the command line tool which sets up the
rc directory, downloads extensions, and passes commands to them.

ReactJo
=======

A command line scaffolding tool for web applications.

Within minutes, it gives you a microservice architecture with: - Node.js
frontend app - React (via Next.js) - Sass, material-ui, and bootstrap -
List/details page for users and models - Create, Update, and Delete
options for users and models (assuming permissions pass) ———— - Django
backend app - Optional user authentication - Model scaffolding - RESTful
API - Customizable permissions

Extensible
~~~~~~~~~~

-  Install an extension or change any of the default ones.
-  New extensions can be generated with a single command
   ``reactjo extend``
-  Deploying an extension is as easy as pushing it to a github repo.

Zero-weight
~~~~~~~~~~~

You don’t need reactjo in production, it can be uninstalled after it’s
done building. Or just .gitignore the reactjorc directory which holds
all the extensions and their bulk.

Interactive, intelligent
~~~~~~~~~~~~~~~~~~~~~~~~

This is not a boilerplate repo, that just gives you a starting point and
leaves you hanging.

Reactjo takes you through a series of questions to determine what you
need, and even gives you the available options so you don’t need to need
to endlessly ask docs “what was that mandatory field I need to pass in…”

After you generate the project, Reactjo can continue to be used to
scaffold more pieces of the project in the future.

Requirements:
=============

-  `Python 3.6 or newer`_
-  `Pip3`_
-  `Node and NPM`_
-  `Git`_
-  `PostgreSQL`_ - Only if you want the app heroku-ready.

Installation:
=============

Open up your command line

.. code:: bash

    > mkdir my_project            # Create a directory.
    > cd my_project               # Enter directory.
    > python3 -m venv env         # Or python -m venv env (windows).
    > source env/bin/activate     # Or just env/Scripts/activate (windows).
    > pip install reactjo         # Finally, we install Reactjo.

5 minute Django + React project.
================================

\```bash > reactjo rc # Creates reactjorc/, downloads default
extensions. Name your project > my_project

    reactjo new # It asks some questions and starts building.

Optionally, scaffold a model
============================

    reactjo content # Asks a lot of questions and st

.. _reactjo.com: https://www.reactjo.com/
.. _Frontend Extension: https://github.com/aaron-price/reactjo-nextjs
.. _Backend Extension: https://github.com/aaron-price/reactjo-django
.. _Extension Template: https://github.com/aaron-price/reactjo-extension-template
.. _Python 3.6 or newer: https://www.python.org/downloads/
.. _Pip3: https://pip.pypa.io/en/stable/installing/
.. _Node and NPM: https://nodejs.org/en/download/
.. _Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. _PostgreSQL: https://www.postgresql.org/download/

.. |Build Status| image:: https://travis-ci.org/aaron-price/reactjo.svg?branch=master
   :target: https://travis-ci.org/aaron-price/reactjo
============
Contributing
============

Contributions of all types are welcome!

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

If you think something's not working correctly, report it here: 
https://github.com/tylerdave/bloomsky-api/issues.

If you are reporting a bug, please include:

* Detailed steps to reproduce the bug.
* Any details about your local setup that might be helpful in troubleshooting.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whomever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whomever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

BloomSky API could always use more documentation, whether
as part of the BloomSky API docs, in docstrings, or even on the web in blog
posts, articles, and such.

New Features & Feedback
~~~~~~~~~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/tylerdave/bloomsky-api/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `BloomSky-API` for local development.

1. Fork the `bloomsky-api` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/bloomsky-api.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv bloomsky-api
    $ cd bloomsky-api/
    $ pip install -e .[develop]

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ flake8 bloomsky_api tests
    $ python setup.py test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.7, 3.3, 3.4, 3.5 and for PyPy. Check
   https://travis-ci.org/tylerdave/bloomsky-api/pull_requests
   and make sure that the tests pass for all supported Python versions.


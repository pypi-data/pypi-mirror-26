============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given. 

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/math-a3k/django-ai/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

django-ai could always use more documentation, whether as part of the 
official django-ai docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at 
https://github.com/math-a3k/django-ai/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)


Artwork
~~~~~~~

Artwork - logos, banners, themes, etc. - is highly appreciated and always welcomed. If you don't feel confortable with GitHub, use the mailing list for submitting: django-ai@googlegroups.com


Monetary
~~~~~~~~

You can support and ensure the `django-ai` development by making money arrive to the project in its different ways:

Donations
  Software development has costs, any help for lessen them is highly appreciated and encourages to keep going.

Sponsoring
  Hire the devs for working in a specific feature you would like to have or a bug to squash in a timely manner.

Hiring, Contracting and Consultancy
  Hire the developers to work (implementing code, models, etc.) for you. Even if it is not `django-ai` related, as long as the devs have enough for a living, the project will keep evolving. 

Contact the lead developer at matematica.a3k@gmail.com for details.


Get Started!
------------

Ready to contribute code or documentation? Here's how to set up `django-ai` 
for local development.

1. Fork the `django-ai` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/django-ai.git

3. Install your local copy into a virtualenv. This is how you set up your fork for local development::

    $ python3 -m venv django-ai-env
    $ source django-ai-env/bin/activate
    $ cd django-ai/
    $ pip install -r requirements_dev.txt

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

        $ flake8 django_ai tests
        $ PYTHONHASHSEED=0 python runtests.py
        $ tox

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website to the ``development`` branch. Once your changes are reviewed, you may be assigned to review another pull request with improvements on your code if deemed neccesary. Once we agree on a final result, it will be merged to ``master``.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3. Check 
   https://travis-ci.org/math-a3k/django-ai/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

    $ PYTHONHASHSEED=0 python -m unittest tests.test_django_ai

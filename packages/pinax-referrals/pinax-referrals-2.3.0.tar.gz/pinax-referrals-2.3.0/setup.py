from setuptools import find_packages, setup

LONG_DESCRIPTION = """
.. image:: http://pinaxproject.com/pinax-design/patches/pinax-referrals.svg
    :target: https://pypi.python.org/pypi/pinax-referrals/

===============
Pinax Referrals
===============

.. image:: https://img.shields.io/pypi/v/pinax-referrals.svg
    :target: https://pypi.python.org/pypi/pinax-referrals/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://pypi.python.org/pypi/pinax-referrals/

.. image:: https://img.shields.io/circleci/project/github/pinax/pinax-referrals.svg
    :target: https://circleci.com/gh/pinax/pinax-referrals
.. image:: https://img.shields.io/codecov/c/github/pinax/pinax-referrals.svg
    :target: https://codecov.io/gh/pinax/pinax-referrals
.. image:: https://img.shields.io/github/contributors/pinax/pinax-referrals.svg
    :target: https://github.com/pinax/pinax-referrals/graphs/contributors
.. image:: https://img.shields.io/github/issues-pr/pinax/pinax-referrals.svg
    :target: https://github.com/pinax/pinax-referrals/pulls
.. image:: https://img.shields.io/github/issues-pr-closed/pinax/pinax-referrals.svg
    :target: https://github.com/pinax/pinax-referrals/pulls?q=is%3Apr+is%3Aclosed

.. image:: http://slack.pinaxproject.com/badge.svg
    :target: http://slack.pinaxproject.com/
    

``pinax-referrals`` provides a site with the ability for users to
publish referral links to specific pages or objects and then record
any responses to those links for subsequent use by the site.

For example, on an object detail page, the site builder would use a
template tag from ``pinax-referrals`` to display a referral link that the user of the
site can send out in a Tweet. Upon clicking that link, a response to that
referral code will be recorded as well as any other activity that the site
builder wants to track for that session.

It is also possible for anonymous referral links/codes to be generated
which is useful in marketing promotions and the like.


Supported Django and Python Versions
------------------------------------

* Django 1.8, 1.10, 1.11, and 2.0
* Python 2.7, 3.4, 3.5, and 3.6
"""

setup(
    author="Pinax Team",
    author_email="developers@pinaxproject.com",
    description="a referrals app for Django",
    name="pinax-referrals",
    long_description=LONG_DESCRIPTION,
    version="2.3.0",
    url="http://github.com/pinax/pinax-referrals/",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "django-appconf>=1.0.1",
        "django>=1.8",
    ],
    package_data={
        "pinax.referrals": [
            "templates/pinax/referrals/*",
        ]
    },
    test_suite="runtests.runtests",
    tests_require=[
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)

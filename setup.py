from setuptools import setup, find_packages
import os

version = open('ftw/workspace/version.txt').read().strip()

tests_require = [
    'zope.testing',
    'collective.testcaselayer',
]


setup(name='ftw.workspace',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Victor Baumann',
      author_email='v.baumann4teamwork.ch',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'ftw.calendarwidget',
          'ftw.tabbedview',
          'plone.principalsource',
          # -*- Extra requirements: -*-
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='ftw.workspace.tests.test_docs.test_suite',
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

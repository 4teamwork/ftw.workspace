from setuptools import setup, find_packages
import os

version = '2.0.1'

tests_require = [
    'plone.app.testing',
    'ftw.file',
    'ftw.testing',
    'ftw.pdfgenerator',
    'ftw.builder',
    'pyquery',
    ]

setup(name='ftw.workspace',
      version=version,
      description='A project folder for plone.',
      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw workspace project folder plone',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.workspace',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'collective.js.jqsmartTruncation',
        'ftw.calendar',
        'ftw.colorbox',
        'ftw.tabbedview',
        'ftw.upgrade',
        'plone.namedfile',
        'plone.principalsource',
        'setuptools',
        # -*- Extra requirements: -*-
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require,
                          pdf=['ftw.pdfgenerator',
                               'ftw.file', ]),

      test_suite='ftw.workspace.tests.test_docs.test_suite',
      entry_points='''
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      ''',
      )

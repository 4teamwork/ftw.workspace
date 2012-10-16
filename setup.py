from setuptools import setup, find_packages
import os

version = '1.6.1'

tests_require = [
    'plone.app.testing',
    'ftw.testing',
    'ftw.pdfgenerator',
    ]

setup(name='ftw.workspace',
      version=version,
      description='A project folder for plone.',
      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.0',
        'Framework :: Plone :: 4.1',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        ],

      keywords='ftw workspace project folder plone',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.workspace/',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        'ftw.tabbedview',
        'ftw.calendar',
        'plone.principalsource',
        'ftw.upgrade',
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

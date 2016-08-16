from setuptools import setup, find_packages
import os

version = '4.1.1'

tests_require = [
    'egov.contactdirectory',
    'ftw.builder',
    'ftw.pdfgenerator',
    'ftw.testbrowser',
    'ftw.testing',
    'plone.app.testing',
    'pyquery',
    'xlrd',
]

contact_require = [
    'egov.contactdirectory'
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
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.workspace',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'collective.deletepermission',
        'ftw.activity',
        'ftw.calendar',
        'ftw.colorbox',
        'ftw.file',
        'ftw.lawgiver',
        'ftw.meeting [pdf, zipexport, calendar]',
        'ftw.notification.base',
        'ftw.notification.email',
        'ftw.participation',
        'ftw.pdfgenerator',
        'ftw.tabbedview[extjs, quickupload]',
        'ftw.upgrade',
        'ftw.zipexport',
        'plone.formwidget.contenttree',
        'plone.namedfile',
        'plone.principalsource',
        'Products.CMFPlacefulWorkflow',
        'setuptools',
        'XlsxWriter',
        'z3c.relationfield',
        # -*- Extra requirements: -*-
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require,
                          zip_export=[],  # For backwards compatibility
                          contact=contact_require),

      test_suite='ftw.workspace.tests.test_docs.test_suite',
      entry_points='''
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      ''',
      )

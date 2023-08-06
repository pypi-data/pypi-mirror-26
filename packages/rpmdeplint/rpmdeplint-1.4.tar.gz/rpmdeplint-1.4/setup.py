from glob import glob
from setuptools import setup
from distutils.command.build import build as _build


# Customization of standard build step: Automatically build the docs as well in
# one build step: python setup.py build
class build(_build):
    sub_commands = _build.sub_commands + [('build_sphinx', lambda self: True)]


# Note that we have some scripts which programmatically change the version
# declared here. Do not adjust the formatting.
name = 'rpmdeplint'
version = '1.4'
release = version

setup(name='rpmdeplint',
      version=version,
      description='Tool to find errors in RPM packages in the context of their dependency graph',
      long_description=open('README.rst').read(),
      url='https://pagure.io/rpmdeplint',
      author='Red Hat, Inc.',
      author_email='qa-devel@lists.fedoraproject.org',
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
      ],
      packages=['rpmdeplint', 'rpmdeplint.tests'],
      install_requires=['six'],
      tests_require=['pytest'],
      data_files = [
          ('/usr/share/man/man1', glob('build/sphinx/man/*.1')),
      ],
      cmdclass = {
          'build': build,
      },
      command_options={
          'build_sphinx': {
              'builder': ('setup.py', 'man'),
              'project': ('setup.py', name),
              'version': ('setup.py', version),
              'release': ('setup.py', release),
          }
      },
      entry_points={
          'console_scripts': [
              'rpmdeplint = rpmdeplint.cli:main',
          ]
      },
)

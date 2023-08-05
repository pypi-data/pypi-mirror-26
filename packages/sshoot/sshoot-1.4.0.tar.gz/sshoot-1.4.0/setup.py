from setuptools import setup, find_packages

from sshoot import (
    __version__,
    __doc__ as description)

tests_require = ['fixtures']


config = {
    'name': 'sshoot',
    'version': __version__,
    'license': 'GPLv3+',
    'description': description,
    'long_description': open('README.rst').read(),
    'long_description_content_type': 'text/markdown',
    'author': 'Alberto Donato',
    'author_email': 'alberto.donato@gmail.com',
    'maintainer': 'Alberto Donato',
    'maintainer_email': 'alberto.donato@gmail.com',
    'url': 'https://github.com/albertodonato/sshoot',
    'download_url': 'https://github.com/albertodonato/sshoot/releases',
    'packages': find_packages(),
    'include_package_data': True,
    'entry_points': {'console_scripts': ['sshoot = sshoot.main:sshoot']},
    'test_suite': 'sshoot',
    'setup_requires': ['Babel'],
    'install_requires': ['PyYAML', 'prettytable', 'argcomplete', 'pyxdg'],
    'tests_require': tests_require,
    'extras_require': {'testing': tests_require},
    'keywords': 'ssh sshuttle vpn',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Networking',
        'Topic :: Utilities']}

setup(**config)

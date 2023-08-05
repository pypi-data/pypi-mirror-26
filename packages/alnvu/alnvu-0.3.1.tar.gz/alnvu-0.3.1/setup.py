import os
import subprocess
from setuptools import setup

subprocess.call(
    ('mkdir -p {pkg}/data && '
     'git describe --tags --dirty > {pkg}/data/ver.tmp '
     '&& mv {pkg}/data/ver.tmp {pkg}/data/ver '
     '|| rm -f {pkg}/data/ver.tmp').format(pkg='alnvu'),
    shell=True, stderr=open(os.devnull, "w"))

# import must follow 'git describe' command above to update version
from alnvu import __version__

params = {
    'author': 'Noah Hoffman',
    'author_email': 'noah.hoffman@gmail.com',
    'description': ('Reformat and condense multiple sequence alignments '
                    'to highlight variability'),
    'name': 'alnvu',
    'package_dir': {'alnvu': 'alnvu'},
    'packages': ['alnvu'],
    'package_data': {'alnvu': ['data/*']},
    'url': 'http://github.com/nhoffman/alnvu',
    'version': __version__,
    'requires': ['python (>= 2.7)'],
    'install_requires': [
        'Jinja2>=2.7',
        'reportlab>=3.0',
        'fastalite>=0.3',
    ],
    'entry_points': {
        'console_scripts': ['av = alnvu.av:main']
    },
    'test_suite': 'tests',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
}

setup(**params)

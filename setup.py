import os

from subprocess import check_call
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

base_dir = os.path.dirname(__file__)


class BuildCommand(build_py):

    def run(self):
        cmd_dir = os.path.join(base_dir, 'rp_sunrise_alarm', 'frontend')
        check_call(['npm', 'install'], cwd=cmd_dir)
        check_call(['npm', 'run', 'build'], cwd=cmd_dir)
        super().run()

setup(
    name='rp-sunrise-alarm',
    version='1.0',
    description='Raspberry Pi Sunrise Alarm',
    long_description=open(os.path.join(base_dir, 'README.rst')).read(),
    url='https://github.com/sebasgo/rp-sunrise-alarm',
    author='Sebastian Gottfried',
    author_email='sebastian.gottfried@posteo.de',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'attrs',
        'Flask',
        'Flask-SQLAlchemy',
        'pygame',
        'redis',
        'requests',
    ],
    extras_require={
        'dev': [
            'check-manifest',
            'pygame',
        ],
    },

    entry_points={
        'console_scripts': [
            'rp-sunrise-alarm-daemon=rp_sunrise_alarm.daemon:main',
        ],
    },
    cmdclass={
        'build_py': BuildCommand
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask,'
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)

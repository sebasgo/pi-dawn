import os

from subprocess import check_call
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


class BuildCommand(build_py):

    def run(self):
        base_dir = os.path.dirname(__file__)
        cmd_dir = os.path.join(base_dir, 'rp_sunrise_alarm', 'frontend')
        check_call(['npm', 'install'], cwd=cmd_dir)
        check_call(['npm', 'run', 'build'], cwd=cmd_dir)
        super().run()

setup(
    name='rp-sunrise-alarm',
    version='1.0',
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
            'rp-sunrise-alarm-daemom=rp_sunrise_alarm.daemon:main',
        ],
    },
    cmdclass={
        'build_py': BuildCommand
    }
)

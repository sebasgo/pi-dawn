import os

from subprocess import check_call
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

base_dir = os.path.dirname(__file__)


class BuildCommand(build_py):

    def run(self):
        cmd_dir = os.path.join(base_dir, 'pi_dawn', 'frontend')
        check_call(['npm', 'install'], cwd=cmd_dir)
        check_call(['npm', 'run', 'build'], cwd=cmd_dir)
        super().run()


def long_description():
    return '{}\n{}'.format(
        open(os.path.join(base_dir, 'README.rst')).read(),
        open(os.path.join(base_dir, 'CHANGES.rst')).read()
    )


setup(
    name='pi-dawn',
    version='1.0',
    description='Pi Dawn',
    long_description=long_description(),
    url='https://github.com/sebasgo/pi-dawn',
    author='Sebastian Gottfried',
    author_email='sebastian.gottfried@posteo.de',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'adafruit-ws2801',
        'attrs',
        'click',
        'Flask',
        'Flask-SQLAlchemy',
        'python-vlc',
        'redis',
    ],
    extras_require={
        'dev': [
            'check-manifest',
            'pygame',
        ],
    },

    entry_points={
        'console_scripts': [
            'pi-dawn-daemon=pi_dawn.daemon:main',
            'pi-dawn-gamma-test=pi_dawn.gamma_test:main',
        ],
    },
    cmdclass={
        'build_py': BuildCommand
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)

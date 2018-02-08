from setuptools import setup, find_packages

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
)

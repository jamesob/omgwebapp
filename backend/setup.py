from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='changeme',
    version='0.0.1',
    description='changeme',
    author='changeme',
    author_email='changeme',
    include_package_data=True,
    zip_safe=False,
    packages=['changeme'],
    install_requires=open('requirements.txt', 'r').readlines(),
    entry_points={
        'console_scripts': [
            'changeme-web = changeme.web:main',
            'changeme-worker = changeme.worker:main',
        ],
    },
)

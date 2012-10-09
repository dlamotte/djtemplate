#!/usr/bin/env python

from setuptools import setup, find_packages

install_requires = [
    'BeautifulSoup==3.2.1',
    'Django>1.4,<1.5',
    'Fabric==1.4.2',
    'PIL==1.1.7',
    'South==0.7.6',
    'dj-database-url==0.2.1',
    'django-debug-toolbar==0.9.4',
    'django-jsonfield==0.8.11',
    'django-model-utils==1.1.0',
    'django-tastypie==0.9.11',
    'django-compressor==1.2',
    'lxml==2.3.4',
    'gunicorn==0.14.6',
    'psycopg2==2.4.5',
    'python-memcached==1.48',
    'pytz==2012d',
    'raven==2.0.6',
    'setproctitle==1.1.6',
]

setup(
    name='{{ project_name }}',
    version='0.1',
    author='',
    author_email='',
    url='',
    description='',
    long_description=open('README.md').read(),
    packages=find_packages('.'),
    zip_safe=False,
    install_requires=install_requires,
    #tests_require=[],
    license='',
    include_package_data=True,
    #entry_points={
    #    'console_scripts': [
    #        'name = {{ package_name }}.cmd:main'
    #    ],
    #},
    classifiers=[],
)

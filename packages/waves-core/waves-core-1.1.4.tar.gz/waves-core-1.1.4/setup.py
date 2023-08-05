import os
from setuptools import find_packages, setup


def import_version():
    from waves.wcore import __version__
    return __version__


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='waves-core',
    version=import_version(),
    packages=find_packages(),
    provides=['waves'],
    include_package_data=True,
    license='GPLv3',
    description='WAVES - core package',
    url='http://waves.atgc-montpellier.fr',
    author='Marc Chakiachvili',
    author_email='marc.chakiachvili@lirmm.fr, marc@archi-logic.fr',
    install_requires=[
        'daemons==1.3.0',
        'Django==1.11.6',
        'django-admin-sortable2==0.6.16',
        'django-crispy-forms==1.7.0',
        'django-polymorphic==1.3',
        'djangorestframework==3.7.1',
        'inflection==0.3.1',
        'psutil==5.4.0',
        'pycrypto==2.6.1',
        'python-magic==0.4.13',
        'saga-python==0.46',
        'setproctitle==1.1.10',
        'swapper==1.1.0',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: System :: Distributed Computing',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Operating System :: Unix'
    ],
)

from pkg_resources import parse_version
from setuptools import setup, find_packages, __version__ as setuptools_version

import versioneer


def has_environment_marker_platform_impl_support():
    """Code extracted from 'pytest/setup.py'
    https://github.com/pytest-dev/pytest/blob/7538680c/setup.py#L31

    The first known release to support environment marker with range operators
    it is 18.5, see:
    https://setuptools.readthedocs.io/en/latest/history.html#id235
    """
    return parse_version(setuptools_version) >= parse_version('18.5')


extras_require = {}

if has_environment_marker_platform_impl_support():
    extras_require[':platform_python_implementation == "PyPy"'] = [
        'PyPyDispatcher>=2.1.0',
    ]

setup(
    name='scrapy-block-inspector',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    url='https://github.com/grammy-jiang/scrapy-block-inspector',
    description='',
    long_description=open('README.rst').read(),
    author='Grammy Jiang',
    maintainer='Grammy Jiang',
    maintainer_email='grammy.jiang@gmail.com',
    license='BSD',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Framework :: Scrapy',
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'scrapy>=1.4.0'
    ],
    extras_require=extras_require,
)

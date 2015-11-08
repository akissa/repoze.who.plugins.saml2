import os
import sys

from imp import load_source
from setuptools import setup, find_packages


TEST_REQUIRES = [
    'webob',
    'repoze.who >= 1.0',
    'nose',
    'coverage',
    'mock'
]

if sys.version_info < (2, 7):
    TEST_REQUIRES.append('unittest2')


def get_readme():
    """Generate long description"""
    pandoc = None
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        pandoc = os.path.join(path, 'pandoc')
        if os.path.isfile(pandoc) and os.access(pandoc, os.X_OK):
            break
    try:
        if pandoc:
            cmd = [pandoc, '-t', 'rst', 'README.md']
            long_description = os.popen(' '.join(cmd)).read()
        else:
            raise ValueError
    except BaseException:
        long_description = open("README.md").read()
    return long_description


def main():
    """Main"""
    version = load_source("version", os.path.join("repoze", "__init__.py"))

    opts = dict(
        name="repoze.who.plugins.saml2",
        version=version.__version__,
        description="SAML2 plugin for repoze.who",
        long_description=get_readme(),
        keywords="web saml2 wsgi repoze.who authentication plugins repoze",
        author=version.__author__,
        author_email=version.__email__,
        url="https://github.com/akissa/repoze.who.plugins.saml2",
        license="MPL 2.0",
        packages=find_packages(exclude=['tests']),
        namespace_packages=[
            'webob',
            'repoze',
            'repoze.who',
            'repoze.who.plugins',
        ],
        include_package_data=True,
        zip_safe=False,
        tests_require=TEST_REQUIRES,
        test_suite='nose.collector',
        install_requires=[
            'repoze.who >= 1.0',
            'zope.interface'
        ],
        classifiers=[
            'Development Status :: 1 - Planning',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
            'Natural Language :: English',
            'Operating System :: OS Independent'],
        )
    setup(**opts)


if __name__ == "__main__":
    main()

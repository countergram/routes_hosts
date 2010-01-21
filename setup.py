from setuptools import setup

longdesc = """\
Adds support for multiple domains to Pylons/Routes, including url generation.

For now, read the comments for documentation.
"""

setup(
    name="routes_hosts",
    version="0.1.0",
    description="Adds support for multiple domains to Pylons/Routes, including url generation",
    long_description=longdesc,
    author="Jason Stitt",
    author_email="js@jasonstitt.com",
    url="http://countergram.com/open-source/",
    packages=['routes_hosts'],
    zip_safe=False,
    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Other Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Topic :: Utilities',
          ],
    )

import re

from setuptools import setup

with open('nexmo/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

setup(name='nexmo',
      version=version,
      description='Nexmo Client Library for Python',
      long_description='This is the Python client library for Nexmo\'s API. To use it you\'ll need a Nexmo account. Sign up `for free at nexmo.com <http://nexmo.com?src=python-client-library>`_.',
      url='http://github.com/Nexmo/nexmo-python',
      author='Tim Craft',
      author_email='mail@timcraft.com',
      license='MIT',
      packages=['nexmo'],
      platforms=['any'],
      install_requires=['requests', 'PyJWT[crypto]'],
      tests_require=['cryptography'],
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ])

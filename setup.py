from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='HeartNSole',
      version='1.0.0',
      author='Ricky',
      packages=['application'],
      install_requires=required
      )

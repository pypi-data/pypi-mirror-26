from setuptools import setup  # Always prefer setuptools over distutils
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

print(reqs)

packages = ['hiveplot']

setup(name='hiveplot',
      version='2017.10.17.21.07',
      author='Eric J. Ma',
      author_email='ericmajinglong@gmail.com',
      description=("Hive plots in Python!"),
      license="MIT",
      keywords="network visualization, matplotlib, hiveplot",
      url='https://github.com/ericmjl/hiveplot',
      packages=packages,
      maintainer='Eric J. Ma',
      maintainer_email='ericmajinglong@gmail.com',
      install_requires=reqs,
      long_description='A utility for making hive plots in matplotlib.',
      classifiers=["Topic :: Scientific/Engineering :: Visualization"]
      )

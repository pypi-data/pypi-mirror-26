from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='irmacl',
      version='1.1.9',
      description='Irma command line tool for API v1.1',
      long_description=readme(),
      url='https://github.com/quarkslab/irma-cli',
      author='irma-dev',
      author_email='irma-dev@quarkslab.com',
      license='ApacheV2',
      packages=['irmacl'],
      install_requires=[
          'requests',
          'marshmallow',
      ],
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)

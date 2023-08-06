from distutils.core import setup
setup(
  name = 'cfmr',
  packages = ['cfmr'], 
  version = '0.0.3',
  description = 'Python support library for CFMR',
  author = 'Donnie Flood',
  author_email = 'pypi@floodfx.com',
  url = 'https://github.com/floodfx/cfmr-python',
  download_url = 'https://github.com/floodfx/cfmr-python/archive/0.0.3.tar.gz',
  install_requires=['boto3'],
  keywords = ['map', 'reduce', 'cloud', 'function', 'aws', 'lambda', 'azure', 'google', 'cloud'], 
  classifiers = [],
)

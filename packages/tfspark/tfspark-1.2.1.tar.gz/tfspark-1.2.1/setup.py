from setuptools import setup

setup(
  name = 'tfspark',
  packages = ['tensorflowonspark'],
  version = '1.2.1',
  description = 'Deep learning with TensorFlow on Apache Spark clusters',
  author = 'Yahoo, Inc.',
  url = 'https://github.com/hopshadoop/TensorFlowOnSpark',
  keywords = ['tensorflowonspark', 'tensorflow', 'spark', 'machine learning', 'yahoo', 'hops'],
  license = 'Apache 2.0',
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7'
  ]
)

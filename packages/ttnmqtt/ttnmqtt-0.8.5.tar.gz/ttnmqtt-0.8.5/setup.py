from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='ttnmqtt',
      version='0.8.5',
      description='small package to make mqtt connection to ttn',
      long_description = readme(),
      author='Emmanuelle Lejeail',
      author_email='manu.lejeail@gmail.com',
      license='MIT',
      packages=['ttnmqtt'],
      install_requires=[
          'paho-mqtt',
          'pydispatch',
      ],
      zip_safe=False)

from setuptools import setup

setup(name='parsa',
      version='1.1.3',
      description='A multiformat text parser',
      url='http://github.com/rdimaio/parsa',
      author='Riccardo Di Maio',
      author_email='riccardodimaio11@gmail.com',
      license='MIT',
      packages=['parsa'],
      entry_points = {
            'console_scripts': [
                  'parsa = parsa.parsa:main'
            ]
      },
      zip_safe=False)
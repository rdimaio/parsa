from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='parsa',
      version='1.1.3',
      description='A multiformat text parser',
      long_description=long_description,
      long_description_content_type="text/markdown",
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
      zip_safe=False,
      classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Intended Audience :: Information Technology",
            "Intended Audience :: Science/Research",
            "Intended Audience :: System Administrators",
            "Intended Audience :: Other Audience",
            "Programming Language :: Python :: 2.7", 
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX",
            "Topic :: Text Processing",
            "Topic :: Utilities",
      ],
)
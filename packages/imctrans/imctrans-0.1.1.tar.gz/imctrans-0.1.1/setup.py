from setuptools import setup, find_packages

setup(name='imctrans',
      version='0.1.1',
      description='IMC Bindings Generator',
      url='http://github.com/oceanscan/imctrans',
      author='Ricardo Martins',
      author_email='rasm@oceanscan-mst.com',
      license='Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)',
      classifiers=[
          "Development Status :: 4 - Beta",
          "Topic :: Software Development :: Code Generators",
          "License :: OSI Approved :: Apache Software License"

      ],
      packages=find_packages('.'),
      package_data={
          'imctrans.cpp': ['assets/src/IMC/Base/*.hpp', 'assets/src/IMC/Base/*.cpp'],
      },
      entry_points={
          'console_scripts': [
              'imctrans=imctrans.cli:main',
          ],
      }
      )

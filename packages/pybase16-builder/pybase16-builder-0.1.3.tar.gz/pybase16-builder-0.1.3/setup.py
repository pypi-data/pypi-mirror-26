from setuptools import setup

setup(
      name='pybase16-builder',
      version='0.1.3',
      description='A base16 colorscheme builder for Python',
      long_description=open('README.rst').read(),
      url='https://github.com/InspectorMustache/pybase16-builder',
      packages=['pybase16_builder'],
      author='Pu Anlai',
      license='MIT',
      classifiers=[
                   'Development Status :: 3 - Alpha',
                   'Intended Audience :: End Users/Desktop',
                   'Topic :: Other/Nonlisted Topic',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3 :: Only'
                  ],
      keywords='base16',
      install_requires=['pystache', 'pyyaml'],
      python_requires='>=3.6',
      entry_points={
                    'console_scripts': [
                        'pybase16 = pybase16_builder.cli:run'
                                       ]
                   }
     )

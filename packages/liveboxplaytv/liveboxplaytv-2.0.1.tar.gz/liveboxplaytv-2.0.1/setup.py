from setuptools import find_packages, setup


setup(
    name='liveboxplaytv',
    version='2.0.1',
    license='GPL3',
    description='Python bindings for the Orange Livebox Play TV appliance',
    long_description=open('README.rst').read(),
    author='Philipp Schmitt',
    author_email='philipp@schmitt.co',
    url='https://github.com/pschmitt/python-liveboxplaytv',
    packages=find_packages(),
    install_requires=['fuzzywuzzy', 'python-Levenshtein', 'pyteleloisirs>=3.2',
                      'requests', 'wikipedia'],
    entry_points={
        'console_scripts': ['liveboxplaytv=liveboxplaytv.cli:main']
    }
)

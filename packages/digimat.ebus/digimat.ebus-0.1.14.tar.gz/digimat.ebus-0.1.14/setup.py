from setuptools import setup, find_packages

setup(
    name='digimat.ebus',
    version='0.1.14',
    description='Digimat ExternalBus',
    namespace_packages=['digimat'],
    author='Frederic Hess',
    author_email='fhess@splust.ch',
    url='http://www.digimat.ch',
    license='PSF',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'digimat.lp',
        'setuptools'
    ],
    dependency_links=[
        ''
    ],
    zip_safe=False)

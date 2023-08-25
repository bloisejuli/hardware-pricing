import setuptools

setuptools.setup(
    name='hardware-pricing',
    version='0.1.0',
    author='crisis',
    author_email='jbloise@fi.uba.ar',
    description='Scraper of hardware components websites',
    url='https://github.com/bloisejuli/hardware-pricing',
    license='MIT',
    packages=['hardware-pricing'],
    install_requires=['requests','pandas','mysql-connector-python','sqlalchemy','requests','datetime'],
    
)
from setuptools import setup

setup(
    name='ssp_9081',
    version='1.0.0-dev',
    packages=['ssp_9081'],
    install_requires=['pyserial>=3.3'],
    python_requires='>3.5',
    url='https://github.com/maslovw/SSP-9081',
    author='maslovw',
    author_email='maslovw@gmail.com',
    license='MIT',
    keywords='SSP-9081 REMOTE PROGRAMMABLE Power Supply',
    description='Handles SSP-9081 (Remote Programmable Power Supply with DC wave form generator'
)
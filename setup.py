from setuptools import setup
import re


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('ssp_9081/bin/ssp9081.py').read(),
    re.M
    ).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name='ssp-9081',
    version=version,
    packages=['ssp_9081'],
    entry_points={"console_scripts": ['ssp9081 = ssp_9081.bin.ssp9081:main']},
    install_requires=['pyserial>=3.3'],
    python_requires='>3.5',
    url='https://github.com/maslovw/SSP-9081',
    author='maslovw',
    author_email='maslovw@gmail.com',
    license='MIT',
    keywords='SSP-9081 REMOTE PROGRAMMABLE Power Supply',
    description='Handles SSP-9081 (Remote Programmable Power Supply with DC wave form generator'
)
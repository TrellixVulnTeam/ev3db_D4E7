from setuptools import setup,find_packages
from ev3db import VERSION

setup(
    name='ev3db',
    version=str(VERSION),
    description='EV3 debug bridge',
    author='Riccardo Isola',
    author_email='riky.isola@gmail.com',
    packages=find_packages(),
    scripts=['scripts/ev3db'],
)

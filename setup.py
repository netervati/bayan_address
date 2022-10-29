from setuptools import setup

setup(
    name='bayan_address',
    version='0.1.1',    
    description='A Python-based address parser for Philippines',
    url='https://github.com/netervati/bayan_address',
    author='Christopher Tabula',
    author_email='netervati@gmail.com',
    license='MIT License',
    packages=['bayan_address', 'bayan_address/parser', 'bayan_address/lib'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: Microsoft :: Windows :: Windows 10',        
        'Programming Language :: Python :: 3.9',
    ],
)

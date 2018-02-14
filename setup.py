# coding=utf8
from setuptools import setup

setup(
    name='multidiff',
    version='0.1',
    description='Binary data diffing for multiple objects or streams of data',
    url='https://github.com/juhakivekas/multidiff',
    author='Juha Kivekäs',
    author_email='stilla@protonmail.com',
    classifiers=[  # Optional
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='diff hexdump visualizer packet-analysis',
    packages=["multidiff"],
    install_requires=[],
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'multidiff=multidiff.command_line_interface:main',
        ],
    },
)

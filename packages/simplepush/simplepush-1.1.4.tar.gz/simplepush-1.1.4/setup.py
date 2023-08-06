"""Simplepush setup script."""
from distutils.core import setup

setup(
    name='simplepush',
    packages=['simplepush'],
    version='1.1.4',
    description='Simplepush python library',
    author='Timm Schaeuble',
    author_email='contact@simplepush.io',
    url='https://simplepush.io',
    keywords=[
        'push', 'notification', 'android', 'logging', 'app', 'simple',
        'encrypted'
    ],
    license='MIT',
    install_requires=[
        'requests',
        'cryptography'
      ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)

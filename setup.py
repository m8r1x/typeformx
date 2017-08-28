from setuptools import setup, find_packages

setup(
    name='TypeformX',
    version='0.1dev',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=[
        'pandas',
        'requests',
        'textblob',
        'textract'
    ],
    test_require=[
        'mock',
        'nose'
    ]
    
    long_description=open('README.md').read()
)

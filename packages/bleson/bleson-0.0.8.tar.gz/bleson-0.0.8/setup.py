from setuptools import setup, find_packages

setup(
    name='bleson',
    version='0.0.8',
    packages= find_packages(),
    url='https://github.com/TheCellule/python-bleson',
    license='MIT',
    author='TheCellule',
    author_email='thecellule@gmail.com',
    description='Bluetooth LE Library',
    # install_requires=[
    #     'blesonwin; platform_system=="Windows"',
    #     'pyobjc; platform_system=="Darwin"',
    #
    # ],
    extras_require = {
        ':platform_system=="Windows"': [
            'blesonwin'
        ],
        ':platform_system=="Darwin"': [
            'pyobjc'
        ]
    }
)

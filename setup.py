from setuptools import setup

setup(
    name='nz',
    version='0.1.0',
    py_modules=['nz'],
    include_package_data=True,
    install_requires=[
        'click',
        'arrow',
        'requests',
        'untangle',
        'terminaltables'
    ],
    entry_points='''
        [console_scripts]
        nz=nz:cli
    ''',
)

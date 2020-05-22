from setuptools import setup

setup(
    name='PJECZ Clasificador',
    version='0.1',
    py_modules=['clasificador'],
    install_requires=[
        'Click',
        'Jinja2',
        'tabulate',
        ],
    entry_points="""
        [console_scripts]
        clasificador=clasificador:cli
        """,
)

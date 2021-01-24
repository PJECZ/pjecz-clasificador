from setuptools import setup

setup(
    name='PJECZ Clasificador',
    version='2.0',
    py_modules=[
        'clasificador',
        'contestador',
    ],
    install_requires=[
        'click',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'imap_tools',
        'Jinja2',
        'tabulate',
    ],
    entry_points="""
        [console_scripts]
        clasificador=clasificador:cli
        contestador=contestador:cli
        """,
)

"""
Setup sirve para installar los comandos click
"""
from setuptools import setup

setup(
    name="pjecz-clasificador",
    version="2.1",
    py_modules=[
        "clasificador",
        "contestador",
    ],
    install_requires=[
        "click",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "imap_tools",
        "Jinja2",
        "rq",
        "tabulate",
    ],
    entry_points="""
        [console_scripts]
        clasificador=clasificador:cli
        contestador=contestador:cli
        """,
)

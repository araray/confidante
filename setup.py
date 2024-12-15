from setuptools import setup, find_packages

setup(
    name="confidante",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "PyYAML>=6.0",
        "tomli>=2.0.1; python_version<'3.11'",
        "tomli_w>=1.0.0",
        "cryptography>=41.0",
    ],
    entry_points={
        'console_scripts': [
            'confidante=confidante.cli:main',
        ],
    }
)

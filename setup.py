from setuptools import setup, find_packages

setup(
    name="suzie-logs",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "click>=8.0.0",
        "pydantic>=2.0.0", 
        "pyyaml>=6.0",
        "python-dateutil>=2.8.0",
        "rich>=13.0.0",
        "langchain>=0.1.0",
        "openai>=1.0.0",
        "gitpython>=3.1.0"
    ],
    entry_points={
        'console_scripts': [
            'suzie=suzie_logs.cli.main:cli',
        ],
    },
)
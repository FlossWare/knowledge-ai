from setuptools import setup, find_packages

with open("../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="knowledge-ai",
    version="0.5",
    author="FlossWare (sfloess)",
    author_email="sfloess@redhat.com",
    description="Universal knowledge ingestion library for AI systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.cee.redhat.com/sfloess/knowledge-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "vectordb-ai>=0.1",
        "semantic-search-ai>=0.1",
        "consensus-ai>=0.1",
        "requests>=2.25.0",
    ],
    extras_require={
        "pdf": [
            "PyPDF2>=3.0.0",
            "pdfminer.six>=20211012",
        ],
        "markdown": [
            "markdown>=3.3.0",
            "markdown-it-py>=2.0.0",
        ],
        "web": [
            "beautifulsoup4>=4.9.0",
            "lxml>=4.6.0",
            "requests>=2.25.0",
        ],
        "code": [
            "docstring-parser>=0.15",
            "ast-comments>=1.0.0",
        ],
        "structured": [
            "PyYAML>=5.4.0",
            "toml>=0.10.0",
        ],
        "rst": [
            "docutils>=0.17.0",
        ],
        "all": [
            "PyPDF2>=3.0.0",
            "pdfminer.six>=20211012",
            "markdown>=3.3.0",
            "markdown-it-py>=2.0.0",
            "beautifulsoup4>=4.9.0",
            "lxml>=4.6.0",
            "docstring-parser>=0.15",
            "PyYAML>=5.4.0",
            "toml>=0.10.0",
            "docutils>=0.17.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "sphinx>=4.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "knowledge-ai=knowledge_ai.cli:main",
        ],
    },
)

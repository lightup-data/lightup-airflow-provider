from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = "1.0.0"

"""Perform the package airflow-provider-lightup setup."""
setup(
    name="lightup-airflow-provider",
    version=__version__,
    description="Lightup Airflow provider.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={"apache_airflow_provider": ["provider_info=lightup_airflow_provider.__init__:get_provider_info"]},
    license="Apache License 2.0",
    packages=find_packages(exclude=["*tests.*", "*tests"]),
    install_requires=[],
    setup_requires=["setuptools", "wheel"],
    author="Lightup Data, Inc",
    author_email="support@lightup.ai",
    url="https://www.lightup.ai/",
    classifiers=[
        "Framework :: Apache Airflow",
        "Framework :: Apache Airflow :: Provider",
    ],
    python_requires="~=3.9",
)

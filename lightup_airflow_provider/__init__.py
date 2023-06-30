from importlib.metadata import version

__name__ = "lightup-airflow-provider"
__version__ = version(__name__)

## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.
def get_provider_info():
    return {
        "package-name": __name__,
        "name": "Lightup Airflow Provider",
        "description": "A Lightup provider for Apache Airflow.",
        "versions": [__version__],
    }

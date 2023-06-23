from airflow.hooks.base_hook import BaseHook
from airflow.models.baseoperator import BaseOperator
from airflow.models import Variable


class LightupBaseOperator(BaseOperator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        conn = BaseHook.get_connection('lightup_endpoint')
        self._url_base = conn.host
        self._refresh_token = conn.password
        self._api_version = Variable.get("lightup_api_version")

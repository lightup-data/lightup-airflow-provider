import requests
import urllib.parse
from typing import Optional

from lightup_base_operator import LightupBaseOperator


class LightupTriggerOperator(LightupBaseOperator):
    template_fields = ['dag_run_id']

    def __init__(
            self,
            workspace_id: Optional[str] = None,
            source_id: Optional[str] = None,
            table_uuids: Optional[list] = None,
            metric_uuids: Optional[list] = None,
            dag_run_id: Optional[str] = None,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._workspace_id = workspace_id
        self._source_id = source_id
        self._table_uuids = table_uuids
        self._metric_uuids = metric_uuids
        self.dag_run_id = dag_run_id

    def execute(self, context):
        endpoint = urllib.parse.urljoin(
            self._url_base, f"/api/{self._api_version}/token/refresh/"
        )
        data = {"refresh": self._refresh_token}
        res = requests.post(endpoint, json=data)
        assert res.status_code == 200
        access_token = res.json()["access"]

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        assert self._workspace_id
        assert self._source_id
        data_string_list = []
        if self._table_uuids:
            data_string_list.append("\"tableUuids\": [" + ", ".join(f"\"{uuid}\"" for uuid in self._table_uuids) + "]")
        if self._metric_uuids:
            data_string_list.append("\"metricUuids\": [" + ", ".join(f"\"{uuid}\"" for uuid in self._metric_uuids) + "]")
        if self.dag_run_id:
            data_string_list.append(f"\"userDefinedId\": \"{self.dag_run_id}\"")
        assert data_string_list

        res = requests.post(
            urllib.parse.urljoin(self._url_base, f"/api/v1/ws/{self._workspace_id}/sources/{self._source_id}/trigger"),
            headers=headers,
            data="{" + ",".join(data_string_list) + "}"
        )
        print(f"trigger >>> dag_run_id = {self.dag_run_id}")
        print(f"trigger >>> http response status_code = {res.status_code}")
        print(f"trigger >>> http response content = {res.content}")

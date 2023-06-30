import json

import requests
import urllib.parse
from typing import Optional
from urllib.parse import quote_plus

from lightup_base_sensor_operator import LightupBaseSensorOperator


class LightupTriggerResultSensor(LightupBaseSensorOperator):
    template_fields = ['dag_run_id']

    def __init__(
            self,
            result_check_func=None,
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
        self.result_check_func = result_check_func

    def poke(self, context):
        endpoint = urllib.parse.urljoin(
            self._url_base, f"/api/{self._api_version}/token/refresh/"
        )
        data = {"refresh": self._refresh_token}
        res = requests.post(endpoint, json=data)
        assert res.status_code == 200
        access_token = res.json()["access"]

        headers = {"Authorization": f"Bearer {access_token}"}
        assert self._workspace_id
        res = requests.get(
            urllib.parse.urljoin(self._url_base,
                                 f"/api/v1/ws/{self._workspace_id}/sources/{self._source_id}/trigger?userDefinedId={quote_plus(self.dag_run_id)}"),
            headers=headers
        )

        print(f"sensor >>> dag_run_id = {self.dag_run_id}")
        print(f"sensor >>> http response status_code = {res.status_code}")
        print(f"sensor >>> http response content = {res.content}")

        if not res:
            print(f"sensor >>> http response is None")
            return False

        content = json.loads(res.content)
        trigger_status = content.get("triggerStatus", {})
        if not trigger_status:
            print(f"sensor >>> trigger_status is None")
            return False

        if self.result_check_func:
            return self.result_check_func(trigger_status)

        if trigger_status["status"] != "completed":
            print(f"sensor >>> status is {trigger_status['status']} instead of 'completed'")
            return False

        if trigger_status["incidentsCount"]:
            print(f"sensor >>> has error")
            return False

        print(f"sensor >>> no error")
        return True

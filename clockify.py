from utils import api_request


class Clockify():

    def __init__(self, api_token: str) -> None:
        self.token = api_token
        self.headers = {
            "X-Api-Key": self.token,
            "content-type": "application/json"
        }
        self.base_url = "https://api.clockify.me/api/v1"
        self.reports_base_url = "https://reports.api.clockify.me/v1"

    def get_workspaces(self) -> dict:
        return api_request(self.base_url, "/workspaces", "GET",
                           headers=self.headers)

    def get_workspace_users(self, workspace_id: str) -> dict:
        return api_request(self.base_url, f"/workspaces/{workspace_id}/users",
                           "GET", headers=self.headers)

    def get_workspace_summary_report(self, workspace_id: str, time_start: str,
                                     time_end, summary_groups_filter=[
                                        'USER', 'PROJECT', 'TIMEENTRY'
                                     ], export_type="JSON") -> dict:
        endpoint = f"/workspaces/{workspace_id}/reports/summary"
        payload = {
            "dateRangeStart": time_start,
            "dateRangeEnd": time_end,
            "summaryFilter": {
                "groups": summary_groups_filter
            },
            "amountShown": "HIDE_AMOUNT",
        }

        return api_request(self.reports_base_url, endpoint, 'POST', payload,
                           headers=self.headers)

    def get_workspace_ids(self):
        workspaces = self.get_workspaces()
        ids = []
        workspace_map = {}
        for workspace in workspaces:
            ids.append(workspace['id'])
            workspace_map[workspace['id']] = workspace['name']
        
        return ids, workspace_map

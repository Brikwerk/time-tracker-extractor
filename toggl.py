from utils import api_request


class Toggl():

    def __init__(self, api_token) -> None:
        self.auth = (api_token, "api_token")
        self.base_url = "https://api.track.toggl.com/api/v9"
        self.reports_base_url = "https://api.track.toggl.com/reports/api/v2"
    
    def get_workspaces(self) -> dict:
        return api_request(self.base_url, "/workspaces", "GET", auth=self.auth)

    def get_workspace_summary_report(self, workspace_id: str, time_start: str,
                                     time_end: str) -> dict:
        endpoint = "/summary"
        params = {
            "user_agent": "python-bot",
            "workspace_id": workspace_id,
            "since": time_end,
            "until": time_start,
            "grouping": "users"
        }

        return api_request(self.reports_base_url, endpoint, 'GET',
                           params=params, auth=self.auth)

    def get_workspace_ids(self):
        workspaces = self.get_workspaces()
        ids = []
        workspace_map = {}
        for workspace in workspaces:
            ids.append(workspace['id'])
            workspace_map[workspace['id']] = workspace['name']
        
        return ids, workspace_map

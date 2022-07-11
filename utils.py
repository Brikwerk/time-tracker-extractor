import datetime
import requests


def get_iso_timestamp(dt: datetime.datetime) -> str:
    return dt.replace(microsecond=0).isoformat()


def get_last_datetime_of_weekday(ref_dt: datetime.datetime,
                                 weekday_name: str) -> datetime.datetime:
    weekday_map = {
        'sunday': 0, 'monday': 1, 'tuesday': 2, 'wednesday': 3,
        'thursday': 4, 'friday': 5, 'saturday': 6
    }
    weekday_idx = weekday_map[weekday_name.lower()]

    delta = weekday_idx - ref_dt.isoweekday()
    if delta > 0: # If the weekday is ahead in time, go back a week
        delta -= 7
    
    return ref_dt + datetime.timedelta(days=delta)


def get_last_friday_or_wednesday(ref_dt: datetime.datetime) -> datetime.datetime:
    last_wed = get_last_datetime_of_weekday(ref_dt, 'wednesday')
    last_fri = get_last_datetime_of_weekday(ref_dt, 'friday')

    if last_wed > last_fri:
        return last_wed
    else:
        return last_fri


def api_request(base_url: str, endpoint: str, action: str,
                payload: dict = None, headers: dict = None,
                auth: dict = None, params: dict = None) -> dict:
    if action not in ["GET", "PUT", "POST", "DELETE"]:
        raise ValueError(f"Request action {action} is invalid.")

    if endpoint[0] != '/':
        raise ValueError("Endpoints should start with a forward slash.")

    url = f"{base_url}{endpoint}"

    if action == "PUT":
        response = requests.put(url, json=payload, headers=headers, auth=auth)
    elif action == "POST":
        response = requests.post(url, json=payload, headers=headers, auth=auth)
    elif action == "DELETE":
        response = requests.delete(url, headers=headers, auth=auth)
    else:
        response = requests.get(url, headers=headers, auth=auth, params=params)

    if response.ok:
        return response.json()
    else:
        try:
            print(response.json())
        except Exception:
            pass
        response.raise_for_status()

from datetime import datetime, timedelta


def add_days(start_date, time_delta):
    start_date = datetime.fromisoformat(start_date)
    date_end = start_date + timedelta(days=time_delta)
    date_end = date_end.strftime("%Y-%m-%dT%H:%M:%S") + "+03:00"
    return date_end


def string_to_list(string):
    return list(eval(string))


def list_to_diclist(names, list_to_change):
    return dict(zip(names, list_to_change))



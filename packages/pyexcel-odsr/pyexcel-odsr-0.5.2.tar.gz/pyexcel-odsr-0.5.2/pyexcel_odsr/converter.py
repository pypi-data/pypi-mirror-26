import sys
import datetime

PY2 = sys.version_info[0] == 2


def float_value(value):
    """convert a value to float"""
    ret = float(value)
    return ret


def date_value(value):
    """convert to data value accroding ods specification"""
    ret = "invalid"
    try:
        # catch strptime exceptions only
        if len(value) == 10:
            ret = datetime.datetime.strptime(
                value,
                "%Y-%m-%d")
            ret = ret.date()
        elif len(value) == 19:
            ret = datetime.datetime.strptime(
                value,
                "%Y-%m-%dT%H:%M:%S")
        elif len(value) > 19:
            ret = datetime.datetime.strptime(
                value[0:26],
                "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        pass
    if ret == "invalid":
        raise Exception("Bad date value %s" % value)
    return ret


def time_value(value):
    """convert to time value accroding the specification"""
    import re
    results = re.match('PT(\d+)H(\d+)M(\d+)S', value)
    if results and len(results.groups()) == 3:
        hour = int(results.group(1))
        minute = int(results.group(2))
        second = int(results.group(3))
        if hour < 24:
            ret = datetime.time(hour, minute, second)
        else:
            ret = datetime.timedelta(hours=hour,
                                     minutes=minute,
                                     seconds=second)
    else:
        ret = None
    return ret


def boolean_value(value):
    """get bolean value"""
    if value == "true":
        ret = True
    else:
        ret = False
    return ret


ODS_FORMAT_CONVERSION = {
    "float": float,
    "date": datetime.date,
    "time": datetime.time,
    'timedelta': datetime.timedelta,
    "boolean": bool,
    "percentage": float,
    "currency": float
}


ODS_WRITE_FORMAT_COVERSION = {
    float: "float",
    int: "float",
    str: "string",
    datetime.date: "date",
    datetime.time: "time",
    datetime.timedelta: "timedelta",
    bool: "boolean"
}

if PY2:
    ODS_WRITE_FORMAT_COVERSION[unicode] = "string"

VALUE_CONVERTERS = {
    "float": float_value,
    "date": date_value,
    "time": time_value,
    "timedelta": time_value,
    "boolean": boolean_value,
    "percentage": float_value
}


VALUE_TOKEN = {
    "float": "value",
    "date": "date-value",
    "time": "time-value",
    "boolean": "boolean-value",
    "percentage": "value",
    "currency": "value",
    "timedelta": "time-value"
}

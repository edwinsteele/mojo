# -*- coding: utf-8 -*-

"""Console script for mojo."""
import datetime
import os
import sys
import click
from anycache import anycache
import requests


SINGLE_RATE_DAILY_SUPPLY_CHARGE = 157.960
SINGLE_RATE_PER_KWH = 24.24
TOU_DAILY_SUPPLY_CHARGE = 184.404
TOU_PEAK_PER_KWH = 34.080
TOU_SHOULDER_PER_KWH = 28.050
TOU_OFFPEAK_PER_KWH = 18.293
TOU_CATEGORY_PEAK = "Peak"
TOU_CATEGORY_SHOULDER = "Shoulder"
TOU_CATEGORY_OFFPEAK = "OffPeak"


@anycache(cachedir="/tmp/mojo-data.anycache", maxsize=None)
def get_day_usage_by_hour(ymd, bearer_token):
    # bearer_token comes from parent scope. We don't put it as a function
    #  argument because it'll become a part of the cache key, which means
    #  we don't reuse the cache results when the bearer_token changes. We
    #  can work around this by using a depfilefunc when creating the
    #  anycache object... later.
    headers = {
        "Authorization": "Bearer %s" % (bearer_token,),
        "Origin": "https://portal.mojopower.com.au",
        "Host": "api.mojopower.com.au",
        "Origin": "https://portal.mojopower.com.au",
        "Referer": "https://portal.mojopower.com.au/energy",
    }
    url = "https://api.mojopower.com.au/app_prod/energy"
    payload = {
        "resolution": "hourly",
        "startDate": ymd
    }
    r = requests.get(url, params=payload, headers=headers)
    return r.json()


def get_import_data_from_day_usage(usage_json):
    imports = usage_json["usageDataSets"]["netImports"]["dataSet"]
    return [(datetime.datetime.strptime(h["x"], "%Y-%m-%d %H:%M:%S"), h["y"])
            for h in imports]


def get_tou_category_for_dt(dt):
    if dt.weekday() >= 5:
        # Weekend
        return TOU_CATEGORY_OFFPEAK

    if dt.hour < 7 or dt.hour >= 22:
        return TOU_CATEGORY_OFFPEAK

    if dt.hour < 13 or dt.hour >= 20:
        return TOU_CATEGORY_SHOULDER

    return TOU_CATEGORY_PEAK


def day_cost_with_tou(offpeak_kwh, shoulder_kwh, peak_kwh):
    return TOU_DAILY_SUPPLY_CHARGE + \
        (offpeak_kwh * TOU_OFFPEAK_PER_KWH) + \
        (shoulder_kwh * TOU_SHOULDER_PER_KWH) + \
        (peak_kwh * TOU_PEAK_PER_KWH)


def day_cost_with_flat(offpeak_kwh, shoulder_kwh, peak_kwh):
    return SINGLE_RATE_DAILY_SUPPLY_CHARGE + \
        (offpeak_kwh + shoulder_kwh + peak_kwh) * SINGLE_RATE_PER_KWH


def analyse_one_day(date_for_analysis, bearer_token):
    peak_kwh = 0
    shoulder_kwh = 0
    offpeak_kwh = 0
    usage = get_day_usage_by_hour(date_for_analysis, bearer_token)
    import_data = get_import_data_from_day_usage(usage)
    for ts, kwh in import_data:
        category = get_tou_category_for_dt(ts)
        if category == TOU_CATEGORY_OFFPEAK:
            offpeak_kwh += kwh
        elif category == TOU_CATEGORY_SHOULDER:
            shoulder_kwh += kwh
        elif category == TOU_CATEGORY_PEAK:
            peak_kwh += kwh

    src_str = day_cost_with_flat(offpeak_kwh, shoulder_kwh, peak_kwh)
    trc_str = day_cost_with_tou(offpeak_kwh, shoulder_kwh, peak_kwh)
    print("%s,%.2f,%.2f" % (date_for_analysis, src_str, trc_str))
    #print("Single rate cost: %.2f" % (src_str,))
    #print("TOU rate cost: %.2f" % (trc_str,))


@click.command()
@click.option("--bearer-token",
              prompt=True,
              default=lambda: os.environ.get("MOJO_BEARER_TOKEN", ""),
              help="mojopower bearer")
@click.argument('start-date')
@click.argument('stop-date')
def main(bearer_token, start_date, stop_date):
    """
    Console script for mojo.

    start and stop dates to be given as YYYY-MM-DD
    """
    print("date,single-rate-cost,tou-rate-cost")
    start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    stop_dt = datetime.datetime.strptime(stop_date, "%Y-%m-%d")
    current_dt = start_dt
    while current_dt < stop_dt:
        analyse_one_day(current_dt.strftime("%Y-%m-%d"), bearer_token)
        current_dt = current_dt + datetime.timedelta(days=1)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

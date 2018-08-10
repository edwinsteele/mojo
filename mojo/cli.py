# -*- coding: utf-8 -*-

"""Console script for mojo."""
import os
import sys
import click
import requests



def get_day_usage_by_hour(ymd, bearer_token):
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
        "startDate": "2018-08-08"
    }
    r = requests.get(url, params=payload, headers=headers)
    return r.json()


@click.command()
@click.option("--bearer-token",
              prompt=True,
              default=lambda: os.environ.get("MOJO_BEARER_TOKEN", ""),
              help="mojopower bearer")
def main(bearer_token):
    """Console script for mojo."""
    print(get_day_usage_by_hour("2018-08-08", bearer_token))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

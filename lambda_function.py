import os
import requests
from datetime import date, timedelta
from munch import munchify  # Dictionaries, but nicer to use

BASE_URL = "https://api.npmjs.org/downloads/point"
DEFAULT_DATE = date(2018, 1, 1)  # Start date for first run & newly-added packages


def lambda_handler(request, context=None):
    # Using an env var for simpler testing, both locally & remotely
    packages = os.environ["NPM_PACKAGES"].split(",")
    payload = initialise_payload()
    
    for package in packages:
        # Use last update if the library has previously been checked, 
        # otherwise fetch all dates since the default
        try:
            last_date = date.fromisoformat(request["state"][package])
        except KeyError:
            last_date = DEFAULT_DATE

        dates = build_date_range(last_date)
        print(f"Fetching {package} downloads for {min(dates)} to {max(dates)}")
        downloads = get_daily_downloads(package, dates)
        payload.insert.npm_downloads.extend(downloads)

        # Set starting date for next invocation
        new_last_date = max(dates)
        payload.state[package] = str(new_last_date)

        # Tell Fivetran if there's still more info to fetch
        if new_last_date < date.today() - timedelta(1):
            payload.hasMore = True

    return payload


def initialise_payload():
    # Skeleton of data to be returned to Fivetran
    payload = {
        # State acts as a bookmarking system for the connector
        "state": {},

        # New data to be added to the destination
        "insert": {
            "npm_downloads": []  # One row per table
        },

        # Data to be marked as deleted in the destination
        "delete": {},

        # Primary key for each table (if missing new data will be appended, not merged)
        "schema": {
            "npm_downloads": {"primary_key": ["package", "start_date"]}
        },
        
        # Indicates whether all available data was retrieved on this invocation.
        # If false, Fivetran will immediately run the lambda again.
        "hasMore": False
    }

    payload = munchify(payload)

    return payload


def build_date_range(last_date):
    # Returns last date & all intervening dates up to (but not including) the 
    # current date, so output will never be an empty list.
    dates = []
    check_date = last_date

    while check_date < date.today() and len(dates) < 20:
        dates.append(check_date)
        check_date = check_date + timedelta(1)
    
    return sorted(dates)


def get_daily_downloads(package, dates):
    results = []

    for d in dates:
        url = f"{BASE_URL}/{d}/{package}"
        resp = requests.get(url)
        resp.raise_for_status()

        json_resp = resp.json()
        # Changing column names to avoid using SQL keywords
        clean_resp = {
            "package": json_resp["package"],
            "start_date": json_resp["start"],
            "end_date": json_resp["end"],
            "downloads": json_resp["downloads"],
        }
        results.append(clean_resp)

    return results

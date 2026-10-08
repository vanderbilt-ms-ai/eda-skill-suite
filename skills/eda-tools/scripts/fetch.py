"""Fetch each piece of a data request once, check it before saving, and keep the raw file unchanged.

Copy this file into the project's tools/ folder (tools/fetch.py) and import it in the setup
notebook:

    from tools.fetch import fetch, fetch_all, csv_check, csv_summary

    pieces = [{"name": "2024-01", "url": URL, "params": {"start": "2024-01-01", "end": "2024-01-31"},
               "dest": "data/raw/2024-01.csv",
               "check": csv_check(date_col="DATE", start="2024-01-01", end="2024-01-31", min_rows=28)}]
    fetch_all(pieces, date_col="DATE")      # a table: piece, status, rows, first, last, reason

A piece already in data/raw/ that passes its check is returned without a request. A response is
checked before it is saved; one that fails is not saved, and the piece is listed as failed with the
reason. Re-run the same call to re-request only the failed pieces.
"""
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class Result:
    path: Path
    status: str   # "on disk", "fetched", or "failed"
    reason: str   # empty unless failed


def not_empty(path):
    """The default check: the file holds something."""
    return "" if Path(path).stat().st_size > 0 else "empty response"


def csv_check(date_col=None, start=None, end=None, min_rows=1, **read_kwargs):
    """A check for a CSV piece: at least min_rows rows, and when date_col is given, the first date
    at or before start and the last date at or after end. Returns "" when the file passes."""
    def check(path):
        try:
            df = pd.read_csv(path, **read_kwargs)
        except Exception as error:          # an HTML error page, a truncated file
            return f"not readable as CSV: {error}"
        if len(df) < min_rows:
            return f"{len(df)} rows, expected at least {min_rows}"
        if date_col:
            if date_col not in df.columns:
                return f"no column {date_col}"
            dates = pd.to_datetime(df[date_col], errors="coerce")
            if start and dates.min() > pd.Timestamp(start):
                return f"first date {dates.min().date()} is after {start}"
            if end and dates.max() < pd.Timestamp(end):
                return f"last date {dates.max().date()} is before {end}"
        return ""
    return check


def csv_summary(path, date_col=None, **read_kwargs):
    """Rows and, when date_col is given, first and last date of a saved CSV piece."""
    df = pd.read_csv(path, **read_kwargs)
    summary = {"rows": len(df), "first": None, "last": None}
    if date_col and date_col in df.columns:
        dates = pd.to_datetime(df[date_col], errors="coerce")
        summary["first"], summary["last"] = dates.min(), dates.max()
    return summary


def fetch(url, dest, check=None, params=None, retries=3, timeout=120, pause=2.0, headers=None):
    """Return a Result for one piece. No request is made when dest exists and passes check."""
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    check = check or not_empty
    if dest.exists() and not check(dest):
        return Result(dest, "on disk", "")
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers=headers or {"User-Agent": "eda-tools fetch"})
    reason = ""
    for attempt in range(retries):
        if attempt:
            time.sleep(pause * attempt)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = response.read()
        except Exception as error:
            reason = f"request failed: {error}"
            continue
        partial = dest.with_name(dest.name + ".part")
        partial.write_bytes(data)
        reason = check(partial)
        if not reason:
            partial.replace(dest)
            return Result(dest, "fetched", "")
        partial.unlink()
    return Result(dest, "failed", reason)


def fetch_all(pieces, date_col=None, **fetch_kwargs):
    """Fetch every piece (a dict with name, url, dest, and optionally params and check) and return a
    table of piece, status, rows, first, last, reason. Show the table in the notebook."""
    rows = []
    for piece in pieces:
        result = fetch(piece["url"], piece["dest"], check=piece.get("check"),
                       params=piece.get("params"), **fetch_kwargs)
        row = {"piece": piece["name"], "status": result.status, "rows": None, "first": None,
               "last": None, "reason": result.reason}
        if result.status != "failed" and str(result.path).lower().endswith(".csv"):
            try:
                row.update(csv_summary(result.path, date_col))
            except Exception as error:
                row["reason"] = f"saved, but not summarized: {error}"
        rows.append(row)
    return pd.DataFrame(rows).set_index("piece")

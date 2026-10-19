"""Scrape the educational Fake Python Jobs site into a CSV file."""

import argparse
import csv
import sys
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://realpython.github.io/fake-jobs/"
FIELDNAMES = ["title", "company", "location", "url"]


def scrape_jobs(source_url: str = SOURCE_URL) -> list[dict[str, str]]:
    """Fetch and extract job cards, keeping missing fields as empty strings."""
    response = requests.get(
        source_url,
        timeout=20,
        headers={"User-Agent": "job-listings-scraper/1.0 (learning project)"},
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    for card in soup.select("div.card-content"):
        title = card.select_one("h2.title")
        company = card.select_one("h3.company")
        location = card.select_one("p.location")
        details_link = card.find("a", string=lambda text: text and "Apply" in text)
        href = details_link.get("href", "") if details_link else ""

        jobs.append(
            {
                "title": title.get_text(" ", strip=True) if title else "",
                "company": company.get_text(" ", strip=True) if company else "",
                "location": location.get_text(" ", strip=True) if location else "",
                "url": urljoin(source_url, href) if href else "",
            }
        )
    return jobs


def save_csv(jobs: list[dict[str, str]], output_path: Path) -> None:
    """Write jobs to a UTF-8 CSV file, including headers when there are no rows."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(jobs)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape Fake Python Jobs into CSV.")
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("jobs.csv"),
        help="CSV destination (default: jobs.csv)",
    )
    parser.add_argument(
        "--url", default=SOURCE_URL,
        help=f"Jobs page URL (default: {SOURCE_URL})",
    )
    args = parser.parse_args()

    try:
        jobs = scrape_jobs(args.url)
        save_csv(jobs, args.output)
    except requests.RequestException as error:
        print(f"Could not fetch jobs: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"Could not write CSV: {error}", file=sys.stderr)
        return 1

    print(f"Saved {len(jobs)} job listings to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Python Job Listings Scraper

A small Python scraper for the educational [Fake Python Jobs](https://realpython.github.io/fake-jobs/) website. It extracts each listing's job title, company, location, and detail page URL, then saves the results as CSV.

## Requirements

- Python 3.9+
- `requests` and `beautifulsoup4` (installed from `requirements.txt`)

## Run

```bash
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

python -m pip install -r requirements.txt
python scraper.py
```

The default output is `jobs.csv` in the current directory. Choose another destination with `-o`:

```bash
python scraper.py --output data/jobs.csv
```

You can also provide a different source page with `--url`. The scraper reports network and file errors, and leaves missing fields empty in the CSV.

## Project page

[roadmap.sh — Python Job Listings Scraper](https://roadmap.sh/projects/job-listings-scraper)

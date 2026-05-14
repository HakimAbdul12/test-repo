# Autotrader car maker logo downloader

This repo contains a script to list and download car maker logos from:

- https://www.autotrader.co.uk/cars/brands?refresh=true

## Usage

```bash
python -m pip install requests beautifulsoup4
python download_autotrader_logos.py
```

The script writes:

- `autotrader_car_makers_and_logos.csv` (maker + logo URL + local filename)
- `autotrader_logos/` (downloaded logo files)

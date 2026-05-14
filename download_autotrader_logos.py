from pathlib import Path
from urllib.parse import urljoin
import csv
import requests
from bs4 import BeautifulSoup

URL = "https://www.autotrader.co.uk/cars/brands?refresh=true"
OUT_DIR = Path("autotrader_logos")
CSV_PATH = Path("autotrader_car_makers_and_logos.csv")


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)

    resp = requests.get(URL, timeout=60)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    logo_links = soup.select('a[href]')
    rows = []
    seen = set()

    for a in logo_links:
        label = a.get_text(" ", strip=True)
        if not label.startswith("Image:") or " logo" not in label:
            continue

        # Example: "Image: Audi logo"
        maker = label.removeprefix("Image:").removesuffix(" logo").strip()
        href = a.get("href", "")
        if not maker or not href or maker in seen:
            continue

        img_url = urljoin(URL, href)
        ext = Path(img_url.split("?")[0]).suffix or ".jpg"
        safe_name = maker.lower().replace(" ", "-").replace("/", "-")
        img_path = OUT_DIR / f"{safe_name}{ext}"

        img_resp = requests.get(img_url, timeout=60)
        img_resp.raise_for_status()
        img_path.write_bytes(img_resp.content)

        rows.append((maker, img_url, str(img_path)))
        seen.add(maker)

    rows.sort(key=lambda r: r[0].lower())

    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["maker", "logo_url", "local_file"])
        w.writerows(rows)

    print(f"Saved {len(rows)} logos to {OUT_DIR}")
    print(f"Wrote listing to {CSV_PATH}")


if __name__ == "__main__":
    main()

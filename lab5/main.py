# Laborator: funcții, metode și importuri pe web
# Student: <Gorceag Vlad>
import argparse
import json

import webtools


def main() -> None:
    """Citește URL-ul din linia de comandă și afișează raportul."""
    parser = argparse.ArgumentParser(description="Generează un raport despre un site web.")
    parser.add_argument(
        "url",
        nargs="?",
        default=webtools.BASE_URL,
        help="URL complet sau cale relativă (implicit: site-ul de bază)",
    )
    parser.add_argument(
        "--output",
        default="report.json",
        help="Fișierul JSON de ieșire (implicit: report.json)",
    )
    args = parser.parse_args()

    report = webtools.site_report(args.url, args.output)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    # Test negativ cerut în laborator: get_status primește un tip invalid.
    try:
        webtools.get_status(123)
    except TypeError:
        print("Test get_status(123): PASS — TypeError detectat.")
    else:
        raise AssertionError("get_status(123) trebuia să ridice TypeError.")

    main()

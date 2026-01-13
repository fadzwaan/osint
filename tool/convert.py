import csv
import json
import argparse
from toon import encode

def csv_to_json(csv_file, output_file):
    """Convert CSV to JSON"""
    data = []
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"CSV converted to JSON: {output_file}")

def csv_to_toon(csv_file, output_file):
    """Convert CSV to TOON"""
    rows = []
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    data = {"records": rows}
    toon_str = encode(data)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(toon_str)
    print(f"CSV converted to TOON: {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert CSV file to JSON or TOON"
    )
    parser.add_argument("csv_file", help="Path to input CSV file")
    parser.add_argument(
        "-f", "--format",
        choices=["json", "toon"],
        default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file name (optional, default: output.json or output.toon)"
    )

    args = parser.parse_args()

    # Determine output file
    if args.output:
        output_file = args.output
    else:
        output_file = "output.json" if args.format == "json" else "output.toon"

    # Run the conversion
    if args.format == "json":
        csv_to_json(args.csv_file, output_file)
    else:
        csv_to_toon(args.csv_file, output_file)

if __name__ == "__main__":
    print("python convert_csv.py input.csv -f json -o my_data.json")
    print("python convert_csv.py input.csv -f toon -o my_data.toon")
    main()

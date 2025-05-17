import pdfplumber
import json

def get_pricelist_nile_trading():
    result = []

    with pdfplumber.open('Nile Trading 2025 Pricelist (1).pdf') as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                if not table or len(table) < 3:
                    continue  # Skip if table is too small or empty

                headers_row = table[1]
                size_labels = [cell.strip() for cell in headers_row[1:4] if cell]

                for row in table[2:]:
                    if not row or not row[0]:
                        continue  # Skip empty or malformed rows

                    product_name = row[0].strip()
                    prices = []

                    for i, size in enumerate(size_labels):
                        raw_price = row[i + 1].strip() if row[i + 1] else ""
                        price = None if raw_price.upper() == "CALL" or raw_price == "-" else float(raw_price)
                        prices.append({
                            "size": size,
                            "price": price
                        })

                    result.append({
                        "product_name": product_name,
                        "prices": prices
                    })

    with open("nile_pricelist.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

get_pricelist_nile_trading()

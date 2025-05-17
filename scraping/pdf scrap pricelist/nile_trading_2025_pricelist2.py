import pdfplumber
import json

def get_pricelist_nile_trading():
    category_map = {}

    with pdfplumber.open('Nile Trading 2025 Pricelist (1).pdf') as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table or len(table) < 3:
                continue

            # Find category from second row
            category_row = table[1]
            if category_row and category_row[0]:
                raw_category = category_row[0].strip()
                if "Nile Stone - " in raw_category:
                    category = raw_category.replace("Nile Stone - ", "").strip().upper()
                else:
                    continue
            else:
                continue

            size_labels = [cell.strip() for cell in category_row[1:4] if cell]

            for row in table[2:]:
                if not row or not row[0]:
                    continue  # skip empty or malformed rows

                product_name = row[0].strip()
                prices = []

                for i, size in enumerate(size_labels):
                    try:
                        raw_price = row[i + 1].strip() if row[i + 1] else ""
                        price = None if raw_price.upper() == "CALL" or raw_price == "-" else float(raw_price)
                        prices.append({
                            "size": size,
                            "price": price
                        })
                    except IndexError:
                        continue

                product_entry = {
                    "product_name": product_name,
                    "prices": prices
                }

                category_map.setdefault(category, []).append(product_entry)

    final_output = [
        {
            "material": cat,
            "products": products
        }
        for cat, products in category_map.items()
    ]

    with open("nile_pricelist2.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

get_pricelist_nile_trading()

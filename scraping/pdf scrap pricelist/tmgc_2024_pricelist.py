import pdfplumber
import json

def get_pricelist_tmgc():
    all_products = []
    standard_sizes = ["12mm", "20mm", "30mm", "40mm", "50mm", "80mm"]

    with pdfplumber.open("TMGC January 2024 Pricelist.pdf") as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:

                header = table[0]
                # Check for 'Other Products' special format
                if "Other Products" in header[0]:
                    for row in table[1:]:
                        if len(row) >= 3 and row[0] and row[2]:
                            price_value = float(row[2].replace("£", "").strip())

                            all_products.append({
                                "product_name": row[0],
                                "price": price_value
                            })
                    continue

                size_headers = header[1:]
                size_map = {i: size for i, size in enumerate(size_headers)}

                # Skip table if no recognizable size columns
                if not any(size in standard_sizes for size in size_headers):
                    continue

                for row in table[1:]:

                    product_name = row[0]
                    prices = []

                    for size in standard_sizes:
                        price_value = None
                        if size in size_headers:
                            col_idx = size_headers.index(size)
                            price_raw = row[col_idx + 1] if col_idx + 1 < len(row) else None

                            if price_raw is not None:
                                try:
                                    price_value = float(price_raw.replace("£", "").strip())
                                except (ValueError, AttributeError):
                                    price_value = None

                        prices.append({
                            "size": size,
                            "price": price_value
                        })

                    all_products.append({
                        "product_name": product_name,
                        "prices": prices
                    })
    with open("tmgc_pricelist.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=2, ensure_ascii=False)

get_pricelist_tmgc()

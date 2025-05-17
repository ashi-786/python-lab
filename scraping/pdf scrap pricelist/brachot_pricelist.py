import pdfplumber
import json

pdf_path = "Brachot 2025 Pricelist.pdf"
all_tables = []

def extract_tables_by_gap(page, gap_threshold=40):
    words = page.extract_words()
    words.sort(key=lambda w: (float(w['top']), float(w['x0'])))  # top-to-bottom, then left-to-right

    tables = []
    current_table = []
    last_top = None

    for word in words:
        top = float(word['top'])

        if last_top is not None and abs(top - last_top) > gap_threshold:
            if current_table:
                tables.append(current_table)
                current_table = []

        current_table.append(word)
        last_top = top

    if current_table:
        tables.append(current_table)

    return tables

with pdfplumber.open(pdf_path) as pdf:
    for page_num in range(6, 8):
        page = pdf.pages[page_num]
        segmented_tables = extract_tables_by_gap(page)

        for segment in segmented_tables:
            rows = {}
            for word in segment:
                top = round(word['top'], 1)
                x0 = float(word['x0'])
                text = word['text']
                if top not in rows:
                    rows[top] = []
                rows[top].append((x0, text))

            # Sort rows and merge words with spacing
            table = []
            for top in sorted(rows.keys()):
                sorted_words = sorted(rows[top], key=lambda x: x[0])
                row = []
                current_cell = sorted_words[0][1]
                last_x = sorted_words[0][0]

                for i in range(1, len(sorted_words)):
                    x, text = sorted_words[i]
                    if x - last_x >= 30:  # gap of at least 30px
                        row.append(current_cell)
                        current_cell = text
                    else:
                        current_cell += ' ' + text
                    last_x = x

                row.append(current_cell)
                table.append(row)

            if len(table) > 1:  # ignore noise
                all_tables.append(table)

# Save to JSON
with open("all_tables.json", "w", encoding="utf-8") as f:
    json.dump(all_tables, f, indent=2, ensure_ascii=False)
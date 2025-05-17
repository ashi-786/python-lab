import camelot
# import matplotlib.pyplot as plt
import json

# Path to your PDF file
pdf_path = "Brachot 2025 Pricelist.pdf"
page_range = "7-8"

# Extract tables using stream method
tables = camelot.read_pdf(
    filepath=pdf_path,
    pages=page_range,
    flavor='stream',
    strip_text='\n',
    # edge_tol=500
)


# for table in tables:
#     fig = camelot.plot(table, kind='text')
#     plt.show()

# combined_df = pd.DataFrame()
# for i, table in enumerate(tables):
#     df = table.df
    # Optional: Add a header to mark where each table starts
    # marker_row = pd.DataFrame([[f"--- Table {i+1} ---"] + [""] * (df.shape[1] - 1)], columns=df.columns)
    
    # combined_df = pd.concat([combined_df, df], ignore_index=True)

# combined_df.to_csv("all_tables_combined.xlsx", index=False)


# tables_json = []
# for i, table in enumerate(tables):
#     df = table.df
#     table_data = {
#         "table_number": i + 1,
#         "columns": df.iloc[0].tolist(),        # First row as header
#         "rows": df.iloc[1:].values.tolist()    # Rest as rows
#     }
#     tables_json.append(table_data)
# print(tables_json)

# with open("brachot_pricelist.json", "w", encoding="utf-8") as f:
#     json.dump(tables_json, f, indent=2, ensure_ascii=False)

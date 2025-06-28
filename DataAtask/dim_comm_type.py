import pandas as pd

input_file = r"C:\Users\user\Downloads\raw_data.xlsx"

df = pd.read_excel(input_file, sheet_name='Sheet1')

unique_comm_types = df['comm_type'].unique()

dim_comm_type = pd.DataFrame({
    'comm_type': unique_comm_types,
    'comm_type_id': range(1, len(unique_comm_types) + 1)
})

output_file = r"C:\Users\user\Desktop\Docs\final_data1.xlsx"

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    dim_comm_type.to_excel(writer, sheet_name='dim_comm_type', index=False)


import pandas as pd
import os

input_file = r"C:\Users\user\Downloads\raw_data.xlsx"

df = pd.read_excel(input_file, sheet_name='Sheet1')

unique_subjects = df['subject'].unique()

dim_subject = pd.DataFrame({
    'subject': unique_subjects,
    'subject_id': range(1, len(unique_subjects) + 1)
})

output_file = r"C:\Users\user\Desktop\Docs\final_data1.xlsx"

with pd.ExcelWriter(output_file, engine='openpyxl', mode='a' if os.path.exists(output_file) else 'w') as writer:
    dim_subject.to_excel(writer, sheet_name='dim_subject', index=False)


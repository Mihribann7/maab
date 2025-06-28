import pandas as pd
import os
import json

input_file = r"C:\Users\user\Downloads\raw_data.xlsx"

df = pd.read_excel(input_file, sheet_name='Sheet1')

unique_users = []

for raw_content in df['raw_content']:
    try:
        content = json.loads(raw_content)
        attendees = content.get('meeting_attendees', [])
        for attendee in attendees:
            unique_users.append({
                'name': attendee.get('name'),
                'email': attendee.get('email'),
                'location': attendee.get('location'),
                'displayName': attendee.get('displayName'),
                'phoneNumber': attendee.get('phoneNumber')
            })
    except json.JSONDecodeError:
        print(f"Warning: Could not parse JSON in raw_content: {raw_content[:50]}...")
        continue

users_df = pd.DataFrame(unique_users)
users_df = users_df.drop_duplicates(subset='email', keep='first')

users_df['user_id'] = range(1, len(users_df) + 1)

users_df = users_df[['user_id', 'name', 'email', 'location', 'displayName', 'phoneNumber']]

output_file = r"C:\Users\user\Desktop\Docs\final_data1.xlsx"

with pd.ExcelWriter(output_file, engine='openpyxl', mode='a' if os.path.exists(output_file) else 'w') as writer:
    users_df.to_excel(writer, sheet_name='dim_user', index=False)
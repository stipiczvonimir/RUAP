import pandas as pd

df = pd.read_csv('Dataset salary 2024.csv')

df = df[df['company_location'] == 'US']
df = df[df['work_year'] == 2024]
df = df.drop(columns=['work_year'])
df = df[df['employment_type'] == 'FT']
df = df.drop(columns=['employment_type'])
df = df.drop(columns=['salary', 'employee_residence', 'salary_currency'])
df = df[df['remote_ratio'] == 0]
df = df.drop(columns=['remote_ratio'])

df.to_csv('new_data.csv', index=False)
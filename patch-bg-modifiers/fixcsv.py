import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('newfile.csv')

# Fix Audio_Path column
df['Audio_Path'] = df['Audio_Path'].apply(lambda x: '/' + x[2:] if x.startswith('//') else x)

# Save the DataFrame to a new CSV file
df.to_csv('output_file.csv', index=False)

print("Audio paths fixed and saved to output_file.csv")

import pandas as pd
import sqlite3
import os

def parse_audio_path(audio_path):
    parts = audio_path.split(os.path.sep)
    last_two_folders_and_file = parts[-2:]
    result_path = os.path.join(*last_two_folders_and_file)
    return result_path


# Define the paths to the CSV file and the SQLite database
csv_file_path = 'output_file.csv'
db_file_path = '../data/speech_database.db'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Define the column names
audio_path_col = 'Audio_Path'
modifier_id_col = 'Background_Modifier_ID'

# Open the SQLite3 database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Iterate over the DataFrame and update the database
for index, row in df.iterrows():
    audio_path = parse_audio_path(row[audio_path_col])
    modifier_id = row[modifier_id_col]

    # Update the database where the Audio_Path matches
    cursor.execute("""
    UPDATE Audio_Data
    SET Background_Modifier_ID = ?
    WHERE Audio_Path LIKE ?
    """, (modifier_id, f'%{audio_path}%'))


    print(audio_path)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database updated successfully.")

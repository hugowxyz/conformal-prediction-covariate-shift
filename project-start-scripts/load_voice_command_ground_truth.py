"""
load_voice_command_ground_truth.py
"""

import argparse
import pandas as pd
import sqlite3
import re
from num2words import num2words 


def preprocess_transcription(transcription):
    # Lowercasing
    transcription = transcription.lower()
    
    # Removing special characters and punctuation
    transcription = re.sub(r'[^a-zA-Z0-9\s]', '', transcription)
    
    # Converting numerical digits into text format
    words = transcription.split()
    for i, word in enumerate(words):
        if word.isdigit():
            words[i] = num2words(int(word))
    transcription = ' '.join(words)
    
    # Removing whitespace and extra spaces
    transcription = ' '.join(transcription.split())
    
    return transcription


def main(file_path, db_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)
    df.drop(columns=["Unnamed: 0"], inplace=True)
    df.rename(
        columns={
            "sentence": "Sentence",
            "intent": "Intent",
            "other info extracted": "Other_Info",
        },
        inplace=True,
    )

    df["Audio_Info_ID"] = range(50)
    df["Sentence"] = df["Sentence"].apply(preprocess_transcription)

    # Connect to SQLite database
    conn = sqlite3.connect(db_path)

    # Write DataFrame to SQLite database
    df.to_sql("Audio_Info", conn, if_exists="append", index=False)

    # Close the connection
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process Excel file and write to SQLite database."
    )
    parser.add_argument(
        "--file_path",
        default="../HMI_questions_and_intents.xlsx",
        help="Path to the Excel file.",
    )
    parser.add_argument(
        "--db_path",
        default="../data/speech_database.db",
        help="Path to the SQLite database file.",
    )

    args = parser.parse_args()

    main(args.file_path, args.db_path)

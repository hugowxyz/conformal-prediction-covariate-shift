"""
load_sqlite_db.py
"""

import os
import sqlite3
import re
import argparse


def load_dataset(root_folder):
    folders = os.listdir(root_folder)
    dataset = []

    for folder in folders:
        folder_path = os.path.join(root_folder, folder)
        files = os.listdir(folder_path)
        files = [os.path.join(folder_path, file) for file in files]
        dataset += files

    return dataset


def split_all_folders(file_path):
    folders = []
    while True:
        file_path, folder = os.path.split(file_path)
        if folder != "":
            folders.insert(0, folder)
        else:
            if file_path != "":
                folders.insert(0, file_path)
            break
    return folders


def extract_audio_number(filename):
    # Define a regular expression pattern to match the audio number
    pattern = r"audio(\d+)(?:-.*)?.webm"
    match = re.match(pattern, filename)
    if match:
        return match.group(1)
    else:
        return None


def main(voice_data_path, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    insert_sql = "INSERT INTO Audio_Data (Audio_Path, Audio_Info_ID, Speaker_ID, Background_Modifier_ID) VALUES (?, ?, ?, ?)"
    data_paths = load_dataset(voice_data_path)

    data = []
    for data_path in data_paths:
        abs_path = os.path.abspath(data_path)
        split_path = split_all_folders(abs_path)
        speaker_id = split_path[-2]
        audio_number = int(extract_audio_number(split_path[-1]))
        data.append((abs_path, audio_number, speaker_id, 0))

    cursor.executemany(insert_sql, data)
    conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process voice data and insert into a database."
    )
    parser.add_argument(
        "--voice_data_path",
        type=str,
        default="../2023-12-04-HMI-dataset",
        help="Path to voice data directory.",
    )
    parser.add_argument(
        "--db_path", type=str, default="../data/speech_database.db", help="Path to the SQLite database file."
    )
    args = parser.parse_args()

    main(args.voice_data_path, args.db_path)

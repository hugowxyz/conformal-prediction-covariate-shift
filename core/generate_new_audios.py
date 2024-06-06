"""
generate_new_audios.py
"""

import os
from pydub import AudioSegment
from db import execute_query
from util import split_all_folders
import uuid
import random
import argparse


def main(background_noise_path, background_noise_id, db_file):
    background_noise = AudioSegment.from_file(background_noise_path)
    background_noise += 10

    query = """
    SELECT Audio_ID, Audio_Path, Audio_Info_ID, Speaker_ID, Background_Modifier_ID 
    FROM Audio_Data
    WHERE Background_Modifier_ID = 0 
    ORDER BY Audio_Info_ID"""
    rows = execute_query(query, db_file=db_file)

    insert_query = """
    INSERT INTO Audio_Data (Audio_Path, Audio_Info_ID, Speaker_ID, Background_Modifier_ID)
    VALUES (?, ?, ?, ?)
    """

    for row in rows:
        file_path = row[1]
        main_audio = AudioSegment.from_file(file_path)
        main_audio_length = len(main_audio)

        max_start_time = len(background_noise) - main_audio_length
        if max_start_time < 0:
            print("MAIN AUDIO LONGER THAN BACKGROUND AUDIO")
            assert 0 == 1

        start_time = random.randint(0, max_start_time)

        # Compute the path of the output file
        output_file_name = f"{str(uuid.uuid4())}-{start_time}.webm"
        split_path = split_all_folders(file_path)
        output_audio_path = os.path.join("/".join(split_path[:-1]), output_file_name)

        # Create the output file
        background_audio = background_noise[start_time:]
        final_audio = main_audio.overlay(background_audio)
        final_audio.export(output_audio_path, format="webm")
        print(f"Exported {output_audio_path}")

        params = (
            output_audio_path,
            row[2],
            row[3],
            background_noise_id,
        )
        execute_query(insert_query, params, db_file=db_file)

    print("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process command line arguments")
    parser.add_argument(
        "background_noise_path",
        type=str,
        help="Path to the background noise audio file",
    )

    parser.add_argument(
        "background_noise_id",
        type=str,
        help="ID of the background noise type",
    )

    parser.add_argument(
        "--db_file",
        default="../data/speech_database.db",
        type=str,
        help="ID of the background noise type",
    )

    args = parser.parse_args()
    main(args.background_noise_path, args.background_noise_id, args.db_file)

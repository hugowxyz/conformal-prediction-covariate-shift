"""
get_new_audios.py
"""

from db import execute_query


def get_new_audios(db_file=None):
    query = """
    SELECT Audio_Data.*
    FROM Audio_Data
    LEFT JOIN Audio_Predictions ON Audio_Data.Audio_ID = Audio_Predictions.Audio_ID
    WHERE Audio_Predictions.Audio_ID IS NULL;"""
    return execute_query(query, db_file=db_file)

"""
compute_wer.py
"""

import jiwer
from db import execute_query

if __name__ == "__main__":
    query = """
    SELECT Audio_Id, Prediction_ID, Prediction, Sentence
    FROM Audio_Data 
    NATURAL JOIN Audio_Predictions
    NATURAL JOIN Audio_Info 
    WHERE Word_Error_Rate IS NULL;
    """

    rows = execute_query(query)

    for row in rows:
        prediction_id = row[1]
        prediction = row[2]
        sentence = row[3]
        wer = jiwer.wer(sentence, prediction)

        update_query = f"""
        UPDATE Audio_Predictions 
        SET Word_Error_Rate = {wer}
        WHERE Prediction_ID={prediction_id} 
        """

        execute_query(update_query)

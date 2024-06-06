"""
compute_predictions.py
"""

from datetime import datetime
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import numpy as np
import librosa

import argparse

from db import execute_query
from get_new_audios import get_new_audios

import re
from num2words import num2words


INSERT_QUERY = """
INSERT INTO Audio_Predictions (Audio_ID, Prediction, Confidence_Score) VALUES (?, ?, ?)
"""

processor = WhisperProcessor.from_pretrained("openai/whisper-tiny.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny.en")


def softmax(x):
    """Compute the softmax function."""
    exp_x = np.exp(x - np.max(x))
    return exp_x / np.sum(exp_x)


def extract_audio_features(audio_file_path):
    audio_sample, sampling_rate = librosa.load(audio_file_path, sr=None)

    target_sampling_rate = 16000
    waveform = librosa.resample(
        audio_sample, orig_sr=sampling_rate, target_sr=target_sampling_rate
    )

    input_features = processor(
        waveform, sampling_rate=target_sampling_rate, return_tensors="pt"
    ).input_features

    return input_features


def compute_predictions(
    audio_file_path, num_return_sentences=50, timeout=10, quiet=False
):
    """
    Compute predictions for transcriptions of an audio file.

    This function takes an audio file path and extracts features from it.
    Then, it generates transcriptions using a pre-trained model and decodes
    the predictions to text. The transcriptions along with their confidence
    scores are stored in a database. Optionally, it can print progress
    messages during execution based on the 'quiet' parameter.

    Parameters:
    - audio_file_path: Path to the audio file.
    - num_return_sentences (int): Number of transcriptions to generate. Default is 50.
    - timeout (int): Maximum time allowed for generation in seconds. Default is 10.
    - quiet (bool): If True, suppress printing progress messages. Default is False.
    """
    input_features = extract_audio_features(audio_file_path)

    predicted_ids = model.generate(
        input_features,
        num_beams=num_return_sentences,
        output_scores=True,
        num_return_sequences=num_return_sentences,
        return_dict_in_generate=True,
        max_time=timeout,
    )

    transcriptions = processor.batch_decode(
        predicted_ids["sequences"], skip_special_tokens=True
    )
    scores = predicted_ids.sequences_scores.to("cpu")
    return transcriptions, scores


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


def remove_duplicate_transcriptions(data):
    """
    Processes a list of tuples (text, confidence) and returns a list of unique texts
    with the highest confidence scores, sorted in descending order of confidence.

    Args:
    data (list of tuples): List of tuples where each tuple contains (text, confidence).

    Returns:
    list of tuples: List of unique texts with their highest confidence scores, sorted
                    by confidence in descending order.
    """
    # Create a dictionary to store unique texts and their corresponding confidence scores
    unique_texts = {}

    # Parse each tuple and store unique texts with the highest confidence score
    for audio_id, text, confidence in data:
        # Only add to dictionary if the text is not already present
        if text not in unique_texts:
            unique_texts[text] = (audio_id, confidence)
        else:
            # Update confidence score if the new one is higher
            if confidence > unique_texts[text][1]:
                unique_texts[text] = (audio_id, confidence)

    # Convert the dictionary back to a list of tuples
    unique_data = [(audio_id, text, confidence) for text, (audio_id, confidence) in unique_texts.items()]

    # Sort the unique_data list in descending order of confidence score
    unique_data.sort(key=lambda x: x[2], reverse=True)

    return unique_data


def main(db_file, quiet):
    new_audios = get_new_audios(db_file)

    for row in new_audios:
        audio_id = row[0]
        audio_file_path = row[1]
        transcriptions, scores = compute_predictions(audio_file_path, quiet=quiet)
        processed_transcriptions = []
        for idx, transcription in enumerate(transcriptions):
            score = float(scores[idx])
            transcription = preprocess_transcription(transcription)
            params = (audio_id, transcription, score)
            processed_transcriptions.append(params)

        processed_transcriptions = remove_duplicate_transcriptions(processed_transcriptions)
        scores = softmax(np.array([x[2] for x in processed_transcriptions]))
        processed_transcriptions = [(audio_id, transcription, scores[idx]) for idx, (audio_id, transcription, score) in enumerate(processed_transcriptions)]
        for transcription in processed_transcriptions:
            execute_query(INSERT_QUERY, transcription, db_file=db_file)

        if not quiet:
            print("Wrote", params, "to DB.")

        if not quiet:
            print(
                f"[{datetime.now().isoformat()}] Finished prediction for",
                (audio_id, audio_file_path),
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process command line arguments")
    parser.add_argument("--db_file", default="../data/speech_database.db", type=str, help="Path to the database file")
    parser.add_argument("--quiet", action="store_true", help="Enable quiet mode")

    args = parser.parse_args()
    main(args.db_file, args.quiet)

    if not args.quiet:
        print("Done!")

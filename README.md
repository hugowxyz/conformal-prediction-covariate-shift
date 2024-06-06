# Project Setup Instructions

When you first open the project, you need to create the SQLite database that contains all of the metadata used for the audio files. You can do this by following these steps:

## Step 1: Set Up the Conda Environment
1. **Create and activate the conda environment**:
    ```bash
    conda env create -f environment.yml
    conda activate cp-snips
    ```

## Step 2: Create the SQLite Database
1. **Enter the `data` folder**:
    ```bash
    cd data
    ```
2. **Create a database in the `data` folder**:
    ```bash
    sqlite3 speech_database.db
    ```
3. **Run the SQL script to create tables**:
    ```sql
    .read create_tables.sql
    ```
4. **Insert speaker information**:
    ```sql
    .read insert_speakers.sql
    ```
5. **Insert data into Background Modifiers and Background Types as needed**.

## Step 3: Populate the Audio Data Folder
1. **Enter the `project-start-scripts` folder**:
    ```bash
    cd project-start-scripts
    ```
2. **Load all the metadata into the database**:
    ```base
    python3 main.py
    ```

CREATE TABLE IF NOT EXISTS Audio_Data (
    Audio_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Audio_Path TEXT,
    Audio_Info_ID INTEGER,
    Speaker_ID TEXT,
    Background_Modifier_ID INT,
    FOREIGN KEY(Audio_Info_ID) REFERENCES Audios(Audio_Info_ID)
    FOREIGN KEY(Speaker_ID) REFERENCES Speakers(Speaker_ID)
    FOREIGN KEY(Background_Modifier_ID) REFERENCES Background_Modifiers(Background_Modifier_ID)
);

CREATE TABLE IF NOT EXISTS Audio_Predictions (
    Prediction_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Audio_ID INTEGER,
    Prediction TEXT,
    Confidence_Score REAL,
    Word_Error_Rate REAL,
    FOREIGN KEY(AUDIO_ID) REFERENCES Audio_Data(Audio_ID)
);

CREATE TABLE IF NOT EXISTS Background_Modifiers (
    Background_Modifier_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Background_Type_ID INTEGER,
    Audio_Amplification INTEGER,
    FOREIGN KEY(Background_Type_ID) REFERENCES Background_Types(Background_Type_ID)
);

CREATE TABLE IF NOT EXISTS Background_Types (
    Background_Type_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Description TEXT
);


CREATE TABLE IF NOT EXISTS Speakers (
    Speaker_ID TEXT PRIMARY KEY,
    Description TEXT
);

CREATE TABLE IF NOT EXISTS Audio_Info (
    Audio_Info_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Sentence TEXT,
    Intent TEXT,
    Other_Info TEXT
);


CREATE TABLE IF NOT EXISTS Featurized_Data (
    Featurized_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    FeatureSet_ID INTEGER,
    Audio_ID INTEGER,
    Feature_ID INTEGER,
    FOREIGN KEY(Audio_ID) REFERENCES Raw_Data(Audio_ID),
    FOREIGN KEY(Feature_ID) REFERENCES Features(Feature_ID)
);

CREATE TABLE IF NOT EXISTS Features (
    Feature_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Description TEXT
);
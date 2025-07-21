import sys
from src.exception import CustomException
from src.logger import logging
from src.utils import load_obj
import pandas as pd

class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self,features):
        try:
            model_path = 'artifact/model.pkl'
            preprocessor_path = 'artifact/preprocessor.pkl'
            model = load_obj(file_path = model_path) 
            preprocessor = load_obj(file_path = preprocessor_path)
            data_scaled = preprocessor.transform(features)
            prediction_data = model.predict(data_scaled)
            return prediction_data
        except Exception as e:
            raise CustomException(e,sys)

class Customdata:
    def __init__(self,
                 gender:str,
                 race_ethnicity:str,
                 parental_level_of_education:str,
                 lunch:str,
                 test_preparation_course:str,
                 reading_score:int,
                 writing_score:int
                 ):
        self.gender = gender or "male"
        self.race_ethnicity = race_ethnicity or "group A"  # ✅ Fix here
        self.parental_level_of_education = parental_level_of_education or "some high school"
        self.lunch = lunch or "standard"
        self.test_preparation_course = test_preparation_course or "none"
        self.reading_score = reading_score
        self.writing_score = writing_score
        
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                'gender': [self.gender],
                'race_ethnicity': [self.race_ethnicity],
                'parental_level_of_education': [self.parental_level_of_education],
                'lunch': [self.lunch],
                'test_preparation_course': [self.test_preparation_course],
                'reading_score': [self.reading_score],
                'writing_score': [self.writing_score]
            }
            return pd.DataFrame(custom_data_input_dict)  # ✅ Fix here
        except Exception as e:
            raise CustomException(e, sys)

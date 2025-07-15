import sys  # For accessing system-specific parameters and exceptions
from dataclasses import dataclass  # To create a simple configuration class with default values

import numpy as np  # For numerical operations, especially arrays
import pandas as pd  # For reading and handling tabular data (CSV files)
from sklearn.compose import ColumnTransformer  # To apply different preprocessing to specific columns
from sklearn.impute import SimpleImputer  # For handling missing values in the dataset
from sklearn.pipeline import Pipeline  # To bundle preprocessing steps
from sklearn.preprocessing import OneHotEncoder,StandardScaler  # For encoding categorical and scaling numerical data
from src.utils import save_obj  # Custom utility function to save Python objects (like preprocessor) to file

from src.exception import CustomException  # Custom exception class for better error messages
from src.logger import logging  # Custom logging setup to track process steps
import os  # For interacting with the operating system (paths, directories)

@dataclass  # Automatically creates init, repr, etc. for the class
class DataTransformationConfig:  # Configuration class for data transformation
    preprocessor_obj_file_path = os.path.join('artifact','preprocessor.pkl')  # Path to save the preprocessor object as .pkl

class DataTransformation:  # Main class for handling transformation of dataset
    def __init__(self):  # Constructor method
         self.data_transformation_config = DataTransformationConfig()  # Initialize config with default values

    def get_transfer_object(self):  # Method to create and return preprocessing object (pipeline)
        try:  # Try block to catch any runtime errors
           
            num_features =[  # Numerical columns to be scaled
                'reading_score',
                'writing_score'
            ]
            cata_features=[  # Categorical columns to be encoded
                'gender',
                'race_ethnicity'
                ,'parental_level_of_education'
                ,'lunch',
                'test_preparation_course'    
            ]

            num_pipeline = Pipeline(  # Define a pipeline for numerical features
                steps=[
                    ("impute",SimpleImputer(strategy='median')),  # Handle missing values using median
                    ("scaler",StandardScaler()),  # Normalize numerical values (mean=0, std=1)
                ]
            )

            cata_pipline = Pipeline(  # Define a pipeline for categorical features
                steps=[
                    ('impute',SimpleImputer(strategy='most_frequent')),  # Fill missing values with most frequent
                    ("one_hot_encoder",OneHotEncoder()),  # Convert categories into binary columns
                    ('scaler',StandardScaler(with_mean=False))  # Scale binary columns without centering (to avoid sparse matrix error)
                ]
            )

            logging.info('numerical column Standared scaling is complete!')  # Log successful numerical preprocessing
            logging.info('catagorical column encoding  is complete!')  # Log successful categorical preprocessing
            preprocessor = ColumnTransformer(  # Combine numerical and categorical pipelines
                [
                    ('num_pipeline',num_pipeline,num_features),  # Apply numerical pipeline to numerical columns
                    ('cat_pipelines',cata_pipline,cata_features)  # Apply categorical pipeline to categorical columns
                ]
            )

            return preprocessor  # Return the complete preprocessor object

        except Exception as e:  # Handle errors
            raise CustomException(e,sys)  # Raise custom error with traceback

    def initiate_data_transformation(self,train_path,test_path):  # Main method to transform train and test datasets
        try:
            train_df = pd.read_csv(train_path)  # Read training dataset
            test_df = pd.read_csv(test_path)  # Read test dataset

            logging.info("Read train and test data completed")  # Log successful reading

            logging.info("obtaining Preprocessing Object.")  # Log before fetching preprocessor

            preprocessing_obj= self.get_transfer_object()  # Get preprocessor pipeline

            target_column_name = "math_score"  # Name of the target variable (label)
            num_columns =[  # Re-declare numeric columns
                'reading_score',
                'writing_score'
            ]

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)  # X_train: drop target column
            target_feature_train_df = train_df[target_column_name]  # y_train: keep only target column

            input_feature_test_df= test_df.drop(columns=[target_column_name],axis=1)  # X_test: drop target column
            target_feature_test_df = test_df[target_column_name]  # y_test: keep only target column

            logging.info(f'applying preprocessing object on training and testing dataframe.')  # Log before transforming

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)  # Fit + transform X_train
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)  # Transform X_test

            train_arr = np.c_[  # Concatenate transformed X_train and y_train
                input_feature_train_arr,np.array(target_feature_train_df)
            ]
            test_arr = np.c_[  # Concatenate transformed X_test and y_test
                input_feature_test_arr,np.array(target_feature_test_df)
            ]
            logging.info('saved preprocessing obj.')  # Log before saving object

            save_obj (  # Save the preprocessing object to file

                file_path=self.data_transformation_config.preprocessor_obj_file_path, # File path to save
                obj = preprocessing_obj  # Preprocessor object
            )
            
            return (  # Return train array, test array, and preprocessor file path
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:  # Catch block
            raise CustomException(e,sys)  # Raise custom exception with system info

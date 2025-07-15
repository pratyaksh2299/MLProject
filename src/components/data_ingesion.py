import os  # for interacting with the operating system (file paths, folders)
import sys  # for accessing system-specific parameters (used in exception handling)
from src.exception import CustomException  # importing custom exception class from your project
from src.logger import logging  # importing logging functionality to log messages
import pandas as pd  # for data handling and manipulation (especially CSV files)

from sklearn.model_selection import train_test_split  # to split dataset into train and test parts
from dataclasses import dataclass  # used to create simple data classes for configuration
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainer,ModelTrainingConfig

@dataclass  # decorator to automatically generate init and repr methods
class DataIngestionConfig:
    train_data_path :str = os.path.join('artifact',"train.csv")  # path to save training data
    test_data_path : str = os.path.join('artifact',"test.csv")  # path to save testing data
    raw_data_path : str = os.path.join('artifact',"data.csv")  # path to save raw (original) data

class DataIngestion:  # main class to handle data ingestion tasks
    def __init__(self):  # constructor to initialize config
        self.ingestion_config = DataIngestionConfig()  # creating config instance with file paths

    def initiate_data_ingestion(self):  # method to start data ingestion process
        logging.info("Entered the data ingestion method or components")  # log entry to track start
        try:
            df = pd.read_csv('notebook\data\stud.csv')  # read input dataset from the given path
            logging.info('Read the dataset as dataframe.')  # log successful reading of data

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)  # create artifact folder if it doesn't exist
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)  # save raw data to artifact folder

            logging.info('Train test split is Initiated.')  # log start of train-test split
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)  # split data: 80% train, 20% test
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)  # save training data
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)  # save testing data
            return (  # return paths of saved train and test data
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            
        except  Exception as e:  # handle any exception that occurs during the process
            raise CustomException(e,sys)  # raise custom exception with original error and system info

if __name__ == '__main__':  
    obj = DataIngestion()  # create an object of the DataIngestion class
    train_data,test_data  =  obj.initiate_data_ingestion()  # call the ingestion method to execute the workflow

    data_transformation = DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr,test_arr))

import json
import os
import sys,pandas as pd
from pandas import DataFrame
from src.utils.main_utils import read_yaml_file
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataValidationConfig
from src.constants import SCHEMA_FILE_PATH

class DataValidation:
    def __init__(self,di_artifact:DataIngestionArtifact,dv_config:DataValidationConfig):
        self.di_artifact=di_artifact
        self.dv_config=dv_config
        self._schema_config=read_yaml_file(file_path=SCHEMA_FILE_PATH)
    def validate_number_of_columns(self,df:DataFrame)->bool:
        status=len(df.columns)==len(self._schema_config["columns"])
        return status
    def does_column_exist(self,df:DataFrame)->bool:
        dataframe_columns = df.columns
        missing_numerical_columns = []
        missing_categorical_columns = []
        for column in self._schema_config["numerical_columns"]:
            if column not in dataframe_columns:
                missing_numerical_columns.append(column)

            

        for column in self._schema_config["categorical_columns"]:
            if column not in dataframe_columns:
                missing_categorical_columns.append(column)

            

        return False if len(missing_categorical_columns)>0 or len(missing_numerical_columns)>0 else True
    
    @staticmethod
    def read_data(file_path)->DataFrame:
        return pd.read_csv(file_path)
    
    def initiate_data_validation(self)->DataValidationArtifact:
        validation_error_message=""
        train_df, test_df = (DataValidation.read_data(file_path=self.di_artifact.trained_file_path),
                                 DataValidation.read_data(file_path=self.di_artifact.test_file_path))

        status=self.validate_number_of_columns(df=train_df)
        if not status:
            validation_error_message+=f"columns missing in train dataframe"
        status=self.validate_number_of_columns(df=test_df)
        if not status:
            validation_error_message+=f"columns missing in test dataframe"
        status=self.does_column_exist(df=train_df)
        if not status:
            validation_error_message+=f"columns missing in train dataframe"
        status=self.does_column_exist(df=test_df)
        if not status:
            validation_error_message+=f"columns missing in test dataframe"
        validation_status=len(validation_error_message)==0
        dv_artifact=DataValidationArtifact(
            validation_status=validation_status,
            message=validation_error_message,
            validation_report_file_path=self.dv_config.validation_report_file
        )
        report_dir=os.path.dirname(self.dv_config.validation_report_file)
        os.makedirs(report_dir,exist_ok=True)
        validation_report = {
            "validation_status": validation_status,
            "message": validation_error_message.strip()
            }
        with open(self.dv_config.validation_report_file,'w') as report_file:
            json.dump(validation_report,report_file,indent=4)
        return dv_artifact


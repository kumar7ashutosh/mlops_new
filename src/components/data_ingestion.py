import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.data_access.proj1_data import Proj1Data

class DataIngestion:
    def __init__(self,di_config:DataIngestionConfig=DataIngestionConfig()):
        self.di_config=di_config
    def export_data_into_feature_store(self)->DataFrame:
        my_data=Proj1Data()
        df=my_data.export_collection_as_dataframe(collection_name=self.di_config.collection_name)
        feature_store_file_path  = self.di_config.feature_store_file_path
        os.makedirs(os.path.dirname(feature_store_file_path),exist_ok=True)
        df.to_csv(feature_store_file_path,index=False,header=True)
        return df
    def split_data(self,df:DataFrame)->None:
        train_set,test_set=train_test_split(df,test_size=self.di_config.train_test_split_ratio)
        os.makedirs(os.path.dirname(self.di_config.training_file_path),exist_ok=True)
        train_set.to_csv(self.di_config.training_file_path,index=False,header=True)
        test_set.to_csv(self.di_config.testing_file_path,index=False,header=True)
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        df=self.export_data_into_feature_store()
        self.split_data(df)
        di_artifact=DataIngestionArtifact(trained_file_path=self.di_config.training_file_path,test_file_path=self.di_config.testing_file_path)
        return di_artifact
    
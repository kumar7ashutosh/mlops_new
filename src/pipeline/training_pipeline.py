import sys
from src.exception import VehicleException
from src.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.entity.config_entity import DataIngestionConfig,DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

class TrainPipeline:
    def __init__(self):
        self.di_config=DataIngestionConfig()
        self.dv_config=DataValidationConfig()
        
        
    def start_data_ingestion(Self)->DataIngestionArtifact:
        data_ingestion=DataIngestion(di_config=Self.di_config)
        di_artifact=data_ingestion.initiate_data_ingestion()
        return di_artifact
    
    def start_data_validation(self,di_artifact:DataIngestionArtifact)->DataValidationArtifact:
        data_validation=DataValidation(di_artifact=di_artifact,dv_config=self.dv_config)
        dv_artifact=data_validation.initiate_data_validation()
        return dv_artifact
    def run_pipeline(self,)->None:
        di_artifact=self.start_data_ingestion()
        dv_artifact=self.start_data_validation(di_artifact=di_artifact)
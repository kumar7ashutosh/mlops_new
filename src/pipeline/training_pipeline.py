import sys
from src.exception import VehicleException
from src.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

class TrainPipeline:
    def __init__(self):
        self.di_config=DataIngestionConfig()
        self.dv_config=DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
    def start_data_ingestion(Self)->DataIngestionArtifact:
        data_ingestion=DataIngestion(di_config=Self.di_config)
        di_artifact=data_ingestion.initiate_data_ingestion()
        return di_artifact
    
    def start_data_validation(self,di_artifact:DataIngestionArtifact)->DataValidationArtifact:
        data_validation=DataValidation(di_artifact=di_artifact,dv_config=self.dv_config)
        dv_artifact=data_validation.initiate_data_validation()
        return dv_artifact
    
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data transformation component
        """
        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                     data_transformation_config=self.data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise VehicleException(e, sys)
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        """
        This method of TrainPipeline class is responsible for starting model training
        """
        try:
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=self.model_trainer_config
                                         )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise VehicleException(e, sys)

    def run_pipeline(self,)->None:
        di_artifact=self.start_data_ingestion()
        dv_artifact=self.start_data_validation(di_artifact=di_artifact)
        data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=di_artifact, data_validation_artifact=dv_artifact)
        model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
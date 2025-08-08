import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
DATABASE_NAME = "Proj1"
COLLECTION_NAME = "Proj1-Data"
MONGODB_URL_KEY = 'mongodb_URL'
DATA_INGESTION_COLLECTION_NAME: str = "Proj1-Data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.25
PIPELINE_NAME: str = ""
ARTIFACT_DIR: str = "artifact"
TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
FILE_NAME: str = "data.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME: str = "report.yaml"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
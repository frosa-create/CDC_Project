from cnnClassifier import logger
from cnnClassifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from cnnClassifier.pipeline.stage_02_prepare_base_model import PrepareBaseModelTrainingPipeline
from cnnClassifier.validation.stage_01_validate_and_sort import sort_chicken_fecal_images
from cnnClassifier.pipeline.stage_03_training import ModelTrainingPipeline
STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e

raw_dir = '/Users/ryanrosa/Downloads/AI_DS_Project_Repos/CDC_Project/artifacts/data_ingestion/data/Chicken_Fecal_Images'
sorted_dir = '/Users/ryanrosa/Downloads/AI_DS_Project_Repos/CDC_Project/artifacts/data_ingestion/data/Chicken_Fecal_Images_Sorted'
valid_labels = ['salmo', 'cocci', 'healthy']

def main():
    try:
        sort_chicken_fecal_images(raw_dir, sorted_dir, valid_labels)
    except Exception as e:
        print(f"❌ Error during data sorting: {e}")

if __name__ == "__main__":
    main()


STAGE_NAME = "Prepare base model"
try:
    logger.info(f"********************")
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    prepare_base_model = PrepareBaseModelTrainingPipeline()
    prepare_base_model.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e



STAGE_NAME = "Training"
try:
    logger.info(f"******************")
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<")
    model_trainer = ModelTrainingPipeline()
    model_trainer.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e


import os
import shutil
import re
from pathlib import Path
from cnnClassifier.entity.config_entity import DataValidationConfig
from cnnClassifier import logger


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_files(self) -> bool:
        try:
            validation_status = None


            if not os.path.exists(self.config.raw_data_dir):
                logger.error(f"Raw data directory does not exist: {self.config.raw_data_dir}")
                validation_status = False
            else:

                image_files = [f for f in os.listdir(self.config.raw_data_dir)
                               if f.lower().endswith(tuple(self.config.valid_extensions))]

                if len(image_files) == 0:
                    logger.error("No valid image files found in raw data directory")
                    validation_status = False
                else:
                    logger.info(f"Found {len(image_files)} image files in raw data directory")
                    validation_status = True


            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            logger.error(f"Error during file validation: {e}")
            raise e

    def sort_and_organize_data(self):
        try:

            os.makedirs(self.config.sorted_data_dir, exist_ok=True)


            for label in self.config.valid_labels:
                label_dir = os.path.join(self.config.sorted_data_dir, label)
                os.makedirs(label_dir, exist_ok=True)
                logger.info(f"Created directory: {label_dir}")

            missing_labels = []
            processed = 0
            skipped_files = []


            for filename in os.listdir(self.config.raw_data_dir):
                if not filename.lower().endswith(tuple(self.config.valid_extensions)):
                    logger.warning(f"Skipping non-image file: {filename}")
                    skipped_files.append(filename)
                    continue

                filepath = os.path.join(self.config.raw_data_dir, filename)


                match = re.match(r'^([a-zA-Z]+)[._-]', filename)
                label = match.group(1).lower() if match else ''


                if label not in self.config.valid_labels:
                    logger.warning(f"Unrecognized label: {label} from filename: {filename}")
                    missing_labels.append(filename)
                    continue


                dest_path = os.path.join(self.config.sorted_data_dir, label, filename)
                logger.info(f"Copying: {filepath} --> {dest_path}")
                shutil.copy2(filepath, dest_path)
                processed += 1


            logger.info(f"✅ Finished sorting {processed} image(s).")

            if skipped_files:
                logger.warning(f"⚠️ Skipped {len(skipped_files)} non-image file(s)")

            if missing_labels:
                logger.warning(f"⚠️ Skipped {len(missing_labels)} image(s) with unknown labels:")
                for f in missing_labels[:10]:
                    logger.warning(f"  - {f}")
                if len(missing_labels) > 10:
                    logger.warning(f"  ... and {len(missing_labels) - 10} more files")

            return True

        except Exception as e:
            logger.error(f"Error during data sorting: {e}")
            raise e

    def validate_sorted_data(self):
        try:
            validation_results = {}
            total_files = 0

            for label in self.config.valid_labels:
                label_dir = os.path.join(self.config.sorted_data_dir, label)

                if not os.path.exists(label_dir):
                    logger.error(f"Label directory does not exist: {label_dir}")
                    validation_results[label] = 0
                    continue


                files = [f for f in os.listdir(label_dir)
                         if f.lower().endswith(tuple(self.config.valid_extensions))]
                file_count = len(files)
                validation_results[label] = file_count
                total_files += file_count

                logger.info(f"Class '{label}': {file_count} files")


                if file_count < self.config.min_files_per_class:
                    logger.warning(f"Class '{label}' has only {file_count} files, "
                                   f"minimum required: {self.config.min_files_per_class}")

            logger.info(f"Total files organized: {total_files}")
            logger.info("Data validation completed successfully!")

            return validation_results

        except Exception as e:
            logger.error(f"Error during sorted data validation: {e}")
            raise e
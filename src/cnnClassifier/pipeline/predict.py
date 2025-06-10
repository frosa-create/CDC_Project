import numpy as np
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image
import os


class PredictionPipeline:
    def __init__(self, filenames):
        if isinstance(filenames, str):
            self.filenames = [filenames]
        else:
            self.filenames = filenames

        # Get the project root directory (go up 3 levels from current script location)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, "..", "..", "..")
        project_root = os.path.abspath(project_root)

        model_path = os.path.join(project_root, "artifacts", "training", "model.h5")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}. Please train your model first.")

        self.model = load_model(model_path)
        print("Model loaded successfully!")

        print("\n" + "=" * 50)
        print("MODEL DEBUG INFO:")
        print("=" * 50)
        print("Model input shape:", self.model.input_shape)
        print("Model output shape:", self.model.output_shape)
        print("Number of classes:", self.model.output_shape[-1])
        print("=" * 50)

    def predict_single(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Image file not found: {filename}")

        # Load and preprocess image
        test_image = image.load_img(filename, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)

        # Normalize the image (as done during training)
        test_image = test_image / 255.0

        # Get predictions
        raw_predictions = self.model.predict(test_image, verbose=0)
        predicted_class = np.argmax(raw_predictions, axis=1)[0]
        confidence = raw_predictions[0][predicted_class]

        # Map class indices to class names
        class_names = ['Cocci', 'Healthy', 'Salmo']
        prediction = class_names[predicted_class]

        return {
            "image": os.path.basename(filename),
            "prediction": prediction,
            "confidence": float(confidence),
            "all_probabilities": raw_predictions[0].tolist()
        }

    def predict_all(self):
        results = []
        for i, filename in enumerate(self.filenames):
            try:
                result = self.predict_single(filename)
                results.append(result)
                print(f"[{i + 1}/{len(self.filenames)}] {result['image']}: {result['prediction']}")
            except Exception as e:
                print(f"Error with {filename}: {e}")

        return results

    def predict(self):
        return self.predict_all()

def check_prerequisites():
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, "..", "..", "..")
    project_root = os.path.abspath(project_root)

    print(f"Current script directory: {current_dir}")
    print(f"Project root directory: {project_root}")
    print(f"Contents of project root: {os.listdir(project_root)}")

    artifacts_path = os.path.join(project_root, "artifacts")
    training_path = os.path.join(project_root, "artifacts", "training")
    model_path = os.path.join(project_root, "artifacts", "training", "model.h5")

    print("Checking Prerequisites")
    print(f"Looking for artifacts directory at: {artifacts_path}")

    if not os.path.exists(artifacts_path):
        print("Artifacts directory not found in project root")
        return False

    print(f"✓ Artifacts directory found at: {artifacts_path}")

    if not os.path.exists(training_path):
        print(f"'artifacts/training' directory not found at: {training_path}")
        if os.path.exists(artifacts_path):
            print(f"Contents of artifacts directory: {os.listdir(artifacts_path)}")
        return False

    print(f"✓ Training directory found at: {training_path}")

    if not os.path.exists(model_path):
        print(f"Model file not found at: {model_path}")
        print("   You need to train your model first!")
        if os.path.exists(training_path):
            print(f"Contents of training directory: {os.listdir(training_path)}")
        return False

    print(f"✓ Model file found at: {model_path}")
    print("All prerequisites met!")
    return True


def get_image_files_from_folder(folder_path, extensions=(".jpg",".jpeg",".png")):
    image_files = []
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            if file.lower().endswith(extensions):
                image_files.append(os.path.join(folder_path, file))
    return image_files

def get_images_from_multiple_folders(folder_paths, extensions=(".jpg",".jpeg",".png")):
    all_images=[]
    for folder_path in folder_paths:
        all_images.extend(get_image_files_from_folder(folder_path, extensions))
    return all_images


if __name__ == "__main__":
    print("Starting predictions...")

    if not check_prerequisites():
        print("Prerequisites not met. Please ensure model is trained and files exist.")
        exit(1)

    # Get project root for image paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, "..", "..", "..")
    project_root = os.path.abspath(project_root)

    image_paths = get_images_from_multiple_folders([
        os.path.join(project_root, 'artifacts/data_ingestion/data/Chicken_Fecal_Images_Sorted/cocci'),
        os.path.join(project_root, 'artifacts/data_ingestion/data/Chicken_Fecal_Images_Sorted/healthy'),
        os.path.join(project_root, 'artifacts/data_ingestion/data/Chicken_Fecal_Images_Sorted/salmo')
    ])

    if not image_paths:
        print('No image files found, please check your paths')
        exit(1)

    print(f"Found {len(image_paths)} images to process")

    try:
        pipeline = PredictionPipeline(image_paths)
        results = pipeline.predict()

        print("\n" + "=" * 50)
        print("FINAL RESULTS SUMMARY:")
        print("=" * 50)

        category_counts = {'Cocci': 0, 'Healthy': 0, 'Salmo': 0}
        folder_accuracy = {'cocci': {'correct': 0, 'total': 0},
                           'healthy': {'correct': 0, 'total': 0},
                           'salmo': {'correct': 0, 'total': 0}}

        for result in results:
            predicted = result['prediction']
            category_counts[predicted] += 1

            # Check accuracy by comparing with folder name
            image_path = next((path for path in image_paths if os.path.basename(path) == result['image']), None)
            if image_path:
                if 'cocci' in image_path:
                    folder_accuracy['cocci']['total'] += 1
                    if predicted == 'Cocci':
                        folder_accuracy['cocci']['correct'] += 1
                elif 'healthy' in image_path:
                    folder_accuracy['healthy']['total'] += 1
                    if predicted == 'Healthy':
                        folder_accuracy['healthy']['correct'] += 1
                elif 'salmo' in image_path:
                    folder_accuracy['salmo']['total'] += 1
                    if predicted == 'Salmo':
                        folder_accuracy['salmo']['correct'] += 1

        print(f"Total images processed: {len(results)}")
        print(f"Cocci predictions: {category_counts['Cocci']}")
        print(f"Healthy predictions: {category_counts['Healthy']}")
        print(f"Salmo predictions: {category_counts['Salmo']}")

        print("\nAccuracy by folder:")
        for folder, stats in folder_accuracy.items():
            if stats['total'] > 0:
                accuracy = (stats['correct'] / stats['total']) * 100
                print(f"{folder.capitalize()}: {stats['correct']}/{stats['total']} ({accuracy:.1f}%)")

        print(f"\nSample results:")
        for i, result in enumerate(results[:10]):  # Show first 10
            print(f"  {result['image']}: {result['prediction']} (confidence: {result['confidence']:.3f})")

    except Exception as e:
        print("Error occurred:", str(e))
        import traceback

        traceback.print_exc()

    print("\nScript completed!")









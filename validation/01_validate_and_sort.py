import os
import shutil

RAW_DIR = '/Users/ryanrosa/Downloads/AI_DS_Project_Repos/CDC_Project/artifacts/data_ingestion/data/Chicken_Fecal_Images'
SORTED_DIR = '/Users/ryanrosa/Downloads/AI_DS_Project_Repos/CDC_Project/artifacts/data_ingestion/data'

valid_labels = ['salmo', 'cocci', 'healthy']

for label in valid_labels:
    os.makedirs(os.path.join(SORTED_DIR, label), exist_ok=True)
    
    
missing_labels = []
processed = 0

for filename in os.listdir(RAW_DIR):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        print(f"Skipping non-image file: {filename}")
        continue

    filepath = os.path.join(RAW_DIR, filename)
    label = filename.split('_')[0].lower()

    if label not in valid_labels:
        print(f"Unrecognized label: {label} from filename: {filename}")
        missing_labels.append(filename)
        continue

    dest_path = os.path.join(SORTED_DIR, label, filename)
    print(f"Copying: {filepath} --> {dest_path}")
    shutil.copy2(filepath, dest_path)
    processed += 1

print(f"\n✅ Finished sorting {processed} image(s).")
if missing_labels:
    print(f"⚠️ Skipped {len(missing_labels)} image(s) with unknown labels:")
    for f in missing_labels:
        print(f"  - {f}")
# Chicken Disease Classification

An end-to-end deep learning project that classifies chicken diseases from fecal image samples, built as a full MLOps pipeline — from data versioning through model training to cloud deployment.

**Author:** Francisco Rosa
**Repo:** [CDC_Project](https://github.com/frosa-create/CDC_Project)

## Overview

This project trains an image classification model to distinguish between three classes; **Coccidiosis**, **Salmonella**, and **Healthy** from photographs of chicken fecal samples, helping enable faster, earlier diagnosis than manual inspection allows. Beyond the model itself, the project implements a reproducible ML pipeline with data version control, containerized deployment, and CI/CD to both AWS and Azure.

**Current model performance:**
- Accuracy: **86.7%**
- Loss: **0.448**

*(from `scores.json`, update this section as you retrain/improve the model)*

## Tech Stack

- **Language:** Python
- **ML:** TensorFlow/Keras, VGG16 transfer learning 
- **Pipeline & versioning:** DVC (Data Version Control)
- **Deployment:** Docker, AWS (EC2 + ECR), Azure Container Registry
- **CI/CD:** GitHub Actions
- **Web app:** Flask (`app.py`)

## Project Structure

```
├── .dvc/              # DVC configuration for data/pipeline versioning
├── .github/workflows/ # CI/CD pipeline definitions
├── artifacts/         # Model artifacts and outputs
├── config/            # Configuration files
├── research/          # Exploratory notebooks and experimentation
├── src/                # Core source code (data pipeline, training, inference)
├── templates/          # Web app templates
├── app.py              # Flask application entry point
├── main.py             # Pipeline orchestration
├── params.yaml          # Model/training parameters
├── dvc.yaml / dvc.lock   # DVC pipeline definition
└── scores.json           # Latest model evaluation metrics
```

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/frosa-create/CDC_Project.git
cd CDC_Project
```

### 2. Create and activate a virtual environment
```bash
conda create -n cdc python=3.8 -y
conda activate cdc
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```
Then open the local host/port shown in the terminal.

### DVC pipeline commands
```bash
dvc init
dvc repro
dvc dag
```

## Deployment

The app is containerized with Docker and deployed via GitHub Actions CI/CD to:

- **AWS:** Docker image built, pushed to ECR, and run on an EC2 instance
- **Azure:** Docker image pushed to Azure Container Registry and run via Azure Web App

See `.github/workflows/` for the full CI/CD pipeline definitions.

## Results & Insights

- The dataset totals just over 200 images across three classes: **Coccidiosis**, **Healthy**, and **Salmonella** — with Coccidiosis and Healthy making up the bulk of the data and Salmonella represented by a notably smaller sample
- Given the class imbalance, the model likely performs strongest on Coccidiosis/Healthy and weakest on Salmonella — worth confirming with a per-class breakdown (confusion matrix) rather than relying on the overall 86.7% accuracy alone
- Model performed strongest on Coccidiosis class, which is represented by the largest sample size of images, followed by Healthy images

## Future Enhancements

- [ ] Collect more Salmonella samples to reduce class imbalance, or apply class weighting / oversampling during training
- [ ] Improve/train model to more accurately depict images of diseases outside the three that it has been trained and tested on

## Future Enhancements

- [ ] 

## License

MIT

# STAT 654 Project

## Dependencies
Install dependencies using the following command:
```bash
pip install -r dependencies.txt
```

Put your kaggle API key in the `kaggle.json` file in the `.kaggle` directory in your home folder.

## Dataset Preparation
* Dataset Link: [Kaggle](https://www.kaggle.com/code/jefmenegazzo/pvs-data-exploration)

## Feature Extraction
TSFresh library is used for feature extraction from the time series data through windowing.

## Feature Selection
Features are auto-selected based on importance using SHAP values.

## Models
* Regression Model (Linear Regression)
* Bysian Model
* Machine Learning Models:
  * SVM
  * Random Forest
  * Neural Network
  * Recurrent Neural Network


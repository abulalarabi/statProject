# STAT 654 Project
The United States road network, consisting of over 4.1 million, is deteriorating due to increased vehicle usage and rough weather, road undulations, rising maintenance costs and safety hazards for motorists. Conventional visual inspection techniques are time-consuming, require significant human intervention. To overcome these challenges, this study will put forward an automated bump detection system that involves inertial sensors, statistical feature extraction, and machine learning algorithms. The pre- processing step includes windowing and feature extraction. In this study, statistical tests are applied to determine the features’ significance, while the SHAP technique is used to quantify the features’ importance. Then, a shorter list of features is obtained that are used to form more preconditions and create an efficient detection model. The decision to use a smaller number of features as the final feature set is justified by the fact that the same level of accuracy and the F1 scores are attained while reducing the computational requirement significantly. The dataset is tested with machine learning algorithms including Logistic Regression, Naive Bayes, Support Vector Machine, K-Nearest Neighbor, Multilayer Perceptron with an architecture of three layers, Random Forest, and Gradient Boosting. Afterward, assessments, such as precision, recall, F1 measure, accuracy, confusion chart, and ROC curve, are performed. Based on the results and analysis, it is found that the Random Forest model provides the highest precision and recall values.

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


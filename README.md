# Data Analytics Bootcamp Final Project
This repository contains the final project developed during the Data Analytics bootcamp with IRONHACK, focusing on **'Facial Emotion Recognition'** using AI tools.

**Main Objectives:**
- Evaluate the performance of AI algorithms in facial emotion detection. 
- Identify factors influencing algorithm performance, including data quality and quantity.
- Explore detectable emotions and note any limitations.

        
## Data Collection, Cleaning and Analysis
### 1. Data Sources:
- API [[code](https://github.com/Beata2307/Facial_emotion_recognition_project/blob/main/Python_Data_Processing/API_connection.ipynb)],
- Web Scraping [[code](https://github.com/Beata2307/Facial_emotion_recognition_project/blob/main/Python_Data_Processing/web_scrapping.ipynb)][[web](https://imotions.com/blog/learning/research-fundamentals/facial-action-coding-system/)]
- Flat Files:
  - [Kaggle](https://www.kaggle.com/datasets/sudarshanvaidya/random-images-for-face-emotion-recognition?select=anger) (224x224 pixel grayscale images)
  - [FER-2013](https://www.kaggle.com/datasets/msambare/fer2013?select=train) (48x48 pixel grayscale images)
  - [Emotions in everyday life](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4689475/#:~:text=The%20most%20frequent%20emotion%20was,negative%20emotions%20simultaneously%20relatively%20frequently) (csv file)

### 2. Data Cleaning and Exploratory Data Analysis (EDA):
**Image Processing for API Data:**
- Check, relabel, or remove images not well-suited for face analysis.
- Utilize a Haarcascade classifier to detect and crop faces in the cleaned dataset [[code](https://github.com/Beata2307/Facial_emotion_recognition_project/blob/main/Python_Data_Processing/Extract_faces_from_images.ipynb)]

**Image Selection for Flat Files Data:**
- Randomly select a specified number of images for each emotion category [[code](https://github.com/Beata2307/Facial_emotion_recognition_project/blob/main/Python_Data_Processing/Extract_faces_from_images.ipynb)]

**CSV File:**
- Clean CSV files to improve data quality and perform exploratory data analysis (EDA) [[code](https://github.com/Beata2307/Facial_emotion_recognition_project/blob/main/Python_Data_Processing/EDA.ipynb)]

### 3. Database Management:
- Create a database with cleaned images, use separate tables for images from different sources and their metadata (e.g., expressed emotion, dimensions, aspect ratio) [[code](https://github.com/Beata2307/Facial_emotion_recognition_project/blob/main/Python_Data_Processing/Images_to_DataFrames.ipynb)]
- Establish relations between tables, develop an Entity Relationship Diagram (ERD), and use SQL queries for data insights.[[code](https://github.com/Beata2307/Facial_emotion_recognition_project/blob/main/SQL/final_project_DB.sql)]

### 4. API Development:
- Build an API to expose processed data and facilitate user access. [[flask API](https://github.com/Beata2307/Facial_emotion_recognition_project/blob/main/Python_Data_Processing/Flask_API.py)]
[[html](https://github.com/Beata2307/Facial_emotion_recognition_project/blob/main/Python_Data_Processing/templates/index.html)]

## Machine Learning Models
The "ML_Models" directory contains Python files. To assess the performance of machine learning models, few approaches were examined:
- Deep Learning algorithms [[code](https://github.com/Beata2307/Facial_emotion_recognition_project/blob/main/ML_models/Deep_Learning.ipynb)],
- Transfer Learning by adjusting pre-trained models for facial emotion recognition [[code](https://github.com/Beata2307/Facial_emotion_recognition_project/blob/main/ML_models/Pre_trained_model.ipynb)],
- Convolutional Neural Networks (CNNs) - different models were tested and trained using Colab resources [[code](https://github.com/Beata2307/Facial_emotion_recognition_project/blob/main/ML_models/CNN_models_test.ipynb)].

A comparison of algorithm performance is available in the presentation. [link](https://github.com/Beata2307/Facial_emotion_recognition_project/blob/main/Facial_emotion_recognition.pdf)

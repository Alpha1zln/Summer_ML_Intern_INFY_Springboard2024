# *** TMDB-Box-Office-Prediction ML Project ****

***
# MILESTONE 1 ::

# Task 1 :
**Data Collection :**

1: [100 movie id fetch using API  and download as csv] 

# Task 2 : 
1 : [100 data pt.s for given 22 cols fetched using API with condition budget > 0 and download as csv]



***
# MILESTONE 2 :: 
**Data Pre-processing  - DATA CLEANING, TRANSFORMATION, VISUALISATION**

# Task 1  :
**Data cleaning ::**
1) change column names : homepage - movie_url, original_title - movie_title
2)Finding and removing duplicate values(dataframes)
3) checking of any null or empty values in dataframes and try to fetch and add that missing data using movie id from  tmdb api's
4)check for any dataframes that has revenue as 0, average the revenue for the rest of dataframes and add it.
5) finally convert that processed output(dataframes) to csv format


# Task 2 :
**Data Visualisation::**
1. Create six different types of graphs using matplotlib and seaborn. Each graph will use a different type of visualization:


# Task 3 :
**Data TRANSFORMATION::**
1. convert release_date(string) to release_day,release_date,release_month(seperate columns,integer format)
2. use one hot encoding for applicable columns(genres,spoken_languages,production_countries)
3. convert to category datatype and to numerical form using pandas library for for applicable columns (status,original_language)

code file upload to github as - tmdb(2nd milestone week 4).ipynb
output csv file upload to google drive as  - tmdb_output(2nd milestone week 4).csv




***
# MILESTONE 3 :: 
** TEST DATA CLEANING**
** TEST DATA TRANSFORMATION**
** TRAINING DATA PREDICTION**
** TEST DATA PREDICTION**

Q1* take  movie_id,revenue and prediction_label columns from the prediction you did for  training data and convert into csv file(if u have split the train data remove it)

Q2* read test data csv that is shared by Mentor

Q3* do data normalization for test data

Q4* check for any missing columns in test data(compare with training data) and add missing columns with null values

Q5* take  movie_id, prediction_label columns from the prediction you did for  test data and convert into csv file

Q6* upload these two csv files to google drive  and to github - ipynb file



***
# MILESTONE 4 :: 
**UI CREATION**

**USER TEST DATA ENTERED, PREDICTION BY MODEL ON WEBPAGE**

Q1* Create a dict using test data, in vscode do predicion using pkl file [having saved model].

Q2* UI CREATION - using flask, streamlit, pkl saved model - in vscode. And finally do prediction using entered data in UI.
  



****
****
****

MI Internship - Infosys Springboard - SY


****

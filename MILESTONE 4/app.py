import streamlit as st
import pandas as pd
import joblib
from datetime import datetime, date
from pycaret.regression import load_model, predict_model

# Load the saved model
model_path = 'C:/Users/shreyas1bst/Desktop/INFY INTERN 2024 SUMMER/official/official submitted data sy/milestone 3 - week 5/code/3 t/ver 3/pkl/final_model.pkl'
loaded_model = joblib.load(model_path)

# Define the lists for production countries, unique languages, and unique genres
unique_countries = [
    'Aruba', 'Australia', 'Austria', 'Bahamas', 'Belgium', 'Botswana', 'Brazil', 'Bulgaria', 
    'Canada', 'Chile', 'China', 'Colombia', 'Cyprus', 'Czech Republic', 'Denmark', 
    'Dominican Republic', 'Finland', 'France', 'Germany', 'Greece', 'Hong Kong', 
    'Hungary', 'Iceland', 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 
    'Jamaica', 'Japan', 'Kenya', 'Kuwait', 'Lebanon', 'Libyan Arab Jamahiriya', 
    'Luxembourg', 'Malaysia', 'Malta', 'Mexico', 'Montenegro', 'Morocco', 'Netherlands', 
    'New Zealand', 'Norway', 'Peru', 'Poland', 'Portugal', 'Puerto Rico', 'Romania', 
    'Russia', 'Saudi Arabia', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 
    'South Africa', 'South Korea', 'Soviet Union', 'Spain', 'Sweden', 'Switzerland', 
    'Taiwan', 'Thailand', 'Turkey', 'Ukraine', 'United Arab Emirates', 
    'United Kingdom', 'United States of America', 'Venezuela', 'Zimbabwe',
    
    'Unnamed: 90', 'ქართული', 'Pусский', '普通话', 'ਪੰਜਾਬੀ', 'සිංහල', 'български език', 'اردو', '广州话 / 廣州話', 'Український', '한국어/조선말', 'العربية', '日本語', 'isiZulu', 'Tiếng Việt', 'Türkçe', 'Íslenska', 'shqip', 'euskera', 'suomi', 'தமிழ்', 
    'ελληνικά', 'فارسی', 'Srpski', 'עִבְרִית', 'پښتو', 'Český', 'ภาษาไทย', 'svenska', 'বাংলা'
]

unique_languages = [
    'Afrikaans', 'Bahasa indonesia', 'Bahasa melayu', 'Bosanski', 'Català', 'Cymraeg', 
    'Dansk', 'Deutsch', 'Eesti', 'English', 'Español', 'Esperanto', 'Français', 
    'Fulfulde', 'Gaeilge', 'Hrvatski', 'Italiano', 'Kiswahili', 'Latin', 'Lietuvių', 
    'Magyar', 'Nederlands', 'No Language', 'Norsk', 'Polski', 'Português', 'Română', 
    'Slovenčina', 'Somali', 'हिन्दी'
]

unique_genres = [
    'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 
    'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 
    'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western'
]

def transform_data(data):
    # Map original_language to integer
    original_language_mapping = {'en': 0, '': 1}
    data['original_language'] = original_language_mapping.get(data.get('original_language', ''), 0)
    
    # Map status to integer
    status_mapping = {'Released': 3, 'Post Production': 2, 'Planned': 1, 'In Production': 0}
    data['status'] = status_mapping.get(data.get('status', ''), 0)
    
    # Initialize input_data with default values
    input_data = {
        'movie_id': 0,
        'budget': 0,
        'movie_url': '',
        'imdb_id': '',
        'original_language': 0,
        'movie_title': '',
        'overview': '',
        'popularity': 0.0,
        'production_companies': '',
        'poster_path': '',
        'runtime': 0,
        'status': 0,
        'tagline': '',
        # 'title': '',
        'keywords': '',
        'cast': '',
        'crew': '',
        'release_day': datetime.now().day,
        'release_month': datetime.now().month,
        'release_year': datetime.now().year
    }

    for genres in unique_genres:
        input_data[genres] = 0

    for spoken_languages in unique_languages:
        input_data[spoken_languages] = 0

    for production_countries in unique_countries:
        input_data[production_countries] = 0
    
    # Fill input_data with form values
    input_data.update({
        'movie_id': int(data.get('movieId', 0)),
        'budget': float(data.get('budget', 0)),
        'movie_url': data.get('movieUrl', ''),
        'imdb_id': data.get('imdbId', ''),
        'original_language': data['original_language'],
        'movie_title': data.get('movieTitle', ''),
        'overview': data.get('overview', ''),
        'popularity': float(data.get('popularity', 0)),
        'production_companies': data.get('production_companies', ''),
        'runtime': int(data.get('runtime', 0)),
        'status': data['status'],
        'tagline': data.get('tagline', ''),
        # 'title': data.get('title', ''),
        'keywords': data.get('keywords', ''),
        'cast': data.get('cast', ''),
        'crew': data.get('crew', ''),
        'release_day': int(data.get('releaseDate', '0000/00/00').split('/')[2]),
        'release_month': int(data.get('releaseDate', '0000/00/00').split('/')[1]),
        'release_year': int(data.get('releaseDate', '0000/00/00').split('/')[0]),
    })
    
    # Set genres, spoken languages, and production countries to 1 if present in data
    for genres in unique_genres:
        input_data[genres] = 1 if genres in data.get('genres', []) else 0
    for spoken_languages in unique_languages:
        input_data[spoken_languages] = 1 if spoken_languages in data.get('spoken_languages', []) else 0
    for production_countries in unique_countries:
        input_data[production_countries] = 1 if production_countries in data.get('production_countries', []) else 0
    
    return input_data

# Streamlit app
# Centering the title using HTML and CSS
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 3em;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

st.markdown('<div class="title">Box Office Prediction</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.header('Enter Movie Details')
    movie_id = st.number_input('Movie ID')
    budget = st.number_input('Budget')
    movie_url = st.text_input('Movie URL')
    imdb_id = st.text_input('IMDB ID')
    original_language = st.selectbox('Original Language', ['en', ''])
    movie_title = st.text_input('Movie Title')
    overview = st.text_input('Overview')
    popularity = st.number_input('Popularity', min_value=0.0, step=0.1)
    production_companies = st.text_input('Production Companies')
    runtime = st.number_input('Runtime')
    status = st.selectbox('Status', ['Released', 'Post Production', 'Planned', 'In Production'])
    tagline = st.text_input('Tagline')
    # title = st.text_input('Title')
    keywords = st.text_input('Keywords')
    cast = st.text_input('Cast')
    crew = st.text_input('Crew')
    release_date = st.date_input('Release Date', min_value=date(1900, 1, 1), max_value=date(2030, 12, 31))
    genres = st.multiselect('Genres', unique_genres)
    spoken_languages = st.multiselect('Spoken Languages', unique_languages)
    production_countries = st.multiselect('Production Countries', unique_countries)

    data = {
        'movieId': movie_id,
        'budget': budget,
        'movieUrl': movie_url,
        'imdbId': imdb_id,
        'original_language': original_language,
        'movieTitle': movie_title,
        'overview': overview,
        'popularity': popularity,
        'production_companies': production_companies,
        'runtime': runtime,
        'status': status,
        'tagline': tagline,
        # 'title': title,
        'keywords': keywords,
        'cast': cast,
        'crew': crew,
        'releaseDate': release_date.strftime('%Y/%m/%d'),
        'genres': genres,
        'spokenLanguages': spoken_languages,
        'productionCountries': production_countries
    }

    if st.button('Predict'):
        transformed_data = transform_data(data)
        
        # Convert the dictionary to a pandas DataFrame
        input_data_df = pd.DataFrame([transformed_data])
        
        # Ensure all expected columns are present in the DataFrame
        all_columns = [
            'movie_id', 'budget', 'movie_url', 'imdb_id', 'original_language', 'movie_title', 'overview', 
            'popularity', 'production_companies', 'poster_path', 'runtime', 'status', 'tagline', 'title', 
            'keywords', 'cast', 'crew', 'release_day', 'release_month', 'release_year'
        ] + unique_genres + unique_languages + production_countries

        for col in all_columns:
            if col not in input_data_df.columns:
                input_data_df[col] = 0
        
        input_data_df['original_language'] = input_data_df['original_language'].astype('category')
        input_data_df['status'] = input_data_df['status'].astype('category')


        # Make predictions using the loaded model
        predictions = predict_model(loaded_model, data=input_data_df)
        
        # Display predictions
        st.subheader('Prediction')
        st.write(f'Predicted Box Office Revenue: {predictions["prediction_label"][0]}')

        # Add a title section with the same movie_title in the code
        st.write(f'Movie Title: {data.get("movieTitle", "")}')

        # Map status and original_language back to their string values for display
        status_reverse_mapping = {3: 'Released', 2: 'Post Production', 1: 'Planned', 0: 'In Production'}
        original_language_reverse_mapping = {0 : 'en', 1 : ''}

        data['status'] = status_reverse_mapping.get(data['status'], 'Released')
        data['original_language'] = original_language_reverse_mapping.get(data['original_language'], 'en')

        # Display entered movie details
        st.subheader('Entered Movie Details')
        st.table(pd.DataFrame([data]).T)

#         # Display entered movie details
#         st.subheader('Entered Movie Details')
#         st.write(data)









# *********************************************
# **********************************************
# import streamlit as st
# import pandas as pd
# import joblib
# from datetime import datetime, date
# from pycaret.regression import load_model, predict_model

# # Load the saved model
# model_path = 'C:/Users/shreyas1bst/Desktop/INFY INTERN 2024 SUMMER/official/official submitted data sy/milestone 3 - week 5/code/3 t/ver 3/pkl/final_model.pkl'
# loaded_model = joblib.load(model_path)

# # Define the lists for production countries, unique languages, and unique genres
# unique_countries = [
#     'Aruba', 'Australia', 'Austria', 'Bahamas', 'Belgium', 'Botswana', 'Brazil', 'Bulgaria', 
#     'Canada', 'Chile', 'China', 'Colombia', 'Cyprus', 'Czech Republic', 'Denmark', 
#     'Dominican Republic', 'Finland', 'France', 'Germany', 'Greece', 'Hong Kong', 
#     'Hungary', 'Iceland', 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 
#     'Jamaica', 'Japan', 'Kenya', 'Kuwait', 'Lebanon', 'Libyan Arab Jamahiriya', 
#     'Luxembourg', 'Malaysia', 'Malta', 'Mexico', 'Montenegro', 'Morocco', 'Netherlands', 
#     'New Zealand', 'Norway', 'Peru', 'Poland', 'Portugal', 'Puerto Rico', 'Romania', 
#     'Russia', 'Saudi Arabia', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 
#     'South Africa', 'South Korea', 'Soviet Union', 'Spain', 'Sweden', 'Switzerland', 
#     'Taiwan', 'Thailand', 'Turkey', 'Ukraine', 'United Arab Emirates', 
#     'United Kingdom', 'United States of America', 'Venezuela', 'Zimbabwe',
    
#     'Unnamed: 90', 'ქართული', 'Pусский', '普通话', 'ਪੰਜਾਬੀ', 'සිංහල', 'български език', 'اردو', '广州话 / 廣州話', 'Український', '한국어/조선말', 'العربية', '日本語', 'isiZulu', 'Tiếng Việt', 'Türkçe', 'Íslenska', 'shqip', 'euskera', 'suomi', 'தமிழ்', 
#     'ελληνικά', 'فارسی', 'Srpski', 'עִבְרִית', 'پښتو', 'Český', 'ภาษาไทย', 'svenska', 'বাংলা'
# ]

# unique_languages = [
#     'Afrikaans', 'Bahasa indonesia', 'Bahasa melayu', 'Bosanski', 'Català', 'Cymraeg', 
#     'Dansk', 'Deutsch', 'Eesti', 'English', 'Español', 'Esperanto', 'Français', 
#     'Fulfulde', 'Gaeilge', 'Hrvatski', 'Italiano', 'Kiswahili', 'Latin', 'Lietuvių', 
#     'Magyar', 'Nederlands', 'No Language', 'Norsk', 'Polski', 'Português', 'Română', 
#     'Slovenčina', 'Somali', 'हिन्दी'
# ]

# unique_genres = [
#     'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 
#     'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 
#     'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western'
# ]

# def transform_data(data):
#     # Map original_language to integer
#     original_language_mapping = {'en': 1, '': 0}
#     data['original_language'] = original_language_mapping.get(data.get('original_language', ''), 0)
    
#     # Map status to integer
#     status_mapping = {'Released': 3, 'Post Production': 2, 'Planned': 1, 'In Production': 0}
#     data['status'] = status_mapping.get(data.get('status', ''), 0)
    
#     # Initialize input_data with default values
#     input_data = {
#         'movie_id': 0,
#         'budget': 0,
#         'movie_url': '',
#         'imdb_id': '',
#         'original_language': 0,
#         'movie_title': '',
#         'overview': '',
#         'popularity': 0.0,
#         'production_companies': '',
#         'poster_path': '',
#         'runtime': 0,
#         'status': 0,
#         'tagline': '',
#         'title': '',
#         'keywords': '',
#         'cast': '',
#         'crew': '',
#         'release_day': datetime.now().day,
#         'release_month': datetime.now().month,
#         'release_year': datetime.now().year
#     }

#     for genres in unique_genres:
#         input_data[genres] = 0

#     for spoken_languages in unique_languages:
#         input_data[spoken_languages] = 0

#     for production_countries in unique_countries:
#         input_data[production_countries] = 0
    
#     # Fill input_data with form values
#     input_data.update({
#         'movie_id': int(data.get('movieId', 0)),
#         'budget': float(data.get('budget', 0)),
#         'movie_url': data.get('movieUrl', ''),
#         'imdb_id': data.get('imdbId', ''),
#         'original_language': data['original_language'],
#         'movie_title': data.get('movieTitle', ''),
#         'overview': data.get('overview', ''),
#         'popularity': float(data.get('popularity', 0)),
#         'production_companies': data.get('production_companies', ''),
#         'runtime': int(data.get('runtime', 0)),
#         'status': data['status'],
#         'tagline': data.get('tagline', ''),
#         'title': data.get('title', ''),
#         'keywords': data.get('keywords', ''),
#         'cast': data.get('cast', ''),
#         'crew': data.get('crew', ''),
#         'release_day': int(data.get('releaseDate', '0000/00/00').split('/')[2]),
#         'release_month': int(data.get('releaseDate', '0000/00/00').split('/')[1]),
#         'release_year': int(data.get('releaseDate', '0000/00/00').split('/')[0]),
#     })
    
#     # Set genres, spoken languages, and production countries to 1 if present in data
#     for genres in unique_genres:
#         input_data[genres] = 1 if genres in data.get('genres', []) else 0
#     for spoken_languages in unique_languages:
#         input_data[spoken_languages] = 1 if spoken_languages in data.get('spoken_languages', []) else 0
#     for production_countries in unique_countries:
#         input_data[production_countries] = 1 if production_countries in data.get('production_countries', []) else 0
    
#     return input_data


# # Streamlit app
# # Centering the title using HTML and CSS
# st.markdown(
#     """
#     <style>
#     .title {
#         text-align: center;
#         font-size: 3em;
#     }
#     </style>
#     """, 
#     unsafe_allow_html=True
# )

# st.markdown('<div class="title">Box Office Prediction</div>', unsafe_allow_html=True)

# col1, col2, col3 = st.columns([1, 4, 1])

# with col2:
#     st.header('Enter Movie Details')
#     movie_id = st.number_input('Movie ID')
#     budget = st.number_input('Budget')
#     movie_url = st.text_input('Movie URL')
#     imdb_id = st.text_input('IMDB ID')
#     original_language = st.selectbox('Original Language', ['en', ''])
#     movie_title = st.text_input('Movie Title')
#     overview = st.text_input('Overview')
#     popularity = st.number_input('Popularity', min_value=0.0, step=0.1)
#     production_companies = st.text_input('Production Companies')
#     runtime = st.number_input('Runtime')
#     status = st.selectbox('Status', ['Released', 'Post Production', 'Planned', 'In Production'])
#     tagline = st.text_input('Tagline')
#     title = st.text_input('Title')
#     keywords = st.text_input('Keywords')
#     cast = st.text_input('Cast')
#     crew = st.text_input('Crew')
#     release_date = st.date_input('Release Date', min_value=date(1900, 1, 1), max_value=date(2030, 12, 31))
#     genres = st.multiselect('Genres', unique_genres)
#     spoken_languages = st.multiselect('Spoken Languages', unique_languages)
#     production_countries = st.multiselect('Production Countries', unique_countries)

#     data = {
#         'movieId': movie_id,
#         'budget': budget,
#         'movieUrl': movie_url,
#         'imdbId': imdb_id,
#         'original_language': original_language,
#         'movieTitle': movie_title,
#         'overview': overview,
#         'popularity': popularity,
#         'production_companies': production_companies,
#         'runtime': runtime,
#         'status': status,
#         'tagline': tagline,
#         'title': title,
#         'keywords': keywords,
#         'cast': cast,
#         'crew': crew,
#         'releaseDate': release_date.strftime('%Y/%m/%d'),
#         'genres': genres,
#         'spokenLanguages': spoken_languages,
#         'productionCountries': production_countries
#     }

#     if st.button('Predict'):
#         transformed_data = transform_data(data)
        
#         # Convert the dictionary to a pandas DataFrame
#         input_data_df = pd.DataFrame([transformed_data])
        
#         # Ensure all expected columns are present in the DataFrame
#         all_columns = [
#             'movie_id', 'budget', 'movie_url', 'imdb_id', 'original_language', 'movie_title', 'overview', 
#             'popularity', 'production_companies', 'poster_path', 'runtime', 'status', 'tagline', 'title', 
#             'keywords', 'cast', 'crew', 'release_day', 'release_month', 'release_year'
#         ] + unique_genres + unique_languages + production_countries
        


#         for col in all_columns:
#             if col not in input_data_df.columns:
#                 input_data_df[col] = 0
        
#         # input_data_df['original_language'] = input_data_df['original_language'].astype('category')
#         # input_data_df['status'] = input_data_df['status'].astype('category')
        
#         # Make predictions using the loaded model
#         predictions = predict_model(loaded_model, data=input_data_df)
        
#         # Display predictions
#         st.subheader('Prediction')
#         st.write(f'Predicted Box Office Revenue: {predictions["prediction_label"][0]}')

#         # Add a title section with the same movie_title in the code
#         st.write(f'Movie Title: {data.get("movieTitle", "")}')


#         # Display entered movie details
#         st.subheader('Entered Movie Details')
#         st.write(data)

#         # # Display entered movie details
#         # st.subheader('Entered Movie Details')
#         # st.table(pd.DataFrame([data]))



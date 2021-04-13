from urllib.request import urlopen
from flask import Flask, render_template,request
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def Cosine_Similarity(ing):

   def get_title_from_index(index):
      return df2[df2.index == index]["title"].values[0]

   def get_recipe_from_index(index):
      return df2[df2.index == index]["Instructions"].values[0]

   def get_ingredients_from_index(index):
      return df2[df2.index == index]["ingredients"].values[0]

   def get_url_from_title(index):
      return df2[df2.index == index]["URL"].values[0]

   def get_index_from_title(title):
      return df2[df2.title == title]["index"].values[0]


   df = pd.read_csv("test.csv", encoding='unicode_escape')
   df1 = pd.DataFrame({"index": [2507], "title": ["test"], "ingredients": [ing]})
   df2 = df.append(df1, ignore_index=True)
   df2.tail()

   features = ['ingredients']

   for feature in features:
      df2[feature] = df2[feature].fillna('')
   def combine_features(row):
      return str(row['ingredients'])

   df2["combined_features"] = df2.apply(combine_features, axis=1)

   print("Combined Features:", df2["combined_features"].head())

   cv = CountVectorizer()

   count_matrix = cv.fit_transform(df2["combined_features"])
   cosine_sim = cosine_similarity(count_matrix)
   print(cosine_sim)

   preference = "test"

   food_index = get_index_from_title(preference)

   similar_food = list(enumerate(cosine_sim[int(food_index)]))


   sorted_similar_food = sorted(similar_food, key=lambda x: x[1], reverse=True)


   test=[]
   for i in range(1,4):
      test.append(get_title_from_index(sorted_similar_food[i][0]))
      test.append(get_ingredients_from_index(sorted_similar_food[i][0]))
      test.append(get_recipe_from_index(sorted_similar_food[i][0]))
      test.append(get_url_from_title(sorted_similar_food[i][0]))


      htmldata = urlopen(test[3+4*(i-1)])

      soup = BeautifulSoup(htmldata, 'html.parser')
      images = soup.find_all("img", class_='img-thumbnail')

      for item in images:
         test[3+4*(i-1)]="https://www.archanaskitchen.com"+(item['src'])


   return test

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/recommend', methods=['POST','GET'])
def recommend():
   string_features=""
   for x in request.form.values():
      string_features=string_features + x +" "
   a=Cosine_Similarity(string_features)
   return render_template('index.html',url=a[3],recipe_name=a[0],ingredients=a[1],recipe=a[2],h1="Ingredients:",h2="Recipe:",url1=a[7],recipe_name1=a[4],ingredients1=a[5],recipe1=a[6],url2=a[11],recipe_name2=a[8],ingredients2=a[9],recipe2=a[10])

if __name__ == '__main__':
   app.run(debug=True)


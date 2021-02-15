import pandas as pd
import sqlite3
import plotly.express as px
from scipy.misc import imsave

directory ='enter your directory'

#connexion
connexion = sqlite3.connect("imdb.db")
c = connexion.cursor()



#Categories
##proportion
query = ("SELECT COUNT(Film.id) AS nb_films, Category.category FROM Film "
         "INNER JOIN Category on Category.id == Film.category_id"
         " GROUP BY Category.category;")
cat = pd.read_sql(query, con = connexion)

fig = px.pie(cat, values='nb_films', names='category', title='Proportion of movies by category')
imsave(direcotry + '/categories_proportion.png, fig)


#link with the grades
query = ("SELECT AVG(Film.grade) AS avg_grade, Category.category FROM Film "
         "INNER JOIN Category on Category.id == Film.category_id "
         "GROUP BY Category.category;")
grade_by_cat = pd.read_sql(query, con = connexion)
fig = px.bar(grade_by_cat, x = 'category', y = 'avg_grade', color='avg_grade', labels={'avg_grade': 'average grade'})
imsave(directory + '/categories_grade.png', fig)

       
#Language
##how many languages?
lang = c.execute("SELECT COUNT(DISTINCT(language)) FROM Film ").fetchmany()[0][0]
print(f"There are {lang} different languages")

##movies_language
query = "SELECT COUNT(id) AS nb_films, language FROM Film GROUP BY language;"
lang = pd.read_sql_query(query, con = connexion)

fig = px.pie(lang, values='nb_films', names='language', title='Proportion of movies by language')
imsave(directory + '/movies_language.png', fig)


##Which the languages the least represented?
query = ("SELECT COUNT(id) AS nb_films, language FROM Film" 
         " GROUP BY language"
         " HAVING nb_films IN (1,2,3)")

pd.read_sql_query(query, con = connexion).head(10).to_csv(path_or_buf = directory + 'language_underrepresentation.csv', index = False)



#Countries
##how many countries?
count = c.execute("SELECT COUNT(DISTINCT(country)) FROM Film ").fetchmany()[0][0]
print(f"There are {count} different countries")
       
##movies_country
query = "SELECT COUNT(id) AS nb_films, country FROM Film GROUP BY country;"
lang = pd.read_sql_query(query, con = connexion)
fig = px.pie(lang, values='nb_films', names='country', title='Proportion of movies by country')
imsave(directory + 'movies_country.png', fig)


##Which country are the least represented?
query = ("SELECT COUNT(id) AS nb_films, country FROM Film" 
         " GROUP BY country"
         " HAVING nb_films IN (1,2,3)")
pd.read_sql_query(query, con = connexion).head(10).to_csv(path_or_buf = directory + 'country_underrepresentation.csv', index = False)


###rate by country
query = ("SELECT ROUND(AVG(Film.grade),2) AS avg_grade, film.country, COUNT(Film.id) AS nb_films FROM Film "
         "GROUP BY film.country "
         "HAVING nb_films != 1 "
         "ORDER BY avg_grade DESC "
         "LIMIT 15; ")

df = pd.read_sql_query(query, con = connexion)

fig = px.bar(df, x = 'country', y = 'avg_grade', color='avg_grade', hover_data=['nb_films'], 
             labels={'avg_grade': 'average grade'})
imsave(directory + 'country_grade.png', fig)



#Actors
##actor most represented
query = ("SELECT Actor.actor, COUNT(Film.id) AS nb_films, ROUND(AVG(Film.grade),2) as avg_grade FROM Casting "
         "INNER JOIN Actor ON Casting.actor_id == Actor.id "
         "INNER JOIN Film ON Film.id == Casting.id_title "
         "GROUP BY Actor.actor "
         "HAVING nb_films > 20 "
         "ORDER BY avg_grade DESC, nb_films DESC")

df = pd.read_sql_query(query, con = connexion)
fig = px.bar(df, x = 'actor', y = 'nb_films', color = 'avg_grade', labels={'nb_films': 'number of movies'})
imsave(directory + '/actor_most_represented_by_grade.png', fig)

##actors with the best grades
query = ("SELECT Actor.actor, COUNT(Film.id) AS nb_films, ROUND(AVG(Film.grade),2) as avg_grade FROM Casting "
         "INNER JOIN Actor ON Casting.actor_id == Actor.id "
         "INNER JOIN Film ON Film.id == Casting.id_title "
         "GROUP BY Actor.actor "
         "ORDER BY avg_grade DESC, nb_films DESC ")

pd.read_sql_query(query, con = connexion).head().to_csv(path_or_buf = directory + 'actors_best_grade.csv', index = False)


##actors with the worst grades
query = ("SELECT Actor.actor, COUNT(Film.id) AS nb_films, ROUND(AVG(Film.grade),2) as avg_grade FROM Casting "
         "INNER JOIN Actor ON Casting.actor_id == Actor.id "
         "INNER JOIN Film ON Film.id == Casting.id_title "
         "GROUP BY Actor.actor "
         "ORDER BY avg_grade ASC, nb_films DESC ")

pd.read_sql_query(query, con = connexion).head().to_csv(path_or_buf = directory + 'actors_worst_grade.csv', index = False)


# Directors
##directors most represented
query = ("SELECT Director.director, COUNT(Film.id) AS nb_films, ROUND(AVG(Film.grade),2) as avg_grade FROM Casting "
         "INNER JOIN Director ON Casting.director_id == Director.id "
         "INNER JOIN Film ON Film.id == Casting.id_title "
         "GROUP BY Director.director "
         "HAVING nb_films > 10 "
         "ORDER BY avg_grade DESC, nb_films DESC")

df = pd.read_sql_query(query, con = connexion)
fig = px.bar(df, x = 'director', y = 'nb_films', color = 'avg_grade', labels={'nb_films': 'number of movies'})
imsave(directory + '/director_most_represented_by_grade.png', fig)


##directors with the best grades
query = ("SELECT Director.director, COUNT(Film.id) AS nb_films, ROUND(AVG(Film.grade),2) as avg_grade FROM Casting "
         "INNER JOIN Director ON Casting.director_id == Director.id "
         "INNER JOIN Film ON Film.id == Casting.id_title "
         "GROUP BY Director.director "
         "ORDER BY avg_grade DESC, nb_films DESC ")

pd.read_sql_query(query, con = connexion).head()


##directors with the worst grades
query = ("SELECT Director.director, COUNT(Film.id) AS nb_films, ROUND(AVG(Film.grade),2) as avg_grade FROM Casting "
         "INNER JOIN Director ON Casting.director_id == Director.id "
         "INNER JOIN Film ON Film.id == Casting.id_title "
         "GROUP BY Director.director "
         "ORDER BY avg_grade ASC, nb_films DESC ")

pd.read_sql_query(query, con = connexion).head()


# > **Same observation with the directors**

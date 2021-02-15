import pandas as pd
import sqlite3
import plotly.express as px
from scipy.misc import imsave

directory ='enter your directory'
#connexion
connexion = sqlite3.connect("imdb.db")
c = connexion.cursor()



#Categories


query = ("SELECT COUNT(Film.id) AS nb_films, Category.category FROM Film "
         "INNER JOIN Category on Category.id == Film.category_id"
         " GROUP BY Category.category;")
cat = pd.read_sql(query, con = connexion)

fig = px.pie(cat, values='nb_films', names='category', title='Proportion of movies by category')
imsave()


# > There are 18 categories. It could be an idea to gather in a common category the less popular movies in `Other`.
# >
# > But before, let's look at how popular they are with the public



query = ("SELECT AVG(Film.grade) AS avg_grade, Category.category FROM Film "
         "INNER JOIN Category on Category.id == Film.category_id "
         "GROUP BY Category.category;")
grade_by_cat = pd.read_sql(query, con = connexion)

px.bar(grade_by_cat, x = 'category', y = 'avg_grade', color='avg_grade', labels={'avg_grade': 'average grade'})


# > Among the less popular categories, we see that if we put musical and western together, it will create a bias since there is a huge gap between both of them.
# >
# > It would be tempting to bring `Music` and `Musical` together. In fact, there are only 2 of each, so it is impossible to generalize. **So, we bring the minorities together.**
# 
# ## Languages and countries
# >
# > How many languages there are and how they are distributed


lang = c.execute("SELECT COUNT(DISTINCT(language)) FROM Film ").fetchmany()[0][0]

print(f"There are {lang} different languages")



query = "SELECT COUNT(id) AS nb_films, language FROM Film GROUP BY language;"
lang = pd.read_sql_query(query, con = connexion)

fig = px.pie(lang, values='nb_films', names='language', title='Proportion of movies by language')
fig.show()


# > Which the languages the least represented?


query = ("SELECT COUNT(id) AS nb_films, language FROM Film" 
         " GROUP BY language"
         " HAVING nb_films IN (1,2,3)")

pd.read_sql_query(query, con = connexion).head(10)


# > We see that there is a majority of movies in English. **The idea would be to bring them togetherg by continent or common area and get rid of movies with particular languages**.
# >
# > Let's do the same with the countries



count = c.execute("SELECT COUNT(DISTINCT(country)) FROM Film ").fetchmany()[0][0]

print(f"There are {count} different countries")




query = "SELECT COUNT(id) AS nb_films, country FROM Film GROUP BY country;"
lang = pd.read_sql_query(query, con = connexion)
fig = px.pie(lang, values='nb_films', names='country', title='Proportion of movies by country')
fig.show()


# > Which country are the least represented?



query = ("SELECT COUNT(id) AS nb_films, country FROM Film" 
         " GROUP BY country"
         " HAVING nb_films IN (1,2,3)")
pd.read_sql_query(query, con = connexion).head(10)


# > **The idea is the same as for the languages**


query = ("SELECT ROUND(AVG(Film.grade),2) AS avg_grade, film.country, COUNT(Film.id) AS nb_films FROM Film "
         "GROUP BY film.country "
         "HAVING nb_films != 1 "
         "ORDER BY avg_grade DESC "
         "LIMIT 15; ")

df = pd.read_sql_query(query, con = connexion)

fig = px.bar(df, x = 'country', y = 'avg_grade', color='avg_grade', hover_data=['nb_films'], 
             labels={'avg_grade': 'average grade'})
fig.show()


# > We notice that the most well rated movies are from the least represented countries - excepted for South Korea and Japan with respectively 75 and 131 movies. This could introduce an overfitting in the future because it is impossible to generalize properly with so few movies. 
# >
# > **The idea to bring together by continent seems to help to counter the problem because it allows to get a mean, much more representative of the reality**
# >
# > Now, it is important to understand the distribution of actors and directors over the database. 
# 
# ## Actors and directors
# 
# ### Actors


query = ("SELECT Actor.actor, COUNT(Film.id) AS nb_films, ROUND(AVG(Film.grade),2) as avg_grade FROM Casting "
         "INNER JOIN Actor ON Casting.actor_id == Actor.id "
         "INNER JOIN Film ON Film.id == Casting.id_title "
         "GROUP BY Actor.actor "
         "HAVING nb_films > 20 "
         "ORDER BY avg_grade DESC, nb_films DESC")

df = pd.read_sql_query(query, con = connexion)

fig = px.bar(df, x = 'actor', y = 'nb_films', color = 'avg_grade', labels={'nb_films': 'number of movies'})
fig.show()


# > It is important to keep some names because it impacts the grade and allows to generalize as much as possible this one. The actors with the best (worst) average grade are those with only one movie to their credit as shown below.



query = ("SELECT Actor.actor, COUNT(Film.id) AS nb_films, ROUND(AVG(Film.grade),2) as avg_grade FROM Casting "
         "INNER JOIN Actor ON Casting.actor_id == Actor.id "
         "INNER JOIN Film ON Film.id == Casting.id_title "
         "GROUP BY Actor.actor "
         "ORDER BY avg_grade DESC, nb_films DESC ")

pd.read_sql_query(query, con = connexion).head()




query = ("SELECT Actor.actor, COUNT(Film.id) AS nb_films, ROUND(AVG(Film.grade),2) as avg_grade FROM Casting "
         "INNER JOIN Actor ON Casting.actor_id == Actor.id "
         "INNER JOIN Film ON Film.id == Casting.id_title "
         "GROUP BY Actor.actor "
         "ORDER BY avg_grade ASC, nb_films DESC ")

pd.read_sql_query(query, con = connexion).head()


# > Hopping to generalize as much as possible, **we will keep the name of the top 17 of well-known actors and put all the others together in a common category : `Other` - because it is impossible to generalize from them.**

# ### Directors



query = ("SELECT Director.director, COUNT(Film.id) AS nb_films, ROUND(AVG(Film.grade),2) as avg_grade FROM Casting "
         "INNER JOIN Director ON Casting.director_id == Director.id "
         "INNER JOIN Film ON Film.id == Casting.id_title "
         "GROUP BY Director.director "
         "HAVING nb_films > 10 "
         "ORDER BY avg_grade DESC, nb_films DESC")

df = pd.read_sql_query(query, con = connexion)

fig = px.bar(df, x = 'director', y = 'nb_films', color = 'avg_grade', labels={'nb_films': 'number of movies'})
fig.show()



query = ("SELECT Director.director, COUNT(Film.id) AS nb_films, ROUND(AVG(Film.grade),2) as avg_grade FROM Casting "
         "INNER JOIN Director ON Casting.director_id == Director.id "
         "INNER JOIN Film ON Film.id == Casting.id_title "
         "GROUP BY Director.director "
         "ORDER BY avg_grade DESC, nb_films DESC ")

pd.read_sql_query(query, con = connexion).head()



query = ("SELECT Director.director, COUNT(Film.id) AS nb_films, ROUND(AVG(Film.grade),2) as avg_grade FROM Casting "
         "INNER JOIN Director ON Casting.director_id == Director.id "
         "INNER JOIN Film ON Film.id == Casting.id_title "
         "GROUP BY Director.director "
         "ORDER BY avg_grade ASC, nb_films DESC ")

pd.read_sql_query(query, con = connexion).head()


# > **Same observation with the directors**

# Webscraping-SQL-ML-project
In this requisitory, We are going to web scrape informations about movies on IMDB - like the length, the title, the categoty - and create a database with SQLite, which is the easiest way for a local project. Then, we will do a small use case by trying to predict the grade of movies with the collected features. 

The programm is not intended to be executed since it is just a little project, just showing a complete work - from collecting the data to a ML approach. So, the support will be in Jupyter Notebook, easier to read and with explanations all along. 

The project is in three parts :
1. **Web Scrapping-SQL.ipynb** : how to collect the data, create the database and insert the values.  
2. **Data_analysis.ipynb**: Use SQLite to study the database.
3. **ML.ipynb**: A machine learning project with the data.

# Webscraping

The goal is to collect the data of the 10 000 most popular movies. If the movie is not rated, we will not include it because the grade is necessary for our project since it is the target.   

The data are collected on this [link](https://www.imdb.com/search/title/?title_type=feature&release_date=2000-01-01,2020-12-31&start=1) from the first page to the 200th page, with the package **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)**. This are the commons step the webscrape with **BeautifulSoup**:
* Get the url with the function `get`
* Parse the HTML file with `BeautifulSoup` with the type of parsor. 
* Detect the `tag`, `CSS`, `class`... of the HTML file to get the informations inside. 

The final step could appear hard because it implies that you know HTML code. In reality, it is not necessary to be familiar with HTML with **BeautifulSoup**. It is very simple thanks to the [devtool inspector](https://developers.google.com/web/tools/chrome-devtools). This link is only for Chrome but you can find a lot of ressources on the web for any browser.  
This is an example: 
![Simplon.co](https://github.com/guipet/Webscraping-SQL-ML-project/blob/main/img/devtool.png)

To go from page to page - to get the 10000 first movies - we need to study the html link to iterate over it. The structure is very simple because there is only one thing that changes at the end : `start=num_page`. Since there are 50 movies on each page, the link for the first page is `start=1`, `start=51` for the second page and so on.... that's why we have 

```py
url_base = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2000-01-01,2020-12-31&start='
start = np.arange(1, 10000, 50)
```
When we have the link, we make a request, ie get the url. Then, we parse the website 
```py
site  = get(url)
parser = BeautifulSoup(site.text, 'html.parser')
```

Once the parser defined, we can see (on the image) all the movies of the page are in the tag `div` of with `class=lister-list`. So, to get the information contained in it, we write: 

```py
parser.find_all(class_ = "lister-item mode-advanced")
```

Last thing. We will make a lot of requests to get our 10000 movies. So, to avoid overloading the website, we need to take a break of few seconds between each request. This is the usefulness of this part of the code:
```py
sleep(randint(8,15))
```
The complete code is below:
```py
from time import sleep
import requests
from requests import get
from bs4 import BeautifulSoup

url_base = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2000-01-01,2020-12-31&start='
start = np.arange(1, 10000, 50)

for i in start: # iterating over the pages
    
    url = url_base + str(i)
    
    #get the website
    site  = get(url)
    
    #break - avoid overloading the site
    print('\n')
    print("break...")
    sleep(randint(8,15))
    print("finished \n")
    
    #BeautifulSoup
    parser = BeautifulSoup(site.text, 'html.parser')
    
    
    for movie in parser.find_all(class_ = "lister-item mode-advanced"):
        #take the informations you want
```
I scraped a lot of informations, so it's a long part - about 3 hours.

# SQLite
**[SQLite](https://www.sqlite.org/index.html)** is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine. SQLite is the most used database engine in the world. SQLite is built into all mobile phones and most computers and comes bundled inside countless other applications that people use every day. A useful tool to easily visualize and interact with a SQLite database is [DB Browser for SQLite](https://sqlitebrowser.org). A database allows us to easily navigate throw the data and study them. The separate tables avoid duplicate rows in the main table

Once the webscraping over, we create the `imdb.db` database and instanciate a cursor, to navigate throw the database, and authorize the foreign key, to link the different tables, with the code:
```py
import sqlite3
connexion = sqlite3.connect("imdb.db")
connexion.execute("PRAGMA foreign_keys = on;")
c = connexion.cursor()
```

**Relation One-to-many**:
* A movie is associated with a director and an actor. At the opposite, an actor and a director are involved in many movies. 
* A movie is caractrized by a category. However, a category defined many movies

*Note*: we could have done the same for the language and country with a movie. But, there is a predominance of the USA and thus, the language UK. It is not very interesting to create a table if 84% of the values are similar for the same column. 

**Relation Many-to-Many**:
* A director can work with different actors and an actor can work with different directors. 

So, regarding to this informations, here is the database schema : 
![Database](https://github.com/guipet/Webscraping-SQL-ML-project/blob/main/utils/Diagramme.png)

There exists many ways to insert value in tables, with dictionnaries, list of tuple. The fact is that we collected the data and we need to iterate over some to build my my foreign keys. So, for the `Film` table, we execute : 
```py
i = 0
for titre, note, duree, votes, pays, langue, category in zip(title, grade, runtime, nb_vote, country, language, cat):
    item = (i, titre, note, duree, votes, pays, langue, category2id[category])
    c.execute('INSERT INTO Film values (?,?,?,?,?,?,?,?)', item)
    i +=1
```
*Note*: `category2id` is a dictionnary that link a category to its value for the foreign key; `category_id` on the diagram. A more elegant way is to organize the data during the webscraping and use the optimized `fetchall` command of **SQLite** at the end.

# Dataviz
 All the visualizations are in the folder `img` and the comments in the dedicated notebook. There were generated with **[Plotly](https://plotly.com/python/)**, a nice package for data visualization. 
 
 
# ML project
We select the needed data of the database and preprocess them for the project. For that, we convert the categorical variables into indicator variables and apply the strategy proposed in the notebook **Data_analysis** - bring the countries sharing a common area together for example. Then, I make a pipeline to train my model and I evaluate it on the test set. I have a decent error but the problem comes from a tail located in the grades below 5 and the model struggles to predict in this area, thus explaining the bad R square of the model. 


 







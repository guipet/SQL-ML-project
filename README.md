# Webscraping-SQL-ML-project
In this requisitory, we are going to web scrape informations about movies on IMDB - like the length, the title, the categoty - and create a database with SQLite, which is the easiest way for a local project. Then, we will do a small use case by trying to predict the grade of movies with the collected features. 

The programm is not intended to be executed since it is just a little project, just showing a complete work - from collecting the data to a ML approach. So, the support will be in Jupyter Notebook, easier to read and with explanations all along. 

The project is in three parts :
1. **Web Scrapping-SQL.ipynb** : how to collect the data, create the database and insert the values.  
2. **Data_analysis.ipynb**: Use SQLite to study the database.
3. **ML.ipynb**: A machine learning project with the data.

# Webscraping

The goal is to collect the data of the 10 000 most popular movies. If the movie is not rated, we will not include it because the grade is stricly necessary for our project since it is the target.   

The data are collected on this [link](https://www.imdb.com/search/title/?title_type=feature&release_date=2000-01-01,2020-12-31&start=1) from the first page to the 10000th page, with the package **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)**. This are the commons step the webscrape with **BeautifulSoup**:
* get the url with the function `get`
* parse the HTML file with `BeautifulSoup` with the type of parsor. 
* detect the `tag`, `CSS`, `class`... of the HTML file to get the informations inside. 

The final step could appear hard because it implies that you know HTML code. In reality, it is not necessary to be familiar with HTML with **BeautifulSoup**. It is very simple thanks to the [devtool inspector](https://developers.google.com/web/tools/chrome-devtools). This link is only for Chrome but you can find a lot of ressources on the web for any browser.  
This is an example: 



To go from page to page, we need to study the html link to iterate over it. The structure is very simple because there is only one thing that changes at the end : `start=num_page`. Since there are 50 movies on each page, the link for the first page is `start=1`, `start=51` for the second page and so on.... that's why we have 
```py
url_base = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2000-01-01,2020-12-31&start='
start = np.arange(1, 10000, 50)
```

To avoid a surcharge the website with our requests, we need to take a break of few seconds. This is the usefulness of this part of the code:
```py
sleep(randint(8,15))
```

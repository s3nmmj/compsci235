# Library Web Application (COMPSCI 235 Assignment 3)

## Description

This a web application to provide with browsing the books, authors, reviewing books, adding books to personal reading list, login and logout.
- Users can browse random books on the `home` page. There are always 12 books selected randomly.
- Users can browse all the books on the `books` page. There are 10 books(the number is configured in .env file `BOOKS_PER_PAGE`) and two pagination buttons displayed. Users can use the `next` and `previous` to browse all the books.
- For each book, there is a detail page, click the `Read More >>` button, will go to the book detail page. On the book detail page, users can add reviews which is login required and add the book to the personal booking list.
- Users can browse all the authors on the `authors` page. Same as the `books` page.
- For the users who have signed in, there will show a `my book` on the navigation. They can brows the books which were added by the users. 
- The application also provide the ability to register a new user. For logout, just click the logout icon.

## Python version

Please use Python version 3.6 or newer versions for development. 


## Installation

**Installation via requirements.txt**

```shell
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

## Testing with the pytest unit tests
```
$ python -m pytest -v tests
$ python -m pytest -v tests_db
```
This command run all the tests. 


## Execution of the web application

**Running the Flask application**

From the project directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

## HTML Template and CSS
The basic HTML template and CSS are from Sample COVID-19 Web Application(https://github.com/martinurschler/2021CompSci235-03-CovidWebApp) and OS Templates (https://www.os-templates.com/free-basic-html5-templates/basic-88)


## Data sources 

The data in the excerpt files were downloaded from (Comic & Graphic):
https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home

On this webpage, you can find more books and authors in the same file format as in our excerpt, for example for different book genres. 
These might be useful to extend your web application with more functionality.

We would like to acknowledge the authors of these papers for collecting the datasets by extracting them from Goodreads:

*Mengting Wan, Julian McAuley, "Item Recommendation on Monotonic Behavior Chains", in RecSys'18.*

*Mengting Wan, Rishabh Misra, Ndapa Nakashole, Julian McAuley, "Fine-Grained Spoiler Detection from Large-Scale Review Corpora", in ACL'19.*

"""
Module to read data from CSV files and HTML file
to populate an SQL database

ITEC649 2019
"""

import csv
import sqlite3
from bs4 import BeautifulSoup
from database import DATABASE_NAME, create_tables


def read_relations(db, openfile):
    """Store the relations listed in filename into the database
    - db      : a connection to a database.
    - openfile: CSV file open for reading and holding a relation per line.
    This function does not return any values. After executing this function, each row of the CSV file
    will be stored as a relation in the database.

    Example of use:
    >>> db = sqlite3.connect(DATABASE_NAME)
    >>> with open('relations.csv') as f:
    >>>    read_relations(db, f)
    """
    pass

# delimiter - A delimiter is a sequence of one or more characters used to specify the boundary between separate,
# independent regions in plain text or other data streams. Example of a delimiter is the comma character,
# which acts as a field delimiter in a sequence of comma-separated values.

    database = db

    read_csv = csv.DictReader(openfile, delimiter=',')
    for row in read_csv:
        database.execute('''insert into relations(product, location) values (?,?)''',(row['product'], row['location']))
        database.commit()


def read_locations(db, openfile):
    """Store the locations listed in the open file into the database
    - db      : a connection to a database.
    - openfile: CSV file open for reading and holding a location per line.
    This function does not return any values or print anything on screen. After executing this function,
    each row of the CSV file will be stored as a location in the database.

    Example of use:
    >>> db = sqlite3.connect(DATABASE_NAME)
    >>> with open('locations.csv') as f:
    >>>     read_locations(db, f)
    """
    pass

    database = db

    read_csv = csv.DictReader(openfile, delimiter=',')

    for row in read_csv:
        database.execute('''insert into locations values (?,?,?,?,?)''', (row['id'],row['number'],row['street'],row['city'],row['state']))
        database.commit()


def read_stock(db, openfile):
    """Read the products from the open file and store them in the database
    - db      : a connection to a database.
    - openfile: HTML file open for reading and listing products.
    This function does not return any values or print anything on screen. After executing this function,
    the products found in the HTML file will be stored as product records in the database.

    Example of use:
    >>> db = sqlite3.connect(DATABASE_NAME)
    >>> with open('index.html', encoding='utf-8') as f:
    >>>     read_stock(db, f)
    """
    pass

    database = db
    html_parser = BeautifulSoup(openfile.read(), 'html.parser')
    html_content = html_parser.find_all("div", class_="product")

    for product in html_content:
        parse_id = product.find_all("a")[0]
        product_id = parse_id.attrs["href"].split('/')[-1]

        product_description = parse_id.contents[0]

        find_stock = product.find_all("div", class_="inventory")[0].contents[0]

        stock_product = find_stock.split(' ')[0]

        value = product.find_all("div", class_="cost")[0].contents[0]

        revenue = value[0:1]
        product_cost = value[1:]

        database.execute('''insert into products values(?,?,?,?,?)''',(product_id,product_description,stock_product,product_cost,revenue))
        database.commit()

def report(db, openfile):
    """Generate a database report and store it in outfile
    - db      : a connection to a database
    - openfile: a CSV file open for writing
    This function does not return any values or print anything on screen. After executing this function,
    the file outfile will contain the product information, one row in the CSV file per product. Each row must
    contain the following information:
      - description
      - price (including the currency symbol)
      - amount in stock
      - store location

    Example of use:
    >>> db = sqlite3.connect(DATABASE_NAME)
    >>> with open('report.csv', 'w') as f:
    >>>     report(db, open('report.csv', 'w'))
    """
    pass

def main():
    """Execute the main code that calls all functions
    This code should call the above functions to read the files "relations.csv",
    "locatons.csv" and "index.html", and generate "report.csv" as described in
    the assignment specifications.
    """
    db = sqlite3.connect(DATABASE_NAME)
    create_tables(db)

    # Write your code below
    database = db

    with open('relations.csv') as f:
        read_relations(database, f)

    with open('locations.csv') as f:
        read_locations(database,f)

    with open('index.html', encoding='utf-8') as f:
        read_stock(database,f)

# Do not edit the code below
if __name__=='__main__':
    main()

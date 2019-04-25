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

    #reading the csv file.
    read_csv = csv.DictReader(openfile, delimiter=',')

    # Inserting all the values of product and location into the database.
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

    #reading the csv file.
    read_csv = csv.DictReader(openfile, delimiter=',')

    # Inserting all the values of id, number, street, city and state into the database.
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

    # Using beautifulsoup, parsing all the values of the HTML page and put it in html_parser.
    html_parser = BeautifulSoup(openfile.read(), 'html.parser')

    # Only selecting the product class which is in the DIV.
    html_content = html_parser.find_all("div", class_="product")


    for product in html_content:

        # Taking all the product number and using split, where discarding '/' in the href,
        # only collecting the number which is at the end of the href link.
        # For example, "a href="https://ilearn.mq.edu.au/product/0",
        # In here getting all the 'a' and from there, discarding "https://ilearn.mq.edu.au/product/" this
        # gives us the number for this example, it would be 0.
        # -1 is indicating the array index where the '0' is stored.
        parse_id_number = product.find_all("a")[0]
        product_id = parse_id_number.attrs["href"].split('/')[-1]


        # Taking the description of 'Ocean Blue Shirt' from the
        # '<a href="https://ilearn.mq.edu.au/product/0">Ocean Blue Shirt</a>'
        product_description = parse_id_number.contents[0]

        # In the find_stock variable, storing all the data of inventory class in DIV.
        # stock_product is storing the 0 index value and discard anything after ' ' or space.
        # For example, in this line of code '<div class="inventory">0 in stock</div>',
        # stock_product is storing only the value (0).
        find_stock = product.find_all("div", class_="inventory")[0].contents[0]
        stock_product = find_stock.split(' ')[0]

        # In the find_stock variable, storing all the data of cost class in DIV.
        value = product.find_all("div", class_="cost")[0].contents[0]

        # Revenue variable store all the value between 0 and 1 in cost class and the value is '$'
        revenue = value[0:1]

        # And for the product_cost variable, it store any value after the '$' and onwards.
        product_cost = value[1:]

        # Inserting these values into the database.
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

    database = db

    # main_database storing all the data from the database by using database.execute
    main_database = database.execute('''SELECT products.description, products.price, products.currency, products.stock, locations.number||', '||locations.street||', '||locations.city||', '||locations.state As "location" FROM 'products' join 'locations' join 'relations' where relations.product = products.id and relations.location = locations.id order by products.price asc;''')

    # writer_csv contains 'description', 'price', 'currency', 'stock' and 'location' in rows
    writer_csv = csv.writer(openfile)
    writer_csv.writerow(['description', 'price', 'currency', 'stock', 'location'])

    # Writing all the values in a row one at a time.
    for row_line in main_database:
        writer_csv.writerow(row_line)

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

    # Calling relations.csv
    with open('relations.csv') as f:
        read_relations(database, f)

    # Calling locations.csv
    with open('locations.csv') as f:
        read_locations(database,f)

    # Parsing the HTML for stock value of products.
    with open('index.html', encoding='utf-8') as f:
        read_stock(database,f)

    # Calling report.csv
    with open('report.csv', 'w') as f:
        report(database, open('report.csv','w'))

# Do not edit the code below
if __name__=='__main__':
    main()

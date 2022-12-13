import os

import mongodb
from application_config_setter import configure_app
from crawler import crawler_consume_url
from product_finder import find_products_by_name


def init():
    print("We will check how many products there are in this fitness website!")
    file = open("last_searches.txt", "r+")
    if os.path.getsize('last_searches.txt') != 0:
        last_line = file.readlines()[-1]
        if last_line:
            print("Your last search: {}".format(last_line))
    product_name = input('Enter the name of your desired brand/product: ')
    file.write("{} \n".format(product_name))
    file.close()
    print("Loading....")
    configure_app()
    connection_string = "mongodb://{}:{}@mongo:27017/".format(os.getenv('DB_USER'), os.getenv('DB_PASS'))
    mongo_client = mongodb.start_db_client(connection_string)
    seed_url = os.getenv('SEED_URL')
    scraped_links = crawler_consume_url(seed_url, 1)
    hyper_links_dic = scraped_links[0]['urls']
    product_count, products_array = find_products_by_name(product_name, hyper_links_dic)
    database = mongo_client["scraping"]

    collection = database["sites_collection"]
    # insert_result = collection.insert_many(scraped_links)
    # print(scraped_links)

    print("-----------------------------------------------")
    if len(products_array) == 0:
        print("No items were found.")
    else:
        print("We have found {} items which match your brand's name".format(product_count))
        print("The following products from this brand are:")
        print(products_array)
    print("-----------------------------------------------")


if __name__ == '__main__':
    init()

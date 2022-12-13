def find_products_by_name(name, hyper_links_dic):
    products_array = []
    product_occurrences = 0
    for key in hyper_links_dic:
            if key.__contains__(name):
                product_occurrences += 1
                products_array.append(key)
    return product_occurrences, products_array
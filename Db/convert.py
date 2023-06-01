def convert_list_for_other_types(list_of_tuples):
    output = []
    list_tuple = list(list_of_tuples)
    for items in list_tuple:
        list_items = list(items)
        clear_items = list_items[0]
        output.append(clear_items)
    return output
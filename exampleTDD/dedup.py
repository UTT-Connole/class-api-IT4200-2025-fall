
def deduplicate(input_list):
    new_list = []
    for i in range(0, len(input_list)):
        if input_list[i] not in new_list:
            new_list.append(input_list[i])
    return new_list

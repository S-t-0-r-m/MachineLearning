import json


def format_element(element: dict[str, str], element_name: str) -> str:
    formated = ""

    for key, value in element.items():
        if key == "type":
            formated =  formated + value + "#" + element_name +"{"
            continue

        formated =  formated + key + ": " + value + " "
    return  formated + "}"


def format_file(style_dict: dict[str, str]):
    formated_file = ""

    for key, value in style_dict.items():
        formated_file = formated_file + format_element(value, key) + "\n"
    
    return formated_file


def load_element_dict(file_name: str, element_name: str) -> str:

    with open(f"./app/style/{file_name}.json") as file:
        json_dict = json.load(file)[element_name]

    return json_dict


def load_file_dict(file_name: str):

    with open(f"./app/style/{file_name}.json") as file:
        json_dict = json.load(file)

    return json_dict


    





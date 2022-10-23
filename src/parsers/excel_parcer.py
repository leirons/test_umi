import requests

from io import BytesIO

import pandas as pd


# Если бы файлов было бы больше, то работал бы через другой способ, именно напрямую с google sheets.
# Или же просто развил бы данный способ


def get_values():
    files = {
        "Products": "https://docs.google.com/spreadsheet/ccc?key=1roypo_8amDEIYc-RFCQrb3WyubMErd3bxNCJroX-HVE&output=csv",
        "Reviews": "https://docs.google.com/spreadsheet/ccc?key=1iSR0bR0TO5C3CfNv-k1bxrKLD5SuYt_2HXhI2yq15Kg&output=csv",
    }
    first = requests.get(files["Products"])
    second = requests.get(files["Reviews"])

    products = first.content
    reviews = second.content

    products = pd.read_csv(BytesIO(products))
    reviews = pd.read_csv(BytesIO(reviews))

    return products.values, reviews.values


get_values()

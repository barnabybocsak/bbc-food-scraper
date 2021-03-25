import requests
from bs4 import BeautifulSoup
import csv
import time
import lxml

allIngredients = []
recipeID = -1
ingredientID = 0


def get_links():
    url = "https://www.bbc.co.uk/food/sitemap.xml"

    document = requests.get(url)

    soup = BeautifulSoup(document.text, "lxml-xml")

    links = []
    for line in soup.find_all('loc'):
        for string in line.stripped_strings:
            if string.startswith('https://www.bbc.co.uk/food/recipes/'):
                links.append(string)

    return links


def get_recipe_entry(link):
    global recipeID
    global ingredientID
    ingredients = []
    recipeQuantity = []
    title = ""
    method = ""
    recipeID += 1

    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    for item in soup.find_all('li', class_='recipe-ingredients__list-item'):
        recipeQuantity.append(item.contents[0])
        ingredients.append(item.contents[1].text)
        if item.contents[1].text.lower() not in allIngredients:
            allIngredients.append(item.contents[1].text)
            writer1.writerow([ingredientID, item.contents[1].text])
            ingredientID += 1

    title = soup.find(class_='gel-trafalgar content-title__text').text
    for item in soup.findAll(class_='recipe-method__list-item-text'):
        method = method + item.text + "\n"

    writer2.writerow([recipeID, title, method])

    for i in range(len(ingredients)):
        writer3.writerow([allIngredients.index(ingredients[i]), recipeID, recipeQuantity[i]])

    print(title)
    #print(method)
    #print(recipeQuantity)
    #print(ingredients)
    print(link)


file1 = open("ingredients.csv", 'a', newline='')
writer1 = csv.writer(file1)
writer1.writerow(["IngredientID", "IngredientName"])

file2 = open("recipes.csv", 'a', newline='')
writer2 = csv.writer(file2)
writer2.writerow(["RecipeID", "RecipeName", "RecipeMethod"])

file3 = open("recipeQuantity.csv", 'a', newline='')
writer3 = csv.writer(file3)
writer3.writerow(["IngredientID", "RecipeID", "RecipeQuantity"])


links = get_links()
print(len(links))

for i in range(len(links)):
    try:
        get_recipe_entry(links[i])
    except:
        print("Not found")

for item in range(len(allIngredients)):
    writer1.writerow([item, allIngredients[item]])

file1.close()
file2.close()
file3.close()
import json


class Pizza:

    def __init__(self, name, price, ingredients):
        self.name = name
        self.price = price
        self.ingredients = ingredients


def getPizzas():
    with open('pizzas.json') as json_file:
        data = json.load(json_file)

        pizzas = list()

        for pizza in data:
            p = Pizza(pizza['name'], pizza['price'], pizza['ingredients'])

            pizzas.append(p)

        return pizzas


def rating(pizzas):
    tot = set()
    for pizza in pizzas:
        for ingredient in pizza.ingredients:
            tot.add(ingredient)

    return len(tot)


def pricePerUniqueIngredient(ingredients, pizza):
    # return price of pizza divided by number of ingredients it has not already in the passed list
    tot = 0
    for ing in pizza.ingredients:
        if ing not in ingredients:
            tot += 1
    if tot > 0:
        return pizza.price / tot
    else:
        return 1000


def pricePerIngredient(pizza):
    return pricePerUniqueIngredient((),pizza)


def uniqueIngredients(pizzas):
    tot = set()
    for pizza in pizzas:
        for ingredient in pizza.ingredients:
            tot.add(ingredient)

    return tot


### START HERE ###
pizzas = getPizzas()
checkout = []  # the list of pizzas we are going to buy
subtotal = 0  # the cost of those pizzas


# Highest possible score: 65/65 as other teams have this score
# First we try

# Make dictionary (map) of cheapest price each ingredient is available for
# ingredients = dict()
# for pizza in pizzas:
#     for ingredient in pizza.ingredients:
#         if ingredient not in ingredients or pizza.price < ingredients[ingredient]:
#             ingredients[ingredient] = pizza.price

# We learn you can get any of all 65 ingredients for 52kr or less,
# but if you want to ensure you have all 65 that would be about 3250kr
# You need to buy pizzas that have good combinations of ingredients


# next we try

# Sort pizzas by price per ingredient
# pizzas = sorted(pizzas, key=pricePerIngredient)
# for pizza in pizzas:
#     if subtotal + pizza.price <= 1000:
#         # Add pizzas while we can still afford it
#         checkout.append(pizza)
#         subtotal += pizza.price
#
#         # Now sort the list again but this time by price per new unique ingredient
#         # (ingredients that we dont already have in the checkout)
#         pizzas.remove(pizza)
#         pizzas = sorted(pizzas, key=lambda pizza: pricePerUniqueIngredient(uniqueIngredients(checkout), pizza))
#     else:
#         break

# Result is 61 ingredients, decent but can be better.


# Next we try

# Backtracking? Maybe we still use the price sorted list and we just add and backtrack pizzas until we have all 65
pizzas = sorted(pizzas, key=pricePerIngredient)

# Pointers points to a pizza index, the hypothetical checkout is just the combination of the pizzas at the pointers
pointers = []
pointers.append(0)  # starting pointer, we add the first pizza
done = False
while not done:
    i = 0
    for pointer in pointers:
        subtotal += pizzas[pointer].price
        if subtotal < 1000:
            # We can afford to buy more pizzas, so add another pointer at the next pizza in the line.
            pointers.append(max(pointers) + 1)
        elif len(uniqueIngredients(checkout)) == 65 and subtotal <= 1000:
            # We found our checkout, we are done
            done = True
            break
        else:
            # we've run out of money, time to move some pointers around
            pointers[i] += 1
        i += 1

# sort pizzas by price
# add pointers until we can't afford any more
#

print(subtotal)
print(len(uniqueIngredients(checkout)))
print(checkout)
string = ""
for pizza in checkout:
    string += pizza.name + ", "

print(string)








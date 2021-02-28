import json
import time


class Pizza:

    def __init__(self, name, price, ingredients):
        self.name = name
        self.price = price
        self.ingredients = ingredients


def getPizzas():
    with open('lesspizzas.json') as json_file:
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
    return pricePerUniqueIngredient((), pizza)


def uniqueIngredients(pizzas):
    tot = set()
    if pizzas:
        if(isinstance(pizzas, list)):
            for pizza in pizzas:
                for ingredient in pizza.ingredients:
                    tot.add(ingredient)
        else:
            for ingredient in pizzas.ingredients:
                tot.add(ingredient)
    return tot


def pizzaListPrice(pizzas):
    tot = 0
    for pizza in pizzas:
        tot += pizza.price

    return tot


### START HERE ###

pizzas = getPizzas()
checkout = []  # the list of pizzas we are going to buy
subtotal = 0  # the cost of those pizzas

# If a pizza has at least all the same ingredients as another pizza and is either cheaper or the same price, remove it.
# i = 0
# for pizza in pizzas:
#     i+=1
#     if i%100==0:
#         print("Checked {} pizzas".format(i))
#     for pizza2 in pizzas:
#         if pizza != pizza2:
#             if pizza2.price >= pizza.price:
#                 if set(pizza2.ingredients).issubset(pizza.ingredients):
#                     pizzas.remove(pizza2)
#                     break
#             elif pizza.price >= pizza2.price:
#                 if set(pizza.ingredients).issubset(pizza2.ingredients):
#                     pizzas.remove(pizza)
#                     break
# # From 10000 pizzas to 7241 pizzas.
# # Write this to new file:
# data = []
# for pizza in pizzas:
#     data.append({
#         'name': pizza.name,
#         'price': pizza.price,
#         'ingredients': pizza.ingredients
#     })
#
# with open('lesspizzas.json', 'w') as outfile:
#     json.dump(data, outfile)

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
# pizzas = sorted(pizzas, key=pricePerIngredient)

# Pointers points to a pizza index, the hypothetical checkout is just the combination of the pizzas at the pointers
# pointers = []
# pointers.append(0)  # starting pointer, we add the first pizza
# done = False
# while not done:
#     i = 0
#     for pointer in pointers:
#         subtotal += pizzas[pointer].price
#         if subtotal < 1000:
#             # We can afford to buy more pizzas, so add another pointer at the next pizza in the line.
#             pointers.append(max(pointers) + 1)
#         elif len(uniqueIngredients(checkout)) == 65 and subtotal <= 1000:
#             # We found our checkout, we are done
#             done = True
#             break
#         else:
#             # we've run out of money, time to move some pointers around
#             pointers[i] += 1
#         i += 1
#
# # sort pizzas by price
# # add pointers until we can't afford any more
#

# Backtracking
# pizzas = sorted(pizzas, key=pricePerIngredient)
# for pizza in pizzas:
#     subtotal = pizza.price
#     # Sort list according to the pizza we're starting the combination with
#     # pizzas2 = sorted(pizzas, key=lambda pizza: pricePerUniqueIngredient(uniqueIngredients(checkout), pizza))
#     pizzas2 = sorted(pizzas, key=lambda p: p.price)
#     pizzas2.remove(pizza)
#     pointers = [0]
#     for pointer in pointers:
#         subtotal += pizzas2[pointer]
#
#     if subtotal > 1000:
#         pointers.pop()
#         pointers[-1] += 1

start_time = time.time()

def recursive_backtracking(pizzas, checkout, printout=0):
    """

    :param pizzas: List of pizzas, sorted by price
    :param checkout: list of pizzas we are planning to buy in this path
    :return: checkout, or false if this is a dead end
    """

    if len(pizzas) == 0:
        print("Found dead end: list empty")
        return False
    for i in range(1, len(pizzas)):
        if pizzaListPrice(checkout) + pizzas[i].price > 1000:
            # Can't afford this, or any of the other pizzas in the list
            #print("Found dead end: price too high")
            return False
        if len(uniqueIngredients(checkout + [pizzas[i]])) >= 65:
            checkout.append(pizzas[i])
            print("Level {} - Kollat {}: {}".format(printout, i, pizzas[i]))
            return checkout
        else:
            checkout.append(pizzas[i])
            ret = recursive_backtracking(pizzas[i+1:], checkout, printout-1)
            if ret:
                return ret
        checkout.pop()
        if printout > 0:
            print("Level {} - Kollat {}: {}".format(printout, i, pizzas[i]))
            print("--- %s seconds ---" % (time.time() - start_time))

    return False



pizzas = sorted(pizzas, key=lambda p: p.price)

for pizza in pizzas:
    if len(pizza.ingredients) < 10:
        pizzas.remove(pizza)

print(len(pizzas))

outputlist = recursive_backtracking(pizzas, [], 17)

print(pizzaListPrice(outputlist))
print(len(uniqueIngredients(outputlist)))
for p in outputlist:
    print("{},".format(p.name), end="")




# print(subtotal)
# print(len(uniqueIngredients(checkout)))
# print(checkout)
# string = ""
# for pizza in checkout:
#     string += pizza.name + ", "
#
# print(string)
#
# for*

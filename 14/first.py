import sys # argv
import math # ceil
from collections import defaultdict

from typing import Tuple


# load the recipes
def parse_chemical(s: str) -> Tuple[int, str]:
    n, chem = s.strip().split(' ')
    return int(n), chem
with open(sys.argv[1]) as f:
    recipes = {}
    for line in f:
        inputs, product = line.split('=>')
        inputs = [parse_chemical(s) for s in inputs.split(',')]
        produced_amount, chem = parse_chemical(product)
        assert chem not in recipes, f"More than one recipe for {chem}"
        recipes[chem] = (inputs, produced_amount)

# find the required amount of ore
required = defaultdict(int, FUEL=1)
def get_next_requirement() -> Tuple[str, int]:
    for chem, amt in required.items():
        if chem != 'ORE' and amt > 0:
            return chem, amt
    raise KeyError("No remaining non-ORE requirements")
while True:
    try:
        required_chem, required_amt = get_next_requirement()
    except KeyError:
        break
    recipe_inputs, produced_per_recipe = recipes[required_chem]
    num_recipe_repeats = math.ceil(required_amt / produced_per_recipe)
    for input_amt, input_chem in recipe_inputs:
        required[input_chem] += input_amt * num_recipe_repeats
    required[required_chem] -= produced_per_recipe * num_recipe_repeats

print(required['ORE'])

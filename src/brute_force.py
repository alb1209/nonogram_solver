from game import NonoGame
from itertools import product
import time


# start = time.monotonic()
# for idx in range(2**25):
#     if idx % 10000 == 0:
#         end = time.monotonic()
#     print(bin(idx)[2:].rjust(25, '0').replace("0", "O").replace("1", "X"))
#     if idx == 100:
#         break
#     # print(f"Progression: {idx / (2**25) :7.2%} {end-start : 8.2f}", end='\r')

from itertools import batched

start = time.monotonic()
for idx, trial in enumerate(product(*["OX" for _ in range(25)])):
    print(list(batched(trial, 5)))
    end = time.monotonic()
    print(f"Progression: {idx / (2**25) :7.2%} {end-start : 8.2f}", end='\r')
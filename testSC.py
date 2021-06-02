
import time
from itertools import chain
import numpy as np

# Set Cover with cost constraint
def setCover(sets,set_reminder,budget,weights):
    min_element = -1
    for i,s in enumerate(sets):
        if len(s.intersection(set_reminder)) > 0:
            try:
                cost = weights[i]/(len(s.intersection(set_reminder)))
                if cost <= budget:
                    budget = cost
                    min_element = i
            except:
                pass
    return(sets[min_element],weights[min_element],min_element)

cover = []
costs = []
pos = []
timeout = time.time() + 60*0.1  # 6 seconds from now
sets = [set([1,2]),set([1,3,4]),set([3,5]),set([2,3]),set([1,4])]
universe = set([1,2,3,4,5])
set_reminder = universe
budget = 5
weights = [3,4,1,4,5]
while len(set_reminder) != 0 and budget != 0:
    if time.time() > timeout:
        break
    set_i, cost_i, loc = setCover(sets,set_reminder,budget,weights)
    print(f'cost:{cost_i}')
    if loc != -1:
        cover.append(set_i)
        set_reminder = set_reminder.difference(set_i)
        costs.append(cost_i)
        pos.append(loc)
        budget = budget - cost_i
        print(f'budget:{budget}')
    time.sleep(1)

res = [i for set in cover for i in set]
print(np.unique(res))

if len(np.unique(res)) == len(universe):
    print(f'SCC: cover={cover}---{sum(costs)},{costs}----{pos}')
    # return(cover,costs,pos)
else:
    print('No cover')
    # return([],[],[])

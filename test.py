# import numpy as np
# import pandas as pd
# import math
#
# Budget = 7
# controls_pair = [[1,2],[3,4],[5,6]]
# cost_matrix = [[[1.2],[2.032]],[[2.5],[4]],[[1.3],[3.3]]]
# efficacy_matrix_l1 = [[0.3,0.6],[0.3,0.9],[0.1,0.4]]
#
# knapsack_matrix = [[0 for x in range(Budget+1)] for x in range(len(controls_pair)+1)]
# print(pd.DataFrame(knapsack_matrix))
# for j in range(len(controls_pair)+1):
#     for c in range(Budget+1):
#         if j == 0 or c == 0:
#             knapsack_matrix[j][c] = 0
#         else:
#             knapsack_matrix[j][c] = knapsack_matrix[j-1][c]
#             for i in range(2):
#                 if c >= (cost_matrix[j-1][i][0]):
#                     # if knapsack_matrix[j][c] < knapsack_matrix[j-1][c-math.floor(cost_matrix[j][i][0])]+efficacy_matrix_l1[j][i]:
#                         # solution_matrix[j][c][i] = 1
#                     knapsack_matrix[j][c] = max(knapsack_matrix[j][c],(knapsack_matrix[j-1][c-math.floor(cost_matrix[j-1][i][0])]+efficacy_matrix_l1[j-1][i]))
#                     # print(knapsack_matrix[j][c])
#                 # else:
#                 #     knapsack_matrix[j][c] = max(knapsack_matrix[j-1][c],knapsack_matrix[j][c])
#
# print(pd.DataFrame(cost_matrix))
# print(pd.DataFrame(efficacy_matrix_l1))
# print(pd.DataFrame(knapsack_matrix))
#
# n=len(controls_pair)
# res = knapsack_matrix[n][Budget]
# print(res)
#
# sol = []
# w = Budget
# for i in range(n, 0, -1):
#     print(f'i={i}')
#     print(f'k[i-1][w]--{knapsack_matrix[i - 1][w]}')
#     if res <= 0:
#         break
#     if res == knapsack_matrix[i - 1][w]:
#         continue
#     else:
#         max_value = max(efficacy_matrix_l1[i-1])
#         max_index = efficacy_matrix_l1[i-1].index(max_value)
#         min_value = min(efficacy_matrix_l1[i-1])
#         min_index = efficacy_matrix_l1[i-1].index(min_value)
#         if  cost_matrix[i-1][max_index][0] <= w:
#             sol.append((i-1,max_index, max_value))
#             res = res - max_value
#             w = w - math.ceil(cost_matrix[i-1][max_index][0])
#         elif cost_matrix[i-1][min_index][0] <= w:
#             sol.append((i-1,min_index, min_value))
#             res = res - min_value
#             w = w - math.ceil(cost_matrix[i-1][min_index][0])
#         else:
#             continue
#
#
# print(sol)

import pygal
dot_chart = pygal.Dot(x_label_rotation=30)
dot_chart.title = 'V8 benchmark results'
dot_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace', 'EarleyBoyer', 'RegExp', 'Splay', 'NavierStokes']
dot_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
dot_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
dot_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
dot_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])
dot_chart.render_to_file('pygal.pdf')

# This Python file uses the following encoding: utf-8

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
# Some data
labels = 'FP','NSF'
explode=(0, 0.05)

clustering_results = [
    (2, 12), (4, 11), (7, 4), (5, 3), (2, 12), (8, 7), (4, 3), (0, 24), (0, 23), 
    (5, 4), (2, 9), (11, 10), (1, 15), (0, 8), (1, 12), (4, 5), (11, 35), (5, 8), 
    (3, 8), (4, 25), (5, 0), (2, 8), (15, 11), (3, 9), (0, 8), (11, 1), (42, 5), 
    (14, 2), (1, 6), (8, 4), (8, 4), (5, 0), (7, 8), (1, 6), (3, 8), (1, 5), (2, 6), 
    (3, 8), (1, 16), (1, 5), (1, 7), (16, 2), (2, 18), (4, 1), (0, 4), (20, 0), 
    (5, 24), (0, 6), (1, 4), (4, 5), (4, 3), (6, 1), (11, 6), (12, 11)
]

conb = [(x, y) for x in xrange(0,8) for y in xrange(0,8)]
the_grid = GridSpec(8, 8)


print clustering_results[0][0]
for i, (x, y) in enumerate(conb):
    if i < 54:
        print i
        fracs = [clustering_results[i][0], clustering_results[i][1]]
        plt.subplot(the_grid[x, y], aspect=1)
        patches, texts, autotexts = plt.pie(fracs, explode=explode,
                                        labels=labels, autopct='%.0f%%',
                                        shadow=False)
        numbers_projects = clustering_results[i][0]+clustering_results[i][1]
        title = "%s|%s" %(i, numbers_projects)
        # title = "c%s" %(i)
        # print title
        plt.title(title)
        autotexts[0].set_color('y')



plt.show()
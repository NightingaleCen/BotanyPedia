plants1 = ['plant1', 'plant2', 'plant3', 'plant4']
plants2 = ['plant1', 'plant2', 'plant3', 'plant4']
r = [(p1, p2) for p1 in plants1 for p2 in plants1 if p1 != p2]
print(r)
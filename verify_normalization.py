slr = [12.1, 32.0, 77.8, 99.1, 78.3]
coral = [-0.05, 0.10, 0.08, 0.17, 0.68]

slr_norm = [(v - min(slr))/(max(slr)-min(slr)) for v in slr]
coral_norm = [(v - min(coral))/(max(coral)-min(coral)) for v in coral]

print("SLR norm:", [round(v, 3) for v in slr_norm])
print("Coral norm:", [round(v, 3) for v in coral_norm])
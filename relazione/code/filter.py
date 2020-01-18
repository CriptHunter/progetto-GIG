for i, p in enumerate(points[:-1]):
    dt = dt + (points[i+1][6] - points[i][6]).total_seconds()
    if dt >= t:
        points_filtered.append(p)
        dt = dt - t

if dt >= t: #l'ultimo punto
    points_filtered.append(points[-1])
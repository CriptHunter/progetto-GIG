for i, p in enumerate(points[:-1]):
    data = (points[i][0], points[i+1][0], )
    cursor.execute(distance_query, data)
    for row in cursor.fetchall():
        ds = ds + row[0]
    if ds >= t:
        points_filtered.append(p)
        ds = ds - t
if ds >= t: #l'ultimo punto
    points_filtered.append(points[-1])
def fix_isolated_point(plist):
	k = 1
	for elem in plist[1:-1]:
		if plist[k-1][1] == plist[k+1][1]:
			plist[k] = (plist[k][0], plist[k+1][1])
		elif plist[k-1][1] != elem[1] and elem[1] != plist[k+1][1]:
			plist[k] = (plist[k][0], plist[k+1][1])
		k = k + 1
	return plist
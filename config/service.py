

def getDistanceBetween(them, us):
    total = 0
    for i in range(len(them)):
        total += (them[i]-us[i])**2
    distance = abs(math.sqrt(total))
    return distance

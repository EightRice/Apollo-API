class Service:
    def getDistanceBetween(them, us):
        total = 0
        for i in range(len(them)):
            if them[i]-us[i] > 0:
                us[i] = them[i]
            total += (them[i]-us[i])**2
        distance = abs(math.sqrt(total))
        return distance

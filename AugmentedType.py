
class AugmentedType:
    def __init__(self,name,color,typenum,numberOfBaseTypes):
        self.typenum = typenum
        self.color = color
        self.numberOfBaseTypes = numberOfBaseTypes
        self.name = name
        self.totalWins =0
        self.totalGames =0 
    def getWinPercent(self):
        return self.totalWins/self.totalGames

class Team:
    def __init__(self,teamTypes):
        self.teamTypes = teamTypes
        self.lossStreak = 0
        self.totalGames = 0
        self.totalWins = 0
    def getWinPercent(self):
        if(self.totalGames ==0):
            return 0
        return self.totalWins/self.totalGames
    def incrementTotalLosses(self,lossStreakCutoff,winPercentCutoff):
        self.totalGames+=1
        self.lossStreak+=1
        if(self.lossStreak>=lossStreakCutoff or(self.totalWins/self.totalGames<winPercentCutoff and self.totalGames>lossStreakCutoff*2)):
            return True
        return False
    def incrementTotalWins(self):
        self.totalWins+=1  
        self.lossStreak =0 
        self.totalGames+=1 
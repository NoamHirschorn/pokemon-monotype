from pokemonData import *
from AugmentedType import AugmentedType
from Team import Team
from itertools import combinations
import numpy as np
import random
import heapq
import matplotlib.pyplot as plt

#How many types define the team
numTypesPerTeam = 2
#How does facing a team immune to all of your STAB(s) affect your chances (value is 1 vs normal effectiveness)
immunityCoeff = 0.002
#How does facing a team resitant to all of your STAB(s) affect your chances (value is 1 vs normal effectiveness)
resistedCoeff = 0.5
#How does facing a team vulnerable to at least one of your STAB(s) affect your chances (value is 1 vs normal effectiveness)
supereffectiveCoeff = 2.0
#How many teams will each type combo start as having
numTeamsPerType = 3
#How heavily will a team looking to switch types favor a team good vs the current meta vs picking randomly
skewLevel = 8
#Is Meta defined by the types of the teams with highest winning percentage (True), or by what are currently the most commmon teams (False)
metaByWinningPercent = False
#A team with how many consecutive losses will switch types
lossStreakCutoff =8
#A team below what winning percetage will switch types
winPercentCutoff = 0.4 
#How many teams are looked at to determine what is the current meta 
numBestTeams = 3
#How many rounds should the simulation run (1 round = each team having a battle)
numRounds = 3000



Table = makeTable(immunityCoeff,resistedCoeff,supereffectiveCoeff)

def generateTypes(numTypesPerTeam):
    Types = []
    combs = list(combinations(basetypenames, numTypesPerTeam))
    
    for typeCombo in combs:
        name = ''.join(typeCombo)
        indexes = [0 for _ in range(numTypesPerTeam)]
        for ind,baseType in enumerate(typeCombo):
            indexes[ind] = basetypenames.index(baseType)
        color = basetypecolors[indexes[numTypesPerTeam-1]]
        tempType = AugmentedType(name,color,indexes,numTypesPerTeam)
        Types.append(tempType)
    return Types

def setUpBattle(Type1,Type2):
   
    Type1Score = 0
    Type2Score = 0
    Type1BestScore = 0
    Type2BestScore = 0
    # print(Type1.name+" \n")
    # print(Type2.name+" \n")
    for Type1Basetype in Type1.typenum:
        Type1Score =1
        for Type2Basetype in Type2.typenum:
            Type1Score *= Table[Type1Basetype][Type2Basetype]
        # print("Round checking \n")
        # print(basetypenames[Type1Basetype]+'\n')
        # print(Type1Score)
        if(Type1Score>Type1BestScore):
            Type1BestScore = Type1Score
    for Type2Basetype in Type2.typenum:
        Type2Score =1
        for Type1Basetype in Type1.typenum:
            Type2Score *= Table[Type2Basetype][Type1Basetype]
        if(Type2Score>Type2BestScore):
            Type2BestScore = Type2Score
    return Type1BestScore/(Type1BestScore+Type2BestScore)
    
def battle(Team1,Team2):
    Type1 = Team1.teamTypes
    Type2 = Team2.teamTypes
    Type1WinChance = setUpBattle(Type1,Type2)
    
    # print('Best Scores: \n')
    # print(Type1BestScore)
    # print(Type2BestScore)
    # print('Win Chances: \n')
    # print(Type1WinChance)
    if(np.random.rand()<Type1WinChance):
        #Type1 Won
        return True
    #Type 2 Won
    return False


#generate list of types
Types = generateTypes(numTypesPerTeam)

#generate list of teams
Teams = ["" for _ in range(len(Types)*numTeamsPerType)]
for i in range(len(Types)):
    for j in range(numTeamsPerType):
        teamInd = i*numTeamsPerType+j
        Teams[teamInd] = Team(Types[i])


#create list of indices
teamlist = list(range(len(Teams)))

def battleMaker():
    random.shuffle(teamlist)
    pairings = np.array_split(teamlist, len(Teams)/2)
    for teampair in pairings:
        Teams[teampair[0]].teamTypes.totalGames+=1
        Teams[teampair[1]].teamTypes.totalGames+=1
        team1winner = battle(Teams[teampair[0]],Teams[teampair[1]])
        if(team1winner):
            winner = 0
            loser = 1
        else: 
            winner = 1
            loser = 0
        Teams[teampair[winner]].teamTypes.totalWins+=1
        Teams[teampair[winner]].incrementTotalWins()
        getNewTypes = Teams[teampair[loser]].incrementTotalLosses(lossStreakCutoff,winPercentCutoff)
        if(getNewTypes):
            newType = findNewType()
            Teams[teampair[loser]] = Team(newType)
    

def getTopTeamsWinningPercent(Top = True):
    winpercents = [0 for _ in range(len(Teams))]
    for i in range(len(Teams)):
        winpercents[i] = round(100*Teams[i].getWinPercent())
    if(Top):
        metaTeams = heapq.nlargest(numBestTeams, enumerate(winpercents),key=lambda x: x[1])
    else:
        metaTeams = heapq.nsmallest(numBestTeams, enumerate(winpercents),key=lambda x: x[1])
    metaTeams = [[x[0] for x in metaTeams],[x[1] for x in metaTeams]]
    return metaTeams

def getMostUsedTypes(Top = True):
    used = [0 for _ in range(len(Types))]
    for i in range(len(Teams)):
        used[Types.index(Teams[i].teamTypes)]+=1
    if(Top):
        metaTypes = heapq.nlargest(numBestTeams, enumerate(used),key=lambda x: x[1])
    else:
        metaTypes = heapq.nsmallest(numBestTeams, enumerate(used),key=lambda x: x[1])
    metaTypes = [[x[0] for x in metaTypes],[x[1] for x in metaTypes]]
    return metaTypes

def findNewType():
    WeightedVotes = [1 for _ in range(len(Types))]
    if(metaByWinningPercent):
        metaTeams = getTopTeamsWinningPercent()
        percents = metaTeams[1]
        metaTeams = metaTeams[0]
        WeightedPercents = percents/np.sum(percents)
        for metaTeamIndex in range(len(metaTeams)):
            metaType = Teams[metaTeams[metaTeamIndex]].teamTypes
            for ind,newType in enumerate(Types):
                chancesWinning = setUpBattle(newType,metaType)
                WeightedVotes[ind]+=(chancesWinning**skewLevel)*WeightedPercents[metaTeamIndex]
    else:
        metaTypes = getMostUsedTypes()
        percents = metaTypes[1]
        metaTypes = metaTypes[0]
        WeightedPercents = percents/np.sum(percents)
        for metaTypeIndex in range(len(metaTypes)):
            metaType = Types[metaTypes[metaTypeIndex]]
            for ind,newType in enumerate(Types):
                    chancesWinning = setUpBattle(newType,metaType)
                    WeightedVotes[ind]+=(chancesWinning**skewLevel)*WeightedPercents[metaTypeIndex]
    #have array sum to 1
    WeightedVotes = WeightedVotes/np.sum(WeightedVotes)
    #hold election
    result = np.random.choice(len(Types),1,p=WeightedVotes)
    return Types[int(result)]

def findBestPerformingTypes():
    winpercents = [0 for _ in range(len(Types))]
    for i in range(len(Types)):
        winpercents[i] = round(10000*Types[i].getWinPercent())
    bestPercents =  heapq.nlargest(3, enumerate(winpercents),key=lambda x: x[1])
    bestTypes =  [x[0] for x in bestPercents]
    bestPercents =  [x[1] for x in bestPercents]
    #bestTeamsAtEnd = getTopTeamsWinningPercent()
    # print("Best Type at end of Season:")
    # print(Teams[bestTeamsAtEnd[0]].teamTypes.name +" : "+ str(100*Teams[bestTeamsAtEnd[0]].teamTypes.getWinPercent()))
    # print("2nd Best Type at end of Season:")
    # print(Teams[bestTeamsAtEnd[1]].teamTypes.name +" : "+ str(100*Teams[bestTeamsAtEnd[1]].teamTypes.getWinPercent()))
    # print("3rd Best Type at end of Season:")
    # print(Teams[bestTeamsAtEnd[2]].teamTypes.name +" : "+ str(100*Teams[bestTeamsAtEnd[2]].teamTypes.getWinPercent()))
    # print("-------------------")
    print("Best Type Overall:")
    print(Types[bestTypes[0]].name +" : "+ str(bestPercents[0]/100) +"%")
    print("2nd Best Type Overall:")
    print(Types[bestTypes[1]].name +" : "+ str(bestPercents[1]/100) +"%")
    print("3rd Best Type Overall:")
    print(Types[bestTypes[2]].name +" : "+ str(bestPercents[2]/100) +"%")
    
    print("#####################################")
    worstPercents =  heapq.nsmallest(3, enumerate(winpercents),key=lambda x: x[1])
    worstTypes =  [x[0] for x in worstPercents]
    worstPercents =  [x[1] for x in worstPercents]
    #bestTeamsAtEnd = getTopTeamsWinningPercent(False)
    # print("Worst Type at end of Season:")
    # print(Teams[bestTeamsAtEnd[0]].teamTypes.name +" : "+ str(100*Teams[bestTeamsAtEnd[0]].teamTypes.getWinPercent()))
    # print("2nd Worst Type at end of Season:")
    # print(Teams[bestTeamsAtEnd[1]].teamTypes.name +" : "+ str(100*Teams[bestTeamsAtEnd[1]].teamTypes.getWinPercent()))
    # print("3rd Worst Type at end of Season:")
    # print(Teams[bestTeamsAtEnd[2]].teamTypes.name +" : "+ str(100*Teams[bestTeamsAtEnd[2]].teamTypes.getWinPercent()))
    # print("-------------------")
    print("Worst Type Overall:")
    print(Types[worstTypes[0]].name +" : "+ str(worstPercents[0]/100) +"%")
    print("2nd Worst Type Overall:")
    print(Types[worstTypes[1]].name +" : "+ str(worstPercents[1]/100) +"%")
    print("3rd Worst Type Overall:")
    print(Types[worstTypes[2]].name +" : "+ str(worstPercents[2]/100) +"%")
    return bestTypes

typesUsed = [0 for _ in range(len(Types))]

perfChart = [[0 for _ in range(numRounds)] for _ in range(len(Types))]
for i in range(numRounds):
    battleMaker()
    tempTypesUsed = [0 for _ in range(len(Types))]

    # metaTypes = getMostUsedTeams()
    # for metaTypeInd in metaTypes:
    #     typesUsed[metaTypeInd]+=1
    # nonMetaTypes = getMostUsedTeams(False)
    # for nonMetaTypeInd in nonMetaTypes:
    #     typesUnUsed[nonMetaTypeInd]+=1
    for j in range(len(Teams)):
        typesUsed[Types.index(Teams[j].teamTypes)]+=1
        tempTypesUsed[Types.index(Teams[j].teamTypes)]+=1
    for j in range(len(Types)):
        perfChart[j][i] = tempTypesUsed[j]
bestTypes = findBestPerformingTypes()
bestPerformer =  heapq.nlargest(3, enumerate(typesUsed),key=lambda x: x[1])
mostUsedTypes =  [x[0] for x in bestPerformer]
bestPerformer =  [x[1] for x in bestPerformer]
print("////////////////////////")
print("Most Used Type Overall:")
print(Types[mostUsedTypes[0]].name +" : "+ str(100*bestPerformer[0]/(numRounds*len(Teams))) +"%")
print("2nd Most Used Type Overall:")
print(Types[mostUsedTypes[1]].name +" : "+ str(100*bestPerformer[1]/(numRounds*len(Teams))) +"%")
print("3rd Most Used Type Overall:")
print(Types[mostUsedTypes[2]].name +" : "+ str(100*bestPerformer[2]/(numRounds*len(Teams))) +"%")

worstPerformer =  heapq.nsmallest(3, enumerate(typesUsed),key=lambda x: x[1])
worstTypes =  [x[0] for x in worstPerformer]
worstPerformer =  [x[1] for x in worstPerformer]
print("////////////////////////")
print("Least Used Type Overall:")
print(Types[worstTypes[0]].name +" : "+ str(100*worstPerformer[0]/(numRounds*len(Teams))) +"%")
print("2nd Least Used Type Overall:")
print(Types[worstTypes[1]].name +" : "+ str(100*worstPerformer[1]/(numRounds*len(Teams))) +"%")
print("3rd Least Used Type Overall:")
print(Types[worstTypes[2]].name +" : "+ str(100*worstPerformer[2]/(numRounds*len(Teams))) +"%")

bestPerformer =  heapq.nlargest(4, enumerate(typesUsed),key=lambda x: x[1])
mostUsedTypes =  [x[0] for x in bestPerformer]
shownTypes =  list(set(mostUsedTypes) | set(bestTypes)) 
for i in shownTypes:
    plt.plot(perfChart[i],color = Types[i].color, label =Types[i].name)
    
plt.legend(loc='upper left')
plt.title('Most used Types')
plt.show()
#TODO
#1)-------------------- Make team creator (3-5 teams of each type to start?)
#2) -------------------Make battle divider to divide teams into battles
#3) -------------------nail down Team class so can update if win or lose
#4) ------------------- create behavior to run to see if team should switch types
#5) -------------------  Allow ranking/analysis of what are some of the top team types
#6) ------------------- create behavior to analyze what would be good matchups against this meta (i.e. weighted randomly picking new team,
# with higher weights being given the better odds are vs a good team, with it mattereing most against the most popular)
#7)--------------------- Store data over what are top team types over time
#8) ------------------display which types were on top the longest and at the end
#9) graph the top few teams over time

# for type in Types:
#     print(type.name+" \n")
# battle(Types[71],Types[16])

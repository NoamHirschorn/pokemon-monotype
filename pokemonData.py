basetypenames = ["Normal","Fire","Water","Electric","Grass","Ice",
             "Fighting","Poison","Ground","Flying","Psychic", "Bug",
             "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]
basetypecolors = ["#E4E4E4","#FFA726","b","y","g","c",
             "r","#A07DA9","#4B461A","#EEC279","#CEB2D3", "#AFBF9D",
             "#978078", "#8644A2", "#346CAB", "k", "#8F8F8F", "m"]

def makeTable(immunityCoeff,resistedCoeff,supereffectiveCoeff):
    Table = [[1.0 for _ in range(len(basetypenames))] for _ in range(len(basetypenames))]
    
    #Immunities
    immunities = [[0,13], #Normal vs Ghost
    [3,8], #Electric vs Ground
    [6,13], #Fighting vs Ghost
    [7,16], #Poison vs Steel
    [8,9], #Ground vs Flying
    [10,15], #Psychic vs Dark
    [13,0], #Ghost vs Normal
    [14,17]] #Dragon vs Fairy  
    for indicies in immunities:
        Table[indicies[0]][indicies[1]] = immunityCoeff
    #Weaknesses
    resistances = [[0,12], #Normal vs Rock
    [0,16], #Normal vs Steel
    [1,1], #Fire vs Fire
    [1,2], #Fire vs Water
    [1,12], #Fire vs Rock
    [1,14], #Fire vs Dragon
    [2,2], #Water vs Water
    [2,4], #Water vs Grass
    [2,14], #Water vs Dragon
    [3,3], #Electric vs Electric
    [3,4], #Electric vs Grass
    [3,14], #Electric vs Dragon
    [4,1], #Grass vs Fire
    [4,4], #Grass vs Grass
    [4,7], #Grass vs Poison
    [4,9], #Grass vs Flying
    [4,11], #Grass vs Bug
    [4,14], #Grass vs Dragon
    [4,16], #Grass vs Steel
    [5,1], #Ice vs Fire
    [5,2], #Ice vs Water
    [5,5], #Ice vs Ice
    [5,16], #Ice vs Steel
    [6,7], #Fighting vs Poison
    [6,9], #Fighting vs Flying
    [6,10], #Fighting vs Psychic
    [6,11], #Fighting vs Bug
    [6,17], #Fighting vs Fairy
    [7,7], #Poison vs Poison
    [7,8], #Poison vs Ground
    [7,12], #Poison vs Rock
    [7,13], #Poison vs Ghost
    [8,4], #Ground vs Grass
    [8,11], #Ground vs Bug
    [9,3], #Flying vs Electric
    [9,12], #Flying vs Rock
    [9,16], #Flying vs Steel
    [10,10], #Psychic vs Psychic
    [10,16], #Psychic vs Steel
    [11,1], #Bug vs Fire
    [11,6], #Bug vs Fighting
    [11,7], #Bug vs Poison
    [11,9], #Bug vs Flying
    [11,13], #Bug vs Ghost
    [11,16], #Bug vs Steel
    [11,17], #Bug vs Fairy
    [12,6], #Rock vs Fighting
    [12,8], #Rock vs Ground
    [12,16], #Rock vs Steel
    [13,15], #Ghost vs Dark
    [14,16], #Dragon vs Steel
    [15,6], #Dark vs Fighting
    [15,15], #Dark vs Dark
    [15,17], #Dark vs Fairy
    [16,1], #Steel vs Fire
    [16,2], #Steel vs Water
    [16,3], #Steel vs Electric
    [16,16], #Steel vs Steel
    [17,1], #Fairy vs Fire
    [17,7], #Fairy vs Poison
    [17,16]] #Fairy vs Steel
    for indicies in resistances:
            Table[indicies[0]][indicies[1]] = resistedCoeff
    #SuperEffectives
    supereffectives = [[1,4], #Fire vs Grass
    [1,5], #Fire vs Ice
    [1,11], #Fire vs Bug
    [1,16], #Fire vs Steel
    [2,1], #Water vs Fire
    [2,8], #Water vs Ground
    [2,12], #Water vs Rock
    [3,2], #Electric vs Water
    [3,9], #Electric vs Flying
    [4,2], #Grass vs Water
    [4,8], #Grass vs Ground
    [4,12], #Grass vs Rock
    [5,4], #Ice vs Grass
    [5,8], #Ice vs Ground
    [5,9], #Ice vs Flying
    [5,14], #Ice vs Dragon
    [6,0], #Fighting vs Normal
    [6,5], #Fighting vs Ice
    [6,12], #Fighting vs Rock
    [6,15], #Fighting vs Dark
    [6,16], #Fighting vs Steel
    [7,4], #Poison vs Grass
    [7,17], #Poison vs Fairy
    [8,1], #Ground vs Fire
    [8,3], #Ground vs Electric
    [8,7], #Ground vs Poison
    [8,12], #Ground vs Rock
    [8,16], #Ground vs Steel
    [9,4], #Flying vs Grass
    [9,6], #Flying vs Fighting
    [9,11], #Flying vs Bug
    [10,6], #Psychic vs Fighting
    [10,7], #Psychic vs Poison
    [11,4], #Bug vs Grass
    [11,10], #Bug vs Psychic
    [11,15], #Bug vs Dark
    [12,1], #Rock vs Fire
    [12,5], #Rock vs Ice
    [12,9], #Rock vs Flying    
    [12,11], #Rock vs Bug
    [13,10], #Ghost vs Psychic
    [13,13], #Ghost vs Ghost
    [14,14], #Dragon vs Dragon
    [15,10], #Dark vs Psychic
    [15,13], #Dark vs Ghost
    [16,5], #Steel vs Ice
    [16,12], #Steel vs Rock
    [16,17], #Steel vs Fairy
    [17,6], #Fairy vs Fighting
    [17,14], #Fairy vs Dragon
    [17,15]] #Fairy vs Dark
    for indicies in supereffectives:
            Table[indicies[0]][indicies[1]] = supereffectiveCoeff

    return Table

    
    



















































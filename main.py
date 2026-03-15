import random
import time
import os


TILE = "[X]"
NO_TILE = "[ ]"
MAX_WIDTH = 26
MAX_HEIGHT = 30

Width = 4
Height = 4
Board = []
Last2MovesHistory = []
GameMode = "Multi Player"
RandomOption = False

Player1Wins = 0
Player2Wins = 0
ComputerWins = 0
PlayerAgainstComputerWins = 0
PlayersTurnAfterLoadingGame = 0


def ResetBoard(difficulty=1):
    global Board, Width, Height, RandomOption
    Board = []
    for Row in range(Height):
        Board.append([])
        for Column in range(Width):
            if RandomOption:
                Board[Row].append(GetRandomTile(difficulty))
            else:
                Board[Row].append(TILE)

def GetRandomTile(difficulty):
    Rand = random.uniform(1, 10)
    if Rand < (11 - difficulty * 1.75):
        return TILE
    else:
        return NO_TILE

def DisplayState(PlayerNumber):
    print("-------------------------")
    if PlayerNumber == -1:
        print(f"Computer's turn")
    else:
        print(f"Player {PlayerNumber}'s turn")
    print()
    DisplayBoard()

def DisplayBoard():
    print("  ", end='')
    for Column in range(Width):
        if Column >= 26:
            Header = chr(Column // 26 + 64) + chr((Column % 26) + 65)
            print(f" {Header} ", end='')
        else:
            Header = chr(Column + 65)
            print(f"  {Header} ", end='')
    print()
    for Row in range(Height):
        if Row >= 9:
            print(Row + 1, end="")
        else:
            print(Row + 1, end=" ")
        for Column in range(Width):
            print(f" {Board[Row][Column]}", end='')
        print()

def ConvertRefToCoords(Ref):
    Column = ord(Ref[0]) - 65
    Row = int(Ref[1:]) - 1
    if Row < Height and Column < Width:
        Coords = [Row, Column]
    else:
        Coords = []
    return Coords

def ConvertCoordsToRef(Row, Column):
    global Height, Width
    Ref = ""
    if Row < Height and Column < Width:
        Letter = chr(Column + 65)
        Number = Row + 1
        Ref = Letter + str(Number)
    return Ref

def ProcessCoordinates(Move):
    if "-" in Move:
        DashPos = Move.index("-")
        FirstRef = Move[0:DashPos]
        SecondRef = Move[DashPos + 1:]
    else:
        FirstRef = Move
        SecondRef = Move
    if ord(FirstRef[0]) > ord(SecondRef[0]):
        FirstRef, SecondRef = SecondRef, FirstRef
    elif int(FirstRef[1:]) > int(SecondRef[1:]):
        FirstRef, SecondRef = SecondRef, FirstRef
    return FirstRef, SecondRef

def CountTilesLeft():
    global Board, Width, Height
    tilesLeft = 0
    for row in range(Height):
        for column in range(Width):
            if Board[row][column] == TILE:
                tilesLeft += 1
    return tilesLeft

def SetBoardSize():
    global Width, Height
    try:
        Width = int(input("Specify board width: "))
        while Width < 2 or Width > MAX_WIDTH:
            if Width > MAX_WIDTH:
                print(f"\033[31mWidth cannot be higher than {MAX_WIDTH}\033[0m")
            elif Width < 2:
                print("\033[31mWidth cannot be lower than 2\033[0m")
            Width = int(input("Specify board width: "))
        Height = int(input("Specify board height: "))
        while Height < 2 or Height > MAX_HEIGHT:
            if Height > MAX_HEIGHT:
                print(f"\033[31mHeight cannot be higher than {MAX_HEIGHT}\033[0m")
            elif Height < 2:
                print("\033[31mHeight cannot be lower than 2\033[0m")
            Height = int(input("Specify board height: "))
    except ValueError:
        print("\033[31mOnly integers are allowed to be entered!\033[0m")
        print("Height and width become 4")
        Width = 4
        Height = 4

def DisplayMenu():
    global GameMode, Width, Height, Player1Wins, Player2Wins, PlayerAgainstComputerWins, ComputerWins, RandomOption
    print("1 - Start game")
    print(f"2 - Set board size (currently {Width} x {Height})")
    print(f"3 - Toggle random option (currently {RandomOption})")
    print("4 - Load test board (4 x 4)")
    print(f"5 - Change game mode (currently {GameMode})")
    print(f"6 - Load the game")
    print("9 - Quit")
    match GameMode:
        case "Multi Player":
            print(f"Current score (Player 1 : Player 2) = {Player1Wins}:{Player2Wins}")
        case "Single Player":
            print(f"Current score (Player : Computer) = {PlayerAgainstComputerWins}:{ComputerWins}")

def SelectDifficulty():
    global RandomOption
    difficulty = ""
    if RandomOption == True:
        while difficulty not in ["low", "mid", "high"]:
            difficulty = input(
                "Select difficulty of the game(\033[32mlow\033[0m, \033[33mmid\033[0m, \033[31mhigh\033[0m): ")
    match difficulty:
        case "low":
            difficulty = 1
        case "mid":
            difficulty = 2
        case "high":
            difficulty = 3
        case _:
            print("Difficulty is set to 0")
            difficulty = 0
    return difficulty

def LoadTestBoard():
    global Width, Height
    Width = 4
    Height = 4
    ResetBoard(False)
    ProcessMove("A1-A4")
    ProcessMove("B1-B4")
    ProcessMove("C1-C4")
    ProcessMove("D1-D2")

def SearchForAllowedMoves():
    global Board, Height, Width
    tilesLeft = CountTilesLeft()
    longestMoveLength = 0
    allowedMoves = []
    for row in range(Height):
        for column in range(Width):
            for i in range(0, Height):
                if row + i < Height:
                    if Board[row + i][column] == TILE:
                        if f"{ConvertCoordsToRef(row, column)}-{ConvertCoordsToRef(row + i, column)}" not in allowedMoves:
                            if i + 1 < tilesLeft:
                                allowedMoves.append(
                                    f"{ConvertCoordsToRef(row, column)}-{ConvertCoordsToRef(row + i, column)}")
                                if i + 1 > longestMoveLength:
                                    longestMoveLength = i + 1
                    else:
                        break
            for j in range(0, Width):
                if column + j < Width:
                    if Board[row][column + j] == TILE:
                        if f"{ConvertCoordsToRef(row, column)}-{ConvertCoordsToRef(row, column + j)}" not in allowedMoves:
                            if j + 1 < tilesLeft:
                                allowedMoves.append(
                                    f"{ConvertCoordsToRef(row, column)}-{ConvertCoordsToRef(row, column + j)}")
                                if j + 1 > longestMoveLength:
                                    longestMoveLength = j + 1
                    else:
                        break
    return allowedMoves, longestMoveLength

def SearchForLongestMoves():
    allowedMoves = SearchForAllowedMoves()
    longestMoveLength = allowedMoves[1]
    allowedMoves = allowedMoves[0]
    longestMoves = []
    for i in allowedMoves:
        MiddleIndex = i.index("-")
        MovePart1 = i[:MiddleIndex]
        MovePart2 = i[MiddleIndex + 1:]
        if MovePart1[0] != MovePart2[0]:
            moveLength = abs(ord(MovePart1[0]) - ord(MovePart2[0])) + 1
        elif MovePart1[1:] != MovePart2[1:]:
            moveLength = abs(int(MovePart1[1:]) - int(MovePart2[1:])) + 1
        else:
            moveLength = 1
        if moveLength == longestMoveLength:
            longestMoves.append(i)
    return longestMoves

def ProcessHint(Move):
    if Move == "H":
        print(f"Hint: Consider {random.choice(SearchForLongestMoves())}")
        return True

def ProcessUndo(Move):
    if Move == "U":
        if Last2MovesHistory[0] == "Letter Move":
            print(f"\033[31mCannot undo a single letter move\033[0m")
        else:
            Restore(Last2MovesHistory[0])
            Last2MovesHistory.pop(0)
            return True
        
def ClearMoveHistory():
    if len(Last2MovesHistory) > 1:
        Last2MovesHistory.pop(0)

def LogMove(Move):
    ClearMoveHistory()
    if len(Move) == 1:
        Last2MovesHistory.append("Letter Move")
    else:
        if Move[:(len(Move)//2)]== Move[(len(Move)//2+1):]:
            Move = Move[:(len(Move)//2)]
        Last2MovesHistory.append(Move)

def Restore(Move):
    FirstRef, SecondRef = ProcessCoordinates(Move)
    StartCoords = ConvertRefToCoords(FirstRef)
    EndCoords = ConvertRefToCoords(SecondRef)
    if StartCoords[0] == EndCoords[0]:
        for Cell in range(StartCoords[1], EndCoords[1] + 1):
            Board[StartCoords[0]][Cell] = TILE
    else:
        for Cell in range(StartCoords[0], EndCoords[0] + 1):
            Board[Cell][StartCoords[1]] = TILE

def ProcessSave(Move, NextPlayer, TestGame):
    global Player1Wins, Player2Wins, PlayerAgainstComputerWins, ComputerWins, Width, Height, Board, Last2MovesHistory, GameMode
    if TestGame:
        print("\033[31mCannot save a test game!\033[0m")
        return False
    if Move == "S":
        with open("cache.txt", "w") as file:
            # Players scores
            file.write(f"Players Wins: {Player1Wins}:{Player2Wins}\n")

            # Player against Computer scores
            file.write(f"Player against Computer wins: {PlayerAgainstComputerWins}:{ComputerWins}\n")

            # Size of the Board
            file.write(f"Size of the Board: {Width}x{Height}\n")

            # Game Mode
            file.write(f"Game Mode: {GameMode}\n")

            # Which Players turn
            file.write(f"Which Players turn: {NextPlayer}\n")

            # Last 2 moves
            file.write(f"Last 2 moves: {",".join(Last2MovesHistory)}\n")

            # State of the Board
            for Row in range(len(Board)):
                if Row < len(Board)-1:
                    file.write(",".join(Board[Row])+"\n")
                else:
                    file.write(",".join(Board[Row]))
        return True
    else:
        return False
    
def LoadGame():
    global Player1Wins, Player2Wins, PlayerAgainstComputerWins, ComputerWins, Width, Height, Board, Last2MovesHistory, GameMode, PlayersTurnAfterLoadingGame
    try:
        with open("cache.txt", "r") as file:
            # Obtain Players scores
            Scores = file.readline()
            Scores = Scores[Scores.index(":")+2:]
            MainIndex = Scores.index(":")
            Player1Wins = int(Scores[:MainIndex])
            Player2Wins = int(Scores[MainIndex+1:Scores.index("\n")])

            # # Obtain Player and Computer scores
            Scores = file.readline()
            Scores = Scores[Scores.index(":")+2:]
            MainIndex = Scores.index(":")
            PlayerAgainstComputerWins = int(Scores[:MainIndex])
            ComputerWins = int(Scores[MainIndex+1:Scores.index("\n")])

            # Obtain size of the Board
            Size = file.readline()
            Size = Size[Size.index(":")+2:]
            MainIndex = Size.index("x")
            Width = int(Size[:MainIndex])
            Height = int(Size[MainIndex+1:Size.index("\n")])

            # Obtain Game mode
            line = file.readline()
            GameMode = line[line.index(":")+2:line.index("\n")]

            # Obtain Players turn
            line = file.readline()
            PlayersTurnAfterLoadingGame = int(line[line.index(":")+2:line.index("\n")])

            # Obtain last 2 moves history
            line = file.readline()
            line = line[line.index(":")+2:line.index("\n")]
            if line != "[]":
                Last2MovesHistory = line.split(",")
            else:
                Last2MovesHistory = []

            # Obtain the Board
            for row in range(Height):
                line = file.readline()
                if row < Height-1:
                    line = line[:line.index("\n")]
                Board.append(line.split(","))
            print("\033[32mThe game has been successfully loaded!\033[0m")
        os.remove("cache.txt")
        return True
    except:
         print(f"\033[31mCouldn't load the Game!\033[0m")
         return False

def ProcessMove(Move, NextPlayer = 0, TestGame = False):
    global Board
    try:
        if ProcessHint(Move) or ProcessUndo(Move):
            return "Correct move"
        if  ProcessSave(Move, NextPlayer, TestGame):
            return "Saved Game"
        FirstRef, SecondRef = ProcessCoordinates(Move)
        StartCoords = ConvertRefToCoords(FirstRef)
        EndCoords = ConvertRefToCoords(SecondRef)
        tilesLeft = CountTilesLeft()
        if StartCoords[0] != EndCoords[0] and StartCoords[1] != EndCoords[1]:
            return "Double row"
        if StartCoords[0] == EndCoords[0]:
            ToRemove = EndCoords[1] - StartCoords[1] + 1
            for Cell in range(StartCoords[1], EndCoords[1] + 1):
                if Board[StartCoords[0]][Cell] == TILE:
                    ToRemove -= 1
                    tilesLeft -= 1
            if ToRemove == 0:
                for Cell in range(StartCoords[1], EndCoords[1] + 1):
                    if tilesLeft < 1:
                        return "Not enough tiles"
                    Board[StartCoords[0]][Cell] = NO_TILE
            else:
                return "Empty tile on the way"
        else:
            ToRemove = EndCoords[0] - StartCoords[0] + 1
            for Cell in range(StartCoords[0], EndCoords[0] + 1):
                if Board[Cell][StartCoords[1]] == TILE:
                    ToRemove -= 1
                    tilesLeft -= 1
            if ToRemove == 0:
                for Cell in range(StartCoords[0], EndCoords[0] + 1):
                    if tilesLeft < 1:
                        return "Not enough tiles"
                    Board[Cell][StartCoords[1]] = NO_TILE
            else:
                return "Empty tile on the way"
        return "Correct move"
    except IndexError:
        return "Outside Index"
    except ValueError:
        return "Incorrect format"

def CheckGameOver():
    Remaining = CountTilesLeft()
    if Remaining == 1:
        return True
    else:
        return False

def ProcessGameOver(NextPlayer):
    global Player1Wins, Player2Wins, PlayerAgainstComputerWins, ComputerWins, Last2MovesHistory
    GameOver = True
    if GameMode == "Multi Player":
        print(f"\033[32mGame over - player {NextPlayer % 2 + 1} wins\033[0m")
        if (NextPlayer % 2 + 1) == 1:
            Player1Wins += 1
        elif (NextPlayer % 2 + 1) == 2:
            Player2Wins += 1
    else:
        if NextPlayer == 1:
            print(f"\033[31mGame over - computer wins\033[0m")
            ComputerWins += 1
        else:
            print(f"\033[32mGame over - player wins\033[0m")
            PlayerAgainstComputerWins += 1
    Last2MovesHistory = []
    print()
    DisplayBoard()
    print()
    print("Press enter to continue")
    input()
    return GameOver

def ProcessComputerMove(NextPlayer):
    randomizer = random.uniform(1, 10)
    if randomizer < 5:
        Move = random.choice(SearchForLongestMoves())
    else:
        Move = random.choice(SearchForAllowedMoves()[0])
    MiddleIndex = Move.index("-")
    if Move[:MiddleIndex] == Move[MiddleIndex + 1:]:
        Move = Move[:MiddleIndex]
    IsValid = ProcessMove(Move, NextPlayer)
    time.sleep(1)
    print(f"The computer made move: {Move}")
    return IsValid

def PlayGame(LoadedGame, TestGame):
    global Player1Wins, Player2Wins, PlayerAgainstComputerWins, ComputerWins, Width, Height, Last2MovesHistory, GameMode
    print(f"Valid moves are within the range A1-{ConvertCoordsToRef(Height - 1, Width - 1)}")
    GameOver = False
    try:
        if not LoadedGame:
            if GameMode == "Multi Player":
                NextPlayer = int(input("Enter which player is going first: "))
                if NextPlayer not in [1, 2]:
                    raise ValueError
            else:
                NextPlayer = random.choice([1, -1])
        else:
            NextPlayer = PlayersTurnAfterLoadingGame
        while not GameOver:
            DisplayState(NextPlayer)
            print()
            IsValid = ""
            while IsValid != "Correct move":
                if NextPlayer > 0:
                    Move = input("Enter move: ")
                    IsValid = ProcessMove(Move, NextPlayer, TestGame)
                    match IsValid:
                        case "Outside Index":
                            print("\033[31mIncorrect index of the tile was enterred!\033[0m")
                        case "Incorrect format":
                            print("\033[31mThe move must be entered in the form, similar to A1-D1!\033[0m")
                        case "Double row":
                            print("\033[31mThe player can only make a move across a single straight line!\033[0m")
                        case "Empty tile on the way":
                            print("\033[31mThere are empty tiles on the way!\033[0m")
                        case "Not enough tiles":
                            print("\033[31mCannot make a move that removes all tiles left from the board!\033[0m")
                        case "Saved Game":
                            print("\033[32mThe game has been successfully saved!\033[0m")
                            return
                        case "Correct move":
                            if GameMode == "Multi Player":
                                LogMove(Move)
                            else:
                                Last2MovesHistory = []
                                LogMove(Move)
                        case _:
                            pass
                else:
                    IsValid = ProcessComputerMove(NextPlayer)
            if GameMode == "Multi Player":
                NextPlayer = NextPlayer % 2 + 1
            else:
                if NextPlayer == 1:
                    NextPlayer = -1
                else:
                    NextPlayer = 1
            if CheckGameOver():
                GameOver = ProcessGameOver(NextPlayer)
    except ValueError:
        print("\033[31mCan only enter 1 or 2 for player order!\033[0m")

def Menu(Playing):
    global RandomOption, GameMode
    while Playing:
        ExitMenu = False
        LoadedGame = False
        TestGame = False
        while not ExitMenu:
            print()
            DisplayMenu()
            try:
                UserInput = int(input("Enter a choice: "))
                match UserInput:
                    case 1:
                        ExitMenu = True
                        difficulty = SelectDifficulty()
                        ResetBoard(difficulty)
                    case 2:
                        SetBoardSize()
                    case 3:
                        RandomOption = not RandomOption
                    case 4:
                        ExitMenu = True
                        if GameMode == "Single Player":
                                GameMode = "Multi Player"
                                print("Game mode is changed to Multi Player")
                        LoadTestBoard()
                        TestGame = True
                    case 5:
                        if GameMode == "Multi Player":
                            GameMode = "Single Player"
                        else:
                            GameMode = "Multi Player"
                    case 6:
                        if LoadGame():
                            ExitMenu = True
                            LoadedGame = True
                    case 9:
                        print("Thank you for playing")
                        ExitMenu = True
                        Playing = False
            except ValueError:
                print("\033[31mOnly integers are allowed to be entered!\033[0m")
        if Playing:
            PlayGame(LoadedGame, TestGame)

def Main():
    Playing = True
    Menu(Playing)
    print("Press enter to continue")
    input()

if __name__ == "__main__":
    Main()
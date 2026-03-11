import random
import time


TILE = "[X]"
NO_TILE = "[ ]"
MAX_WIDTH = 26
MAX_HEIGHT = 30

Width = 4
Height = 4
Board = []
Last2MovesHistory = []

Player1Wins = 0
Player2Wins = 0
ComputerWins = 0
PlayerAgainstComputerWins = 0


def ResetBoard(RandomOption, difficulty=1):
    global Board
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
    Ref = ""
    if Row < Height and Column < Width:
        Letter = chr(Column + 65)
        Number = Row + 1
        Ref = Letter + str(Number)
    return Ref

def SearchForAllowedMoves():
    tilesLeft = 0
    longestMoveLength = 0
    allowedMoves = []
    for row in range(Height):
        for column in range(Width):
            if Board[row][column] == TILE:
                tilesLeft += 1
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
        print(f"Undo")
        # ======================================================================================================
        return True

def ProcessCoordinates(Move):
    if "-" in Move:
        DashPos = Move.index("-")
        FirstRef = Move[0:DashPos]
        SecondRef = Move[DashPos + 1:]
    else:
        FirstRef = Move
        SecondRef = Move
    if ord(FirstRef[0]) > ord(SecondRef[0]):
        FirstRef = FirstRef + SecondRef
        SecondRef = FirstRef[:len(SecondRef)]
        FirstRef = FirstRef[len(SecondRef):]
    elif int(FirstRef[1:]) > int(SecondRef[1:]):
        FirstRef = FirstRef + SecondRef
        SecondRef = FirstRef[:(len(FirstRef) - len(SecondRef))]
        FirstRef = FirstRef[len(SecondRef):]
    return FirstRef, SecondRef

def CountTilesLeft(Board):
    tilesLeft = 0
    for row in range(Height):
        for column in range(Width):
            if Board[row][column] == TILE:
                tilesLeft += 1
    return tilesLeft

def ProcessMove(Move):
    try:
        if ProcessHint(Move):
            return "Correct move"
        FirstRef, SecondRef = ProcessCoordinates(Move)
        StartCoords = ConvertRefToCoords(FirstRef)
        EndCoords = ConvertRefToCoords(SecondRef)
        tilesLeft = CountTilesLeft(Board)
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
        return "Empty string"
    except ValueError:
        return "Incorrect format"

def SetBoardSize():
    global Width
    global Height
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

def DisplayMenu(RandomOption, GameMode):
    print("1 - Start game")
    print(f"2 - Set board size (currently {Width} x {Height})")
    print(f"3 - Toggle random option (currently {RandomOption})")
    print("4 - Load test board (4 x 4)")
    print(f"5 - Change game mode (currently {GameMode})")
    print("9 - Quit")
    match GameMode:
        case "Multi Player":
            print(f"Current score (Player 1 : Player 2) = {Player1Wins}:{Player2Wins}")
        case "Single Player":
            print(f"Current score (Player : Computer) = {PlayerAgainstComputerWins}:{ComputerWins}")

def LoadTestBoard():
    global Width
    global Height
    Width = 4
    Height = 4
    ResetBoard(False)
    ProcessMove("A1-A4")
    ProcessMove("B1-B4")
    ProcessMove("C1-C4")
    ProcessMove("D1-D2")

def CheckGameOver():
    Remaining = CountTilesLeft(Board)
    if Remaining == 1:
        return True
    else:
        return False

def ProcessGameOver(GameMode, NextPlayer):
    global Player1Wins, Player2Wins, PlayerAgainstComputerWins, ComputerWins
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
    print()
    DisplayBoard()
    print()
    print("Press enter to continue")
    input()
    return GameOver

def ProcessComputerMove():
    randomizer = random.uniform(1, 10)
    if randomizer < 5:
        Move = random.choice(SearchForLongestMoves())
    else:
        Move = random.choice(SearchForAllowedMoves()[0])
    MiddleIndex = Move.index("-")
    if Move[:MiddleIndex] == Move[MiddleIndex + 1:]:
        Move = Move[:MiddleIndex]
    IsValid = ProcessMove(Move)
    time.sleep(1)
    print(f"The computer made move: {Move}")
    return IsValid

def PlayGame(GameMode):
    global Player1Wins, Player2Wins, PlayerAgainstComputerWins, ComputerWins, Width
    print(f"Valid moves are within the range A1-{ConvertCoordsToRef(Height - 1, Width - 1)}")
    GameOver = False
    try:
        if GameMode == "Multi Player":
            NextPlayer = int(input("Enter which player is going first: "))
        else:
            NextPlayer = random.choice([1, -1])
        while not GameOver:
            DisplayState(NextPlayer)
            print()
            IsValid = ""
            while IsValid != "Correct move":
                if NextPlayer > 0:
                    Move = input("Enter move: ")
                    IsValid = ProcessMove(Move)
                    match IsValid:
                        case "Empty string":
                            print("\033[31mThe entered string is empty!\033[0m")
                        case "Incorrect format":
                            print("\033[31mThe move must be entered in the form, similar to A1-D1!\033[0m")
                        case "Double row":
                            print("\033[31mThe player can only make a move across a single straight line!\033[0m")
                        case "Empty tile on the way":
                            print("\033[31mThere are empty tiles on the way!\033[0m")
                        case "Not enough tiles":
                            print("\033[31mCannot make a move that removes all tiles left from the board!\033[0m")
                        case "Correct move":
                            pass
                        case _:
                            pass
                else:
                    ProcessComputerMove()
            if GameMode == "Multi Player":
                NextPlayer = NextPlayer % 2 + 1
            else:
                if NextPlayer == 1:
                    NextPlayer = -1
                else:
                    NextPlayer = 1
            if CheckGameOver():
                GameOver = ProcessGameOver(GameMode, NextPlayer)
    except ValueError:
        print("\033[31mCan only enter 1 or 2 for player order!\033[0m")

def SelectDifficulty(RandomOption):
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

def Menu(Playing, RandomOption, GameMode):
    while Playing:
        ExitMenu = False
        while not ExitMenu:
            print()
            DisplayMenu(RandomOption, GameMode)
            try:
                UserInput = int(input("Enter a choice: "))
                if UserInput == 1:
                    ExitMenu = True
                    difficulty = SelectDifficulty(RandomOption)
                    ResetBoard(RandomOption, difficulty)
                elif UserInput == 2:
                    SetBoardSize()
                elif UserInput == 3:
                    RandomOption = not RandomOption
                elif UserInput == 4:
                    ExitMenu = True
                    if GameMode == "Single Player":
                            GameMode = "Multi Player"
                            print("Game mode is changed to Multi Player")
                    LoadTestBoard()
                elif UserInput == 5:
                    if GameMode == "Multi Player":
                        GameMode = "Single Player"
                    else:
                        GameMode = "Multi Player"
                elif UserInput == 9:
                    print("Thank you for playing")
                    ExitMenu = True
                    Playing = False
            except ValueError:
                print("\033[31mOnly integers are allowed to be entered!\033[0m")
        if Playing:
            PlayGame(GameMode)

def Main():
    Playing = True
    RandomOption = False
    GameMode = "Multi Player"
    Menu(Playing, RandomOption, GameMode)
    print("Press enter to continue")
    input()


if __name__ == "__main__":
    Main()

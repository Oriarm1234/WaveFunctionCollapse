example = """

#This program is intended to be used as a prototype for my A-Level project.
#This is the WFC (Wave Function Collapse) module i intend to make for the project

#This program needs to be able to interpret a config file so it can be easily read by the main file

#Example of config file>


#Room Definitions
@Tile Arena[tags="Level1"]
@Tile LeftRightCorridor[tags="Level1 Corridor" sides = "LEFT RIGHT"]
@Tile UpDownCorridor[tags="Level1 Corridor" sides = "UP DOWN"]
@Tile LeftUpCorridor[tags="Level1 Corridor" sides = "LEFT UP"]
@Tile LeftDownCorridor[tags="Level1 Corridor" sides = "LEFT DOWN"]
@Tile RightUpCorridor[tags="Level1 Corridor" sides = "RIGHT UP"]
@Tile RightDownCorridor[tags="Level1 Corridor" sides = "RIGHT DOWN"]


#Rooms Rules

!Arena(*) < LeftRightCorridor #Any side can be accessed by tiles with only the tags "Level1 Corridor"



"""

from string import ascii_letters,digits



#Interpreter


class Interpreter:

    # This class will be used to interpret the config file and return useable data
    # When the text is processed it will be seperated into seperate tokens
    # These tokens are then formatted into a way that the main program can read

    def __init__(self):
        self.text = ""
        self.textPos = None
        self.tokPos = None
        self.currentChar = ""
        self.currentTok = [None]
        self.output = {}
        self.tokens = []
        self.tiles = {}

    def push(self,text):

        text = "\n".join(map(lambda x: x.split("#")[0],text.split("\n"))) #Iterate through the lines and remove any comments

        self.text=text
    

    def advance(self):
        if self.textPos == None and len(self.text) > 0:
            self.textPos=0
            self.currentChar = self.text[self.textPos]
        
        elif len(self.text)-1 > self.textPos if self.textPos != None else False:
            self.textPos+=1
            self.currentChar = self.text[self.textPos]
        
        else:
            self.textPos = None
            self.currentChar = ""
    
    def advanceTok(self):
        if self.tokPos == None and len(self.tokens) > 0:
            self.tokPos=0
            self.currentTok = self.tokens[self.tokPos]
        
        elif len(self.tokens)-1 > self.tokPos if self.tokPos != None else False:
            self.tokPos+=1
            self.currentTok = self.tokens[self.tokPos]
        
        else:
            self.tokPos = None
            self.currentTok = [None]

    def makeIdentifier(self):
        identifier = ""
        if self.textPos == None:self.advance()
        while self.currentChar != "" and self.currentChar in ascii_letters+digits:
            identifier+=self.currentChar
            self.advance()
        
        return identifier
    
    def makeString(self):
        string = ""
        if self.currentChar not in "\"\'":
            raise SyntaxError("Expected \" or \'")
        self.advance()
        while self.currentChar not in ["\"","\'",None]:
            string+=self.currentChar
            self.advance()
        else:
            if self.currentChar == None:
                raise SyntaxError("Expected closing \" or \'")
        self.advance()
        
        return string
    
    def checkTok(self, acceptedToks = [], unacceptedToks = [], typeError="", valueError="", unacceptedMessage="", raiseError=True):
        if self.currentTok[0] == None\
                or (self.currentTok[0] not in acceptedToks[0] if len(acceptedToks) > 0 else False):

            if raiseError:raise SyntaxError(typeError)
            return False
        if ((self.currentTok[1] not in acceptedToks[1] if len(acceptedToks) > 1 else False) if len(self.currentTok)>1 else False):
            if raiseError:raise ValueError(valueError)
            return False
        
        
        if (self.currentTok[0] in unacceptedToks[0] if len(unacceptedToks) > 0 else False):
            if raiseError:raise ValueError(unacceptedMessage)
            return False
        if ((self.currentTok[1] in unacceptedToks[1] if len(unacceptedToks) > 1 else False) if len(self.currentTok)>1 else False):
            if raiseError:raise ValueError(unacceptedMessage)
            return False
        return True
    
    def eval(self):

        if self.currentTok[0] != None:
            if self.currentTok[0] == "SPECIAL":
                if self.currentTok[1] == "@": #Constructor
                    
                    self.advanceTok()
                    self.checkTok([["IDENTIFIER"]], [[]], "Expected constructor type!")
                    Type = self.currentTok[1]
                    self.advanceTok()
                    if Type == "Tile":
                        self.checkTok([["IDENTIFIER"]], [[]], "Expected Identifier!")
                        name = self.currentTok[1]
                        self.tiles[name] = {"rules":{"LEFT":[],"RIGHT":[],"UP":[],"DOWN":[]}}
                        self.advanceTok()
                        if self.currentTok[0] == "SPECIAL" and self.currentTok[1] == "[":
                            self.tiles[name].update(self.evalBrackets("[",dict))


                            
                        


                elif self.currentTok[1] == "!":
                    
                    self.advanceTok()
                    
                    self.checkTok([["IDENTIFIER"]], [[]], "Expected Identifier!")
                    tile1 = self.currentTok[1]
                    if tile1 not in self.tiles:
                        raise NameError(f"\'{tile1}\' does not exist yet!")
                    self.advanceTok()
                    
                    sides = list(self.evalBrackets("(", set))
                    if "*" in sides:
                        if len(sides) == 1:
                            sides = self.tiles[tile1].get("sides", ["LEFT","RIGHT","UP","DOWN"])
                        else:
                            raise SyntaxError("Invalid character in this context!")
                    
                    incorrectSides = list(x for x in sides if x not in self.tiles[tile1].get("sides", ["LEFT","RIGHT","UP","DOWN"]))
                    
                    if incorrectSides != []:
                        raise BaseException(f"{tile1} does not have the side{'s' if len(incorrectSides) > 1 else ''} {', '.join(incorrectSides)}")

                    
                    if not self.checkTok([["SPECIAL"], ["<",">"]], raiseError = False):
                        for side in sides:
                            oppSide = {"LEFT":"RIGHT","UP":"DOWN","DOWN":"UP","RIGHT":"LEFT"}[side]
                            for tile in self.tiles:
                                if tile == tile1:
                                    continue
                                if oppSide in self.tiles[tile].get("sides", ["LEFT","RIGHT","UP","DOWN"])\
                                        and tile not in self.tiles[tile1]["rules"][side]:
                                    self.tiles[tile1]["rules"][side].append(tile)
                    elif self.checkTok([["SPECIAL"], ["<"]], raiseError = False):
                        self.advanceTok()
                        if not self.checkTok([["SPECIAL"],["*"]], raiseError=False):
                            self.checkTok([["IDENTIFIER"]], [[]], "Expected Identifier or '*'!")
                        tile2 = self.currentTok[1]
                        if tile2 not in self.tiles and tile2 != "*":
                            raise NameError(f"\'{tile1}\' does not exist yet!")
                        self.advanceTok()


                        if tile2 == "*":
                            tiles = []
                            if self.currentTok[0] == "SPECIAL" and self.currentTok[1] == "[":
                                keys = self.evalBrackets("[", dict)
                                for key in keys:
                                    for tile in self.tiles:
                                        fitsSearch = tile != tile1
                                        if key in self.tiles[tile]:
                                            for val in keys[key]:
                                                if val not in self.tiles[tile][key]:
                                                    fitsSearch = False
                                        else:
                                            fitsSearch = False

                                        if fitsSearch:
                                            tiles.append(tile)
                            else:
                                tiles.extend(self.tiles.keys())
                            for tile in tiles:
                                oppSides = list({"LEFT":"RIGHT","UP":"DOWN","DOWN":"UP","RIGHT":"LEFT"}[side] for side in self.tiles[tile].get("sides", ["LEFT","RIGHT","UP","DOWN"]))
                                sharedSides=list(side for side in sides if side in oppSides)
                                for side in sharedSides:
                                    if tile not in self.tiles[tile1]["rules"][side]:self.tiles[tile1]["rules"][side].append(tile)

                        else:
                            oppSides = list({"LEFT":"RIGHT","UP":"DOWN","DOWN":"UP","RIGHT":"LEFT"}[side] for side in self.tiles[tile2].get("sides", ["LEFT","RIGHT","UP","DOWN"]))
                            sharedSides=list(side for side in sides if side in oppSides)
                            for side in sharedSides:
                                if tile2 not in self.tiles[tile1]["rules"][side]:self.tiles[tile1]["rules"][side].append(tile2)
                    
                    else:
                        self.advanceTok()
                        if not self.checkTok([["SPECIAL"],["*"]], raiseError=False):
                            self.checkTok([["IDENTIFIER"]], [[]], "Expected Identifier or '*'!")
                        tile2 = self.currentTok[1]
                        if tile2 not in self.tiles and tile2 != "*":
                            raise NameError(f"\'{tile1}\' does not exist yet!")
                        self.advanceTok()


                        if tile2 == "*":
                            tiles = []
                            if self.currentTok[0] == "SPECIAL" and self.currentTok[1] == "[":
                                keys = self.evalBrackets("[", dict)
                                for key in keys:
                                    for tile in self.tiles:
                                        fitsSearch = True
                                        if key in self.tiles[tile]:
                                            for val in keys[key]:
                                                if val not in self.tiles[tile][key]:
                                                    fitsSearch = False
                                        else:
                                            fitsSearch = False

                                        if fitsSearch:
                                            tiles.append(tile)
                            else:
                                tiles.extend(self.tiles.keys())
                            for tile in tiles:
                                oppSides = list({"LEFT":"RIGHT","UP":"DOWN","DOWN":"UP","RIGHT":"LEFT"}[side] for side in self.tiles[tile].get("sides", ["LEFT","RIGHT","UP","DOWN"]))
                                sharedSides=list(side for side in sides if side in oppSides)
                                for side in sharedSides:
                                    if tile in self.tiles[tile1]["rules"][side]:self.tiles[tile1]["rules"][side].remove(tile)

                        else:
                            oppSides = list({"LEFT":"RIGHT","UP":"DOWN","DOWN":"UP","RIGHT":"LEFT"}[side] for side in self.tiles[tile2].get("sides", ["LEFT","RIGHT","UP","DOWN"]))
                            sharedSides=list(side for side in sides if side in oppSides)
                            for side in sharedSides:
                                if tile2 in self.tiles[tile1]["rules"][side]:self.tiles[tile1]["rules"][side].remove(tile2)








                        
                                




                    
                    

                    


    
    def evalBrackets(self,bracket,returnType):
        self.checkTok([["SPECIAL"], [bracket]], [[]], f"Expected \'{bracket}\' Character!", f"Expected \'{bracket}\' Character!")
        self.advanceTok()
        data = returnType()
        while self.checkTok(unacceptedToks=[[],["]" if bracket == "[" else ")"]], raiseError=False):
            identifier = self.currentTok[1]
            if self.currentTok[0] == "IDENTIFIER":
                
                if returnType == dict:
                    self.advanceTok()
                    self.checkTok([["SPECIAL"], ["="]])
                    self.advanceTok()
                    self.checkTok([["STRING"]], [], "Expected String!")
                    if identifier not in data:data[identifier]=[]
                    data[identifier].extend(list(filter(lambda x: x!="",self.currentTok[1].split(" "))))
                else:
                    data.update({identifier})
            elif self.currentTok[0] == "SPECIAL" and self.currentTok[1] == "*":
                if returnType == set:
                    data.update({identifier})
                else:
                    raise SyntaxError("Expected Identifer!")
            self.advanceTok()
        self.advanceTok()
    
        return data
                
                    

                    


    
    def parse(self):

        self.textPos = None
        self.tokPos = None
        self.currentChar = ""
        self.currentTok = [None]
        self.output = {}
        self.tokens = []
        self.tiles = {}
        
        self.advance()

        while self.textPos != None:
            
            if self.currentChar in ascii_letters+digits:
                self.tokens.append(["IDENTIFIER", self.makeIdentifier()])
            
            elif self.currentChar in "\"\'":
                self.tokens.append(["STRING", self.makeString()])
            
            elif self.currentChar in "!@()*<>=\"\'[],":
                self.tokens.append(["SPECIAL", self.currentChar])
                self.advance()
            
            elif self.currentChar in " \n\t":
                self.advance()

            else:
                raise SyntaxError(f"Invalid Character!({self.currentChar})")

        self.advanceTok()
        while self.currentTok[0] != None:
            self.eval()

class Map(Interpreter):
    All = []

    def __init__(self, configCode):
        Map.All.append(self)
        super().__init__()
        self.push(configCode)
        self.parse()
        self.rooms = {}
        
        self.random = __import__("random")
        self.choice = self.random.choice

        self.rooms[(0,0)] = self.choice(list(self.tiles.keys()))
        
    
    def generateRoom(self):
        pass

    def createRoom(self):
        room = object()
        room.possibleRooms = list(self.tiles.keys())

            
            
        



with open("WFC.config","r") as file:
    contents = file.read()

tileMap = Map(contents)

print(tileMap.rooms)


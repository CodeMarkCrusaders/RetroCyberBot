from .character import Character
import sys
import os
import json
sys.path.append(os.path.dirname(sys.path[0]))

class User():
    def __init__(self, id : str) -> None:

        self.ID = id

        if os.path.exists(f'User\\{id}'):

            self.Load()
            
            from Data_classes.all_user import AllUser
            for hr in list(self.GetAllChar()):
                AllUser.all_character[f'{id}!{hr.GetID()}'] = hr
            
        else:

            self.CharacterList: list[Character] = [] 
            self.SelectedCharacter = None
            self.selected_val = None
            self.AccessLevel = 'Normal'

            self.Save()

    def AppendCharacter (self) -> None:

        CharacterID = f"{self.ID}{len(self.CharacterList)}"

        NewCharacter = Character(CharacterID)

        NewCharacter.ScreenName = 'reg_stage1'
        
        self.SelectedCharacter = NewCharacter

        self.CharacterList.append(NewCharacter)

    def GetNameScreen(self) -> None:

        return self.SelectedCharacter.ScreenName

    def GetChar(self, id = 'selected') -> Character:

        if id == 'selected':

            return self.SelectedCharacter

        else:

            return self.CharacterList[id]

    def GetAllChar(self) -> list[Character]:

        return self.CharacterList

    def ChooseChar(self , id: int) -> None:

        self.SelectedCharacter = self.CharacterList[id]

    def SetValue(self,Value) -> str:

        return 1

    def Save(self, CharacterID = 'All') -> str:  

        if not os.path.exists(f'User\\{self.ID}'):

            os.mkdir(f'User\\{self.ID}')

        Data = {
            'LenListCharacter': len(self.CharacterList),
            'AccessLevel': self.AccessLevel
        }
        with open(f'User\\{self.ID}\\UserData.txt', 'w') as outfile:
            json.dump(Data, outfile)

        if CharacterID == 'Selected':

            Data = self.SelectedCharacter.GetSaveData()
            CharacterID = self.SelectedCharacter.GetID()

            with open(f'User\\{self.ID}\\{CharacterID}.txt', 'w') as outfile:
                json.dump(Data, outfile)

        elif CharacterID == 'All':

            for Character in self.CharacterList:

                Data = Character.GetSaveData()
                CharacterID = Character.GetID()

                with open(f'User\\{self.ID}\\{CharacterID}.txt', 'w') as outfile:
                    json.dump(Data, outfile)
        
        else:
            Data = self.CharacterList[CharacterID].GetSaveData()

            with open(f'User\\{self.ID}\\{CharacterID}.txt', 'w') as outfile:
                json.dump(Data, outfile)
                    
        return 'Сохранено'
     
    def Load(self):

        with open(f'User\\{self.ID}\\UserData.txt') as json_file:

            Data = json.load(json_file)

        self.CharacterList: list[Character] = [] 
        self.SelectedCharacter = None
        self.AccessLevel = Data['AccessLevel']
        self.Screen = None

        for i in range(Data['LenListCharacter']):

            with open(f'User\\{self.ID}\\{self.ID}!{i}.txt') as json_file:

                CharacterData = json.load(json_file)

            self.CharacterList.append(Character(i))
            self.CharacterList[i].Load(CharacterData)


            

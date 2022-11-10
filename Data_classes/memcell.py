class MemoryCell():
    
    def __init__(self, memory : dict) -> None:

        self.Memory: dict[str,Meaning] = { } 
        self.SelectedMeaning = None

        for NameMeaning,DataMeaning in memory.items():

            ClassMeaning = DataMeaning['CM']
            ErrorMessage = DataMeaning['EM']
            StartValue   = DataMeaning['SV']

            self.Memory[NameMeaning] = Meaning(ClassMeaning , ErrorMessage , StartValue)

    def Binding (self):

        return self

    def GetMemory (self, NamePart: str):

        return self.Memory[NamePart].GetData()

    def GetAllMemory(self)  -> dict:

        Data = {}

        for NameMeaning,DataMeaning in self.Memory.items():

            DataMeaning: Meaning

            Data[NameMeaning] = DataMeaning.GetData()

        return Data

    def СhooseMeaning(self , NameMeaning: str) -> None:

        self.SelectedMeaning = NameMeaning

    def SetMeaning(self , Value) -> str:

        answer = self.Memory[self.SelectedMeaning].Set(Value)

        return answer

    def ChooseSetMeaning(self, NameMeaning: str, Value) -> str:

        answer = self.Memory[NameMeaning].Set(Value)

        return answer

    def Filled(self) -> bool:

        Filled = not None in self.GetAllMemory().values()

        return Filled

    def AllReset (self):

        for NameMeaning in self.Memory.keys():

            self.Memory[NameMeaning].Reset()

    def Reset(self, NameMeaning):

        self.Memory[NameMeaning].Reset()


class Meaning:

    def __init__(self, ClassMeaning, ErrorMessage = None, StartValue = None) -> None:
        
        self.ClassMeaning = ClassMeaning

        if ErrorMessage == None:

            self.ErrorMessage = 'Ошибка!!\nКакая хз'

        self.Value = StartValue

    def Set(self , value):

        if self.ClassMeaning == int:

            value = int(value)

        if isinstance(value, self.ClassMeaning):
            
            self.Value = value

            return '1'

        else:

            return self.ErrorMessage

    def GetData(self):

        return self.Value

    def Reset(self):

        self.Value = None

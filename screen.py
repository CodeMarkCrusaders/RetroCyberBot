from discord import Embed
from method.link import link
from Data_classes.Data_user import User
from discord.ui import View


class Screen(View):
    def __init__(self, user: User) -> None:
        super().__init__(timeout = None)

        self.Memory = []
        self.Data = {}

        self.Embed = None
        self.ControlUser = user
        self.SelectedCharacter = None
        self.ScreenName = ''
        self.HistoryPosition = -1

    def BackPos(self) -> bool: #возможность вернуться на предыдущий экран в истории

        position = self.HistoryPosition

        if position == -1:

            position = len(self.Memory) - 1

        if position == 0:

            return False
        
        else:

            return True

    async def Back(self) -> None:
        
        self.clear_items()

        if self.HistoryPosition == -1:

            self.HistoryPosition = len(self.Memory) - 2

        else:

            self.HistoryPosition -= 1 

        method_name = self.Memory[self.HistoryPosition]

        link[method_name](self)

    def ForwardPos(self) -> bool:#возможность перейти на следующий в истории экран

        if self.HistoryPosition != -1 and self.HistoryPosition + 1 != len(self.Memory):

            return True

        else:

            return False

    async def Forward(self) -> None:

        method_name = self.Memory[self.HistoryPosition]

        link[method_name](self)

        self.HistoryPosition += 1 

    async def Show(self, method_name):

        if self.HistoryPosition != -1:
            self.Memory = self.Memory[:self.HistoryPosition + 1]

        self.clear_items()

        self.Memory.append(method_name)

        self.HistoryPosition = -1

        self.ScreenName = method_name

        link[method_name](self)

    async def Update(self) -> None:

        #self.SelectedCharacter  = self.ControlUser.GetChar()

        if self.ScreenName != '':

            self.clear_items()

            link[self.ScreenName](self)


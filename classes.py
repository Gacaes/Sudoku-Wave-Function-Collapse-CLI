from random import choice as randc

class Cell:
    def __init__(self, x:int, y:int, chunk:int = 0, weight:float = 1.0):
        """_summary_

        Args:
            x (int): _description_
            y (int): _description_
            chunk (int, optional): _description_. Defaults to 0.
        """        
        self.possibilities = [i for i in range(1,10)]
        self.length = 9
        self.value = ' '
        self.x = x
        self.y = y
        self.position = [self.x, self.y]
        self.chunk = chunk
        self.weight = weight

    def __str__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """        
        #show possibilities else collapsed state
        return str(self.value)
    
    def __int__(self) -> int:
        #show collapsed state else ' '
        pass


    def pop(self,value:int) -> int:
        """_summary_

        Args:
            value (int): _description_

        Raises:
            ValueError: _description_

        Returns:
            int: _description_
        """        
        if len(self.possibilities)-1:
            try:
                self.possibilities.remove(value)
                self.length -= 1
            except ValueError:
                #the value already doesn't exist
                pass
            return self.length
        else:
            #the value already doesn't exist - this trips before the try except
            raise CollapsedError(f'Cell has already collapsed. self.possibilities = {self.possibilities}, value = {value}')

    def collapse(self, value=None) -> int:
        """_summary_

        Args:
            value (_type_, optional): _description_. Defaults to None.

        Returns:
            int: _description_
        """
        if not self.length-1:
            raise CollapsedError(f'Cell has already collapsed. self.possibilities = {self.possibilities}, value = {value}')
        if value is None:
            value = randc(self.possibilities)
        self.value,self.possibilities = int(value),[int(value)]
        self.length = 1
        return value

class CollapsedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
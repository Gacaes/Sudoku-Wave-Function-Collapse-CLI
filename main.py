from random import randint as randi
from random import choice as randc
#use random.choices for weight inclusion
#a=['a','b','c']
#b=[1,.5,.1]
#ans=choices(a,b,k=1000)
#len(ans)=1000, ans.count('a')=610, ans.count('b')=323, ans.count('c')=67
from classes import *




class Board:

    def __init__(self, width:int = 9, height:int = 9, x_chunk_size:int = 3, y_chunk_size:int = 3, difficulty:float = .25):
        """_summary_

        Args:
            width (int, optional): The width of the board: the length of the rows. Defaults to 9.
            height (int, optional): The height of the board: the length of the columns. Defaults to 9.
            x_chunk_size (int, optional): _description_. Defaults to 3.
            y_chunk_size (int, optional): _description_. Defaults to 3.
            difficulty (float, optional): Currently unused. Defaults to .25.

        Raises:
            ValueError: width must be exactly divisable by x_chunk_size
            ValueError: height must be exactly divisable by y_chunk_size
        """
        if width%x_chunk_size:
            raise ValueError(f'x_chunk_size ({x_chunk_size}) must be a factor of width ({width})')
        if height%y_chunk_size:
            raise ValueError(f'y_chunk_size ({y_chunk_size}) must be a factor of height ({height})')
        
        self.current_array : list = self.new_empty()
        self.lowest_entropies : list = self.get_entropies()
        self.chunks : list = Board.chunk(self.current_array)
        self.width : int = width
        self.height : int = height
        self.collapsed:bool = False

    def __str__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """        
        array=[]
        '''for y_ in range(3):
            for y__ in range(3):
                for x_ in range(3):
                    array_ = []
                    for x__ in range(3):
                        array_.append(str(self.current_array[y_*3+y__][x_*3+x__]))
                    array.append("|".join(array_))'''
        for y_block in range(3):
            y_add = y_block*3
            y_array = []

            for y in range(y_add,y_add+3):
                x_block_seperator = '|'
                x_array = []

                for x_block in range(3):
                    x_add = x_block*3
                    x_block_string = ''

                    for x in range(x_add,x_add+3):
                        #add x strings into x block string
                        x_block_string += str(self.current_array[y][x])
                        #e.g. 123

                    #add x block strings into x array to be joined into y string
                    x_array.append(x_block_string)

                #join x block strings and append to y array to be joined into y block string
                y_array.append(x_block_seperator.join(x_array))
                #e.g. 123|456|789
            
            #join y strings to y block string and append to board array to be joined into board string
            array.append("\n".join(y_array))
            #e.g.
            #123|...\n
            #456|...\n
            #789|...\
            #add y block string seperator to board array
            if y_block-2:
                array.append("---+---+---")
        
        #join y block string and y block string seperators
        return "\n".join(array)

        return "---+---+---\n".join([
            "\n".join([
                "|".join([
                    "".join([
                        str(self.current_array[yj][j]) for j in range(3*i,3*i+3)
                        ]) for i in range(3)
                    ]) for yj in range(3*yi,3*yi+3)
                ]) for yi in range(3)
            ])
        for i in range(11):
            if (i+1)%4:
                string=""
                for j in range(11):
                    if (j+1)%4:
                        string+="0"
                    else:
                        string+="|"
                array.append(string)
            else:
                array.append("---+---+---")
        del string,i,j
        return array
    


    def change_cell(self,x:int,y:int,value:int)->None:
        """Collapses the cell at the given x and y co-ordinates to the given value

        Args:
            x (int): The x co-ordinate of the cell to collapse
            y (int): The y co-ordinate of the cell to collapse
            value (int): The value to collapse the cell to

        Raises:
            ValueError: Raised if the given cell has already collapsed
            IndexError: Raised if give x or y co-ordinates are out of range of the current board's dimensions
        """        
        self.current_array[y][x].collapse(value)
        return 
    
        if not (x in range(1,10) or y in range(1,10) or value in range(1,10)):
            raise ValueError(f'At least 1 of the following arguments is not in range(1,10): x={x},y={y},value={value}')
        y=y+((y+1)//4)
        x=x+((x+1)//4)
        new_string = str(self.current_array[y][:x])
        new_string += str(value)
        new_string += str(self.current_array[y][x+1:])
        self.current_array[y] = str(new_string)
        del new_string,x,y

    @staticmethod
    def new_empty() -> list:
        """_summary_

        Returns:
            list: _description_
        """        
        return [[Cell(__, _) for __ in range(9)] for _ in range(9)]
        for i in range(11):
            if (i+1)%4:
                string=""
                for j in range(11):
                    if (j+1)%4:
                        string+="0"
                    else:
                        string+="|"
                array.append(string)
            else:
                array.append("---+---+---")
        del string,i,j
        return array
    
    @staticmethod
    def chunk(array:list, size:int = 3) -> list:
        """_summary_

        Args:
            array (list): _description_
            size (int, optional): _description_. Defaults to 3.

        Returns:
            list: _description_
        """        
        #array_ = [list([]).copy()]*(len(array)//size)*(len(array[0])//size)
        array_ = [[] for _ in range((len(array)//size)*(len(array[0])//size))]
        for y in range(len(array)):
            y_chunk = y//size

            for x in range(len(array[y])):
                x_chunk = x//size
                index = y_chunk*size + x_chunk

                #set the cell's chunk position
                array[y][x].chunk = index
                #append cell to chunk list
                array_[index].append(array[y][x])
                continue

        return array_
    
    def get_entropies(self) -> list:
        """_summary_

        Raises:
            Exception: _description_

        Returns:
            list: _description_
        """        
        entropies = []
        lowest_entropies = []
        #get all cell entropies and append into entropies list
        for row in self.current_array:
            for cell in row:
                entropies.append(cell.length)
        if sum(entropies) == len(self.current_array)*len(self.current_array[0]):
            raise Exception('All cells have been collapsed')
    
        #get the lowest entropy
        lowest = min(entropies)
        #get it's index
        index = entropies.index(lowest)

        for i in range(entropies.count(lowest)):
            #i is also a count for how many times one of the lowest entropies has been appended to lowest_entropies list

            #update the index and i to account for cells that have been popped from the entropies list already
            index = entropies.index(lowest) + i
            lowest_entropies.append(self.current_array[index//9][index%9])
            #make sure to take off i when popping for the entropies list
            entropies.pop(index-i)

        return lowest_entropies
    
    def collapse(self) -> list:
        """_summary_

        Returns:
            list: _description_
        """        
        #cell = randc(self.lowest_entropies) #randc i.e. random.choice doesn't seem to like choosing a cell from anything other than the 0th row
        randint = randi(0,80)
        cell = self.lowest_entropies[randint]

        #return [randint,self.lowest_entropies.index(cell), len(self.lowest_entropies),randint%9] #for debugging

        value = cell.collapse()
        #now propogate and pop value from cells in same cell block, column and row

        #all cells in same cell chunk
        for cell_ in self.chunks[cell.chunk]:
            try:
                cell_.pop(value)
            except CollapsedError:
                #the cell we just collapsed
                pass
        
        #all cells in same column
        for _ in self.current_array:
            cell_ = _[cell.position[0]]
            try:
                cell_.pop(value)
            except CollapsedError:
                #already popped in chunk
                pass

        #all cells in same row
        for cell_ in self.current_array[cell.position[1]]:
            try:
                cell_.pop(value)
            except CollapsedError:
                #already popped in chunk or column
                pass
        
        #then update the entropies
        self.lowest_entropies = self.get_entropies()
        return cell.position
        




        



if __name__ == "__main__":
    board = Board()
    #collapse the first cell
    pos = board.collapse()
    #print the position of the cell that was collapsed
    print('\n',pos,'\n')
    #print the full board formatted
    print(board)
    
    '''print('\n\nChunk:\n')
    main_cell = board.current_array[pos[1]][pos[0]]
    for cell in board.chunks[main_cell.chunk]:
        print(cell.possibilities)
    print('Row:\n')
    for cell in board.current_array[pos[1]]:
        print(cell.possibilities)
    print('Column:\n')
    for _ in board.current_array:
        print(_[pos[0]].possibilities)'''
    #print([str(cell) for cell in board.current_array[pos[1]]])

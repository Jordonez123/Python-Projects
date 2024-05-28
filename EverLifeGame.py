from collections import defaultdict
class EverLifeGame:
    # TODO: Make it possible so that the player is able to
    # exit the game at any point through interaction with the added input
    def __init__(self):
        # control  if the game is still happening
        self.run = True
        self.GAME_LENGTH = 0
        # starting at position 0
        # only to set up the game
        self.cells_alive_position = []
        self.time_step = 0
        
        # keys are time steps int
        # values are {branch int: branch string}
        self.branch_states = defaultdict(dict)

        # keep track of current time_step branches
        self.current_time_step_branches = {}
        
        # make sure that we do not repeat previously considered cycles
        # (branch_string, branch_number)
        self.cycles_encountered = []

    def set_game_length(self) -> None:
        GAME_LENGTH = input("Please enter the length of the game as an integer: ")
        # actually check that the GAME_LENGTH is a digit
        while GAME_LENGTH.isdigit() == False:
            # continue to ask for a valid input
            GAME_LENGTH = input("Please enter the length of the game as an integer: ")
        
        while int(GAME_LENGTH) <= 0:
            # ask for a game length of at least equal to 1
            GAME_LENGTH = input("Re-enter game length as at least equal to `1`: ")
        
        self.GAME_LENGTH = int(GAME_LENGTH)

    def set_cells_alive(self) -> None:
        # ask user for the position of the cells that are to be set as alive
        # position starting at 0 as outlined in README.txt
        cells_alive_position = input("Please enter the position of the cells started to be marked as alive: ").replace(' ', '').split(',')
        # need to check that all of the entered position values are digits
        # checks if there is currently an invalid value in the list
        invalid_position = all(element.isdigit() for element in cells_alive_position)

        # need to check that all of the entered position values are within the
        # range of the GAME_LENGTH
        max_range = self.GAME_LENGTH - 1
        min_range = 0
        #  iterate through the cells position list and check
        out_of_range = all(int(element) <= max_range and int(element) >= 0 for element in cells_alive_position)


        while invalid_position == False or out_of_range == False:
            if invalid_position == False:
                # warn that there is non-numeric in the list
                print("There is a non-numeric in the list")
                
            
            if out_of_range == False:
                # warn that there is a value that is out of range
                print("There is a value in the list that is either negative or bigger than the game length")
            
            cells_alive_position = input("Please enter the position of the cells started to be marked as alive: ").split(',')
            invalid_position = all(element.isdigit() for element in cells_alive_position)
            out_of_range = all(int(element) <= max_range and int(element) >= min_range for element in cells_alive_position)


        self.cells_alive_position = [int(element) for element in cells_alive_position]

    def display_time_step_zero(self) -> None:
        first_branch = ['0'] * self.GAME_LENGTH
        for position in self.cells_alive_position:
            first_branch[position] = '1'

        # ----printing string representation of time step 0 ---
        print('---------------------------')
        print(f"Time step: {self.time_step}")
        first_branch_string = ''.join(first_branch)
        self.branch_states[self.time_step][1] = first_branch_string
    
    # switches cells per branch
    def toggle_cells(self, branch_list: list) -> str:
        # example string 001110011110
        if len(branch_list) == 1:
            return ''.join(branch_list)
        
        toggle_positions = []
        for i in range(len(branch_list)):
            if i == 0:
                if (branch_list[-1] == '1') or (branch_list[1] == '1'):
                    toggle_positions.append(0)
            elif i == len(branch_list) - 1:
                if (branch_list[-2] == '1') or (branch_list[0] == '1'):
                    toggle_positions.append(len(branch_list) - 1)
            else:
                if (branch_list[i-1] == '1') or (branch_list[i+1] == '1'):
                    toggle_positions.append(i)


        # update the branch string
        for position in toggle_positions:
            if branch_list[position] == '1':
                branch_list[position] = '0'
            else:
                branch_list[position] = '1'

        return ''.join(branch_list)


    def get_current_time_step_branches(self) -> dict:
        return self.branch_states.get(self.time_step)
    
    def check_cycles(self, branch_number: int, branch_string: str) -> int:
        # gather states for time steps less than current for same branch number
        cycle_lengths = []
        longest_cycle = 0
        for i in range(self.time_step):
            # want to skip over the states where the branching did not occur
            try:
                if (self.branch_states[i][branch_number] == branch_string) \
                    and (branch_string,branch_number) not in self.cycles_encountered:
                    #(f'current_ts_branches: {self.current_time_step_branches}')
                    #print(f'i: {i}, branch_states[{i}][{branch_number}]: {self.branch_states[i][branch_number]}, branch_string: {branch_string}')
                    
                    # add newly encountered cycle to the list of ones being tracked
                    self.cycles_encountered.append((branch_string, branch_number))
                    # cycle length = self.time_step - i
                    cycle_lengths.append(self.time_step - i) # second number is the length of the cycle
            except:
                continue
        
        if len(cycle_lengths) > 0:
            #print(f'cycle_lengths array: {cycle_lengths}')
            longest_cycle = max(cycle_lengths)
        
        return longest_cycle
    
    def display_current_time_step_branches(self):
        for item in self.current_time_step_branches.items():
            print(f'branch {item[0]}: {item[1]}', end=" ")
        print("")

    def next_action(self) -> str:
        self.current_time_step_branches = self.get_current_time_step_branches()
        # call on a function to print out the current time step's branches
        self.display_current_time_step_branches()
        
        choice = input('Please enter `Advance`, `Split`, or `QUIT`: ').replace(' ', '')
        while choice.lower() not in ['advance', 'split', 'quit']:
            choice = input('Please enter `Advance`, `Split`, or `QUIT`: ')
        return choice.lower()

    def advance(self) -> None:
        print("You've chosen to advance.")
        for item in self.current_time_step_branches.items():
            toggled_branch_string = self.toggle_cells(list(item[1]))
            # update with toggled value
            self.branch_states[self.time_step+1][item[0]] = toggled_branch_string

        self.time_step += 1
        
        print('---------------------------')
        print("Time step: ", self.time_step)

    def split(self) -> None:
        # note: Time step stays remains unchanged
        # split a particular branch
        branch_number = int(input("Please enter the branch for the split: "))

        # check that proposed branch length > 1
        # TODO: check that the branch number proposed exists!
        while len(self.current_time_step_branches[branch_number]) < 2:
            branch_number = int(input("Branches must have a minimum length of 2: "))

        split_location = int(input("Please enter the split location of the branch: "))

        while (split_location < 0) or (split_location > len(self.current_time_step_branches[branch_number])):
            split_location = int(input("Please enter a valid split position: "))

        
        # retrieve branch to be split
        branch_to_be_split = self.branch_states[self.time_step][branch_number]
        
        # split branch
        left_branch, right_branch = branch_to_be_split[:split_location], branch_to_be_split[split_location:]

        # reassign branch_to_be_split to left_branch
        self.branch_states[self.time_step][branch_number] = left_branch

        # have to deal with the case where we are splitting with multiple branches available
        if len(self.branch_states[self.time_step]) > 1:
            # deal with reassigning branch number values for other branches in current time step
            for item in self.branch_states[self.time_step].copy().items():
                branch, branch_string = item[0], item[1]
                if item[0] > branch_number:
                    # delete old entry
                    del self.branch_states[self.time_step][item[0]]
                    # increase the branch number by one
                    self.branch_states[self.time_step][branch + 1] = branch_string
        
        # case where we only have one branch to split on
        # deal with the right side of the split
        self.branch_states[self.time_step][branch_number + 1] = right_branch

    def quit_game(self) -> None:
        print("You've chosen to end the game")
        exit()

    # main game loop
    def play_game(self):
        print("Hello Welcome to EverLife Cycle!")
        self.set_game_length()
        self.set_cells_alive()
        self.display_time_step_zero()

        while self.run:
            # ask user what they would like to do next
            choice = self.next_action()
            if choice == 'advance':

                self.advance()
            
            elif choice == 'split':
                self.split()
            
            else:
                self.quit_game()
            
            # make sure to call here this since the update was only previously
            # called inside of self.get_current_time_step_branches
            self.current_time_step_branches = self.get_current_time_step_branches
            # check for cycles here
            
            cycle_length = 0
            for item in self.get_current_time_step_branches().items():
                cycle_length = self.check_cycles(item[0], item[1])

                if cycle_length > 0:
                    print(f"Cycle encountered in branch {item[0]}. Cycle length: {cycle_length}")
                    cycle_length = 0

if __name__ == '__main__':
    newGame = EverLifeGame().play_game()


class VariablePath:
    def __init__(self, variable_tuples):
        self.crossing_node, self.variable_type_name, self.value_path, self.variable_path = variable_tuples


    def print_variable_path(self):

        variable_name = self.variable_path[0].sentence

        print('-----------')
        print(self.variable_type_name)
        print('------------')
        print(f'{self.variable_type_name} val: {variable_name}')

        print('path a')

        for i in range(len(self.value_path)):
            sentence = self.value_path[i].sentence

            print(f'{i} =  {sentence}')

        print('path b')

        for i in range(len(self.variable_path)):
            sentence = self.variable_path[i].sentence

            print(f'{i} =  {sentence}')

        print('----------------------------------------------------')



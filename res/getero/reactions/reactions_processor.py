import os

from numba.core.ir import Raise


class ReactProcessor:
    def __init__(self):
        self.reactions = []

    def load(self, filename):
        file = open(filename,"r")
        Lines = file.readlines()
        self.define_surface_particles(Lines[0])
        self.define_gas_particles(Lines[3])
        print(self.surface_name_to_num)
        #print(self.surface_num_to_name)

        print(self.gas_name_to_num)
        #print(self.gas_num_to_name)
        for i in range(7,len(Lines)):
            if Lines[i]!="\n":
                self.process_reaction(Lines[i])




    def define_surface_particles(self,curr_str):
        self.surface_name_to_num = {}
        self.surface_num_to_name = {}
        curr_str = curr_str.split()
        for i in range(len(curr_str)):
            self.surface_name_to_num[curr_str[i]]=i
            self.surface_num_to_name[i]=curr_str[i]

    def define_gas_particles(self,curr_str):
        self.gas_name_to_num = {}
        self.gas_num_to_name = {}
        curr_str = curr_str.split()
        for i in range(len(curr_str)):
            self.gas_name_to_num[curr_str[i]] = i
            self.gas_num_to_name[i] = curr_str[i]

    def process_reaction(self, curr_str):
        self.reactions.append(Reaction(curr_str, self))

class Reaction:
    def __init__(self, curr_str, master: ReactProcessor):
        #print("---")
        #print(curr_str)
        self.master = master
        self.curr_str = (curr_str.replace("\n","")).split()
        #print(len(self.curr_str))
        self.reacts = []
        self.gas_products = []
        self.surface_products = []
        self.start_particle = None
        self.process_reaction(self.curr_str[0])

        print("Sp: ",self.start_particle," reacts: ", self.reacts, " gas_products: ", self.gas_products, " surface_products: ", self.surface_products)

    def process_reaction(self, str_reaction):
        #print(str_reaction)
        reacts, products = str_reaction.split("=")
        reacts, products = reacts.split("+"), products.split("+")
        for react in reacts:
            if react in self.master.gas_name_to_num:
                if self.start_particle is None:
                    self.start_particle = self.master.gas_name_to_num[react]
                else:
                    raise Exception("To start gas particles!!!")
            elif react in self.master.surface_name_to_num:
                self.reacts.append(self.master.surface_name_to_num[react])
            else:
                raise Exception("Unknown particle: ",react)

        for product in products:
            if product in self.master.gas_name_to_num:
                self.gas_products.append(self.master.gas_name_to_num[product])
            elif product in self.master.surface_name_to_num:
                self.surface_products.append(self.master.surface_name_to_num[product])
            else:
                raise Exception("Unknown particle: ",product)



A = ReactProcessor()
A.load("../../data/getero_cl2_ar.txt")

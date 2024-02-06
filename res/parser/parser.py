from res.const.parse_step import BAD_NAMES, CORRECT_ORDER
from res.parser.entities.factory import entity_factory

import res.config.step as config

from res.const.plot_config import PLOT_ORDER
class Parser:
    def __init__(self,filename):
        self.filename = filename
        self.objects = self.parse_step_file(filename)

    def parse_step_file(self, filename):
        f = open(filename)
        A = f.read()
        f.close()
        A = A.replace("\n","").split("#")
        str_objects = []
        new_object = []
        for i in range(len(A)):
            if "=" in A[i]:
                if new_object!=[]:
                    str_objects.append(new_object)
                new_object = []
            new_object.append(A[i])
        str_objects = str_objects[1:]
        objects = {}
        last_name = []
        for i in range(len(str_objects)):
            curr = str_objects[i]
            curr = "".join(curr)
            curr = curr.split("=")
            curr_id = int(curr[0])
            curr_str_data = curr[1][:-2]
            num_end = curr_str_data.index("(")
            curr_name = curr_str_data[:num_end]

            curr_params = curr_str_data[num_end+1:]
            if (last_name == "CARTESIAN_POINT") and (curr_name != "CARTESIAN_POINT"):
                break
            last_name = curr_name
            norm_el = True
            for name in BAD_NAMES:
                if name in curr_name:
                    norm_el = False
            if norm_el:
                if curr_name in objects:
                    objects[curr_name][curr_id] = curr_params[3:]
                else:
                    objects[curr_name] = {curr_id: curr_params[3:]}
        return objects

    def parsing(self):
        self.data = {}
        self.path_to_entities = {}
        #for key in self.objects:
        #    print("---")
        #    print(key + ":")
        #    print("---")
        #    for id in self.objects[key]:
        #        print(id, self.objects[key][id])
        print()
        for curr_type in CORRECT_ORDER:
            if curr_type in self.objects:
                self.path_to_entities[curr_type] = []
                for id in self.objects[curr_type]:
                    self.data[id] = entity_factory(curr_type, id, self.objects[curr_type][id], self.data)
                    self.path_to_entities[curr_type].append(id)
                del self.objects[curr_type]
        for key in self.objects:
            print(key, len(self.objects[key].keys()))
        num_entities = 0
        for curr_type in PLOT_ORDER:
            if curr_type in self.path_to_entities:
                num_entities+=len(self.path_to_entities[curr_type])
        print("Number of entities to draw: ", num_entities)
        config.max_num_entity = num_entities





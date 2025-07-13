import os
from pyglet import resource
from pyglet.resource import ResourceNotFoundException


class ResourceManager:
    def __init__(self, resource_folder_path: str, absolute_path=False):
        self.__resource_folder_path = resource_folder_path
        self.__resources = {}
        resources_categories = {}
        try:
            with open("extensions.txt", "r") as extensions_file:
                for line in extensions_file:
                    category, extensions = line.strip().split(":")
                    extensions = extensions.split(";")
                    for ext in extensions: resources_categories[ext] = category
        except FileNotFoundError:
            raise FileNotFoundError("extension file not found")

        if not absolute_path: path = resource_folder_path.replace("\\", "/")
        else: path = f"{os.getcwd()}\\{resource_folder_path}".replace("\\", "/")
        try:
            for filename in os.listdir(path):
                name, extension = filename.split(".")
                print(filename, f"{path}/{filename}")
                category = resources_categories[extension]
                match category:
                    case "image":
                        self.__resources[name] = resource.image(f"{path}/{filename}")
                    case "sound":
                        pass
        except ResourceNotFoundException:
            print("resources not found via path", self.__resource_folder_path)



    def get(self, name): return self.__resources[name]



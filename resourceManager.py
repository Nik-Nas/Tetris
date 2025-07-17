import os
from typing import Iterable

from pyglet import resource, media
from pyglet.media import Player, Source
from pyglet.media.exceptions import MediaException
from pyglet.resource import ResourceNotFoundException


class ResourceManager:
    def __init__(self, resource_folder_path: str, absolute_path=False):

        # making final path
        if not absolute_path:
            self.__path = resource_folder_path.replace("\\", "/")
        else:
            self.__path = f"{os.getcwd()}\\{resource_folder_path}".replace("\\", "/")

        # creating dictionaries for different types of resources
        self._images = {}
        self._audios = {}
        self._animations = {}
        self._videos = {}

        # reading file with media type - extension associations
        categories = {}
        with open("extensions.txt", "r") as extensions_file:
            for line in extensions_file:
                category, extensions = line.strip().split(":")
                for ext in extensions.split(";"): categories[ext] = category

        # trying to get all files in given resource directory
        try:
            for filename in os.listdir(self.__path):
                # splitting filename into it's name and it's extension
                name, extension = filename.split(".")

                # finding category of current file in the list by its extension
                category = categories[extension]

                #import resource according to its type
                match category:
                    case "image":
                        self._images[name] = resource.image(f"{self.__path}/{filename}")
                    case "sound":
                        self._audios[name] = media.load(f"{self.__path}/{filename}")
                        pass
        except (ResourceNotFoundException, MediaException):
            #if things gone a little bit piz@ec, make sure developer will be noted
            print("resources not found via path", self.__path)
        del categories

    def image(self, name):
        return self._images[name]

    def audio(self, name):
        return self._audios[name]

    def animation(self, name):
        return self._animations[name]

    def video(self, name):
        return self._videos[name]

    @property
    def images(self):
        return self._images

    @property
    def audios(self):
        return self._audios

    @property
    def videos(self):
        return self._videos

    @property
    def animations(self):
        return self._animations


class CustomSource(Source):
    last_id = -1

    def __init__(self, source: Source = None) -> None:
        if source is not None:
            self.__dict__.update(source.__dict__)
        else:
            super().__init__()
        self._player_id = -1
        self.last_id += 1
        self._id = self.last_id

    @property
    def id(self): return self._id

    @property
    def player_id(self): return self._player_id


class CustomPlayer(Player):
    last_id = -1

    def __init__(self, group: str):
        super().__init__()
        self.last_id += 1
        self._id = self.last_id
        self.group = group

    @property
    def id(self): return  self._id

    @property
    def source(self) -> CustomSource | None: return super()._source

    @property
    def current_track_name(self): return self.source.name

    def _set_source(self, new_source: CustomSource | None) -> None: super()._set_source(new_source)

    def queue(self, source: CustomSource | Iterable[CustomSource]) -> None: super().queue(source)

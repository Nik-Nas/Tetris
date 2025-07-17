from pyglet.media import Player

from resourceManager import ResourceManager


class AudioManager:
    default_player_id = 0

    def __init__(self, resource_manager: ResourceManager):
        self._tracks = {}
        self._fxs = {}
        self._players = {0: Player()}
        self._limit = 100
        self._last_player_id = 0
        audios = resource_manager.audios
        for name, audio in audios.items():
            # TODO add differentiation by ending of filename
            if audio.duration <= 10.0:
                self._fxs[name] = audio
            else:
                self._tracks[name] = audio

    def add_player(self, group="in-game") -> int:
        self._last_player_id += 1
        self._players[self._last_player_id] = Player()
        return self._last_player_id


    def delete_player(self, player_id: str) -> None:
        if player_id == 0 or player_id not in self._players:
            raise ValueError("Invalid id (such player does not exists or given id is default")
        for index, player in self._players.items():
            if index == player_id:
                player.delete()
                return
        raise ValueError(f"player with given id({player_id}) doesn't exist")

    def play_track(self, name: str, player_id=0, loop=False, volume=100.0) -> None:
        if player_id not in self._players:
            raise ValueError("Invalid id (such player does not exists)")
        if name not in self._tracks: raise ValueError(f"track with name {name} does not exists")
        player = self._players[player_id]
        if loop: player.loop = True
        player.volume = volume / 100
        player.queue(self._tracks[name])
        player.play()


    def pause_track(self, name: str):
        if name is None: raise ValueError("name of track could not be None")
        if name not in self._tracks: raise ValueError(f"track with name {name} does not exists")

        player_id = self._tracks[name].player_id
        if player_id >= 0:
            player = self._players[player_id]
            player.pause()

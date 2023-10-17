from core.replay.data.PlayerState import PlayerState


class PlayerStateChange:
    @staticmethod
    def get(curr_state: PlayerState, prev_state: PlayerState = None):
        if prev_state is None:
            return None
        return PlayerStateChange(on_dead=not prev_state.is_dead and curr_state.is_dead,
                                 on_blast_pickup=not prev_state.has_blast and curr_state.has_blast)

    def __init__(self, on_dead: bool, on_blast_pickup: bool):
        self.__on_dead = on_dead
        self.__on_blast_pickup = on_blast_pickup

    @property
    def on_dead(self) -> bool:
        return self.__on_dead

    @property
    def on_blast_pickup(self) -> bool:
        return self.__on_blast_pickup

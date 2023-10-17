from core.replay.data.FrameData import FrameData
from core.replay.data.GameObjectState import GameObjectState


class FrameObjectsChange:
    @staticmethod
    def get(curr_frame: FrameData, prev_frame: FrameData = None):
        if prev_frame is None:
            created = curr_frame.bonuses
            created.update(curr_frame.projectiles)
            if len(created) == 0:
                return None

            return FrameObjectsChange(created=created,
                                      updated={},
                                      deleted={})
        else:
            prev = prev_frame.all_objects.keys()
            curr = curr_frame.all_objects.keys()
            updated_ids = prev & curr
            created_ids = curr - prev
            deleted_ids = prev - curr

            if len(updated_ids) == 0 and len(created_ids) == 0 and len(deleted_ids) == 0:
                return None

            return FrameObjectsChange(created={oid: curr_frame.all_objects[oid] for oid in created_ids},
                                      updated={oid: curr_frame.all_objects[oid] for oid in updated_ids},
                                      deleted={oid: prev_frame.all_objects[oid] for oid in deleted_ids})

    def __init__(self,
                 created: dict[str, GameObjectState],
                 updated: dict[str, GameObjectState],
                 deleted: dict[str, GameObjectState]):
        self.__created = created
        self.__updated = updated
        self.__deleted = deleted

    @property
    def created(self) -> dict[str, GameObjectState]:
        return self.__created

    @property
    def updated(self) -> dict[str, GameObjectState]:
        return self.__updated

    @property
    def deleted(self) -> dict[str, GameObjectState]:
        return self.__deleted

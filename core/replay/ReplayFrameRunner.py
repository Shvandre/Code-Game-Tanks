from core.objects.Blast import Blast
from core.objects.Bonus import Bonus
from core.objects.BonusBlast import BonusBlast
from core.objects.BonusRepair import BonusRepair
from core.objects.Bullet import Bullet
from core.objects.Projectile import Projectile
from core.objects.Tank import Tank
from core.replay.data.FrameObjectsChange import FrameObjectsChange
from core.replay.data.ReplayData import ReplayData


class ReplayFrameRunner:
    def __init__(self, replay_data: ReplayData, tanks: [Tank], projectiles: [Projectile], bonuses: [Bonus]):
        self.__replay_data = replay_data
        self.__tanks = tanks
        self.__projectiles = projectiles
        self.__bonuses = bonuses
        self.__current_frame_index = 0
        self.__prev_frame = None

    def has_next_frame(self):
        return self.__current_frame_index < self.__replay_data.frames_count

    def update(self):
        if not self.has_next_frame():
            return
        frame = self.__replay_data.frame(self.__current_frame_index)

        self.__update_tanks(frame)
        objects_change = FrameObjectsChange.get(curr_frame=frame, prev_frame=self.__prev_frame)
        if objects_change is not None:
            self.__update_objects(frame, objects_change)

        self.__prev_frame = frame
        self.__current_frame_index += 1

    def __update_tanks(self, frame):
        for tank in self.__tanks:
            if tank.id not in frame.players:
                raise Exception(f'ERROR ON FRAME {self.__current_frame_index}: tank {tank.id} not found in state')
            tank_state = frame.players[tank.id]
            tank.update_tank_from_replay_frame(x=tank_state.x,
                                               y=tank_state.y,
                                               angle=tank_state.angle,
                                               score=tank_state.score,
                                               health=tank_state.health,
                                               has_blast=tank_state.has_blast)
            tank.update_ui()

    def __update_objects(self, frame, objects_change):
        self.__projectiles[:] = [p for p in self.__projectiles if p.id not in objects_change.deleted]
        for projectile in self.__projectiles:
            if projectile.id in objects_change.updated:
                state = frame.projectiles[projectile.id]
                projectile.update_object_from_replay_frame(x=state.x,
                                                           y=state.y,
                                                           angle=state.angle)

        self.__bonuses[:] = [b for b in self.__bonuses if b.id not in objects_change.deleted]
        for bonus in self.__bonuses:
            if bonus.id in objects_change.updated:
                state = frame.bonuses[bonus.id]
                bonus.update_object_from_replay_frame(x=state.x,
                                                      y=state.y,
                                                      angle=state.angle)

        for oid, state in objects_change.created.items():
            if state.is_bullet:
                self.__projectiles.append(
                    Bullet(oid=oid,
                           x=state.x,
                           y=state.y,
                           angle=state.y,
                           owner=None,
                           is_ui=True)
                )
            elif state.is_blast:
                self.__projectiles.append(
                    Blast(oid=oid,
                          x=state.x,
                          y=state.y,
                          angle=state.y,
                          owner=None,
                          is_ui=True)
                )
            elif state.is_bonus_repair:
                self.__bonuses.append(
                    BonusRepair(oid=oid,
                                x=state.x,
                                y=state.y,
                                spawned_at=frame.id,
                                is_ui=True)
                )
            elif state.is_bonus_blast:
                self.__bonuses.append(
                    BonusBlast(oid=oid,
                               x=state.x,
                               y=state.y,
                               spawned_at=frame.id,
                               is_ui=True)
                )
        if len(self.__projectiles) is not len(frame.projectiles):
            print(f'INCONSISTENT STATE on frame {frame.id}: projectiles count {len(self.__projectiles)}(form scene) != {len(frame.projectiles)}(from frame state)')

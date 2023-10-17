from bots.BotAggressive import BotAggressive
from bots.BotInadequate import BotInadequate
from bots.IdleBot import IdleBot


class PresetBots:

    @staticmethod
    def staticDefender(name="Бот без тяги"):
        return IdleBot(name)

    @staticmethod
    def random(name="Рандомный"):
        return BotInadequate(name)

    @staticmethod
    def attacking(name="Бот-атакующий"):
        return BotAggressive(name)

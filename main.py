from MyBot import MyBot
from bots.PresetBots import PresetBots
from core.Game import Game


def main():
    game = Game.create()
    game.setup_new_battle(
        "Бой",
        [
            PresetBots.attacking("Игрок 1"),
            PresetBots.attacking("Игрок 2"),
            PresetBots.random("Игрок 3"),
            MyBot("Мой бот"),
        ]
    )
    game.run()


if __name__ == "__main__":
    main()

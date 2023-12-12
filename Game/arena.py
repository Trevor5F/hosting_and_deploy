from typing import Dict, Any, Optional
from unit import BaseUnit


class BaseSingleton(type):
    _instances: Dict[Any, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    const = 2.3
    player: BaseUnit
    enemy: BaseUnit
    battle_result: str = ''
    game_is_running = False


    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        self.game_is_running = True
        self.player = player
        self.enemy = enemy


    def _check_players_hp(self) -> Optional[str]:
        if self.player.hp > 0 and self.enemy.hp > 0:
            return None
        if self.player.hp > 0:
            battle_result = 'Игрок победил!'
        elif self.enemy.hp > 0:
            battle_result = 'Игрок проиграл!'
        else:
            battle_result = 'Ничья!'
        self.battle_result = battle_result
        return battle_result



    def _stamina_regeneration(self):
        self.player.stamina = round(self.player.stamina + self.const * self.player.stamina_modify, 1)
        if self.player.stamina > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina


        self.enemy.stamina = round(self.enemy.stamina + self.const * self.enemy.stamina_modify, 1)
        if self.enemy.stamina > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina


    def next_turn(self) -> Optional[str]:
        if self._check_players_hp():
            return self._end_game()
        else:
            self._stamina_regeneration()
        return self.enemy.hit(self.player)



    def _end_game(self) -> Optional[str]:
        Arena._instances = {}
        self.game_is_running = False
        return self.battle_result


    def player_hit(self) -> Optional[str]:
        return self.player.hit(self.enemy)


    def player_use_skill(self) -> Optional[str]:
        return self.player.use_skill(self.enemy)

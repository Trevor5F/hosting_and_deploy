from abc import ABC

class Skill(ABC):
    _name: str
    _damage: float
    _necessary_stamina: float


    def use(self, unit, target) -> str:
        if unit.stamina >= self._necessary_stamina:
             target.get_damage(self._damage)
             return f"{unit.name} использует {self._name} и наносит {self._damage} урона сопернику."
        return f"{unit.name} попытался использовать {self._name}, но у него не хватило выносливости."


class FuryPunch(Skill):
    _name = "Свирепый пинок"
    _damage = 12
    _necessary_stamina = 6



class HardShot(Skill):
    _name = "Мощный укол"
    _damage = 15
    _necessary_stamina = 5


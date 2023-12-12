from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
import pymorphy2
from equipment import Weapon, Armor
from classes import UnitClass
from random import randint


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.stamina_modify = unit_class.stamina_mod
        self.weapon: Weapon
        self.armor: Armor
        self._is_skill_used = False


    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon


    def equip_armor(self, armor: Armor):
        self.armor = armor


    def _count_damage(self, target: BaseUnit) -> float:
        attackers_damage = self.weapon.get_damage_by_weapon() * self.unit_class.attack
        self.stamina = round(self.stamina - self.weapon.stamina_per_hit, 1)
        if self.stamina < 0:
            self.stamina = 0


        if target.stamina >= target.armor.stamina_per_turn:
            target_armor = target.armor.defence * target.unit_class.armor
            target.stamina = round(target.stamina - target.armor.stamina_per_turn, 1)
        else:
            target_armor = 0


        damage = round(attackers_damage - target_armor, 1)
        if damage > 0:
            target.get_damage(damage)
        else:
            damage = 0

        return damage


    def get_damage(self, damage: float):
        self.hp = round(self.hp - damage, 1)
        if self.hp < 0:
            self.hp = 0


    def use_skill(self, target: BaseUnit) -> Optional[str]:
        if self._is_skill_used:
            return None
        result = self.unit_class.skill.use(unit=self, target=target)
        if result:
            self._is_skill_used = True
        return result


    @abstractmethod
    def hit(self, target: BaseUnit) -> Optional[str]:
        pass


    def strike(self, target: BaseUnit) -> str:
        if self.stamina >= self.weapon.stamina_per_hit:
            hit_dem = self._count_damage(target)
            if hit_dem != 0:
                return f" {self.name} используя {self._get_accusative(self.weapon.name)} пробивает " \
                       f"{self._get_accusative(target.armor.name)} {self._get_accusative(target.name).title()} и наносит {hit_dem} урона. "
            return f" {self.name} используя {self._get_accusative(self.weapon.name)} наносит удар, " \
                   f"но {target.armor.name} {self._get_accusative(target.name).title()} его останавливает. "
        return f" {self.name} попытался использовать {self._get_accusative(self.weapon.name)}, " \
               f"но у него не хватило выносливости. "

    @staticmethod
    def _get_accusative(word: str) -> str:
        morph = pymorphy2.MorphAnalyzer()
        result = [morph.parse(elem)[0].inflect({'accs'}).word for elem in word.split()]
        return ' '.join(result)


    def name(self) -> str:
        return self.name


    def unit_class(self) -> UnitClass:
        return self.unit_class


    def hp(self) -> float:
        return self.hp


    def stamina(self) -> float:
        return self.stamina


    def weapon(self) -> Weapon:
        return self.weapon


    def armor(self) -> Armor:
        return self.armor


    def stamina_modify(self) -> float:
        return self.stamina_modify



class PlayerUnit(BaseUnit):
    def hit(self, target: BaseUnit) -> Optional[str]:
        return self.strike(target)


class PC_Unit(BaseUnit):
    def hit(self, target: BaseUnit) -> Optional[str]:
        if not self._is_skill_used and randint(1, 10) <= 1:
            return self.use_skill(target)
        return self.strike(target)


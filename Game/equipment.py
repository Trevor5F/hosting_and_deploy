import json
from dataclasses import dataclass
import random
from typing import List, Optional

import marshmallow_dataclass


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float # Количество затрачиваемой выносливости за удар

    def get_damage_by_weapon(self) -> float:
        damage = random.uniform(self.min_damage, self.max_damage) # случайное число с плавающей точкой
        return round(damage, 1) # до одного знака


@dataclass
class Armor:
    id: int
    name: str
    defence: float # Очки защиты
    stamina_per_turn: float # Количество затрачиваемой выносливости за ход


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment(): # Снаряжение
    def __init__(self):
        self._equipment = self._get_data()

    @staticmethod
    def _get_data():
        with open('data/equipment.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        try:
            return marshmallow_dataclass.class_schema(EquipmentData)().load(data)
        except:
            raise ValueError

    def get_weapon(self, name: str) -> Optional[Weapon]:
        for weapon in self._equipment.weapons:
            if name == weapon.name:
                return weapon
        return None


    def get_weapon_names(self) -> List[str]:
        return [weapon.name for weapon in self._equipment.weapons]


    def get_armor(self, name: str) -> Optional[Armor]:
        for armor in self._equipment.armors:
            if name == armor.name:
                return armor
        return None


    def get_armor_names(self) -> List[str]:
        return [armor.name for armor in self._equipment.armors]

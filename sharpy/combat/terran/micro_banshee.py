from typing import *

from sc2.ids.buff_id import BuffId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2
from sc2.units import Units
from sharpy.combat import *
from sc2.ids.ability_id import AbilityId
from sc2.unit import Unit
from sharpy.interfaces.combat_manager import MoveType


class MicroBanshee(GenericMicro):
    def __init__(self):
        super().__init__()

    def init_group(
        self,
        rules: "MicroRules",
        group: CombatUnits,
        units: Units,
        enemy_groups: List[CombatUnits],
        move_type: MoveType,
        original_target: Point2,
    ):
        super().init_group(
            rules, group, units, enemy_groups, move_type, original_target
        )

    def group_solve_combat(self, units: Units, current_command: Action) -> Action:
        return current_command

    def unit_solve_combat(self, unit: Unit, current_command: Action) -> Action:
        # There no reason to cloak if near only structures
        enemy_units = self.cache.enemy_in_range(unit.position, 10).filter(lambda unit: self.unit_values.can_shoot_air(unit))
        if unit.energy > 40 and len(enemy_units) > 0 :
            return Action(None, False, AbilityId.BEHAVIOR_CLOAKON_GHOST)

        if unit.energy < 10 and len(enemy_units) == 0:
            return Action(None, False, AbilityId.BEHAVIOR_CLOAKOFF_GHOST)


        return super().unit_solve_combat(unit, current_command)
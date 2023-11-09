from typing import List
from sc2.unit import Unit
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sharpy.managers.core import *
from sharpy.managers.core.roles import unit_task
from sharpy.plans.terran import *
from typing import List, Optional
from sharpy.interfaces import IZoneManager

from sc2.ids.unit_typeid import UnitTypeId
from sharpy.plans.acts import *
from sharpy.plans.acts.terran import *
from sharpy.plans.require import *
from sharpy.plans.tactics import *
from sharpy.plans.tactics.terran import *
from sharpy.combat import MicroRules
from sc2.ids.effect_id import EffectId


from sharpy.knowledges import Knowledge

from sc2.ids.unit_typeid import UnitTypeId
from sc2.units import Units
from sharpy.combat import *
from sc2.unit import Unit
from sharpy.interfaces.combat_manager import MoveType

from sharpy.plans.acts import ActBase

workers = {UnitTypeId.SCV, UnitTypeId.DRONE, UnitTypeId.PROBE}

class MarineSplit(MicroStep):
    def group_solve_combat(self, units: Units, current_command: Action) -> Action:
        pass


    def unit_solve_combat(self, unit: Unit, current_command: Action) -> Action:

        pass

class DisruptorSplit(ActBase):
    def __init__(self, marines_to_start: int = 1):
        self.micro = MicroRules()
        self.micro.load_default_methods()
        self.micro.generic_micro = MarineSplit()
        # Following would work for a specific unit type:
        # self.micro.unit_micros[UnitTypeId.REAPER]
        super().__init__()
        
    async def start(self, knowledge: "Knowledge"):
        self.zone_manager = knowledge.get_required_manager(IZoneManager)
        await super().start(knowledge)
        # MicroRules is also a Component and needs start
        self.role_manager = knowledge.get_required_manager(UnitRoleManager)    
        await self.micro.start(knowledge)
        
    async def execute(self) -> bool:
        for effect in self.ai.state.effects:
            if effect.id == EffectId.RAVAGERCORROSIVEBILECP:

                if UnitExists(UnitTypeId.MARINE):
                    for unit in self.cache.own(UnitTypeId.MARINE):        
                        self.combat.add_unit(unit)
                        for epos in effect.positions:
                            if unit.position.distance_to_point2(epos) < 5:
                                return Action(unit.position.towards(epos, -5), False, AbilityId.MOVE_MOVE)


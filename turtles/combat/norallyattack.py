from typing import List
from sc2.unit import Unit
from sc2.ids.unit_typeid import UnitTypeId
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

from sharpy.knowledges import Knowledge

from sc2.ids.unit_typeid import UnitTypeId
from sc2.units import Units
from sharpy.combat import *
from sc2.unit import Unit
from sharpy.interfaces.combat_manager import MoveType

from sharpy.plans.acts import ActBase

workers = {UnitTypeId.SCV, UnitTypeId.DRONE, UnitTypeId.PROBE, UnitTypeId.MULE}

combat_units = {UnitTypeId.LIBERATOR, UnitTypeId.WIDOWMINE, UnitTypeId.MARINE, UnitTypeId.MARAUDER, UnitTypeId.MEDIVAC,
UnitTypeId.SIEGETANK, UnitTypeId.GHOST, UnitTypeId.VIKINGFIGHTER, UnitTypeId.VIKINGASSAULT, UnitTypeId.SIEGETANKSIEGED, UnitTypeId.RAVEN}

class AttackPlz(MicroStep):
    def group_solve_combat(self, units: Units, current_command: Action) -> Action:
        pass


    def unit_solve_combat(self, unit: Unit, current_command: Action) -> Action:

        pass

class NoRallyAttack(ActBase):
    def __init__(self, units_to_start: int = 20, movetype = MoveType.SearchAndDestroy):
        self.micro = MicroRules()
        self.micro.load_default_methods()
        self.micro.generic_micro = AttackPlz()
        self.units_to_start = units_to_start
        self.movetype = movetype
        super().__init__()
        
    async def start(self, knowledge: "Knowledge"):
        self.zone_manager = knowledge.get_required_manager(IZoneManager)
        await super().start(knowledge)
        # MicroRules is also a Component and needs start
        self.role_manager = knowledge.get_required_manager(UnitRoleManager)    
        await self.micro.start(knowledge)
        
    async def execute(self) -> bool:
        target = self.zone_manager.enemy_start_location
        if self.ai.supply_army >= self.units_to_start:
            for unit in self.cache.own(combat_units):
                self.combat.add_unit(unit)
                self.roles.set_task(8, unit)
            
            self.combat.execute(target, self.movetype)

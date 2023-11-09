from sc2.ids.unit_typeid import UnitTypeId
from sc2.units import Units
from sharpy.combat import *
from sc2.unit import Unit
from sharpy.interfaces.combat_manager import MoveType

from sharpy.plans.acts import ActBase
from sharpy.knowledges import Knowledge

from turtles.infotables.protosscounters import ProtossCounters
from turtles.infotables.terrancounters import TerranCounters
from turtles.infotables.zergcounters import ZergCounters
from turtles.infotables.terranunitdata import TerranUnitData
from sharpy.plans.require import *
from sharpy.plans.acts import *
from sharpy.plans.build_step import Step


from dataclasses import dataclass
from operator import attrgetter
from typing import Any

@dataclass
class UnitResponse:
    unit_data: Any
    threat_level: float

protoss = ProtossCounters()
zerg = ZergCounters()
terran = TerranCounters()
unitdata = TerranUnitData()

class BuildRax(GridBuilding):
    def __init__(self):
        self.foo = None
        self.marinecounters = protoss.marinecounters + zerg.marinecounters + terran.marinecounters
        self.maraudercounters = protoss.maraudercounters + zerg.maraudercounters + terran.maraudercounters
        self.vikingcounters = protoss.vikingcounters + zerg.vikingcounters + terran.vikingcounters
        self.widowminecounters = protoss.widowminecounters + zerg.widowminecounters + terran.widowminecounters
        self.tankcounters = protoss.tankcounters + zerg.tankcounters + terran.tankcounters
        self.liberatorcounters = protoss.liberatorcounters + zerg.liberatorcounters + terran.liberatorcounters
        self.ghostcounters = protoss.ghostcounters + zerg.ghostcounters + terran.ghostcounters
        self.thorcounters = zerg.thorcounters + terran.thorcounters
        self.battlecruisercounters = terran.battlecruisercounters
        super().__init__(UnitTypeId.BARRACKS, 0)
        # super().__init__()


    async def start(self, knowledge: "Knowledge"):
        await super().start(knowledge)

    async def get_threats(self):
        enemy_units = self.ai.all_enemy_units
        marine = 0
        marauder = 0
        viking = 0
        widowmine = 0
        tank = 0
        liberator = 0
        ghost = 0
        thor = 0
        battlecruiser = 0
        if not enemy_units == []:
            for enemy in enemy_units:
                for unit in self.marinecounters:
                    if enemy.type_id == unit.unit_id:
                        marine += unit.threat_level

                for unit in self.maraudercounters:
                    if enemy.type_id == unit.unit_id:
                        marauder += unit.threat_level

                for unit in self.vikingcounters:
                    if enemy.type_id == unit.unit_id:
                        viking += unit.threat_level

                for unit in self.widowminecounters:
                    if enemy.type_id == unit.unit_id:
                        widowmine += unit.threat_level   

                for unit in self.tankcounters:
                    if enemy.type_id == unit.unit_id:
                        tank += unit.threat_level

                for unit in self.liberatorcounters:
                    if enemy.type_id == unit.unit_id:
                        liberator += unit.threat_level

                for unit in self.ghostcounters:
                    if enemy.type_id == unit.unit_id:
                        ghost += unit.threat_level            

                for unit in self.thorcounters:
                    if enemy.type_id == unit.unit_id:
                        thor += unit.threat_level

                for unit in self.battlecruisercounters:
                    if enemy.type_id == unit.unit_id:
                        battlecruiser += unit.threat_level

        threats = [marine, marauder, viking, widowmine, tank, liberator, ghost, thor, battlecruiser]
        return threats

    async def request_units(self):
        threats = await self.get_threats()
        marine = UnitResponse(unitdata.marine, threats[0])     
        marauder = UnitResponse(unitdata.marauder, threats[1])
        viking = UnitResponse(unitdata.viking, threats[2])
        widowmine = UnitResponse(unitdata.widowmine, threats[3])
        tank = UnitResponse(unitdata.siegetank, threats[4])
        liberator = UnitResponse(unitdata.liberator, threats[5])
        ghost = UnitResponse(unitdata.ghost, threats[6])
        thor = UnitResponse(unitdata.thor, threats[7])
        battlecruiser = UnitResponse(unitdata.battlecruiser, threats[8])

        units = [marine, marauder, viking, widowmine, tank, liberator, ghost, thor, battlecruiser]  
        units = sorted(units,key=attrgetter("threat_level"),reverse=True)

        if units[0].unit_data.production == UnitTypeId.BARRACKS:
            return 2 + self.cache.own_townhalls.amount
        elif units[1].unit_data.production == UnitTypeId.BARRACKS:
            return 1 + self.cache.own_townhalls.amount
        elif units[2].unit_data.production == UnitTypeId.BARRACKS:
            return 0 + self.cache.own_townhalls.amount

        return(0)


    async def execute(self):
        self.to_count = await self.request_units()
        return await super().execute()

class BuildFactories(GridBuilding):
    def __init__(self):
        self.foo = None
        self.marinecounters = protoss.marinecounters + zerg.marinecounters + terran.marinecounters
        self.maraudercounters = protoss.maraudercounters + zerg.maraudercounters + terran.maraudercounters
        self.vikingcounters = protoss.vikingcounters + zerg.vikingcounters + terran.vikingcounters
        self.widowminecounters = protoss.widowminecounters + zerg.widowminecounters + terran.widowminecounters
        self.tankcounters = protoss.tankcounters + zerg.tankcounters + terran.tankcounters
        self.liberatorcounters = protoss.liberatorcounters + zerg.liberatorcounters + terran.liberatorcounters
        self.ghostcounters = protoss.ghostcounters + zerg.ghostcounters + terran.ghostcounters
        self.thorcounters = zerg.thorcounters + terran.thorcounters
        self.battlecruisercounters = terran.battlecruisercounters
        super().__init__(UnitTypeId.FACTORY, 0)
        # super().__init__()


    async def start(self, knowledge: "Knowledge"):
        await super().start(knowledge)

    async def get_threats(self):
        enemy_units = self.ai.all_enemy_units
        marine = 0
        marauder = 0
        viking = 0
        widowmine = 0
        tank = 0
        liberator = 0
        ghost = 0
        thor = 0
        battlecruiser = 0
        if not enemy_units == []:
            for enemy in enemy_units:
                for unit in self.marinecounters:
                    if enemy.type_id == unit.unit_id:
                        marine += unit.threat_level

                for unit in self.maraudercounters:
                    if enemy.type_id == unit.unit_id:
                        marauder += unit.threat_level

                for unit in self.vikingcounters:
                    if enemy.type_id == unit.unit_id:
                        viking += unit.threat_level

                for unit in self.widowminecounters:
                    if enemy.type_id == unit.unit_id:
                        widowmine += unit.threat_level   

                for unit in self.tankcounters:
                    if enemy.type_id == unit.unit_id:
                        tank += unit.threat_level

                for unit in self.liberatorcounters:
                    if enemy.type_id == unit.unit_id:
                        liberator += unit.threat_level

                for unit in self.ghostcounters:
                    if enemy.type_id == unit.unit_id:
                        ghost += unit.threat_level            

                for unit in self.thorcounters:
                    if enemy.type_id == unit.unit_id:
                        thor += unit.threat_level

                for unit in self.battlecruisercounters:
                    if enemy.type_id == unit.unit_id:
                        battlecruiser += unit.threat_level

        threats = [marine, marauder, viking, widowmine, tank, liberator, ghost, thor, battlecruiser]
        return threats

    async def request_units(self):
        threats = await self.get_threats()
        marine = UnitResponse(unitdata.marine, threats[0])     
        marauder = UnitResponse(unitdata.marauder, threats[1])
        viking = UnitResponse(unitdata.viking, threats[2])
        widowmine = UnitResponse(unitdata.widowmine, threats[3])
        tank = UnitResponse(unitdata.siegetank, threats[4])
        liberator = UnitResponse(unitdata.liberator, threats[5])
        ghost = UnitResponse(unitdata.ghost, threats[6])
        thor = UnitResponse(unitdata.thor, threats[7])
        battlecruiser = UnitResponse(unitdata.battlecruiser, threats[8])

        units = [marine, marauder, viking, widowmine, tank, liberator, ghost, thor, battlecruiser]  
        units = sorted(units,key=attrgetter("threat_level"),reverse=True)

        if units[0].unit_data.production == UnitTypeId.FACTORY:
            return 2 + self.cache.own_townhalls.amount
        elif units[1].unit_data.production == UnitTypeId.FACTORY:
            return 0 + self.cache.own_townhalls.amount
        elif units[2].unit_data.production == UnitTypeId.FACTORY:
            return 0 + self.cache.own_townhalls.amount

        return(0)


    async def execute(self):
        self.to_count = await self.request_units()
        return await super().execute()

class BuildStarports(GridBuilding):
    def __init__(self):
        self.foo = None
        self.marinecounters = protoss.marinecounters + zerg.marinecounters + terran.marinecounters
        self.maraudercounters = protoss.maraudercounters + zerg.maraudercounters + terran.maraudercounters
        self.vikingcounters = protoss.vikingcounters + zerg.vikingcounters + terran.vikingcounters
        self.widowminecounters = protoss.widowminecounters + zerg.widowminecounters + terran.widowminecounters
        self.tankcounters = protoss.tankcounters + zerg.tankcounters + terran.tankcounters
        self.liberatorcounters = protoss.liberatorcounters + zerg.liberatorcounters + terran.liberatorcounters
        self.ghostcounters = protoss.ghostcounters + zerg.ghostcounters + terran.ghostcounters
        self.thorcounters = zerg.thorcounters + terran.thorcounters
        self.battlecruisercounters = terran.battlecruisercounters
        super().__init__(UnitTypeId.STARPORT, 0)
        # super().__init__()


    async def start(self, knowledge: "Knowledge"):
        await super().start(knowledge)

    async def get_threats(self):
        enemy_units = self.ai.all_enemy_units
        marine = 0
        marauder = 0
        viking = 0
        widowmine = 0
        tank = 0
        liberator = 0
        ghost = 0
        thor = 0
        battlecruiser = 0
        if not enemy_units == []:
            for enemy in enemy_units:
                for unit in self.marinecounters:
                    if enemy.type_id == unit.unit_id:
                        marine += unit.threat_level

                for unit in self.maraudercounters:
                    if enemy.type_id == unit.unit_id:
                        marauder += unit.threat_level

                for unit in self.vikingcounters:
                    if enemy.type_id == unit.unit_id:
                        viking += unit.threat_level

                for unit in self.widowminecounters:
                    if enemy.type_id == unit.unit_id:
                        widowmine += unit.threat_level   

                for unit in self.tankcounters:
                    if enemy.type_id == unit.unit_id:
                        tank += unit.threat_level

                for unit in self.liberatorcounters:
                    if enemy.type_id == unit.unit_id:
                        liberator += unit.threat_level

                for unit in self.ghostcounters:
                    if enemy.type_id == unit.unit_id:
                        ghost += unit.threat_level            

                for unit in self.thorcounters:
                    if enemy.type_id == unit.unit_id:
                        thor += unit.threat_level

                for unit in self.battlecruisercounters:
                    if enemy.type_id == unit.unit_id:
                        battlecruiser += unit.threat_level

        threats = [marine, marauder, viking, widowmine, tank, liberator, ghost, thor, battlecruiser]
        return threats

    async def request_units(self):
        threats = await self.get_threats()
        marine = UnitResponse(unitdata.marine, threats[0])     
        marauder = UnitResponse(unitdata.marauder, threats[1])
        viking = UnitResponse(unitdata.viking, threats[2])
        widowmine = UnitResponse(unitdata.widowmine, threats[3])
        tank = UnitResponse(unitdata.siegetank, threats[4])
        liberator = UnitResponse(unitdata.liberator, threats[5])
        ghost = UnitResponse(unitdata.ghost, threats[6])
        thor = UnitResponse(unitdata.thor, threats[7])
        battlecruiser = UnitResponse(unitdata.battlecruiser, threats[8])

        units = [marine, marauder, viking, widowmine, tank, liberator, ghost, thor, battlecruiser]  
        units = sorted(units,key=attrgetter("threat_level"),reverse=True)

        if units[0].unit_data.production == UnitTypeId.STARPORT:
            return 2 + self.cache.own_townhalls.amount
        elif units[1].unit_data.production == UnitTypeId.STARPORT:
            return 0 + self.cache.own_townhalls.amount
        elif units[2].unit_data.production == UnitTypeId.STARPORT:
            return 0 + self.cache.own_townhalls.amount

        return(0)


    async def execute(self):
        self.to_count = await self.request_units()
        return await super().execute()

class BuildArmory(GridBuilding):
    def __init__(self):
        self.foo = None
        self.marinecounters = protoss.marinecounters + zerg.marinecounters + terran.marinecounters
        self.maraudercounters = protoss.maraudercounters + zerg.maraudercounters + terran.maraudercounters
        self.vikingcounters = protoss.vikingcounters + zerg.vikingcounters + terran.vikingcounters
        self.widowminecounters = protoss.widowminecounters + zerg.widowminecounters + terran.widowminecounters
        self.tankcounters = protoss.tankcounters + zerg.tankcounters + terran.tankcounters
        self.liberatorcounters = protoss.liberatorcounters + zerg.liberatorcounters + terran.liberatorcounters
        self.ghostcounters = protoss.ghostcounters + zerg.ghostcounters + terran.ghostcounters
        self.thorcounters = zerg.thorcounters + terran.thorcounters
        self.battlecruisercounters = terran.battlecruisercounters
        super().__init__(UnitTypeId.ARMORY, 0)
        # super().__init__()


    async def start(self, knowledge: "Knowledge"):
        await super().start(knowledge)

    async def get_threats(self):
        enemy_units = self.ai.all_enemy_units
        marine = 0
        marauder = 0
        viking = 0
        widowmine = 0
        tank = 0
        liberator = 0
        ghost = 0
        thor = 0
        battlecruiser = 0
        if not enemy_units == []:
            for enemy in enemy_units:
                for unit in self.marinecounters:
                    if enemy.type_id == unit.unit_id:
                        marine += unit.threat_level

                for unit in self.maraudercounters:
                    if enemy.type_id == unit.unit_id:
                        marauder += unit.threat_level

                for unit in self.vikingcounters:
                    if enemy.type_id == unit.unit_id:
                        viking += unit.threat_level

                for unit in self.widowminecounters:
                    if enemy.type_id == unit.unit_id:
                        widowmine += unit.threat_level   

                for unit in self.tankcounters:
                    if enemy.type_id == unit.unit_id:
                        tank += unit.threat_level

                for unit in self.liberatorcounters:
                    if enemy.type_id == unit.unit_id:
                        liberator += unit.threat_level

                for unit in self.ghostcounters:
                    if enemy.type_id == unit.unit_id:
                        ghost += unit.threat_level            

                for unit in self.thorcounters:
                    if enemy.type_id == unit.unit_id:
                        thor += unit.threat_level

                for unit in self.battlecruisercounters:
                    if enemy.type_id == unit.unit_id:
                        battlecruiser += unit.threat_level

        threats = [marine, marauder, viking, widowmine, tank, liberator, ghost, thor, battlecruiser]
        return threats

    async def request_units(self):
        threats = await self.get_threats()
        marine = UnitResponse(unitdata.marine, threats[0])     
        marauder = UnitResponse(unitdata.marauder, threats[1])
        viking = UnitResponse(unitdata.viking, threats[2])
        widowmine = UnitResponse(unitdata.widowmine, threats[3])
        tank = UnitResponse(unitdata.siegetank, threats[4])
        liberator = UnitResponse(unitdata.liberator, threats[5])
        ghost = UnitResponse(unitdata.ghost, threats[6])
        thor = UnitResponse(unitdata.thor, threats[7])
        battlecruiser = UnitResponse(unitdata.battlecruiser, threats[8])

        units = [marine, marauder, viking, widowmine, tank, liberator, ghost, thor, battlecruiser]  
        units = sorted(units,key=attrgetter("threat_level"),reverse=True)

        if units[0].unit_data.unitid == UnitTypeId.THOR:
            return 1
        elif units[1].unit_data.unitid == UnitTypeId.THOR:
            return 1
        elif units[2].unit_data.unitid == UnitTypeId.THOR:
            return 1
        if units[0].unit_data.unitid == UnitTypeId.WIDOWMINE:
            return 1

        return(0)


    async def execute(self):
        self.to_count = await self.request_units()
        return await super().execute()


class BuildGhostAcademy(GridBuilding):
    def __init__(self):
        self.foo = None
        self.marinecounters = protoss.marinecounters + zerg.marinecounters + terran.marinecounters
        self.maraudercounters = protoss.maraudercounters + zerg.maraudercounters + terran.maraudercounters
        self.vikingcounters = protoss.vikingcounters + zerg.vikingcounters + terran.vikingcounters
        self.widowminecounters = protoss.widowminecounters + zerg.widowminecounters + terran.widowminecounters
        self.tankcounters = protoss.tankcounters + zerg.tankcounters + terran.tankcounters
        self.liberatorcounters = protoss.liberatorcounters + zerg.liberatorcounters + terran.liberatorcounters
        self.ghostcounters = protoss.ghostcounters + zerg.ghostcounters + terran.ghostcounters
        self.thorcounters = zerg.thorcounters + terran.thorcounters
        self.battlecruisercounters = terran.battlecruisercounters
        super().__init__(UnitTypeId.GHOSTACADEMY, 0)
        # super().__init__()


    async def start(self, knowledge: "Knowledge"):
        await super().start(knowledge)

    async def get_threats(self):
        enemy_units = self.ai.all_enemy_units
        marine = 0
        marauder = 0
        viking = 0
        widowmine = 0
        tank = 0
        liberator = 0
        ghost = 0
        thor = 0
        battlecruiser = 0
        if not enemy_units == []:
            for enemy in enemy_units:
                for unit in self.marinecounters:
                    if enemy.type_id == unit.unit_id:
                        marine += unit.threat_level

                for unit in self.maraudercounters:
                    if enemy.type_id == unit.unit_id:
                        marauder += unit.threat_level

                for unit in self.vikingcounters:
                    if enemy.type_id == unit.unit_id:
                        viking += unit.threat_level

                for unit in self.widowminecounters:
                    if enemy.type_id == unit.unit_id:
                        widowmine += unit.threat_level   

                for unit in self.tankcounters:
                    if enemy.type_id == unit.unit_id:
                        tank += unit.threat_level

                for unit in self.liberatorcounters:
                    if enemy.type_id == unit.unit_id:
                        liberator += unit.threat_level

                for unit in self.ghostcounters:
                    if enemy.type_id == unit.unit_id:
                        ghost += unit.threat_level            

                for unit in self.thorcounters:
                    if enemy.type_id == unit.unit_id:
                        thor += unit.threat_level

                for unit in self.battlecruisercounters:
                    if enemy.type_id == unit.unit_id:
                        battlecruiser += unit.threat_level

        threats = [marine, marauder, viking, widowmine, tank, liberator, ghost, thor, battlecruiser]
        return threats

    async def request_units(self):
        threats = await self.get_threats()
        marine = UnitResponse(unitdata.marine, threats[0])     
        marauder = UnitResponse(unitdata.marauder, threats[1])
        viking = UnitResponse(unitdata.viking, threats[2])
        widowmine = UnitResponse(unitdata.widowmine, threats[3])
        tank = UnitResponse(unitdata.siegetank, threats[4])
        liberator = UnitResponse(unitdata.liberator, threats[5])
        ghost = UnitResponse(unitdata.ghost, threats[6])
        thor = UnitResponse(unitdata.thor, threats[7])
        battlecruiser = UnitResponse(unitdata.battlecruiser, threats[8])

        units = [marine, marauder, viking, widowmine, tank, liberator, ghost, thor, battlecruiser]  
        units = sorted(units,key=attrgetter("threat_level"),reverse=True)

        if units[0].unit_data.unitid == UnitTypeId.GHOST:
            return 1
        elif units[1].unit_data.unitid == UnitTypeId.GHOST:
            return 1
        elif units[2].unit_data.unitid == UnitTypeId.GHOST:
            return 1
         
        return(0)


    async def execute(self):
        self.to_count = await self.request_units()
        return await super().execute()
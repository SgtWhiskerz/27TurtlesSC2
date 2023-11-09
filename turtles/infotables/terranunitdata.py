from typing import List, Optional
from xml.etree.ElementInclude import include
from sc2.unit import Unit
from sc2.ids.unit_typeid import UnitTypeId
from sharpy.managers import ManagerBase
from sharpy.managers.core import *
from sharpy.plans.terran import *
from typing import List, Optional
from sc2.game_info import GameInfo
from sc2.game_data import GameData
from sc2.game_state import GameState
from sc2.data import Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sharpy.interfaces import IZoneManager
from sharpy.managers.extensions import BuildDetector, ChatManager
from sharpy.plans.acts import *
from sharpy.plans.acts.terran import *
from sharpy.plans.require import *
from sharpy.plans.tactics import *
from sharpy.plans.tactics.terran import *
from sharpy.plans import BuildOrder, Step, SequentialList, StepBuildGas
from sc2.ids.upgrade_id import UpgradeId
from sharpy.interfaces.combat_manager import MoveType

class UnitData():
    def __init__(self,unitid,minerals,gas,supply, buildtime, productionfacility,addon=None,additionalrequirments=None):
        self.unitid = unitid
        self.minerals = minerals
        self.gas = gas
        self.supply = supply
        self.buildtime = buildtime
        self.production = productionfacility
        self.addon = addon
        self.additional = additionalrequirments


class TerranUnitData():
    def __init__(self):
        self.scv = UnitData(UnitTypeId.SCV, 50, 0, 1, 12, UnitTypeId.COMMANDCENTER)
        self.marine = UnitData(UnitTypeId.MARINE, 50, 0 ,1, 18, UnitTypeId.BARRACKS)
        self.marauder = UnitData(UnitTypeId.MARAUDER, 100, 25, 2, 21, UnitTypeId.BARRACKS, UnitTypeId.BARRACKSTECHLAB)
        self.reaper = UnitData(UnitTypeId.REAPER, 50, 50, 1, 32, UnitTypeId.BARRACKS)
        self.ghost = UnitData(UnitTypeId.GHOST, 150, 125, 2, 29, UnitTypeId.BARRACKS, UnitTypeId.BARRACKSTECHLAB, UnitTypeId.GHOSTACADEMY)
        self.hellion = UnitData(UnitTypeId.HELLION, 100, 0, 2, 21, UnitTypeId.FACTORY)
        self.hellbat = UnitData(UnitTypeId.HELLIONTANK, 100, 0, 2, 21, UnitTypeId.FACTORY, None, UnitTypeId.ARMORY)
        self.widowmine = UnitData(UnitTypeId.WIDOWMINE, 75, 25, 2, 21, UnitTypeId.FACTORY)
        self.siegetank = UnitData(UnitTypeId.SIEGETANK, 150, 125, 3, 32, UnitTypeId.FACTORY, UnitTypeId.FACTORYTECHLAB)
        self.cyclone = UnitData(UnitTypeId.CYCLONE, 150, 100, 3, 32, UnitTypeId.FACTORY, UnitTypeId.FACTORYTECHLAB)
        self.thor = UnitData(UnitTypeId.THOR, 300, 200, 6, 43, UnitTypeId.FACTORY, UnitTypeId.FACTORYTECHLAB, UnitTypeId.ARMORY)
        self.viking = UnitData(UnitTypeId.VIKINGFIGHTER, 150, 75, 2, 30, UnitTypeId.STARPORT)
        self.medivac = UnitData(UnitTypeId.MEDIVAC, 100, 100, 2, 30, UnitTypeId.STARPORT)
        self.liberator = UnitData(UnitTypeId.LIBERATOR, 150, 150, 3, 43, UnitTypeId.STARPORT)
        self.raven = UnitData(UnitTypeId.RAVEN, 100, 200, 2, 43, UnitTypeId.STARPORT, UnitTypeId.STARPORTTECHLAB)
        self.banshee = UnitData(UnitTypeId.BANSHEE, 150, 100, 3, 43, UnitTypeId.STARPORT, UnitTypeId.STARPORTTECHLAB)
        self.battlecruiser = UnitData(UnitTypeId.BATTLECRUISER, 400, 300, 6, 64, UnitTypeId.STARPORT, UnitTypeId.STARPORTTECHLAB, UnitTypeId.FUSIONCORE)


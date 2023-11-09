from typing import List, Optional
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

from sharpy.knowledges import Knowledge, KnowledgeBot
from sc2.position import Point2

from sharpy.plans.acts import ActBase

REACTORS = {UnitTypeId.BARRACKSREACTOR, UnitTypeId.FACTORYREACTOR, UnitTypeId.STARPORTREACTOR, UnitTypeId.REACTOR}
TECHLABS = {UnitTypeId.BARRACKSTECHLAB, UnitTypeId.FACTORYTECHLAB, UnitTypeId.STARPORTTECHLAB, UnitTypeId.TECHLAB}
TECHLABS_AND_REACTORS = REACTORS.union(TECHLABS)

class ResumeWork(ActBase):
    async def execute(self) -> bool:
        building: Unit
        buildings = self.ai.structures.not_ready.exclude_type(TECHLABS_AND_REACTORS)
        scv_constructing = self.ai.units.filter(lambda unit: unit.is_constructing_scv)

        if buildings.amount > scv_constructing.amount:
            for building in buildings:
                if self.knowledge.unit_values.build_time(building.type_id) > 0 and not scv_constructing.closer_than(
                    building.radius + 0.5, building):

                        self.knowledge.print(f"[Building continue] {building.type_id} {building.position}")
                        workers = self.ai.units(UnitTypeId.SCV).ready
                        if workers.exists:
                            scv = workers.closest_to(building)
                            scv(AbilityId.SMART, building)
        return True
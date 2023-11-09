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
from sharpy.combat import MoveType


from sharpy.knowledges import Knowledge, KnowledgeBot
from sc2.position import Point2

from sharpy.plans.acts import ActBase
from turtles.ResumeWork import ResumeWork

class DodgeRampAttack(PlanZoneAttack):
    async def execute(self) -> bool:
        base_ramp = self.zone_manager.expansion_zones[-1].ramp
        for effect in self.ai.state.effects:
            if effect.id != "FORCEFIELD":
                continue
            pos: Point2 = base_ramp.bottom_center
            for epos in effect.positions:
                if pos.distance_to_point2(epos) < 5:
                    return await self.small_retreat()

        return await super().execute()

    async def small_retreat(self):
        attacking_units = self.roles.attacking_units
        natural = self.zone_manager.expansion_zones[-2]

        for unit in attacking_units:
            self.combat.add_unit(unit)

        self.combat.execute(natural.gather_point, MoveType.DefensiveRetreat)
        return False
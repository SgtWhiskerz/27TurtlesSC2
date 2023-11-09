from typing import List, Optional
from sc2.unit import Unit
from sc2.ids.unit_typeid import UnitTypeId
from sharpy.managers import ManagerBase
from sharpy.managers.core import *
from sharpy.managers.core.zone_manager import MapName
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

import random

from sharpy.plans.acts import ActBase


from turtles.biobuild import MacroBio
from turtles.HellbatBansheeAllin import HellbatBanshee
from turtles.fiverax import FiveRax
from turtles.combat.norallyattack import NoRallyAttack
from turtles.reactivebio import ReactiveBio

class Turtles(KnowledgeBot):
    def __init__(self):
        super().__init__("Turtles")

    def configure_managers(self) -> Optional[List["ManagerBase"]]:
        return [BuildDetector(), ChatManager()]

    async def create_plan(self) -> BuildOrder:
        self.knowledge.data_manager.set_build("bio")
        worker_scout = Step(None, WorkerScout(), skip_until=UnitExists(UnitTypeId.SUPPLYDEPOT, 1))

        if self.opponent_id == "2d827274-9986-4c99-9d39-fa96a2dcf8ec" or self.opponent_id == "c033a97a-667d-42e3-91e8-13528ac191ed" or self.opponent_id == "4730ecca-ea78-4bcf-b571-22b46d9fd4ec":
            self.build = FiveRax()
        else:
            self.build = ReactiveBio()

        # self.attack = PlanZoneAttack(60)

        await self.chat_send("GLHF!")
        await self.chat_send("You better watch about because im about to be terran you apart <3")
        
        tactics = [
            PlanCancelBuilding(),
            LowerDepots(),
            PlanWorkerOnlyDefense(),
            PlanZoneDefense(),
            worker_scout,
            Step(None, CallMule(50), skip=Time(5 * 60)),
            Step(None, CallMule(100), skip_until=Time(5 * 60)),
            Step(None, ScanEnemy(), skip_until=Time(5 * 60)),
            DistributeWorkers(),
            SpeedMining(),
            PlanAddonSwap(factory_reactor_count=0,starport_reactor_count=1,barracks_reactor_count=1),
            Step(None, SpeedMining(), lambda ai: ai.client.game_step > 5),
            PlanZoneGatherTerran(),
            # self.attack,
            # PlanFinishEnemy(),
        ]

        return BuildOrder([self.build, tactics])



class LadderBot(Turtles):
    @property
    def my_race(self):
        return Race.Terran

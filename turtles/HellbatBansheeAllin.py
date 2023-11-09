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
from turtles.ResumeWork import ResumeWork


class HellbatBanshee(BuildOrder):
    zone_manager: IZoneManager

    def __init__(self):
        self.worker_rushed = False
        self.salvage_bunker = False
        self.rush_bunker = BuildPosition(UnitTypeId.BUNKER, Point2((0, 0)), exact=True)

        warn = WarnBuildMacro(
            [
                (UnitTypeId.SUPPLYDEPOT, 1, 18),
                (UnitTypeId.BARRACKS, 1, 42),
                (UnitTypeId.REFINERY, 1, 44),
                (UnitTypeId.COMMANDCENTER, 2, 60 + 44),
                (UnitTypeId.BARRACKSREACTOR, 1, 120),
                (UnitTypeId.FACTORY, 1, 120 + 21),
            ],
            [],
        )

        scv = [
            Step(None, TerranUnit(UnitTypeId.MARINE, 2), skip_until=lambda k: self.rush_detected),
            Step(None, MorphOrbitals(), skip_until=UnitReady(UnitTypeId.BARRACKS, 1)),
            Step(
                None,
                ActUnit(UnitTypeId.SCV, UnitTypeId.COMMANDCENTER, 16 + 6),
                skip=UnitExists(UnitTypeId.COMMANDCENTER, 2),
            ),
            Step(
                None,
                ActUnit(UnitTypeId.SCV, UnitTypeId.COMMANDCENTER, 32 + 12),
                skip=UnitExists(UnitTypeId.COMMANDCENTER, 3),
            ),
            Step(
                None,
                ActUnit(UnitTypeId.SCV, UnitTypeId.COMMANDCENTER, 48 + 12),
                skip=UnitExists(UnitTypeId.COMMANDCENTER, 4),
            ),
            Step(
                None,
                ActUnit(UnitTypeId.SCV, UnitTypeId.COMMANDCENTER, 80),
            ),
        ]

        opener = [
            Step(Supply(13), GridBuilding(UnitTypeId.SUPPLYDEPOT, 1, priority=True)),
            GridBuilding(UnitTypeId.BARRACKS, 1, priority=True),
            StepBuildGas(2, Supply(15)),
            GridBuilding(UnitTypeId.FACTORY, 1),
            Expand(2),
            AutoDepot(),
            GridBuilding(UnitTypeId.FACTORY, 2),
            StepBuildGas(2),
            GridBuilding(UnitTypeId.STARPORT, 1),
            BuildAddon(UnitTypeId.FACTORYREACTOR, UnitTypeId.FACTORY, 2),
            BuildAddon(UnitTypeId.STARPORTTECHLAB, UnitTypeId.STARPORT, 1),

            AutoDepot(),


        ]

        buildings = [
            ResumeWork(),
        ]

        tech = [
            GridBuilding(UnitTypeId.ARMORY, 1),
            Step(UnitExists(UnitTypeId.ARMORY), Tech(UpgradeId.BANSHEECLOAK)),

        ]

        bunker = [
            Step(None, self.rush_bunker, skip_until=lambda k: self.rush_detected),
            ManTheBunkers(),
        ]

        go_time = [
            # Step(UnitExists(UnitTypeId.BANSHEE,3,include_killed=True), zone_attack_all_in())
        ]

        army = [
            BuildOrder(
                [
                    Step(None, TerranUnit(UnitTypeId.BANSHEE,priority=True)),
                    Step(None, TerranUnit(UnitTypeId.HELLION), skip=UnitReady(UnitTypeId.ARMORY)),
                    Step(UnitReady(UnitTypeId.ARMORY), TerranUnit(UnitTypeId.HELLIONTANK)),
                    TerranUnit(UnitTypeId.MARINE, 8),

                ]
            ),
     ]

        use_money = BuildOrder(
            [


            ]
        )


        super().__init__([warn, scv, opener, tech, army, use_money, bunker, buildings, go_time])

    async def start(self, knowledge: "Knowledge"):
        await super().start(knowledge)
        self.zone_manager = knowledge.get_required_manager(IZoneManager)
        self.build_detector = knowledge.get_required_manager(BuildDetector)
        self.rush_bunker.position = self.zone_manager.expansion_zones[0].ramp.ramp.barracks_in_middle

    @property
    def rush_detected(self) -> bool:
        return self.build_detector.rush_detected

    async def execute(self) -> bool:
        if not self.worker_rushed and self.ai.time < 50:
            self.worker_rushed = self.cache.enemy_workers.filter(
                lambda u: u.distance_to(self.ai.start_location) < u.distance_to(self.zone_manager.enemy_start_location)
            )
        if self.ai.time > 300:
            self.salvage_bunker = True

        return await super().execute()
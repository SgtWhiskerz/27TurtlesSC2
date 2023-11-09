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


from sharpy.knowledges import Knowledge, KnowledgeBot
from sc2.position import Point2

from sharpy.plans.acts import ActBase
from turtles.ResumeWork import ResumeWork
from turtles.combat.reaperharass import ReaperHarass
from turtles.combat.disruptorsplits import DisruptorSplit
from turtles.combat.norallyattack import NoRallyAttack

class MacroBio(BuildOrder):
    zone_manager: IZoneManager

    def __init__(self):
        self.worker_rushed = False
        self.salvage_bunker = False
        self.rush_bunker = BuildPosition(UnitTypeId.BUNKER, Point2((0, 0)), exact=True)

        viking_counters = [
            UnitTypeId.COLOSSUS,
            UnitTypeId.MEDIVAC,
            UnitTypeId.RAVEN,
            UnitTypeId.VOIDRAY,
            UnitTypeId.CARRIER,
            UnitTypeId.TEMPEST,
            UnitTypeId.BROODLORD,
            UnitTypeId.VIPER,
            UnitTypeId.BATTLECRUISER,
            UnitTypeId.LIBERATOR,
            UnitTypeId.WARPPRISM,
        ]

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
            Step(None, TerranUnit(UnitTypeId.MARINE, 2), skip_until=lambda k: self.worker_rushed),
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

        cloak_counter = [
            Step(
                Any(
                    [
                        EnemyBuildingExists(UnitTypeId.DARKSHRINE),
                        EnemyUnitExistsAfter(UnitTypeId.DARKTEMPLAR),
                        EnemyUnitExistsAfter(UnitTypeId.BANSHEE),
                        EnemyUnitExistsAfter(UnitTypeId.GHOST),
                        EnemyUnitExistsAfter(UnitTypeId.LURKER),

                    ]
                ),
                None,
            ),
            Step(None, GridBuilding(UnitTypeId.ENGINEERINGBAY, 1)),
            Step(None, DefensiveBuilding(UnitTypeId.MISSILETURRET, DefensePosition.Entrance, 2)),
            Step(None, DefensiveBuilding(UnitTypeId.MISSILETURRET, DefensePosition.CenterMineralLine, None)),
        ]
        cloak_counter2 = [
            Step(
                Any(
                    [
                        EnemyBuildingExists(UnitTypeId.DARKSHRINE),
                        EnemyUnitExistsAfter(UnitTypeId.DARKTEMPLAR),
                        EnemyUnitExistsAfter(UnitTypeId.BANSHEE),
                        EnemyUnitExistsAfter(UnitTypeId.GHOST),
                        EnemyUnitExistsAfter(UnitTypeId.LURKER),


                    ]
                ),
                None,
            ),
            Step(None, GridBuilding(UnitTypeId.STARPORT, 2)),
            Step(None, BuildAddon(UnitTypeId.STARPORTTECHLAB, UnitTypeId.STARPORT, 1)),
            Step(UnitReady(UnitTypeId.STARPORT, 1), ActUnit(UnitTypeId.RAVEN, UnitTypeId.STARPORT, 2)),
        ]

        opener = [
            Step(Supply(13), GridBuilding(UnitTypeId.SUPPLYDEPOT, 1, priority=True)),
            GridBuilding(UnitTypeId.BARRACKS, 1, priority=True),
            StepBuildGas(1, Supply(15)),
            TerranUnit(UnitTypeId.REAPER, 1, only_once=True),   
            Step(
                None,
                BuildAddon(UnitTypeId.BARRACKSREACTOR, UnitTypeId.BARRACKS, 1),
                skip_until=Any(
                    [
                        RequireCustom(lambda k: not self.rush_detected),
                    ]
                ),
            ),
            Step(
                None,
                Expand(2),
                skip_until=Any(
                    [
                        RequireCustom(lambda k: not self.rush_detected),
                    ]
                ),
            ),            
            GridBuilding(UnitTypeId.BARRACKS, 2, Supply(21)),
            GridBuilding(UnitTypeId.SUPPLYDEPOT, 2),
            GridBuilding(UnitTypeId.FACTORY, 1),
            StepBuildGas(2),
            SequentialList(
            Step(
                None,
                BuildAddon(UnitTypeId.BARRACKSTECHLAB, UnitTypeId.BARRACKS, 1),
                skip_until=Any(
                    [
                        RequireCustom(lambda k: not self.rush_detected),
                    ]
                ),
            ),
            Step(None, BuildAddon(UnitTypeId.FACTORYREACTOR, UnitTypeId.FACTORY, 1),skip=UnitExists(UnitTypeId.STARPORT, 1)),
            BuildAddon(UnitTypeId.BARRACKSREACTOR, UnitTypeId.BARRACKS, 1),
            BuildAddon(UnitTypeId.BARRACKSTECHLAB, UnitTypeId.BARRACKS, 1),
            GridBuilding(UnitTypeId.STARPORT, 1),
            Step(None,Expand(2),skip_until=Supply(40)),
            GridBuilding(UnitTypeId.SUPPLYDEPOT, 3),
            ),


            AutoDepot(),
            BuildAddon(UnitTypeId.FACTORYTECHLAB, UnitTypeId.FACTORY, 1),
            Step(UnitExists(UnitTypeId.FACTORYTECHLAB, 1), BuildAddon(UnitTypeId.FACTORYREACTOR, UnitTypeId.FACTORY, 1)),
            Step(UnitExists(UnitTypeId.STARPORTTECHREACTOR, 1), BuildAddon(UnitTypeId.STARPORTTECHLAB, UnitTypeId.STARPORT, 1)),
            BuildAddon(UnitTypeId.BARRACKSREACTOR, UnitTypeId.BARRACKS, 1),
            BuildAddon(UnitTypeId.BARRACKSTECHLAB, UnitTypeId.BARRACKS, 1),

        ]

        buildings = [
            ResumeWork(),
        ]

        tech = [
            Step(None, Tech(UpgradeId.STIMPACK)),
            Step(None, Tech(UpgradeId.SHIELDWALL)),
            Step(None, Tech(UpgradeId.PUNISHERGRENADES)),


            Step(TechReady(UpgradeId.SHIELDWALL), GridBuilding(UnitTypeId.ENGINEERINGBAY, 2)),

            Step(UnitExists(UnitTypeId.ENGINEERINGBAY), Tech(UpgradeId.TERRANINFANTRYWEAPONSLEVEL1)),
            Step(UnitExists(UnitTypeId.ENGINEERINGBAY), Tech(UpgradeId.TERRANINFANTRYARMORSLEVEL1)),

            Step(TechReady(UpgradeId.TERRANINFANTRYWEAPONSLEVEL1), GridBuilding(UnitTypeId.ARMORY, 1)),

            Step(UnitReady(UnitTypeId.ARMORY), Tech(UpgradeId.DRILLCLAWS)),
            

            Step(UnitExists(UnitTypeId.ARMORY), Tech(UpgradeId.TERRANINFANTRYWEAPONSLEVEL2)),
            Step(UnitExists(UnitTypeId.ARMORY), Tech(UpgradeId.TERRANINFANTRYARMORSLEVEL2)),

            Step(UnitExists(UnitTypeId.GHOSTACADEMY), Tech(UpgradeId.PERSONALCLOAKING)),

            Step(TechReady(UpgradeId.TERRANINFANTRYWEAPONSLEVEL2), Tech(UpgradeId.TERRANINFANTRYWEAPONSLEVEL3)),
            Step(TechReady(UpgradeId.TERRANINFANTRYARMORSLEVEL2), Tech(UpgradeId.TERRANINFANTRYARMORSLEVEL3)),
        ]

        swap = [
            Step(UnitReady(UnitTypeId.STARPORT), ExecuteAddonSwap()),
        ]

        reaper = [
            ReaperHarass(),
        ]

        marine = [
            DisruptorSplit(),
        ]

        attack = [
            Step(UnitExists(UnitTypeId.MEDIVAC, 2),NoRallyAttack(24),skip=UnitExists(UnitTypeId.COMMANDCENTER, 3, include_killed=True, include_pending=True)),
            Step(None,NoRallyAttack(60),skip=Supply(70,supply_type=Workers)),
            Step(UnitExists(UnitTypeId.COMMANDCENTER, 4, include_killed=True),NoRallyAttack(90),skip=Supply(200)),
            Step(Supply(200), PlanFinishEnemy())


        ]

        bunker = [
            Step(None, self.rush_bunker, skip_until=lambda k: self.rush_detected),
            ManTheBunkers(),
        ]

        air = [
            Step(UnitReady(UnitTypeId.STARPORT, 1), TerranUnit(UnitTypeId.MEDIVAC, 2, priority=True)),
            Step(None, TerranUnit(UnitTypeId.VIKINGFIGHTER, 1, priority=True)),
            Step(
                None,
                TerranUnit(UnitTypeId.VIKINGFIGHTER, 4, priority=True),
                skip_until=self.RequireAnyEnemyUnits(viking_counters, 1),
            ),
            Step(UnitReady(UnitTypeId.STARPORT, 1), TerranUnit(UnitTypeId.MEDIVAC, 4, priority=True)),
            Step(
                None,
                TerranUnit(UnitTypeId.VIKINGFIGHTER, 15, priority=True),
                skip_until=self.RequireAnyEnemyUnits(viking_counters, 4),
            ),
            Step(UnitReady(UnitTypeId.STARPORTREACTOR, 1), TerranUnit(UnitTypeId.MEDIVAC, 2, priority=True),skip=UnitExists(UnitTypeId.COMMANDCENTER, 3,include_pending=True)),
            Step(UnitReady(UnitTypeId.STARPORTREACTOR, 1), TerranUnit(UnitTypeId.MEDIVAC, 4, priority=True),skip_until=UnitExists(UnitTypeId.COMMANDCENTER, 3,include_pending=True)),
            Step(UnitReady(UnitTypeId.MEDIVAC, 4), TerranUnit(UnitTypeId.LIBERATOR, 16)),

        ]

        ground = [
            Step(UnitExists(UnitTypeId.REAPER, 1, include_killed=True), TerranUnit(UnitTypeId.MARINE, 4)),
            BuildOrder(
                [
                    TerranUnit(UnitTypeId.MARINE, 20),
                    TerranUnit(UnitTypeId.GHOST, 7),
                    Step(None, BuildAddon(UnitTypeId.BARRACKSREACTOR, UnitTypeId.BARRACKS, 4), skip_until=UnitExists(UnitTypeId.COMMANDCENTER, 3,include_pending=True)),
                    Step(None, BuildAddon(UnitTypeId.BARRACKSTECHLAB, UnitTypeId.BARRACKS, 4), skip_until=UnitExists(UnitTypeId.COMMANDCENTER, 3,include_pending=True)),
                    Step(TechReady(UpgradeId.STIMPACK), TerranUnit(UnitTypeId.MARAUDER, 5, priority=True)),
                    Step(UnitExists(UnitTypeId.COMMANDCENTER, 3, include_pending=True), TerranUnit(UnitTypeId.MARAUDER, 25)),
                    Step(UnitExists(UnitTypeId.COMMANDCENTER, 3, include_pending=True), TerranUnit(UnitTypeId.MARINE, 100)),
                    Step(None,TerranUnit(UnitTypeId.SIEGETANK, 8),skip_until=UnitExists(UnitTypeId.COMMANDCENTER, 3,include_pending=True)),
                    Step(UnitExists(UnitTypeId.FACTORYREACTOR),TerranUnit(UnitTypeId.WIDOWMINE, 2)),
                    Step(UnitExists(UnitTypeId.FACTORYREACTOR),TerranUnit(UnitTypeId.WIDOWMINE, 10),skip_until=UnitExists(UnitTypeId.STARPORTREACTOR))

                ]
            ),
     ]

        use_money = BuildOrder(
            [
                Step(Minerals(400), Expand(3), skip_until=UnitExists(UnitTypeId.MEDIVAC, 1,include_pending=True,include_killed=True)),
                Step(Minerals(200), GridBuilding(UnitTypeId.BARRACKS, 4), skip_until=UnitExists(UnitTypeId.COMMANDCENTER, 3,include_pending=True)),
                Step(Minerals(200), GridBuilding(UnitTypeId.FACTORY, 2), skip_until=UnitExists(UnitTypeId.COMMANDCENTER, 3,include_pending=True)),
                Step(Minerals(200), GridBuilding(UnitTypeId.STARPORT, 2), skip_until=UnitExists(UnitTypeId.COMMANDCENTER, 3,include_pending=True)),
                Step(UnitExists(UnitTypeId.STARPORTREACTOR), BuildAddon(UnitTypeId.STARPORTTECHLAB, UnitTypeId.STARPORT, 1)),
                Step(UnitReady(UnitTypeId.STARPORTTECHLAB, 1), TerranUnit(UnitTypeId.RAVEN,1)),
                Step(Minerals(400), Expand(4), skip_until=UnitExists(UnitTypeId.COMMANDCENTER, 3)),
                Step(Minerals(200), BuildGas(4), skip_until=UnitExists(UnitTypeId.STARPORTREACTOR, 1,include_killed=True)),
                Step(Minerals(200), BuildGas(6), skip_until=UnitExists(UnitTypeId.COMMANDCENTER, 3)),
                Step(Minerals(200), BuildGas(8), skip_until=UnitExists(UnitTypeId.COMMANDCENTER, 4)),
                Step(Minerals(400), GridBuilding(UnitTypeId.BARRACKS, 8), skip_until=UnitExists(UnitTypeId.COMMANDCENTER, 3,include_pending=True)),
                Step(None, GridBuilding(UnitTypeId.GHOSTACADEMY, 1), skip_until=UnitExists(UnitTypeId.COMMANDCENTER, 4,include_pending=True)),
                Step(Minerals(600), Expand(5)),

            ]
        )


        super().__init__([warn, scv, opener, cloak_counter, cloak_counter2, tech, ground, swap, air, use_money, bunker, buildings, reaper, marine, attack])

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

        return await super().execute()
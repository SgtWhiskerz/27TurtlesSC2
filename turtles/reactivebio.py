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
from turtles.combat.bansheeharass import BansheeHarass
from turtles.combat.disruptorsplits import DisruptorSplit
from turtles.combat.norallyattack import NoRallyAttack
from turtles.decisions.buildingdecisions import BuildRax, BuildFactories, BuildStarports, BuildArmory, BuildGhostAcademy
from turtles.decisions.unitdecisions import BuildUnitsMarine, BuildUnitsMarauder, BuildUnitsBattlecruiser, BuildUnitsGhost, BuildUnitsLiberator, BuildUnitsTank, BuildUnitsThor, BuildUnitsViking, BuildUnitsWidowMine


class ReactiveBio(BuildOrder):
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
        scv = [
            Step(None, TerranUnit(UnitTypeId.MARINE, 2), skip_until=lambda k: self.worker_rushed),
            Step(None, MorphOrbitals(), skip_until=UnitReady(UnitTypeId.BARRACKS, 1)),
            Step(
                None,
                ActUnit(UnitTypeId.SCV, UnitTypeId.COMMANDCENTER, 30),
                skip=UnitExists(UnitTypeId.COMMANDCENTER, 2),
            ),
            Step(
                None,
                ActUnit(UnitTypeId.SCV, UnitTypeId.COMMANDCENTER, 50),
                skip=UnitExists(UnitTypeId.COMMANDCENTER, 3),
            ),
            Step(
                None,
                ActUnit(UnitTypeId.SCV, UnitTypeId.COMMANDCENTER, 64),
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
            StepBuildGas(1, Supply(15)),
            Step(UnitExists(UnitTypeId.REAPER,include_killed=True,include_pending=True),AutoDepot(),skip=UnitExists(UnitTypeId.FACTORYREACTOR)),   
            Step(
                None,
                Expand(2),
                skip_until=Any(
                    [
                        RequireCustom(lambda k: not self.rush_detected),
                    ]
                ),
            ),
            GridBuilding(UnitTypeId.FACTORY, 1),
            StepBuildGas(2),
            DefensiveBuilding(UnitTypeId.BUNKER, DefensePosition.Entrance,1),

            BuildAddon(UnitTypeId.FACTORYTECHLAB, UnitTypeId.FACTORY, 1),
            BuildAddon(UnitTypeId.BARRACKSREACTOR, UnitTypeId.BARRACKS, 1),
            GridBuilding(UnitTypeId.STARPORT, 1),
            TerranUnit(UnitTypeId.SIEGETANK, 1, only_once=True),
            BuildAddon(UnitTypeId.STARPORTTECHLAB, UnitTypeId.STARPORT, 1),
            Expand(3),

            Step(None, BuildAddon(UnitTypeId.FACTORYREACTOR, UnitTypeId.FACTORY, 1),skip=UnitExists(UnitTypeId.STARPORT, 1)),
            Step(None,Expand(2, priority=True),skip_until=Supply(40)),
            Step(UnitExists(UnitTypeId.STARPORTREACTOR, include_killed=True),AutoDepot()),   

            BuildAddon(UnitTypeId.BARRACKSREACTOR, UnitTypeId.BARRACKS, 1),
            BuildAddon(UnitTypeId.BARRACKSTECHLAB, UnitTypeId.BARRACKS, 1),

            Step(UnitExists(UnitTypeId.STARPORTREACTOR, include_killed=True), BuildAddon(UnitTypeId.FACTORYTECHLAB, UnitTypeId.FACTORY, 1)),

        ]

        buildings = [
            ResumeWork(),
        ]

        reaper = [
            ReaperHarass(),

        ]

        units = [
            TerranUnit(UnitTypeId.REAPER, 1, only_once=True),
            Step(UnitExists(UnitTypeId.REAPER, include_killed=True),TerranUnit(UnitTypeId.MARINE, 16),skip=UnitExists(UnitTypeId.BANSHEE, 2, include_killed=True)),
            Step(UnitExists(UnitTypeId.BANSHEE, 2, include_killed=True), TerranUnit(UnitTypeId.RAVEN, 1))

        ]
        banshee = [
            Step(None,TerranUnit(UnitTypeId.BANSHEE, 2, only_once=True)),
            Step(UnitExists(UnitTypeId.BANSHEE, 2),BansheeHarass()),
        ]
        rax = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildRax()),

        ]
        factory = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildFactories()),
        ]
        starport = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildStarports()),

        ]
        armory = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildArmory()),
        ]
        ghostacademy = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildGhostAcademy()),
        ]
        marine = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildUnitsMarine())
        ]
        marauder = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildUnitsMarauder())
        ]
        viking = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildUnitsViking())
        ]
        mine = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildUnitsWidowMine())
        ]
        tank = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildUnitsTank())
        ]
        liberator = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildUnitsLiberator())
        ]
        ghost = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildUnitsGhost())
        ]
        thor = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildUnitsThor())
        ]
        battlecruiser = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildUnitsBattlecruiser())
        ]
        gasses = [
            Step(UnitExists(UnitTypeId.COMMANDCENTER, 2),StepBuildGas(4)),
            Step(UnitExists(UnitTypeId.COMMANDCENTER, 3),StepBuildGas(6)),
            Step(UnitExists(UnitTypeId.COMMANDCENTER, 4),StepBuildGas(7)),

        ]

        upgrades = [

            Step(UnitExists(UnitTypeId.ENGINEERINGBAY), Tech(UpgradeId.TERRANINFANTRYWEAPONSLEVEL1)),
            Step(UnitExists(UnitTypeId.ENGINEERINGBAY), Tech(UpgradeId.TERRANINFANTRYARMORSLEVEL1)),

            Step(TechReady(UpgradeId.TERRANINFANTRYWEAPONSLEVEL1), GridBuilding(UnitTypeId.ARMORY, 1)),

            Step(UnitExists(UnitTypeId.ARMORY), Tech(UpgradeId.TERRANVEHICLEWEAPONSLEVEL1)),
            Step(UnitExists(UnitTypeId.ARMORY), Tech(UpgradeId.TERRANINFANTRYWEAPONSLEVEL2)),
            Step(UnitExists(UnitTypeId.ARMORY), Tech(UpgradeId.TERRANINFANTRYARMORSLEVEL2)),
            Step(TechReady(UpgradeId.TERRANVEHICLEWEAPONSLEVEL1), Tech(UpgradeId.TERRANVEHICLEWEAPONSLEVEL2)),


            Step(TechReady(UpgradeId.TERRANINFANTRYWEAPONSLEVEL2), Tech(UpgradeId.TERRANINFANTRYWEAPONSLEVEL3)),
            Step(TechReady(UpgradeId.TERRANINFANTRYARMORSLEVEL2), Tech(UpgradeId.TERRANINFANTRYARMORSLEVEL3)),
            Step(TechReady(UpgradeId.TERRANVEHICLEWEAPONSLEVEL2), Tech(UpgradeId.TERRANVEHICLEWEAPONSLEVEL3)),


        ]

        abilities = [
            Step(None, Tech(UpgradeId.BANSHEECLOAK)),
            Step(None, Tech(UpgradeId.STIMPACK)),
            Step(None, Tech(UpgradeId.SHIELDWALL)),

            Step(UnitExists(UnitTypeId.MARAUDER, 8, include_pending=True), Tech(UpgradeId.PUNISHERGRENADES)),
            Step(UnitExists(UnitTypeId.GHOSTACADEMY), Tech(UpgradeId.PERSONALCLOAKING)),

        ]

        barracksaddons = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildAddon(UnitTypeId.BARRACKSREACTOR, UnitTypeId.BARRACKS, 2)),
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildAddon(UnitTypeId.BARRACKSTECHLAB, UnitTypeId.BARRACKS, 10)),
        ]
        factoryaddons = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildAddon(UnitTypeId.FACTORYTECHLAB, UnitTypeId.FACTORY, 1)),
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildAddon(UnitTypeId.FACTORYTECHLAB, UnitTypeId.FACTORY, 10)),
        ]
        starportaddons = [
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildAddon(UnitTypeId.STARPORTTECHLAB, UnitTypeId.STARPORT, 2)),
            Step(UnitExists(UnitTypeId.BANSHEE,include_killed=True), BuildAddon(UnitTypeId.STARPORTTECHLAB, UnitTypeId.STARPORT, 10)),
        ]
        bunker = [
            Step(None, self.rush_bunker, skip_until=lambda k: self.rush_detected),
            ManTheBunkers(),
        ]
        ebays = [
            Step(Supply(100), GridBuilding(UnitTypeId.ENGINEERINGBAY, 2)),
        ]

        expansions = [
            Step(Supply(110), Expand(4)),
            Step(Minerals(1000), Expand(7)),
        ]

        attack1 = [
            Step(UnitExists(UnitTypeId.BANSHEE, 2),NoRallyAttack(20),skip=Supply(50,supply_type=Workers)),
        ]
        attack2 = [
            Step(None,NoRallyAttack(50),skip=Supply(70,supply_type=Workers)),
        ]
        attack3 = [
            Step(None,NoRallyAttack(70),skip=Supply(200)),
        ]
        finish = [
            Step(Supply(200), PlanFinishEnemy())
        ]
        repair = [
            Repair(),
        ]

        super().__init__([warn, gasses, scv, banshee, repair, barracksaddons, factoryaddons, starportaddons, opener, bunker, buildings, cloak_counter, cloak_counter2, reaper,expansions, ebays, abilities, attack1,attack2,attack3,finish, units, upgrades,marauder,viking,mine,tank,liberator, ghostacademy, ghost,armory, thor,battlecruiser,rax,factory,marine,starport])

    async def start(self, knowledge: "Knowledge"):
        await super().start(knowledge)
        self.zone_manager = knowledge.get_required_manager(IZoneManager)
        self.build_detector = knowledge.get_required_manager(BuildDetector)
        self.rush_bunker.position = self.zone_manager.expansion_zones[0].ramp.ramp.barracks_in_middle

        self.reacting = False
        if UnitExists(UnitTypeId.BANSHEE, include_killed=True, include_pending=True):
            self.reacting = True

    @property
    def rush_detected(self) -> bool:
        return self.build_detector.rush_detected

    async def execute(self) -> bool:
        if not self.worker_rushed and self.ai.time < 50:
            self.worker_rushed = self.cache.enemy_workers.filter(
                lambda u: u.distance_to(self.ai.start_location) < u.distance_to(self.zone_manager.enemy_start_location)
            )

        return await super().execute()
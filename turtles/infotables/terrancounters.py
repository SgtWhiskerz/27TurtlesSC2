from sc2.ids.unit_typeid import UnitTypeId

from dataclasses import dataclass

@dataclass
class TerranThreats:
    unit_id: UnitTypeId
    threat_level: float


class TerranCounters():
    def __init__(self):
        self.scv = TerranThreats(UnitTypeId.SCV, 1)
        self.marine = TerranThreats(UnitTypeId.MARINE, 1)
        self.marauder = TerranThreats(UnitTypeId.MARAUDER, 2)
        self.reaper = TerranThreats(UnitTypeId.REAPER, 1.5)
        self.ghost = TerranThreats(UnitTypeId.GHOST, 2.5)
        self.hellion = TerranThreats(UnitTypeId.HELLION, 2)
        self.hellbat = TerranThreats(UnitTypeId.HELLIONTANK, 2)
        self.widowmine = TerranThreats(UnitTypeId.WIDOWMINE, 3)
        self.cyclone = TerranThreats(UnitTypeId.CYCLONE, 2.5)
        self.siegetank = TerranThreats(UnitTypeId.SIEGETANK, 4)
        self.siegetanksieged = TerranThreats(UnitTypeId.SIEGETANKSIEGED, 4)
        self.thor = TerranThreats(UnitTypeId.THOR, 3)
        self.medivac = TerranThreats(UnitTypeId.MEDIVAC, 1.5)
        self.viking = TerranThreats(UnitTypeId.VIKINGFIGHTER, 2.5)
        self.landedviking = TerranThreats(UnitTypeId.VIKINGASSAULT, 2.5)
        self.raven = TerranThreats(UnitTypeId.RAVEN, 3)
        self.banshee = TerranThreats(UnitTypeId.BANSHEE, 4)
        self.battlecruiser = TerranThreats(UnitTypeId.BATTLECRUISER, 5)
        self.liberator = TerranThreats(UnitTypeId.LIBERATOR, 4)

        self.marinecounters = [self.marine, self.marauder, self.thor, self.medivac, self.raven, self.reaper]
        self.maraudercounters = [self.cyclone, self.reaper, self.widowmine, self.thor]
        self.vikingcounters = [self.medivac, self.viking, self.raven, self.banshee, self.battlecruiser, self.liberator]
        self.widowminecounters = [self.hellion, self.hellbat, self.viking]
        self.tankcounters = [self.marine, self.marauder, self.ghost, self.widowmine, self.cyclone, self.siegetank, self.siegetanksieged, self.thor]
        self.liberatorcounters = [self.marauder, self.siegetank]
        self.ghostcounters = [self.ghost, self.raven]
        self.thorcounters = [self.battlecruiser]
        self.battlecruisercounters = [self.marine, self.banshee, self.siegetank, self.siegetanksieged]

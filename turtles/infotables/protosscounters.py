from sc2.ids.unit_typeid import UnitTypeId

from dataclasses import dataclass

@dataclass
class ProtossThreats:
    unit_id: UnitTypeId
    threat_level: float


class ProtossCounters():
    def __init__(self):
        self.probe = ProtossThreats(UnitTypeId.PROBE, 1)
        self.zealot = ProtossThreats(UnitTypeId.ZEALOT, 2)
        self.stalker = ProtossThreats(UnitTypeId.STALKER, 2)
        self.sentry = ProtossThreats(UnitTypeId.SENTRY, 2.5)
        self.adept = ProtossThreats(UnitTypeId.ADEPT, 2)
        self.phoenix = ProtossThreats(UnitTypeId.PHOENIX, 3)
        self.oracle = ProtossThreats(UnitTypeId.ORACLE, 3.5)
        self.voidray = ProtossThreats(UnitTypeId.VOIDRAY, 4)
        self.observer = ProtossThreats(UnitTypeId.OBSERVER, 1)
        self.warpprism = ProtossThreats(UnitTypeId.WARPPRISM, 2.1)
        self.immortal = ProtossThreats(UnitTypeId.IMMORTAL, 4)
        self.hightemplar = ProtossThreats(UnitTypeId.HIGHTEMPLAR, 4.5)
        self.darktemplar = ProtossThreats(UnitTypeId.DARKTEMPLAR, 3)
        self.archon = ProtossThreats(UnitTypeId.ARCHON, 4)
        self.carrier = ProtossThreats(UnitTypeId.CARRIER, 6)
        self.tempest = ProtossThreats(UnitTypeId.TEMPEST, 6)
        self.mothership = ProtossThreats(UnitTypeId.MOTHERSHIP, 7)
        self.colossus = ProtossThreats(UnitTypeId.COLOSSUS, 4)
        self.disruptor = ProtossThreats(UnitTypeId.DISRUPTOR, 4)


        self.marinecounters = [self.zealot, self.phoenix, self.voidray, self.immortal, self.darktemplar, self.observer]
        self.maraudercounters = [self.stalker, self.archon, self.hightemplar]
        self.vikingcounters = [self.carrier, self.tempest, self.mothership, self.colossus, self.oracle]
        self.widowminecounters = [self.zealot, self.adept]
        self.tankcounters = [self.stalker, self.immortal, self.colossus, self.disruptor, self.sentry]
        self.liberatorcounters = [self.immortal, self.hightemplar, self.archon, self.disruptor, self.colossus]
        self.ghostcounters = [self.hightemplar, self.archon, self.oracle]

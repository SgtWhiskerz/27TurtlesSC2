from sc2.ids.unit_typeid import UnitTypeId

from dataclasses import dataclass

@dataclass
class ZergThreats:
    unit_id: UnitTypeId
    threat_level: float




class ZergCounters():
    def __init__(self):

        self.drone = ZergThreats(UnitTypeId.DRONE, 1)
        self.zergling = ZergThreats(UnitTypeId.ZERGLING, 0.6)
        self.roach = ZergThreats(UnitTypeId.ROACH, 1.1)
        self.queen = ZergThreats(UnitTypeId.QUEEN, 2)
        self.overlord = ZergThreats(UnitTypeId.OVERLORD, 0)
        self.overseer = ZergThreats(UnitTypeId.OVERSEER, 0.5)
        self.ravager = ZergThreats(UnitTypeId.RAVAGER, 2.5)
        self.baneling = ZergThreats(UnitTypeId.BANELING, 2)
        self.hydralisk = ZergThreats(UnitTypeId.HYDRALISK, 2)
        self.mutalisk = ZergThreats(UnitTypeId.MUTALISK, 2.5)
        self.lurker = ZergThreats(UnitTypeId.LURKER, 5)
        self.infestor = ZergThreats(UnitTypeId.INFESTOR, 3.5)
        self.corruptor = ZergThreats(UnitTypeId.CORRUPTOR, 2)
        self.swarmhost = ZergThreats(UnitTypeId.SWARMHOSTMP, 2)
        self.viper = ZergThreats(UnitTypeId.VIPER, 4)
        self.ultralisk = ZergThreats(UnitTypeId.ULTRALISK, 5)
        self.broodlord = ZergThreats(UnitTypeId.BROODLORD, 6)

        self.marinecounters = [self.zergling, self.hydralisk, self.corruptor, self.overlord, self.overseer, self.queen]
        self.maraudercounters = [self.roach, self.ravager, self.lurker, self.ultralisk]
        self.vikingcounters = [self.broodlord, self.viper]
        self.widowminecounters = [self.zergling, self.baneling, self.mutalisk]
        self.tankcounters = [self.roach, self.ravager, self.queen, self.hydralisk, self.lurker, self.infestor]
        self.liberatorcounters = [self.roach, self.queen, self.lurker, self.infestor, self.swarmhost, self.ultralisk]
        self.thorcounters = [self.broodlord, self.viper]
        self.ghostcounters = [self.ravager, self.lurker, self.infestor, self.viper, self.ultralisk, self.broodlord]

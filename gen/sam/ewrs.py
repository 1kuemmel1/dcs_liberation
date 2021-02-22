from dcs.vehicles import AirDefence
from dcs.unittype import VehicleType

from gen.sam.group_generator import GroupGenerator


class EwrGenerator(GroupGenerator):
    @property
    def unit_type(self) -> VehicleType:
        raise NotImplementedError

    def generate(self) -> None:
        self.add_unit(
            self.unit_type, "EWR", self.position.x, self.position.y, self.heading
        )


class BoxSpringGenerator(EwrGenerator):
    """1L13 "Box Spring" EWR."""

    unit_type = AirDefence.EWR_1L13


class TallRackGenerator(EwrGenerator):
    """55G6 "Tall Rack" EWR."""

    unit_type = AirDefence.EWR_55G6


class DogEarGenerator(EwrGenerator):
    """9S80M1 "Dog Ear" EWR.

    This is the SA-8 search radar, but used as an early warning radar.
    """

    unit_type = AirDefence.CP_9S80M1_Sborka


class RolandEwrGenerator(EwrGenerator):
    """Roland EWR.

    This is the Roland search radar, but used as an early warning radar.
    """

    unit_type = AirDefence.SAM_Roland_EWR


class FlatFaceGenerator(EwrGenerator):
    """P-19 "Flat Face" EWR.

    This is the SA-3 search radar, but used as an early warning radar.
    """

    unit_type = AirDefence.SAM_SR_P_19


class PatriotEwrGenerator(EwrGenerator):
    """Patriot EWR.

    This is the Patriot search/track radar, but used as an early warning radar.
    """

    unit_type = AirDefence.SAM_Patriot_STR_AN_MPQ_53


class BigBirdGenerator(EwrGenerator):
    """64H6E "Big Bird" EWR.

    This is the SA-10 track radar, but used as an early warning radar.
    """

    unit_type = AirDefence.SAM_SA_10_S_300PS_SR_64H6E


class SnowDriftGenerator(EwrGenerator):
    """9S18M1 "Snow Drift" EWR.

    This is the SA-11 search radar, but used as an early warning radar.
    """

    unit_type = AirDefence.SAM_SA_11_Buk_SR_9S18M1


class StraightFlushGenerator(EwrGenerator):
    """1S91 "Straight Flush" EWR.

    This is the SA-6 search/track radar, but used as an early warning radar.
    """

    unit_type = AirDefence.SAM_SA_6_Kub_STR_9S91


class HawkEwrGenerator(EwrGenerator):
    """Hawk EWR.

    This is the Hawk search radar, but used as an early warning radar.
    """

    unit_type = AirDefence.SAM_Hawk_SR_AN_MPQ_50

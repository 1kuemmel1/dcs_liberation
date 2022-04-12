from typing import Any, Optional
from dcs import Mission
from dcs.unitgroup import FlyingGroup
from dcs.statics import Fortification
from game.ato import Flight
from game.ato.flighttype import FlightType
from game.ato.flightwaypointtype import FlightWaypointType
from game.missiongenerator.airsupport import CargoInfo, LogisticsInfo
from game.settings.settings import Settings
from game.transfers import TransferOrder


ZONE_RADIUS = 300
CRATE_ZONE_RADIUS = 50
TARGET_ZONE_RADIUS = 1500


class LogisticsGenerator:
    def __init__(
        self,
        flight: Flight,
        group: FlyingGroup[Any],
        transfer: Optional[TransferOrder] = None,
    ) -> None:
        self.flight = flight
        self.group = group
        self.transfer = transfer

    def generate_logistics(self, mission: Mission, settings: Settings) -> LogisticsInfo:
        # Add Logisitcs info for the flight
        logistics_info = LogisticsInfo()
        logistics_info.blue = self.flight.blue
        logistics_info.pilot_names = [u.name for u in self.group.units]

        if self.flight.flight_type == FlightType.AIR_ASSAULT:
            target_zone = f"TARGET_ZONE_{self.flight.id}"
            mission.triggers.add_triggerzone(
                self.flight.package.target.position,
                TARGET_ZONE_RADIUS,
                False,
                target_zone,
            )
            logistics_info.target_zone = target_zone

        pickup_point = None
        for waypoint in self.flight.points:
            if (
                waypoint.waypoint_type
                not in [
                    FlightWaypointType.PICKUP,
                    FlightWaypointType.DROP_OFF,
                ]
                or waypoint.only_for_player
                and not self.flight.client_count
            ):
                continue
            # Create Pickup and DropOff zone
            zone_name = f"{waypoint.waypoint_type.name}_{self.flight.id}"
            mission.triggers.add_triggerzone(
                waypoint.position, ZONE_RADIUS, False, zone_name
            )
            if waypoint.waypoint_type == FlightWaypointType.PICKUP:
                pickup_point = waypoint.position
                logistics_info.pickup_zone = zone_name
            else:
                logistics_info.drop_off_zone = zone_name

        if self.transfer and self.flight.client_count > 0 and pickup_point is not None:
            # Add spawnable crates for client airlifts
            crate_location = pickup_point.random_point_within(
                ZONE_RADIUS - CRATE_ZONE_RADIUS, CRATE_ZONE_RADIUS
            )
            crate_zone = f"crate_spawn_{self.flight.id}"
            mission.triggers.add_triggerzone(
                crate_location, CRATE_ZONE_RADIUS, False, crate_zone
            )
            logistics_info.cargo = [
                CargoInfo(cargo_unit_type.dcs_id, crate_zone, amount)
                for cargo_unit_type, amount in self.transfer.units.items()
            ]
            if settings.plugin_option("ctld.logisticunit"):
                country = mission.country(self.flight.country)
                logistic_unit = mission.static_group(
                    country,
                    f"logistic_{self.flight.id}",
                    Fortification.FARP_Ammo_Dump_Coating,
                    pickup_point,
                )
                logistics_info.logistic_unit = logistic_unit.units[0].name
        return logistics_info

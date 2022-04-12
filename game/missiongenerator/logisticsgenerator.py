from nntplib import GroupInfo
from typing import Any
from dcs import Mission
from dcs.unitgroup import FlyingGroup
from game.ato import Flight
from game.ato.flightstate.inflight import InFlight
from game.ato.flightwaypointtype import FlightWaypointType
from game.missiongenerator.airsupport import LogisticsInfo


class LogisticsGenerator:
    def __init__(self, flight: Flight, group: FlyingGroup[Any]) -> None:
        self.flight = flight
        self.group = group

    def generate_logistics(self, mission: Mission) -> LogisticsInfo:
        # Add Logisitcs info for the flight
        logistics_info = LogisticsInfo()
        logistics_info.blue = self.flight.blue
        logistics_info.pilot_names = [u.name for u in self.group.units]
        target_zone = f"TARGET_ZONE_{self.flight.id}"
        mission.triggers.add_triggerzone(
            self.flight.package.target.position, 1500, False, target_zone
        )
        logistics_info.target_zone = target_zone
        has_pickup_zone = False
        for waypoint in self.flight.points:
            if waypoint.waypoint_type not in [
                FlightWaypointType.PICKUP,
                FlightWaypointType.DROP_OFF,
            ]:
                continue
            # Create Pickup and DropOff zone
            zone_name = f"{waypoint.waypoint_type.name}_{self.flight.id}"
            mission.triggers.add_triggerzone(waypoint.position, 300, False, zone_name)
            if waypoint.waypoint_type == FlightWaypointType.PICKUP:
                has_pickup_zone = True
                logistics_info.pickup_zone = zone_name
            else:
                logistics_info.drop_off_zone = zone_name

        if isinstance(self.flight.state, InFlight):
            # TODO Preload if flight is already in the air
            logistics_info.preload = True
        elif not has_pickup_zone:
            # TODO Improve the position
            # Create Pickup Zone at Takeoff WP
            zone_name = f"PICKUP_{self.flight.id}"
            mission.triggers.add_triggerzone(
                self.flight.flight_plan.waypoints[0].position, 300, False, zone_name
            )
            logistics_info.pickup_zone = zone_name
        return logistics_info

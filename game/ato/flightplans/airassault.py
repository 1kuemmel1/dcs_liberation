from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Iterator, Type
from game.ato.flightplans.airlift import AirliftLayout
from game.ato.flightplans.standard import StandardFlightPlan
from game.theater.missiontarget import MissionTarget
from game.utils import feet
from .ibuilder import IBuilder
from .waypointbuilder import WaypointBuilder

if TYPE_CHECKING:
    from ..flight import Flight
    from ..flightwaypoint import FlightWaypoint


class Builder(IBuilder):
    def build(self) -> AirAssaultLayout:

        altitude = feet(1500)
        altitude_is_agl = True

        builder = WaypointBuilder(self.flight, self.coalition)
        pickup_zone = MissionTarget(
            "Pickup Zone", self.flight.departure.position.random_point_within(1200, 600)
        )
        assault_area = builder.assault_area(self.package.target)
        heading_from_target = self.package.target.position.heading_between_point(
            pickup_zone.position
        )
        drop_off_zone = MissionTarget(
            "Dropoff zone",
            self.package.target.position.point_from_heading(heading_from_target, 1200),
        )

        return AirAssaultLayout(
            departure=builder.takeoff(self.flight.departure),
            nav_to_pickup=builder.nav_path(
                self.flight.departure.position,
                pickup_zone.position,
                altitude,
                altitude_is_agl,
            ),
            pickup=builder.pickup(pickup_zone),
            nav_to_drop_off=builder.nav_path(
                pickup_zone.position,
                drop_off_zone.position,
                altitude,
                altitude_is_agl,
            ),
            drop_off=builder.drop_off(drop_off_zone),
            stopover=None,
            assault_area=assault_area,
            nav_to_home=builder.nav_path(
                drop_off_zone.position,
                self.flight.arrival.position,
                altitude,
                altitude_is_agl,
            ),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )


@dataclass(frozen=True)
class AirAssaultLayout(AirliftLayout):
    assault_area: FlightWaypoint

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.nav_to_pickup
        if self.pickup:
            yield self.pickup
        yield from self.nav_to_drop_off
        yield self.drop_off
        yield self.assault_area
        yield from self.nav_to_home
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


class AirAssaultFlightPlan(StandardFlightPlan[AirAssaultLayout]):
    def __init__(self, flight: Flight, layout: AirAssaultLayout) -> None:
        super().__init__(flight, layout)

    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def tot_waypoint(self) -> FlightWaypoint | None:
        return self.layout.drop_off

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        # TOT planning isn't really useful for transports. They're behind the front
        # lines so no need to wait for escorts or for other missions to complete.
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        return None

    @property
    def mission_departure_time(self) -> timedelta:
        return self.package.time_over_target

from dcs.point import MovingPoint, PointAction
from dcs.task import Land

from .pydcswaypointbuilder import PydcsWaypointBuilder


class HeloLandBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        if self.flight.is_helo:
            # Use Land Task with 30s duration for helos
            waypoint.add_task(Land(waypoint.position, duration=30))
            return waypoint
        raise RuntimeError("Helo Landing Task can only be assigned to helos")

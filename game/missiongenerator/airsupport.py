from __future__ import annotations
from collections import defaultdict

from dataclasses import dataclass, field
from datetime import timedelta
from typing import Optional, TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from game.radio.radios import RadioFrequency
    from game.radio.tacan import TacanChannel


@dataclass
class AwacsInfo:
    """AWACS information for the kneeboard."""

    group_name: str
    callsign: str
    freq: RadioFrequency
    depature_location: Optional[str]
    start_time: Optional[timedelta]
    end_time: Optional[timedelta]
    blue: bool


@dataclass
class TankerInfo:
    """Tanker information for the kneeboard."""

    group_name: str
    callsign: str
    variant: str
    freq: RadioFrequency
    tacan: TacanChannel
    start_time: Optional[timedelta]
    end_time: Optional[timedelta]
    blue: bool


@dataclass(frozen=True)
class JtacInfo:
    """JTAC information."""

    group_name: str
    unit_name: str
    callsign: str
    region: str
    code: str
    blue: bool
    freq: RadioFrequency


@dataclass
class CargoInfo:
    """Cargo information."""

    unit_type: str = field(default_factory=str)
    spawn_zone: str = field(default_factory=str)
    amount: int = field(default=1)


@dataclass
class LogisticsInfo:
    """Logistics information."""

    pilot_names: list[str] = field(default_factory=list)
    pickup_zone: str = field(default_factory=str)
    drop_off_zone: str = field(default_factory=str)
    target_zone: str = field(default_factory=str)
    blue: bool = field(default_factory=bool)
    cargo: list[CargoInfo] = field(default_factory=list)
    logistic_unit: str = field(default_factory=str)


@dataclass
class AirSupport:
    awacs: list[AwacsInfo] = field(default_factory=list)
    tankers: list[TankerInfo] = field(default_factory=list)
    jtacs: list[JtacInfo] = field(default_factory=list)
    logistics: dict[UUID, LogisticsInfo] = field(
        default_factory=lambda: defaultdict(LogisticsInfo)
    )

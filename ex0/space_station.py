from pydantic import BaseModel, Field
from pydantic import ValidationError
from datetime import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)

    name: str = Field(min_length=1, max_length=50)

    crew_size: int = Field(ge=1, le=20)

    power_level: float = Field(ge=0.0, le=100.0)

    oxygen_level: float = Field(ge=0.0, le=100.0)

    last_maintenance: datetime

    is_operational: bool = Field(default=True)

    notes: Optional[str] = Field(default=None, max_length=200)

    def __str__(self) -> str:
        status = "Operational" if self.is_operational else "Offline"
        return (
            f"ID: {self.station_id}\n"
            f"Name: {self.name}\n"
            f"Crew: {self.crew_size} people\n"
            f"Power: {self.power_level}%\n"
            f"Oxygen: {self.oxygen_level}%\n"
            f"Status: {status}"
        )


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    s = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6, power_level=85.5,
        oxygen_level=92.3, is_operational=True,
        last_maintenance=datetime(2024, 1, 15, 10, 0, 0))

    print("Valid station created:")
    print(s)

    print("\n========================================")
    print("Expected validation error:")
    try:
        SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=22, power_level=85.5,
            oxygen_level=92.3, is_operational=True,
            last_maintenance=datetime(2024, 1, 15, 10, 0, 0))
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])


if __name__ == "__main__":
    main()

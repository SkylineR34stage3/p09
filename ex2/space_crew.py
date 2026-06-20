from pydantic import BaseModel, Field, model_validator
from enum import Enum
from datetime import datetime


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)

    name: str = Field(min_length=2, max_length=50)

    rank: Rank

    age: int = Field(ge=18, le=80)

    specialization: str = Field(min_length=3, max_length=30)

    years_experience: int = Field(ge=0, le=50)

    is_active: bool = Field(default=True)

    def describe(self) -> str:
        return (
            f"- {self.name} ({self.rank.value}) "
            f"- {self.specialization}\n"
        )


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)

    mission_name: str = Field(min_length=3, max_length=100)

    destination: str = Field(min_length=3, max_length=50)

    launch_date: datetime

    duration_days: int = Field(ge=1, le=3650)

    crew: list[CrewMember] = Field(min_length=1, max_length=12)

    mission_status: str = Field(default="planned")

    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_rules(self) -> 'SpaceMission':
        has_leader = any(
            m.rank in (Rank.commander, Rank.captain) for m in self.crew
        )
        experienced = sum(1 for m in self.crew if m.years_experience >= 5)
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        if self.duration_days > 365 and experienced / len(self.crew) < 0.5:
            raise ValueError("Long missions need 50% experienced crew")
        if not all(m.is_active for m in self.crew):
            raise ValueError("All crew members must be active")
        return self

    def __str__(self) -> str:
        crew_list = "".join(m.describe() for m in self.crew)
        return (
            f"Mission: {self.mission_name}\n"
            f"ID: {self.mission_id}\n"
            f"Destination: {self.destination}\n"
            f"Duration: {self.duration_days} days\n"
            f"Budget: ${self.budget_millions}M\n"
            f"Crew size: {len(self.crew)}\n"
            f"Crew members:\n"
            f"{crew_list}"
        )


def get_crew() -> list[CrewMember]:
    return [
        CrewMember(member_id="1boba", name="Sarah Connor",
                   rank=Rank.commander, age=34,
                   specialization="Mission Command",
                   years_experience=3),
        CrewMember(member_id="2buba", name="John Smith",
                   rank=Rank.lieutenant, age=43,
                   specialization="Navigation",
                   years_experience=7),
        CrewMember(member_id="3biba", name="Alice Johnson",
                   rank=Rank.officer, age=23,
                   specialization="Engineering",
                   years_experience=5)
    ]


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")

    crew = get_crew()
    print("Valid mission created:")
    sm = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2024, 1, 15, 10, 0, 0),
        duration_days=900,
        crew=crew,
        budget_millions=2500.0
    )
    print(sm)


if __name__ == "__main__":
    main()

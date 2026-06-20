from pydantic import BaseModel, Field, model_validator
from enum import Enum
from datetime import datetime
from typing import Optional


class ContactType(Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)

    timestamp: datetime

    location: str = Field(min_length=3, max_length=100)

    contact_type: ContactType

    signal_strength: float = Field(ge=0.0, le=10.0)

    duration_minutes: int = Field(ge=1, le=1440)

    witness_count: int = Field(ge=1, le=100)

    message_received: Optional[str] = Field(default=None, max_length=500)

    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_rules(self) -> 'AlienContact':
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if (
            self.contact_type == ContactType.physical
            and not self.is_verified
        ):
            raise ValueError("Physical contact reports must be verified")
        if (
            self.contact_type == ContactType.telepathic
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        if (self.signal_strength > 7.0 and self.message_received is None):
            raise ValueError("Signal with strength more than 7.0"
                             " requires a decodable content")
        return self


def main() -> None:
    pass


if __name__ == "__main__":
    main()

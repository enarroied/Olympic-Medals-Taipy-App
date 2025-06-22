from dataclasses import dataclass


@dataclass
class MedalColorMap:
    gold: str = "#FFD700"
    silver: str = "#C0C0C0"
    bronze: str = "#CD7F32"

    def as_dict(self):
        return {"Gold": self.gold, "Silver": self.silver, "Bronze": self.bronze}

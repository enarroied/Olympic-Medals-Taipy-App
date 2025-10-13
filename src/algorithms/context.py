from dataclasses import dataclass


@dataclass
class GenderCategoryColorMap:
    men: str = "#6baed6"  # Light blue
    women: str = "#fb6a4a"  # Light red
    open: str = "#74c476"  # Light green
    mixed: str = "#9e9ac8"  # Light purple

    def as_dict(self):
        return {
            "Men": self.men,
            "Women": self.women,
            "Open": self.open,
            "Mixed": self.mixed,
        }


@dataclass
class MedalColorMap:
    gold: str = "#FFD700"
    silver: str = "#C0C0C0"
    bronze: str = "#CD7F32"

    def as_dict(self):
        return {"Gold": self.gold, "Silver": self.silver, "Bronze": self.bronze}

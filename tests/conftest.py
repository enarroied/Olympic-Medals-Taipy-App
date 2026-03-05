"""
conftest.py – shared fixtures and mocks for the algorithms test suite.

The `context` module is an external dependency not present in this repo;
we mock it here so every test file can import the algorithm modules cleanly.
"""

import sys
from pathlib import Path
from types import ModuleType

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# ---------------------------------------------------------------------------
# Mock the `context` module (MedalColorMap, GenderCategoryColorMap)
# ---------------------------------------------------------------------------

_context = ModuleType("context")


class _MedalColorMap:
    def as_dict(self):
        return {"Gold": "#FFD700", "Silver": "#C0C0C0", "Bronze": "#CD7F32"}


class _GenderCategoryColorMap:
    def as_dict(self):
        return {"Men": "#1f77b4", "Women": "#e377c2", "Mixed": "#2ca02c"}


_context.MedalColorMap = _MedalColorMap
_context.GenderCategoryColorMap = _GenderCategoryColorMap
sys.modules.setdefault("context", _context)

# ---------------------------------------------------------------------------
# Shared sample DataFrames
# ---------------------------------------------------------------------------


@pytest.fixture
def df_olympic_medals():
    """Minimal medals DataFrame used across multiple tests."""
    return pd.DataFrame(
        {
            "Olympiad": [
                "Rio 2016",
                "Rio 2016",
                "Tokyo 2020",
                "Tokyo 2020",
                "PyeongChang 2018",
                "PyeongChang 2018",
            ],
            "Olympic_year": [2016, 2016, 2020, 2020, 2018, 2018],
            "Olympic_season": [
                "summer",
                "summer",
                "summer",
                "summer",
                "winter",
                "winter",
            ],
            "Committee": ["USA", "GBR", "USA", "CHN", "NOR", "USA"],
            "Discipline": [
                "Athletics",
                "Swimming",
                "Athletics",
                "Gymnastics",
                "Biathlon",
                "Skiing",
            ],
            "Event": [
                "100m",
                "200m freestyle",
                "100m",
                "Floor",
                "Sprint",
                "Slalom",
            ],
            "Gender": ["Men", "Women", "Men", "Women", "Men", "Women"],
            "Medal_type": ["Gold", "Silver", "Bronze", "Gold", "Gold", "Silver"],
        }
    )


@pytest.fixture
def df_medals_season():
    """Aggregated season-level medals DataFrame for MedalsBySeason tests."""
    return pd.DataFrame(
        {
            "Olympiad": [
                "Athens 2004",
                "Beijing 2008",
                "Rio 2016",
                "Salt Lake 2002",
                "Turin 2006",
            ],
            "Olympic_season": [
                "summer",
                "summer",
                "summer",
                "winter",
                "winter",
            ],
            "Medal_type": ["Gold", "Silver", "Bronze", "Gold", "Silver"],
            "Medal_count": [100, 90, 80, 50, 45],
        }
    )


@pytest.fixture
def df_total_medals_by_olympiad_and_committee():
    """Wide-format DataFrame used by MedalsByCountry tests."""
    return pd.DataFrame(
        {
            "Olympic_year": [2016, 2016, 2020, 2020, 2018, 2018],
            "Olympiad": [
                "Rio 2016",
                "Rio 2016",
                "Tokyo 2020",
                "Tokyo 2020",
                "PyeongChang 2018",
                "PyeongChang 2018",
            ],
            "Olympic_season": [
                "summer",
                "summer",
                "summer",
                "summer",
                "winter",
                "winter",
            ],
            "Medal_type": ["All", "Gold", "All", "Gold", "All", "Gold"],
            "Total_medals": [300, 100, 310, 105, 100, 40],
            "USA": [40, 15, 38, 14, 10, 4],
            "GBR": [27, 9, 22, 7, 5, 2],
        }
    )


@pytest.fixture
def df_grouped_medals_olympiads():
    """Pivot-style DataFrame used by MedalsByOlympics tests."""
    return pd.DataFrame(
        {
            "Olympiad": ["Rio 2016", "Rio 2016", "Rio 2016", "Tokyo 2020"],
            "Committee": ["USA", "GBR", "CHN", "USA"],
            "Gold": [46, 27, 26, 39],
            "Silver": [37, 23, 18, 41],
            "Bronze": [38, 17, 26, 33],
        }
    )


@pytest.fixture
def df_olympic_cities():
    """City-level DataFrame used by MedalMap tests."""
    return pd.DataFrame(
        {
            "Country": ["United States", "United States", "Norway", "Norway"],
            "ISO_code_mapping": ["USA", "USA", "NOR", "NOR"],
            "Olympic_season": ["summer", "winter", "winter", "winter"],
            "total_medals": [2638, 305, 148, 203],
            "total_medals_gold": [1022, 105, 60, 82],
            "total_medals_silver": [795, 112, 49, 72],
            "total_medals_bronze": [821, 88, 39, 49],
        }
    )

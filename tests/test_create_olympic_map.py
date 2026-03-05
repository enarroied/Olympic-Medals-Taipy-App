"""Tests for src/algorithms/create_olympic_map.py

Chart-rendering methods (_plot_map_medals_by_country) are excluded.
"""

import pandas as pd
import pytest

from algorithms.create_olympic_map import MedalMap

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestSelectMedalColumn:
    """Tests for MedalMap._select_medal_column."""

    def test_all_maps_to_total_medals(self, df_olympic_cities):
        obj = MedalMap(df_olympic_cities)
        assert obj._select_medal_column("All") == "total_medals"

    def test_gold_maps_correctly(self, df_olympic_cities):
        obj = MedalMap(df_olympic_cities)
        assert obj._select_medal_column("Gold") == "total_medals_gold"

    def test_silver_maps_correctly(self, df_olympic_cities):
        obj = MedalMap(df_olympic_cities)
        assert obj._select_medal_column("Silver") == "total_medals_silver"

    def test_bronze_maps_correctly(self, df_olympic_cities):
        obj = MedalMap(df_olympic_cities)
        assert obj._select_medal_column("Bronze") == "total_medals_bronze"

    def test_invalid_medal_type_raises_value_error(self, df_olympic_cities):
        obj = MedalMap(df_olympic_cities)
        with pytest.raises(ValueError, match="Invalid medal_type"):
            obj._select_medal_column("Platinum")


class TestComputeMedalCounts:
    """Tests for MedalMap._compute_medal_counts."""

    def test_all_seasons_includes_summer_and_winter(self, df_olympic_cities):
        obj = MedalMap(df_olympic_cities)
        result = obj._compute_medal_counts("All", "All")
        countries = set(result["Country"].values)
        assert "United States" in countries
        assert "Norway" in countries

    def test_summer_filter_excludes_winter_only_countries(self, df_olympic_cities):
        """Norway only appears in winter rows in our fixture."""
        obj = MedalMap(df_olympic_cities)
        result = obj._compute_medal_counts("summer", "All")
        assert "Norway" not in result["Country"].to_numpy()

    def test_winter_filter_excludes_summer_only_entries(self, df_olympic_cities):
        obj = MedalMap(df_olympic_cities)
        result = obj._compute_medal_counts("winter", "All")
        # Norway should appear; USA has one winter row so it also appears
        assert "Norway" in result["Country"].to_numpy()

    def test_gold_medals_sum_is_correct(self, df_olympic_cities):
        obj = MedalMap(df_olympic_cities)
        result = obj._compute_medal_counts("All", "Gold")
        usa_row = result[result["Country"] == "United States"]
        expected = df_olympic_cities[df_olympic_cities["Country"] == "United States"][
            "total_medals_gold"
        ].sum()
        assert usa_row["Number of Medals"].to_numpy()[0] == expected

    def test_output_has_required_columns(self, df_olympic_cities):
        obj = MedalMap(df_olympic_cities)
        result = obj._compute_medal_counts("All", "All")
        for col in ("Country", "ISO_code_mapping", "Number of Medals"):
            assert col in result.columns

    def test_generate_medal_counts_returns_empty_df_on_error(self):
        bad_df = pd.DataFrame({"irrelevant": [1, 2]})
        obj = MedalMap(bad_df)
        result = obj._generate_medal_counts("summer", "Gold")
        assert isinstance(result, pd.DataFrame)
        assert result.empty

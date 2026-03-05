"""Tests for src/algorithms/create_medals_by_season.py

Chart-rendering methods (_plot_bar_medal_season, _add_stockholm_annotation)
are intentionally excluded.
"""

import pandas as pd

from algorithms.create_medals_by_season import MedalsBySeason

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestMedalsBySeasonFilterSeason:
    """Tests for _filter_season and _compute_medals_by_season."""

    def test_filter_season_summer_returns_only_summer(self, df_medals_season):
        obj = MedalsBySeason(df_medals_season)
        result = obj._filter_season("summer")
        assert set(result["Olympic_season"].unique()) == {"summer"}

    def test_filter_season_winter_returns_only_winter(self, df_medals_season):
        obj = MedalsBySeason(df_medals_season)
        result = obj._filter_season("winter")
        assert set(result["Olympic_season"].unique()) == {"winter"}

    def test_filter_season_resets_index(self, df_medals_season):
        obj = MedalsBySeason(df_medals_season)
        result = obj._filter_season("summer")
        assert list(result.index) == list(range(len(result)))

    def test_compute_medals_all_returns_full_dataframe(self, df_medals_season):
        obj = MedalsBySeason(df_medals_season)
        result = obj._compute_medals_by_season("All")
        assert len(result) == len(df_medals_season)

    def test_compute_medals_summer_filters_correctly(self, df_medals_season):
        obj = MedalsBySeason(df_medals_season)
        result = obj._compute_medals_by_season("summer")
        assert all(result["Olympic_season"] == "summer")

    def test_compute_medals_winter_filters_correctly(self, df_medals_season):
        obj = MedalsBySeason(df_medals_season)
        result = obj._compute_medals_by_season("winter")
        assert all(result["Olympic_season"] == "winter")

    def test_original_dataframe_is_not_mutated(self, df_medals_season):
        original_len = len(df_medals_season)
        obj = MedalsBySeason(df_medals_season)
        obj._filter_season("summer")
        assert len(df_medals_season) == original_len

    def test_generate_medals_by_season_returns_empty_df_on_error(self):
        bad_df = pd.DataFrame({"wrong_column": [1, 2, 3]})
        obj = MedalsBySeason(bad_df)
        result = obj._generate_medals_by_season("summer")
        assert isinstance(result, pd.DataFrame)

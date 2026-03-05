"""Tests for src/algorithms/create_medals_by_country.py

Chart-rendering methods (_plot_fig_total_medals_by_country) are excluded.

Note on _filter_dataset: the method drops Olympic_season and Medal_type from
its output (they are used only for row-filtering, not returned). Season/type
assertions therefore check row counts against the original DataFrame rather
than inspecting the result columns directly.
"""

import pandas as pd

from algorithms.create_medals_by_country import MedalsByCountry

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestFilterDataset:
    """Tests for MedalsByCountry._filter_dataset."""

    def test_filters_by_season_summer_row_count(
        self, df_total_medals_by_olympiad_and_committee
    ):
        obj = MedalsByCountry(df_total_medals_by_olympiad_and_committee)
        result = obj._filter_dataset(["USA"], "summer", "All")
        expected = (
            (df_total_medals_by_olympiad_and_committee["Olympic_season"] == "summer")
            & (df_total_medals_by_olympiad_and_committee["Medal_type"] == "All")
        ).sum()
        assert len(result) == expected

    def test_filters_by_season_winter_row_count(
        self, df_total_medals_by_olympiad_and_committee
    ):
        obj = MedalsByCountry(df_total_medals_by_olympiad_and_committee)
        result = obj._filter_dataset(["USA"], "winter", "All")
        expected = (
            (df_total_medals_by_olympiad_and_committee["Olympic_season"] == "winter")
            & (df_total_medals_by_olympiad_and_committee["Medal_type"] == "All")
        ).sum()
        assert len(result) == expected

    def test_filters_by_medal_type_row_count(
        self, df_total_medals_by_olympiad_and_committee
    ):
        obj = MedalsByCountry(df_total_medals_by_olympiad_and_committee)
        result = obj._filter_dataset(["USA"], "summer", "Gold")
        expected = (
            (df_total_medals_by_olympiad_and_committee["Olympic_season"] == "summer")
            & (df_total_medals_by_olympiad_and_committee["Medal_type"] == "Gold")
        ).sum()
        assert len(result) == expected

    def test_output_contains_requested_committees(
        self, df_total_medals_by_olympiad_and_committee
    ):
        obj = MedalsByCountry(df_total_medals_by_olympiad_and_committee)
        result = obj._filter_dataset(["USA", "GBR"], "summer", "All")
        assert "USA" in result.columns
        assert "GBR" in result.columns

    def test_output_excludes_filter_columns(
        self, df_total_medals_by_olympiad_and_committee
    ):
        """Olympic_season and Medal_type are used for filtering only, not returned."""
        obj = MedalsByCountry(df_total_medals_by_olympiad_and_committee)
        result = obj._filter_dataset(["USA"], "summer", "All")
        assert "Olympic_season" not in result.columns
        assert "Medal_type" not in result.columns


class TestComputePercentage:
    """Tests for MedalsByCountry._compute_percentage."""

    def test_percentage_is_within_0_100(
        self, df_total_medals_by_olympiad_and_committee
    ):
        obj = MedalsByCountry(df_total_medals_by_olympiad_and_committee)
        df = obj._filter_dataset(["USA", "GBR"], "summer", "All")
        result = obj._compute_percentage(df.copy(), ["USA", "GBR"])
        assert (result["USA"] >= 0).all() and (result["USA"] <= 100).all()

    def test_percentage_sums_across_committees(
        self, df_total_medals_by_olympiad_and_committee
    ):
        obj = MedalsByCountry(df_total_medals_by_olympiad_and_committee)
        df = obj._filter_dataset(["USA", "GBR"], "summer", "All")
        result = obj._compute_percentage(df.copy(), ["USA", "GBR"])
        row_sums = result["USA"] + result["GBR"]
        assert (row_sums <= 100 + 1e-6).all()

    def test_percentage_handles_zero_total_medals(self):
        """When Total_medals is 0, percentage should be 0 (fillna(0))."""
        df = pd.DataFrame(
            {
                "Olympic_year": [2000],
                "Olympiad": ["Sydney 2000"],
                "Total_medals": [0],
                "USA": [0],
            }
        )
        obj = MedalsByCountry(df)
        result = obj._compute_percentage(df.copy(), ["USA"])
        assert result["USA"].iloc[0] == 0.0


class TestComputeMedalsByCommittee:
    """Tests for MedalsByCountry._compute_medals_by_committee."""

    def test_total_mode_does_not_have_total_medals_column(
        self, df_total_medals_by_olympiad_and_committee
    ):
        obj = MedalsByCountry(df_total_medals_by_olympiad_and_committee)
        result = obj._compute_medals_by_committee(
            ["USA"], "summer", "All", "Total medals"
        )
        assert "Total_medals" not in result.columns

    def test_percentage_mode_values_differ_from_raw(
        self, df_total_medals_by_olympiad_and_committee
    ):
        obj = MedalsByCountry(df_total_medals_by_olympiad_and_committee)
        raw = obj._compute_medals_by_committee(["USA"], "summer", "All", "Total medals")
        pct = obj._compute_medals_by_committee(["USA"], "summer", "All", "Percentage")
        assert (pct["USA"] <= 100).all()
        assert not raw["USA"].equals(pct["USA"])

"""Tests for src/algorithms/create_medals_by_olympics.py

Chart-rendering methods (_plot_by_committee) are excluded.
"""

import pandas as pd

from algorithms.create_medals_by_olympics import MedalsByOlympics

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestComputeDataByOlympics:
    """Tests for MedalsByOlympics._compute_data_by_olympics."""

    def test_filters_to_correct_olympiad(self, df_grouped_medals_olympiads):
        obj = MedalsByOlympics(df_grouped_medals_olympiads)
        result = obj._compute_data_by_olympics("Rio 2016")
        assert len(result) == 3  # USA, GBR, CHN rows

    def test_olympiad_column_is_dropped(self, df_grouped_medals_olympiads):
        obj = MedalsByOlympics(df_grouped_medals_olympiads)
        result = obj._compute_data_by_olympics("Rio 2016")
        assert "Olympiad" not in result.columns

    def test_medal_columns_are_present(self, df_grouped_medals_olympiads):
        obj = MedalsByOlympics(df_grouped_medals_olympiads)
        result = obj._compute_data_by_olympics("Rio 2016")
        for col in ("Gold", "Silver", "Bronze"):
            assert col in result.columns

    def test_unknown_olympiad_returns_empty(self, df_grouped_medals_olympiads):
        obj = MedalsByOlympics(df_grouped_medals_olympiads)
        result = obj._compute_data_by_olympics("Narnia 1900")
        assert result.empty

    def test_original_dataframe_is_not_mutated(self, df_grouped_medals_olympiads):
        original_cols = list(df_grouped_medals_olympiads.columns)
        obj = MedalsByOlympics(df_grouped_medals_olympiads)
        obj._compute_data_by_olympics("Rio 2016")
        assert list(df_grouped_medals_olympiads.columns) == original_cols


class TestGenerateDataByOlympics:
    """Tests for the error-handling wrapper _generate_data_by_olympics."""

    def test_returns_empty_dataframe_on_error(self):
        bad_df = pd.DataFrame({"no_olympiad_col": [1, 2]})
        obj = MedalsByOlympics(bad_df)
        result = obj._generate_data_by_olympics("Rio 2016")
        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_returns_correct_data_on_success(self, df_grouped_medals_olympiads):
        obj = MedalsByOlympics(df_grouped_medals_olympiads)
        result = obj._generate_data_by_olympics("Tokyo 2020")
        assert len(result) == 1
        assert result.iloc[0]["Committee"] == "USA"

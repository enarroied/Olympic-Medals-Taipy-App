"""Tests for src/algorithms/create_sunburst.py

Chart-rendering methods (_plot_sunburst_medals) are excluded.
"""

from algorithms.create_sunburst import SunburstByGender

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestMakeInitialSunburst:
    """Tests for SunburstByGender._make_initial_sunburst."""

    def test_output_contains_required_columns(self, df_olympic_medals):
        obj = SunburstByGender(df_olympic_medals)
        for col in ("Olympiad", "Gender", "Discipline", "Event"):
            assert col in obj.df_sunburst.columns

    def test_output_has_no_extra_columns(self, df_olympic_medals):
        obj = SunburstByGender(df_olympic_medals)
        assert set(obj.df_sunburst.columns) == {
            "Olympiad",
            "Gender",
            "Discipline",
            "Event",
        }

    def test_all_values_are_strings(self, df_olympic_medals):
        obj = SunburstByGender(df_olympic_medals)
        for col in obj.df_sunburst.columns:
            assert obj.df_sunburst[col].dtype == object  # str dtype is 'object'

    def test_row_count_matches_input(self, df_olympic_medals):
        obj = SunburstByGender(df_olympic_medals)
        assert len(obj.df_sunburst) == len(df_olympic_medals)

    def test_original_dataframe_is_not_mutated(self, df_olympic_medals):
        original_cols = set(df_olympic_medals.columns)
        SunburstByGender(df_olympic_medals)
        assert set(df_olympic_medals.columns) == original_cols


class TestComputeSunburstData:
    """Tests for SunburstByGender._compute_sunburst_data."""

    def test_all_returns_full_dataset(self, df_olympic_medals):
        obj = SunburstByGender(df_olympic_medals)
        result = obj._compute_sunburst_data("All")
        assert len(result) == len(df_olympic_medals)

    def test_specific_olympiad_filters_correctly(self, df_olympic_medals):
        obj = SunburstByGender(df_olympic_medals)
        result = obj._compute_sunburst_data("Rio 2016")
        assert all(result["Olympiad"] == "Rio 2016")

    def test_unknown_olympiad_returns_empty(self, df_olympic_medals):
        obj = SunburstByGender(df_olympic_medals)
        result = obj._compute_sunburst_data("Narnia 1900")
        assert result.empty

    def test_winter_olympiad_returns_correct_rows(self, df_olympic_medals):
        obj = SunburstByGender(df_olympic_medals)
        result = obj._compute_sunburst_data("PyeongChang 2018")
        assert len(result) == 2  # two winter rows in fixture
        assert all(result["Olympiad"] == "PyeongChang 2018")

"""Tests for src/algorithms/create_medal_by_olympic_and_discipline.py

Chart-rendering methods (_plot_medals_grid_common, _plot_grid_for_country)
are excluded.
"""

import pandas as pd

from algorithms.create_medal_by_olympic_and_discipline import (
    MedalsByOlympicAndDiscipline,
)

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestFilterOlympicSeason:
    """Tests for MedalsByOlympicAndDiscipline._filter_olympic_season."""

    def test_summer_filter_returns_only_summer_rows(self, df_olympic_medals):
        obj = MedalsByOlympicAndDiscipline(df_olympic_medals)
        result = obj._filter_olympic_season(df_olympic_medals, "summer")
        assert all(result["Olympic_season"] == "summer")

    def test_winter_filter_returns_only_winter_rows(self, df_olympic_medals):
        obj = MedalsByOlympicAndDiscipline(df_olympic_medals)
        result = obj._filter_olympic_season(df_olympic_medals, "winter")
        assert all(result["Olympic_season"] == "winter")

    def test_summer_and_winter_are_exhaustive(self, df_olympic_medals):
        obj = MedalsByOlympicAndDiscipline(df_olympic_medals)
        summer = obj._filter_olympic_season(df_olympic_medals, "summer")
        winter = obj._filter_olympic_season(df_olympic_medals, "winter")
        assert len(summer) + len(winter) == len(df_olympic_medals)


class TestDisciplineAttributes:
    """Tests that discipline lists are built correctly on __init__."""

    def test_summer_disciplines_are_a_subset_of_all_disciplines(
        self, df_olympic_medals
    ):
        obj = MedalsByOlympicAndDiscipline(df_olympic_medals)
        all_disciplines = set(df_olympic_medals["Discipline"].unique())
        assert set(obj.summer_disciplines).issubset(all_disciplines)

    def test_winter_disciplines_are_a_subset_of_all_disciplines(
        self, df_olympic_medals
    ):
        obj = MedalsByOlympicAndDiscipline(df_olympic_medals)
        all_disciplines = set(df_olympic_medals["Discipline"].unique())
        assert set(obj.winter_disciplines).issubset(all_disciplines)

    def test_summer_and_winter_disciplines_do_not_overlap(self, df_olympic_medals):
        obj = MedalsByOlympicAndDiscipline(df_olympic_medals)
        overlap = set(obj.summer_disciplines) & set(obj.winter_disciplines)
        assert overlap == set()


class TestPivotOlympicByDiscipline:
    """Tests for MedalsByOlympicAndDiscipline._pivot_olympic_by_discipline."""

    def test_pivot_returns_dataframe(self, df_olympic_medals):
        obj = MedalsByOlympicAndDiscipline(df_olympic_medals)
        df_summer = obj._filter_olympic_season(df_olympic_medals, "summer")
        result = obj._pivot_olympic_by_discipline(df_summer)
        assert isinstance(result, pd.DataFrame)

    def test_pivot_columns_are_disciplines(self, df_olympic_medals):
        obj = MedalsByOlympicAndDiscipline(df_olympic_medals)
        df_summer = obj._filter_olympic_season(df_olympic_medals, "summer")
        result = obj._pivot_olympic_by_discipline(df_summer)
        assert result.columns.name == "Discipline"

    def test_pivot_index_contains_olympiad_and_year(self, df_olympic_medals):
        obj = MedalsByOlympicAndDiscipline(df_olympic_medals)
        df_summer = obj._filter_olympic_season(df_olympic_medals, "summer")
        result = obj._pivot_olympic_by_discipline(df_summer)
        assert "Olympiad" in result.index.names
        assert "Olympic_year" in result.index.names

    def test_pivot_values_are_non_negative_integers(self, df_olympic_medals):
        obj = MedalsByOlympicAndDiscipline(df_olympic_medals)
        df_summer = obj._filter_olympic_season(df_olympic_medals, "summer")
        result = obj._pivot_olympic_by_discipline(df_summer)
        assert (result >= 0).all().all()


class TestCreateMedalsGrid:
    """Tests for MedalsByOlympicAndDiscipline._create_medals_grid."""

    def test_grid_filters_to_requested_committee(self, df_olympic_medals):
        obj = MedalsByOlympicAndDiscipline(df_olympic_medals)
        result = obj._create_medals_grid(
            obj.df_summer, obj.summer_disciplines, committee="USA"
        )
        # All rows in the pivot correspond to olympiads where USA participated
        # There should be at least one non-zero entry for USA's disciplines
        assert result.sum().sum() > 0

    def test_grid_contains_all_disciplines_as_columns(self, df_olympic_medals):
        obj = MedalsByOlympicAndDiscipline(df_olympic_medals)
        result = obj._create_medals_grid(
            obj.df_summer, obj.summer_disciplines, committee="USA"
        )
        assert set(obj.summer_disciplines).issubset(set(result.columns))

    def test_grid_fills_missing_disciplines_with_zero(self, df_olympic_medals):
        obj = MedalsByOlympicAndDiscipline(df_olympic_medals)
        # GBR only has Swimming in the fixture; Athletics should be 0
        result = obj._create_medals_grid(
            obj.df_summer, obj.summer_disciplines, committee="GBR"
        )
        assert "Athletics" in result.columns
        assert result["Athletics"].sum() == 0

    def test_unknown_committee_returns_all_zeros(self, df_olympic_medals):
        obj = MedalsByOlympicAndDiscipline(df_olympic_medals)
        result = obj._create_medals_grid(
            obj.df_summer, obj.summer_disciplines, committee="XYZ"
        )
        assert result.empty or result.sum().sum() == 0

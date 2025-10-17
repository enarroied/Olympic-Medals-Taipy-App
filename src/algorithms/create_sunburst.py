import plotly.express as px
from algorithms.context import GenderCategoryColorMap


class SunburstByGender:
    """Handles sunburst data preparation and chart generation for medals by gender."""

    def __init__(self, df_olympic_medals, gender_colors=None):
        self.gender_colors = gender_colors or GenderCategoryColorMap()
        self.df_sunburst = self._make_initial_sunburst(df_olympic_medals)

    def _make_initial_sunburst(self, df_olympic_medals):
        """Return a DataFrame ready for sunburst charting."""
        return (
            df_olympic_medals[["Olympiad", "Gender", "Discipline", "Event"]]
            .astype(str)
            .copy()
        )

    def _compute_sunburst_data(self, selected_olympiad_for_sunburst="All"):
        """Internal helper: returns the sunburst DataFrame filtered by Olympiad."""
        df_filtered = self.df_sunburst
        if selected_olympiad_for_sunburst != "All":
            df_filtered = df_filtered[
                df_filtered["Olympiad"] == selected_olympiad_for_sunburst
            ]
        return df_filtered

    def _plot_sunburst_medals(self, df_sunburst, selected_olympiad_for_sunburst):
        """Internal helper: create the Plotly sunburst figure."""
        fig = px.sunburst(
            df_sunburst,
            path=["Gender", "Discipline", "Event"],
            color="Gender",
            color_discrete_map=self.gender_colors.as_dict(),
            title=f"Total Medals by Gender, Discipline, and Event -\
                  {selected_olympiad_for_sunburst}",
        )
        return fig

    def create_sunburst_medals(self, selected_olympiad_for_sunburst="All"):
        """Gets filtered data and generates sunburst chart."""
        df_filtered = self._compute_sunburst_data(selected_olympiad_for_sunburst)
        return self._plot_sunburst_medals(df_filtered, selected_olympiad_for_sunburst)

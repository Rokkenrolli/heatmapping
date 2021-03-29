import _plotly_utils.basevalidators


class CoordinatesValidator(_plotly_utils.basevalidators.AnyValidator):
    def __init__(
        self, plotly_name="coordinates", parent_name="layout.mapbox.layer", **kwargs
    ):
        super(CoordinatesValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "plot"),
            role=kwargs.pop("role", "info"),
            **kwargs
        )

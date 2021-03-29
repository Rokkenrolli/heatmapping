import _plotly_utils.basevalidators


class PathValidator(_plotly_utils.basevalidators.StringValidator):
    def __init__(self, plotly_name="path", parent_name="layout.shape", **kwargs):
        super(PathValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc+arraydraw"),
            role=kwargs.pop("role", "info"),
            **kwargs
        )

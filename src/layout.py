from dash import dcc, html

layout = html.Div(
    [
        html.H1("Hybrid Image Playground", style={"textAlign": "center"}),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Upload(
                            id="upload-image-1",
                            children=html.Div(
                                ["Drag and Drop or ", html.A("Select Image 1")]
                            ),
                            style={
                                "width": "100%",
                                "height": "60px",
                                "lineHeight": "60px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "margin": "10px",
                            },
                            multiple=False,
                            accept="image/*",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    id="output-image-upload-1", style={"width": "50%"}
                                ),
                                html.Div(
                                    id="output-image-upload-1-filtered",
                                    style={"width": "50%"},
                                ),
                            ],
                            style={"display": "flex", "width": "100%"},
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "width": "45%",
                        "verticalAlign": "top",
                        "marginRight": "5%",
                    },
                ),
                html.Div(
                    [
                        dcc.Upload(
                            id="upload-image-2",
                            children=html.Div(
                                ["Drag and Drop or ", html.A("Select Image 2")]
                            ),
                            style={
                                "width": "100%",
                                "height": "60px",
                                "lineHeight": "60px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "margin": "10px",
                            },
                            multiple=False,
                            accept="image/*",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    id="output-image-upload-2", style={"width": "50%"}
                                ),
                                html.Div(
                                    id="output-image-upload-2-filtered",
                                    style={"width": "50%"},
                                ),
                            ],
                            style={"display": "flex", "width": "100%"},
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "width": "45%",
                        "verticalAlign": "top",
                    },
                ),
            ],
            style={"textAlign": "center"},
        ),
    ]
)

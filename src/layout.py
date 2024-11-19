from dash import dcc, html


def image_upload(i):
    return html.Div(
        [
            dcc.Loading(
                [
                    html.Div(
                        [
                            dcc.Upload(
                                id=f"upload-image-{i}",
                                children=html.A(f"Select Image {i}"),
                                multiple=False,
                                accept="image/*",
                            ),
                        ],
                        style={
                            "width": "100%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "5px",
                            "borderStyle": "dashed",
                            "borderRadius": "20px",
                            "textAlign": "center",
                            "backgroundColor": "#f0f0f0",
                        },
                    ),
                    html.Div(
                        [
                            html.Div(
                                id=f"output-image-upload-{i}",
                                style={"width": "50%"},
                            ),
                            html.Div(
                                id=f"output-image-upload-{i}-filtered",
                                style={"width": "50%"},
                            ),
                        ],
                        style={"display": "flex", "width": "100%"},
                    ),
                ],
                overlay_style={
                    "visibility": "visible",
                    "filter": "blur(7px)",
                },
                type="circle",
            ),
        ],
        style={
            "display": "inline-block",
            "width": "40%",
            "verticalAlign": "top",
        },
    )


layout = html.Div(
    [
        html.H1("Hybrid Image Playground"),
        html.H3("Upload Images"),
        html.Div(
            [
                image_upload(1),
                image_upload(2),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-evenly",
                "width": "100%",
                "verticalAlign": "top",
            },
        ),
        html.Div(
            [
                html.H3(id="cf-slider-output"),
                dcc.Slider(
                    1,
                    100,
                    1,
                    value=25,
                    marks=None,
                    id="cf-slider",
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
        ),
        html.H3("Hybrid Image"),
        html.Div(
            [
                dcc.Loading(
                    [
                        html.Div(
                            id="output-image-hybrid",
                            style={
                                "width": "100%",
                                "height": "100%",
                                "textAlign": "center",
                                "margin": "10px",
                                "display": "flex",
                                "justify-content": "center",
                            },
                        ),
                    ],
                    overlay_style={
                        "visibility": "visible",
                        "filter": "blur(7px)",
                    },
                    type="circle",
                ),
            ],
            style={
                "display": "inline-block",
                "width": "100%",
                "verticalAlign": "top",
            },
        ),
    ],
    style={
        "textAlign": "center",
    },
)

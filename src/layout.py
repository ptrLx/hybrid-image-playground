from dash import dcc, html

# enum of filter modes
GAUSSIAN = "Gaussian"
CUT = "Circular cut"


def image_upload(i):
    return html.Div(
        [
            dcc.Loading(
                [
                    html.Div(
                        [
                            dcc.Upload(
                                id=f"upload-image-{i}",
                                children=html.A(
                                    f"Select Image {i} ({'LP' if i == 1 else 'HP'})"
                                ),
                                multiple=False,
                                accept="image/*",
                            ),
                        ],
                        style={
                            "width": "100%",
                            "minWidth": "300px",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "5px",
                            "borderStyle": "dashed",
                            "borderRadius": "20px",
                            "textAlign": "center",
                            "backgroundColor": "#f0f0f0",
                            "boxSizing": "border-box",
                        },
                    ),
                    html.Div(
                        id=f"output-images-{i}",
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
            "verticalAlign": "top",
        },
    )


layout = html.Div(
    [
        # Top bar
        html.Div(
            [
                html.Div(
                    [
                        html.H1("Hybrid Image Playground"),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3("Image Size"),
                                        dcc.Dropdown(
                                            [128, 256, 512, 1024, 2048],
                                            256,
                                            id="image-size",
                                            clearable=False,
                                            style={
                                                "width": "auto",  # Set width to auto to fit text
                                                "minWidth": "100px",  # Optional: Set a minimum width if needed
                                            },
                                        ),
                                    ],
                                ),
                                html.Div(
                                    [
                                        html.H3("Filter Mode"),
                                        dcc.Dropdown(
                                            [GAUSSIAN, CUT],
                                            CUT,
                                            id="filter-mode",
                                            clearable=False,
                                            style={
                                                "width": "auto",  # Set width to auto to fit text
                                                "minWidth": "150px",  # Optional: Set a minimum width if needed
                                            },
                                        ),
                                    ],
                                ),
                                html.Div(
                                    [
                                        html.H3("Cut-off Frequency"),
                                        html.Div(
                                            [
                                                dcc.Slider(
                                                    1,
                                                    100,
                                                    1,
                                                    value=25,
                                                    marks=None,
                                                    id="cf-slider",
                                                    tooltip={
                                                        "placement": "bottom",
                                                        "always_visible": True,
                                                    },
                                                ),
                                            ],
                                            style={
                                                "width": "auto",
                                                "minWidth": "300px",
                                            },
                                        ),
                                    ]
                                ),
                            ],
                            style={
                                "display": "flex",
                                "align-items": "left",
                                "justify-content": "left",
                                "flex-wrap": "wrap",
                                "gap": "10px",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "align-items": "center",
                        "justify-content": "space-between",
                        "background-color": "#d3d3d3",
                        "flex-wrap": "wrap",
                        "padding": "10px",
                    },
                )
            ]
        ),
        # Content
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Upload Images"),
                        html.Div(
                            [
                                image_upload(1),
                                image_upload(2),
                            ],
                            style={
                                "display": "flex",
                                "flexDirection": "column",
                                "width": "100%",
                                "verticalAlign": "top",
                                "gap": "10px",
                            },
                        ),
                    ],
                    style={
                        "width": "50%",
                        "boxSizing": "border-box",
                    },
                ),
                html.Div(
                    dcc.Loading(
                        [
                            html.H3("Filter Masks"),
                            html.Div(
                                [
                                    html.Div(
                                        id="filter-mask-1",
                                        style={
                                            "display": "inline-block",
                                            "width": "40%",
                                            "verticalAlign": "top",
                                        },
                                    ),
                                    html.Div(
                                        id="filter-mask-2",
                                        style={
                                            "display": "inline-block",
                                            "width": "40%",
                                            "verticalAlign": "top",
                                        },
                                    ),
                                ],
                            ),
                            html.H3("Hybrid Image"),
                            html.Div(
                                [
                                    html.Div(
                                        id="output-image-hybrid",
                                        style={
                                            "width": "100%",
                                            "height": "100%",
                                            "textAlign": "center",
                                            "display": "flex",
                                            "justify-content": "center",
                                        },
                                    ),
                                ],
                                style={
                                    "display": "inline-block",
                                    "width": "100%",
                                    "verticalAlign": "top",
                                },
                            ),
                        ],
                        overlay_style={
                            "visibility": "visible",
                            "filter": "blur(7px)",
                        },
                        type="circle",
                    ),
                    style={
                        "width": "50%",
                        "boxSizing": "border-box",
                    },
                ),
            ],
            style={
                "display": "flex",
                "width": "100%",
                "gap": "25px",
                "padding": "20px",
            },
        ),
    ],
    style={"textAlign": "center"},
)

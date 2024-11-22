import dash_bootstrap_components as dbc
from dash import dcc, html

# enum of filter modes
GAUSSIAN = "Gaussian"
CUT = "Circular cut"


def __image_upload(i):
    return html.Div(
        [
            dcc.Loading(
                html.Div(
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
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "10px",
                    },
                ),
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


__filter_controls = html.Div(
    [
        html.Div(
            [
                html.H3("Image Size"),
                dcc.Dropdown(
                    [128, 256, 512, 1024, 2048],
                    256,
                    id="image-size",
                    clearable=False,
                ),
            ],
            style={
                "width": "auto",
                "minWidth": "100px",
            },
        ),
        html.Div(
            [
                html.H3("Filter Mode"),
                dcc.Dropdown(
                    [GAUSSIAN, CUT],
                    CUT,
                    id="filter-mode",
                    clearable=False,
                ),
            ],
            style={
                "width": "auto",
                "minWidth": "150px",
            },
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
                dcc.Checklist(
                    [
                        {
                            "label": "Scale independent",
                            "value": "scale-independent",
                        }
                    ],
                    value=[],
                    id="is-scale-independent-cf",
                    inline=True,
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
)

__upload_images_section = html.Div(
    [
        html.H3("Upload Images"),
        html.Div(
            [
                __image_upload(1),
                __image_upload(2),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "width": "auto",
                "minWidth": "300px",
                "verticalAlign": "top",
                "gap": "10px",
            },
        ),
    ],
    style={
        "display": "flex",
        "flexDirection": "column",
        "boxSizing": "border-box",
    },
)

__hybrid_image_section = html.Div(
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
            html.P(id="cf-scale-info"),
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
        "display": "flex",
        "flexDirection": "column",
        "boxSizing": "border-box",
    },
)

layout = html.Div(
    [
        # Top bar
        html.Div(
            [html.H1("Hybrid Image Playground"), __filter_controls],
            style={
                "display": "flex",
                "justify-content": "space-between",
                "background-color": "#d3d3d3",
                "flex-wrap": "wrap",
                "padding": "10px",
                "textAlign": "left",
            },
        ),
        # Content
        html.Div(
            [
                __upload_images_section,
                __hybrid_image_section,
            ],
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "justify-content": "space-evenly",
                "width": "100%",
                "gap": "25px",
            },
        ),
    ],
    style={"textAlign": "center"},
)

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
                                        f"Select Image for {'Low' if i == 1 else 'High'} Frequency Portion"
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


__filter_controls = dbc.Row(
    [
        dbc.Col(
            [
                html.H6("Image Size"),
                dcc.Dropdown(
                    [128, 256, 512, 1024, 2048],
                    256,
                    id="image-size",
                    clearable=False,
                    style={"color": "black"},
                ),
            ],
            style={
                "width": "auto",
                "minWidth": "100px",
            },
        ),
        dbc.Col(
            [
                html.H6("Filter Mode"),
                dcc.Dropdown(
                    [GAUSSIAN, CUT],
                    CUT,
                    id="filter-mode",
                    clearable=False,
                    style={"color": "black"},
                ),
            ],
            style={
                "width": "auto",
                "minWidth": "150px",
            },
        ),
        dbc.Col(
            [
                html.H6("Cut-off Frequency"),
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
                        "padding-bottom": "10px",
                    },
                ),
                html.Div(
                    [
                        dbc.Checklist(
                            [
                                {
                                    "label": " Scale Independent",
                                    "value": "scale-independent",
                                }
                            ],
                            value=[],
                            id="is-scale-independent-cf",
                            inline=True,
                        ),
                        dbc.Tooltip(
                            "By default, the mask radius has a fixed pixel size determined by the cutoff frequency."
                            " If set, the mask radius is determined by the cutoff frequency, but scaled with the image size.",
                            target="is-scale-independent-cf",
                            placement="bottom",
                        ),
                    ],
                    style={"textDecoration": "underline", "color": "white"},
                ),
            ],
        ),
    ],
    className="g-0 ms-auto mt-3 mt-md-0",
    # align="center",
    style={
        "justify-content": "space-evenly",
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
        dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        dbc.NavbarBrand("Hybrid Image Playground", className="ms-2"),
                        href="https://github.com/ptrLx/hybrid-image-playground/",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                    dbc.Collapse(
                        __filter_controls,
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True,
                    ),
                ],
            ),
            color="dark",
            sticky="top",
            dark=True,
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
                "paddingTop": "20px",
                "gap": "25px",
                "paddingLeft": "10px",
                "paddingRight": "10px",
            },
        ),
    ],
    style={"textAlign": "center"},
)

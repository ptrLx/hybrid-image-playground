import dash_bootstrap_components as dbc
from dash import dcc, html

# enum of filter modes
CUT = "Circular cut"
GAUSSIAN = "Gaussian"

FILTER_MASKS = [
    CUT,
    GAUSSIAN,
]


def __image_upload(i):
    return html.Div(
        [
            dcc.Loading(
                html.Div(
                    [
                        dcc.Upload(
                            id=f"upload-image-{i}",
                            children=html.A(
                                f"Select Image for {'Low' if i == 1 else 'High'} Frequency Portion",
                                style={
                                    "padding": "10px",
                                    "fontWeight": "bold",
                                    "height": "60px",
                                    "display": "flex",
                                    "justifyContent": "center",
                                    "alignItems": "center",
                                    "textAlign": "center",
                                },
                            ),
                            multiple=False,
                            accept="image/*",
                        ),
                        html.Div(
                            id=f"output-images-{i}",
                        ),
                    ],
                    style={
                        "borderWidth": "5px",
                        "borderStyle": "dashed",
                        "borderRadius": "20px",
                        "boxSizing": "border-box",
                        "display": "flex",
                        "flexDirection": "column",
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
                    FILTER_MASKS,
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
                        html.Div(
                            [
                                html.P("Low Pass"),
                                dcc.Slider(
                                    1,
                                    100,
                                    1,
                                    value=25,
                                    marks=None,
                                    id="cf-slider-lp",
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
                                html.P("High Pass"),
                                dcc.Slider(
                                    1,
                                    100,
                                    1,
                                    value=25,
                                    marks=None,
                                    id="cf-slider-hp",
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
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                    },
                ),
                html.Div(
                    [
                        dbc.Checklist(
                            [
                                {
                                    "label": " Lock Low/High Frequency Cutoff",
                                    "value": "lock-cf",
                                }
                            ],
                            value=["lock-cf"],
                            id="is-locked-cf",
                            inline=True,
                        ),
                        dbc.Tooltip(
                            "Lock the low and high frequency cutoffs to the same value.",
                            target="is-locked-cf",
                            placement="bottom",
                        ),
                    ],
                    style={"textDecoration": "underline", "color": "white"},
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
                            "By default, the mask radius has a fixed pixel size determined by the cutoff frequency (cycle/degree)."
                            " If set, the mask radius is determined by the cutoff frequency, but scaled with the image size (cycle/image).",
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
                            "display": "flex",
                            "flexDirection": "column",
                            "width": "100%",
                        },
                    ),
                    html.Div(
                        id="filter-mask-2",
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "width": "100%",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "flexDirection": "row",
                    "justifyContent": "space-evenly",
                    "gap": "10px",
                },
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
                        dbc.NavbarBrand("Hybrid Image Playground", className="ms-1"),
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
                "padding": "10px",
                "gap": "25px",
            },
        ),
    ],
    style={"textAlign": "center"},
)

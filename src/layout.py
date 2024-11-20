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
        dcc.Loading(
            [
                html.H3("Image Size"),
                dcc.Dropdown(
                    [128, 256, 512, 1024, 2048],
                    256,
                    id="image-size",
                    clearable=False,
                    style={
                        "width": "200px",
                        "justifyContent": "center",
                        "margin": "auto",
                    },
                ),
                html.H3(id="cf-slider-output"),
                html.Div(
                    [
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
                    style={
                        "width": "600px",
                        "justifyContent": "center",
                        "margin": "auto",
                    },
                ),
                html.H3("Filter Mode"),
                dcc.Dropdown(
                    [GAUSSIAN, CUT],
                    CUT,
                    id="filter-mode",
                    clearable=False,
                    style={
                        "width": "200px",
                        "justifyContent": "center",
                        "margin": "auto",
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
                                "margin": "10px",
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
    ],
    style={
        "textAlign": "center",
    },
)

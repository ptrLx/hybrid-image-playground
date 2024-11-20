import base64
import logging

import cv2
import dash
import numpy as np
from dash import dcc, html
from dash.dependencies import Input, Output

from hybrid_image import HybridImage

logger = logging.getLogger(__name__)

hi = HybridImage()


def __get_filter_mode(filter_mode):
    if filter_mode == "Gaussian":
        return hi.GAUSSIAN
    else:
        return hi.CUT


def __decode_image(contents):
    # Split the base64 string
    content_type, content_string = contents.split(",")

    # Decode the base64 string
    decoded = base64.b64decode(content_string)

    return decoded


def __encode_image(image):
    # Encode the image to base64
    _, buffer = cv2.imencode(".png", image)
    output = base64.b64encode(buffer).decode()

    return f"data:image/png;base64,{output}"


def __update_output_images(contents, filter_function, image_size, cf, filter_mode):
    if contents is not None:
        decoded = __decode_image(contents)
        original_image, filter_mask, ft, filtered_center, filtered_image = (
            filter_function(decoded, image_size, __get_filter_mode(filter_mode), cf)
        )
        return html.Div(
            [
                html.Img(
                    src=__encode_image(original_image),
                    style={"width": "30%"},
                ),
                html.Img(
                    src=__encode_image(filtered_image),
                    style={"width": "30%"},
                ),
                html.Img(
                    src=__encode_image(filter_mask),
                    style={"width": "30%"},
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-evenly",
                "margin": "10px",
            },
        )

    return html.Div()


def add_callbacks(app):
    @app.callback(
        Output("output-images-1", "children"),
        [
            Input("upload-image-1", "contents"),
            Input("image-size", "value"),
            Input("cf-slider", "value"),
            Input("filter-mode", "value"),
        ],
    )
    def update_output_images_1(contents, image_size, cf, filter_mode):
        return __update_output_images(
            contents, hi.apply_low_pass_filter, image_size, cf, filter_mode
        )

    @app.callback(
        Output("output-images-2", "children"),
        [
            Input("upload-image-2", "contents"),
            Input("image-size", "value"),
            Input("cf-slider", "value"),
            Input("filter-mode", "value"),
        ],
    )
    def update_output_images_2(contents, image_size, cf, filter_mode):
        return __update_output_images(
            contents, hi.apply_high_pass_filter, image_size, cf, filter_mode
        )

    @app.callback(
        Output("output-image-hybrid", "children"),
        [
            Input("output-images-1", "children"),
            Input("output-images-2", "children"),
            Input("image-size", "value"),
        ],
    )
    def update_output_hybrid(contents1, contents2, image_size):
        if (
            contents1["props"]["children"] is not None
            and contents2["props"]["children"] is not None
        ):
            decoded1 = __decode_image(contents1["props"]["children"][1]["props"]["src"])
            decoded2 = __decode_image(contents2["props"]["children"][1]["props"]["src"])

            image = hi.create_hybrid_image(decoded1, decoded2, image_size)

            return html.Img(
                src=__encode_image(image), style={"width": "45%", "margin": "10px"}
            )
        else:
            return html.Div()

    @app.callback(Output("cf-slider-output", "children"), Input("cf-slider", "value"))
    def update_output(value):
        return f"Cutoff Frequency {value}"

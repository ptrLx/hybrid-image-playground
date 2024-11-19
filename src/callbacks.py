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


def decode_and_process_image(contents, process_func, image_size, cf=None):
    # Split the base64 string
    content_type, content_string = contents.split(",")

    # Decode the base64 string
    decoded = base64.b64decode(content_string)

    if cf is not None:
        image = process_func(decoded, image_size, cf=cf)
    else:
        image = process_func(decoded, image_size)

    # Encode the image to base64
    _, buffer = cv2.imencode(".png", image)
    output = base64.b64encode(buffer).decode()

    return html.Img(
        src=f"data:image/png;base64,{output}", style={"width": "45%", "margin": "10px"}
    )


def decode_and_create_hi(contents1, contents2, image_size):
    # Split the base64 string
    content_type1, content_string1 = contents1.split(",")
    content_type2, content_string2 = contents2.split(",")

    # Decode the base64 string
    decoded1 = base64.b64decode(content_string1)
    decoded2 = base64.b64decode(content_string2)

    image = hi.create_hybrid_image(decoded1, decoded2, image_size)

    # Encode the image to base64
    _, buffer = cv2.imencode(".png", image)
    output = base64.b64encode(buffer).decode()

    return html.Img(
        src=f"data:image/png;base64,{output}", style={"width": "45%", "margin": "10px"}
    )


def add_callbacks(app):
    @app.callback(
        Output("output-image-upload-1", "children"),
        [Input("upload-image-1", "contents"), Input("image-size", "value")],
    )
    def update_output_1(contents, image_size):
        if contents is not None:
            return decode_and_process_image(
                contents, hi.create_image_preview, image_size
            )
        return html.Div()

    @app.callback(
        Output("output-image-upload-1-filtered", "children"),
        [
            Input("upload-image-1", "contents"),
            Input("image-size", "value"),
            Input("cf-slider", "value"),
        ],
    )
    def update_output_1_filtered(contents, image_size, cf):
        if contents is not None:
            return decode_and_process_image(
                contents, hi.apply_low_pass_filter, image_size, cf
            )
        return html.Div()

    @app.callback(
        Output("output-image-upload-2", "children"),
        [Input("upload-image-2", "contents"), Input("image-size", "value")],
    )
    def update_output_2(contents, image_size):
        if contents is not None:
            return decode_and_process_image(
                contents, hi.create_image_preview, image_size
            )
        return html.Div()

    @app.callback(
        Output("output-image-upload-2-filtered", "children"),
        [
            Input("upload-image-2", "contents"),
            Input("image-size", "value"),
            Input("cf-slider", "value"),
        ],
    )
    def update_output_2_filtered(contents, image_size, cf):
        if contents is not None:
            return decode_and_process_image(
                contents, hi.apply_high_pass_filter, image_size, cf
            )
        return html.Div()

    @app.callback(
        Output("output-image-hybrid", "children"),
        [
            Input("output-image-upload-1-filtered", "children"),
            Input("image-size", "value"),
            Input("output-image-upload-2-filtered", "children"),
        ],
    )
    def update_output_hybrid(contents1, image_size, contents2):
        if contents1.get("type") == "Img" and contents2.get("type") == "Img":
            return decode_and_create_hi(
                contents1["props"]["src"], contents2["props"]["src"], image_size
            )
        else:
            return html.Div()

    @app.callback(Output("cf-slider-output", "children"), Input("cf-slider", "value"))
    def update_output(value):
        return f"Cutoff Frequency {value}"

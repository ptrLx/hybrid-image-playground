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


def decode_and_process_image(contents, process_func):
    # Split the base64 string
    content_type, content_string = contents.split(",")

    # Decode the base64 string
    decoded = base64.b64decode(content_string)

    image = process_func(decoded)

    # Encode the image to base64
    _, buffer = cv2.imencode(".png", image)
    output = base64.b64encode(buffer).decode()

    return html.Img(
        src=f"data:image/png;base64,{output}", style={"width": "45%", "margin": "10px"}
    )


def decode_and_create_hi(contents1, contents2):
    # Split the base64 string
    content_type1, content_string1 = contents1.split(",")
    content_type2, content_string2 = contents2.split(",")

    # Decode the base64 string
    decoded1 = base64.b64decode(content_string1)
    decoded2 = base64.b64decode(content_string2)

    image = hi.create_hybrid_image(decoded1, decoded2)

    # Encode the image to base64
    _, buffer = cv2.imencode(".png", image)
    output = base64.b64encode(buffer).decode()

    return html.Img(
        src=f"data:image/png;base64,{output}", style={"width": "45%", "margin": "10px"}
    )


def add_callbacks(app):
    @app.callback(
        Output("output-image-upload-1", "children"),
        Input("upload-image-1", "contents"),
    )
    def update_output_1(contents):
        if contents is not None:
            return decode_and_process_image(contents, hi.create_image_preview)
        return html.Div()

    @app.callback(
        Output("output-image-upload-1-filtered", "children"),
        Input("upload-image-1", "contents"),
    )
    def update_output_1_filtered(contents):
        if contents is not None:
            return decode_and_process_image(contents, hi.apply_low_pass_filter)
        return html.Div()

    @app.callback(
        Output("output-image-upload-2", "children"),
        Input("upload-image-2", "contents"),
    )
    def update_output_2(contents):
        if contents is not None:
            return decode_and_process_image(contents, hi.create_image_preview)
        return html.Div()

    @app.callback(
        Output("output-image-upload-2-filtered", "children"),
        Input("upload-image-2", "contents"),
    )
    def update_output_2_filtered(contents):
        if contents is not None:
            return decode_and_process_image(contents, hi.apply_high_pass_filter)
        return html.Div()

    @app.callback(
        Output("output-image-hybrid", "children"),
        [
            Input("output-image-upload-1-filtered", "children"),
            Input("output-image-upload-2-filtered", "children"),
        ],
    )
    def update_output_hybrid(contents1, contents2):
        if contents1.get("type") == "Img" and contents2.get("type") == "Img":
            return decode_and_create_hi(
                contents1["props"]["src"], contents2["props"]["src"]
            )
        else:
            return html.Div()

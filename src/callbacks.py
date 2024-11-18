import base64
import logging

import cv2
import dash
import numpy as np
from dash import dcc, html
from dash.dependencies import Input, Output

logger = logging.getLogger(__name__)

size = 256


def create_image_preview(contents):
    # Split the base64 string
    content_type, content_string = contents.split(",")

    # Decode the base64 string
    decoded = base64.b64decode(content_string)

    # Convert the bytes to a NumPy array
    np_arr = np.frombuffer(decoded, np.uint8)

    # Decode the NumPy array to an image
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (size, size))

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
            return create_image_preview(contents)
        return html.Div()

    @app.callback(
        Output("output-image-upload-2", "children"),
        Input("upload-image-2", "contents"),
    )
    def update_output_2(contents):
        if contents is not None:
            return create_image_preview(contents)
        return html.Div()

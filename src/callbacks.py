import base64
import logging

import cv2
from dash import html
from dash.dependencies import Input, Output, State

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


def __update_output_images(
    contents, image_size, cf, is_scale_independent_cf, filter_mode, use_high_pass=False
):
    if contents is not None:
        filter_function = (
            hi.apply_high_pass_filter if use_high_pass else hi.apply_low_pass_filter
        )

        decoded = __decode_image(contents)
        original_image_bw, filter_mask, ft, filtered_center, filtered_image = (
            filter_function(
                decoded,
                image_size,
                __get_filter_mode(filter_mode),
                cf,
                is_scale_independent_cf,
            )
        )

        filter_mask *= 255  # scale up the mask to 255 grayscale values

        # Scale Fourier Transform brightness down
        filtered_center /= 512

        # * Instead of scaling the brightness of the Fourier Transform, we can set the values bigger than 2048 to 2048
        # # Use numpy to set values bigger than 2048 to 2048 in filtered_center (for visualization of the filtered Fourier Transform)
        # filtered_center[filtered_center > 2047] = 2047
        # # Rescale the filtered_center to 0-255
        # filtered_center = cv2.normalize(filtered_center, None, 0, 255, cv2.NORM_MINMAX)
        # # filtered_center /= 8  # scale down the filtered_center to 0-255 grayscale values

        return (
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=__encode_image(original_image_bw),
                                style={"width": "100%"},
                            ),
                            html.P("Scaled Image (black & white)"),
                        ],
                        style={"width": "100%"},
                    ),
                    html.Div(
                        [
                            html.Img(
                                src=__encode_image(filtered_center),
                                style={"width": "100%"},
                            ),
                            html.P("Filtered FT"),
                        ],
                        style={"width": "100%"},
                    ),
                    html.Div(
                        [
                            html.Img(
                                src=__encode_image(filtered_image),
                                style={"width": "100%"},
                            ),
                            html.P("Filtered Image"),
                        ],
                        style={"width": "100%"},
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "10px",
                    "width": "100%",
                    "padding": "10px",
                },
            ),
            html.Div(
                [
                    html.Img(
                        src=__encode_image(filter_mask),
                        style={"width": "100%"},
                    ),
                    html.P(f"{'High' if use_high_pass else 'Low'} Pass Filter Mask"),
                ],
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "width": "100%",
                },
            ),
        )

    return html.Div(), html.Div()


def add_callbacks(app):
    @app.callback(
        [Output("output-images-1", "children"), Output("filter-mask-1", "children")],
        [
            Input("upload-image-1", "contents"),
            Input("image-size", "value"),
            Input("cf-slider-lp", "value"),
            Input("is-scale-independent-cf", "value"),
            Input("filter-mode", "value"),
        ],
    )
    def update_output_images_1(
        contents, image_size, cf, is_scale_independent_cf_arr, filter_mode
    ):
        is_scale_independent_cf = "scale-independent" in is_scale_independent_cf_arr
        return __update_output_images(
            contents,
            image_size,
            cf,
            is_scale_independent_cf,
            filter_mode,
        )

    @app.callback(
        [Output("output-images-2", "children"), Output("filter-mask-2", "children")],
        [
            Input("upload-image-2", "contents"),
            Input("image-size", "value"),
            Input("cf-slider-hp", "value"),
            Input("is-scale-independent-cf", "value"),
            Input("filter-mode", "value"),
        ],
    )
    def update_output_images_2(
        contents, image_size, cf, is_scale_independent_cf_arr, filter_mode
    ):
        is_scale_independent_cf = "scale-independent" in is_scale_independent_cf_arr
        return __update_output_images(
            contents,
            image_size,
            cf,
            is_scale_independent_cf,
            filter_mode,
            use_high_pass=True,
        )

    @app.callback(
        Output("output-image-hybrid", "children"),
        [
            Input("output-images-1", "children"),
            Input("output-images-2", "children"),
            Input("image-size", "value"),
        ],
    )
    def update_output_hybrid(output_images1, output_images2, image_size):
        if output_images1 is None or output_images2 is None:
            return html.Div()

        children1 = output_images1.get("props").get("children")
        children2 = output_images2.get("props").get("children")

        if children1 is None or children2 is None:
            return html.Div()

        decoded1 = __decode_image(children1[2]["props"]["children"][0]["props"]["src"])
        decoded2 = __decode_image(children2[2]["props"]["children"][0]["props"]["src"])

        image = hi.create_hybrid_image(decoded1, decoded2, image_size)

        return html.Img(src=__encode_image(image), style={"width": "100%"})

    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        [Output("cf-slider-hp", "value"), Output("cf-slider-hp", "disabled")],
        [
            Input("cf-slider-lp", "value"),
            Input("cf-slider-hp", "value"),
            Input("is-locked-cf", "value"),
        ],
    )
    def update_cf_slider_hp(cf_lp, cf_hp, is_locked_cf_arr):
        is_locked = "lock-cf" in is_locked_cf_arr
        return (cf_lp if is_locked else cf_hp), is_locked

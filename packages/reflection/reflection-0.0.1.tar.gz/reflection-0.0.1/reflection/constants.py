__all__ = []

ALIGNMENTS = {
    "left",
    "right",
    "center"
}
ANCHORS = {
    "top": "n",
    "bottom": "s",
    "left": "w",
    "right": "e",
    "fill": ""
}
BUFFER_SIZE = 4096
BUTTON_OPTIONS = {
    "background": "background",
    "foreground": "foreground",
    "align": "justify"
}
COLORS = {
    "white": "#ffffff",
    "black": "#000000",
    "red": "#ff0000",
    "green": "#00ff00",
    "blue": "#0000ff",
    "yellow": "#ffff00",
    "orange": "#f87217",
    "grey": "#808080",
    "gray": "#808080",
    "pink": "#ee1289",
    "purple": "#9400d3",
}
ENTRY_OPTIONS = {
    "background": "background",
    "foreground": "foreground",
    "align": "justify"
}
FRAME_OPTIONS = {
    "background": "background",
}
HEX_COLOR = "#([0-9a-f]{3}){1,3}"
NAMED_STYLES = {
    "night": {
        "background": "#141414",
        "foreground": "#f8f8f8"
    },
}
STATES = {
    "enabled": "normal",
    "disabled": "disabled",
    "readonly": "readonly"
}
TEXT_OPTIONS = {
    "background": "background",
    "foreground": "foreground",
    "align": "justify"
}
WINDOW_OPTIONS = {
    "background": "background",
}


ANCHOR_NOT_STR = "anchor must be a 'str' object"
ANCHOR_REPEATED = "repeated alignment argument: {}"
ANCHOR_CONFLICT = "{} alignment argument conflicts with {}"
ANCHOR_FILL_COMBINED = "\
'fill' can't be used in combination with other alignment arguments"
ANCHOR_UNKNOWN = "anchor must be any of {}".format(
    str(list(ANCHORS.keys()))[1:-1]
)

GENERIC_NOT_INTEGER = "{} must be an 'int' object"
GENERIC_NOT_POSITIVE = "{} must be a positive integer"

PARENT_WRONG_TYPE = "\
parent must derive from 'Widget' or be a 'Window' instance"

COLOR_NOT_STRING = "color must be a 'str' object"
COLOR_UNKNOWN = "color must be any of {} or be a hex color code".format(
    str(list(COLORS.keys()))[1:-1]
)

IMAGE_NOT_STRING = "image must be a 'str' object"
IMAGE_NOT_FILE = "image path does not exist or is not a file"

VALUE_NOT_STRING = "value must be a 'str' object"

STYLE_WRONG_TYPE = "style must be a 'style.Style' object"

ALIGN_NOT_STRING = "align must be a 'str' object"
ALIGN_UNKNOWN = "align must be any of {}".format(
    str(ALIGNMENTS)[1:-1]
)

STATE_NOT_STRING = "state must be a 'str' object"
STATE_UNKNOWN = "state must be any of {}".format(
    str(list(STATES.keys()))[1:-1]
)

TITLE_NOT_STRING = "title must be a 'str' object"

APPLICATION_NOT_EXISTS = "can't invoke {}, no 'Application' instance exists"
APPLICATION_ALREADY_EXISTS = "\
can't create this widget, an 'Application' instance already exists"
WIDGET_DESTROYED = "can't invoke {}, widget has been destroyed"
WIDGET_ALREADY_DESTROYED = "\
can't destroy this widget, widget has already been destroyed"

IMAGE_STREAM_FAILED = "failed to stream image from URL"
IMAGE_BUFFER_FAILED = "failed to load image into memory"

STYLE_OPTION_UNKNOWN = "styling for this widget must be any of {}"
STYLE_NAME_UNKNOWN = "style name must be any of {} or be None".format(
    str(list(NAMED_STYLES.keys()))[1:-1]
)

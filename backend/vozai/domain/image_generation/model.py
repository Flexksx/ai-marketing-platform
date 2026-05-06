from enum import StrEnum

import public


@public.add
class ImageAspectRatio(StrEnum):
    SQUARE = "1:1"
    PORTRAIT_4_5 = "4:5"
    PORTRAIT_3_4 = "3:4"
    PORTRAIT_2_3 = "2:3"
    PORTRAIT_9_16 = "9:16"
    LANDSCAPE_16_9 = "16:9"
    LANDSCAPE_4_3 = "4:3"
    LANDSCAPE_3_2 = "3:2"
    LANDSCAPE_5_4 = "5:4"
    LANDSCAPE_21_9 = "21:9"


@public.add
class ImageResolution(StrEnum):
    STANDARD = "1K"
    HIGH = "2K"

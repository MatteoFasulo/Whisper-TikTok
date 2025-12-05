def rgb_to_bgr(rgb: str) -> str:
    """Convert RGB hex to BGR hex."""
    if rgb.startswith("#"):
        rgb = rgb[1:]
    r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
    return b + g + r

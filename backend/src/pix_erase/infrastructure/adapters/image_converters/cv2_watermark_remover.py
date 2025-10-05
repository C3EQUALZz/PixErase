# Helper function to check if a pixel is within a wider black color range in RGB
def is_text_color_rgb(img_array):
    # Widen the range to accommodate thinner or lighter black text
    mask = (
        # Descent WaterMark Preset
        # (img_array[:, :, 0] < 130) &  # Red channel threshold increased
        # (img_array[:, :, 1] < 200) &  # Green channel threshold increased
        # (img_array[:, :, 2] < 200)    # Blue channel threshold increased
        # 25, 190
        # # BrownishGreen WaterMark
        #   (img_array[:, :, 0] < 60) &  # Red channel threshold increased
        #   (img_array[:, :, 1] < 115) &  # Green channel threshold increased
        #   (img_array[:, :, 2] < 200)    # Blue channel threshold increased
        # 30,210
        # # Blue JB WaterMark
        # (img_array[:, :, 0] < 200) &  # Red channel threshold increased
        # (img_array[:, :, 1] < 200) &  # Green channel threshold increased
        # (img_array[:, :, 2] < 175)    # Blue channel threshold increased
        # # 0,250
        # # BADIMAGE WaterMark WITH RED WATERMARK
        # (img_array[:, :, 0] < 175) &  # Red channel threshold increased
        # (img_array[:, :, 1] < 200) &  # Green channel threshold increased
        # (img_array[:, :, 2] < 200)    # Blue channel threshold increased

        # GreenishGreen WaterMark
        # (img_array[:, :, 0] < 120) &  # Red channel threshold increased
        # (img_array[:, :, 1] < 120) &  # Green channel threshold increased
        # (img_array[:, :, 2] < 120)    # Blue channel threshold increased

        # QR CODE
        # (img_array[:, :, 0] < 150) &  # Red channel threshold increased
        # (img_array[:, :, 1] < 150) &  # Green channel threshold increased
        # (img_array[:, :, 2] < 150)    # Blue channel threshold increased
        # # 0,180

        # # Prod
            (img_array[:, :, 0] < 130) &  # Red channel threshold increased
            (img_array[:, :, 1] < 200) &  # Green channel threshold increased
            (img_array[:, :, 2] < 200)  # Blue channel threshold increased

    )
    return mask

class Cv2WatermarkRemover:
    def __init__(self) -> None:
        ...

    def convert(self, data: bytes) -> bytes:
        ...

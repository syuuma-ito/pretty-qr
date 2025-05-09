from typing import Literal, Union

from PIL import Image, ImageDraw

from .utils import get_finder_pattern_location, get_qr_matrix, is_finder_pattern


def create_rounded_qr(
    data: str,
    version: Union[None, int] = None,
    error_correction: Literal["L", "M", "Q", "H"] = "L",
    box_size: int = 20,
    border: int = 4,
    #
    fill_color: str = "black",
    back_color: str = "white",
    finder_color: str = "black",
    finder_radius: float = 1,
) -> Image.Image:
    """
    角丸のQRコード画像を生成する関数

    Args:
        data (str): QRにするデータ
        version (Union[None, int], optional): QRコードバージョン. Defaults to None.
        error_correction (Literal[&quot;L&quot;, &quot;M&quot;, &quot;Q&quot;, &quot;H&quot;], optional): 誤り補正レベル. Defaults to "L".
        box_size (int, optional): 1ドットの大きさ. Defaults to 20.
        border (int, optional): 余白のドット数. Defaults to 4.

        fill_color (Union[str, list[str]], optional): QRコードの色. Defaults to "black".
        back_color (str, optional): QRコードの背景色. Defaults to "white".
        finder_color (str, optional): ファインダーパターンの色. Defaults to "black".
        finder_radius (float, optional): ファインダーパターンの角丸半径. Defaults to 1.

    Returns:
        PIL.Image.Image: 生成されたQRコード画像オブジェクト。
    """
    matrix = get_qr_matrix(
        data,
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )

    qr_size = len(matrix)
    img_size = qr_size * box_size
    radius = int(box_size / 2)

    image = Image.new("RGBA", (img_size, img_size), back_color)
    draw = ImageDraw.Draw(image)

    for r in range(qr_size):
        for c in range(qr_size):
            if not matrix[r][c]:
                continue

            if is_finder_pattern(r, c, border, qr_size):
                continue

            x0 = c * box_size
            y0 = r * box_size
            x1 = x0 + box_size
            y1 = y0 + box_size

            neighbors = {
                "top": matrix[r - 1][c] if r > 0 else False,
                "bottom": matrix[r + 1][c] if r < qr_size - 1 else False,
                "left": matrix[r][c - 1] if c > 0 else False,
                "right": matrix[r][c + 1] if c < qr_size - 1 else False,
            }

            draw.ellipse([x0, y0, x1, y1], fill=fill_color, outline=fill_color)

            if neighbors["top"]:
                draw.rectangle([x0, y0, x1, y0 + radius], fill=fill_color)
            if neighbors["bottom"]:
                draw.rectangle([x0, y1 - radius, x1, y1], fill=fill_color)
            if neighbors["left"]:
                draw.rectangle([x0, y0, x0 + radius, y1], fill=fill_color)
            if neighbors["right"]:
                draw.rectangle([x1 - radius, y0, x1, y1], fill=fill_color)

    # 角丸のファインダーパターンを描画
    finder_patterns = get_finder_pattern_location(border, qr_size)
    for pattern in finder_patterns:
        draw.rounded_rectangle(
            [x * box_size for x in pattern],
            fill=finder_color,
            radius=(box_size * finder_radius * 2),
        )
        draw.rounded_rectangle(
            [
                (pattern[0] + 1) * box_size,
                (pattern[1] + 1) * box_size,
                (pattern[2] - 1) * box_size,
                (pattern[3] - 1) * box_size,
            ],
            fill=back_color,
            radius=(box_size * finder_radius),
        )
        draw.rounded_rectangle(
            [
                (pattern[0] + 2) * box_size,
                (pattern[1] + 2) * box_size,
                (pattern[2] - 2) * box_size,
                (pattern[3] - 2) * box_size,
            ],
            fill=finder_color,
            radius=(box_size * finder_radius),
        )

    return image

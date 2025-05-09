import random
from typing import Literal, Union

from PIL import Image, ImageDraw

from .utils import get_finder_pattern_location, get_qr_matrix, is_finder_pattern


def create_dot_qr(
    data: str,
    version: Union[None, int] = None,
    error_correction: Literal["L", "M", "Q", "H"] = "L",
    box_size: int = 20,
    border: int = 4,
    #
    fill_color: Union[str, list[str]] = "black",
    back_color: str = "white",
    finder_color: str = "black",
    finder_radius: float = 1.0,
    #
    dot_radius: float = 1.0,
    dot_size: Union[float, list[float]] = 0.8,
) -> Image.Image:
    """ドットのQRコードを生成する関数

    Args:
        data (str): QRにするデータ
        version (Union[None, int], optional): QRコードバージョン. Defaults to None.
        error_correction (Literal[&quot;L&quot;, &quot;M&quot;, &quot;Q&quot;, &quot;H&quot;], optional): 誤り補正レベル. Defaults to "L".
        box_size (int, optional): 1ドットの大きさ. Defaults to 20.
        border (int, optional): 余白のドット数. Defaults to 4.

        fill_color (Union[str, list[str]], optional): QRコードの色.リストの場合は、それぞれのドットについてランダムで選ばれます. Defaults to "black".
        back_color (str, optional): QRコードの背景色. Defaults to "white".
        finder_color (str, optional): ファインダーパターンの色. Defaults to "black".
        finder_radius (float, optional): ファインダーパターンの角丸半径. Defaults to 1.

        dot_radius (float, optional): 角丸にする比率(0.0～1.0) 1.0で完全な円、0.0で四角. Defaults to 1.0.
        dot_size (Union[float, list[float]], optional): 1ドットの大きさの比率.リストの場合は、それぞれのドットについてランダムで選ばれます. Defaults to 0.8.

    Returns:
        PIL.Image.Image: 生成されたQRコード画像オブジェクト。
    """

    if isinstance(dot_size, float):
        dot_size = [dot_size]
    elif isinstance(dot_size, list):
        pass
    else:
        raise ValueError("dot_size must be a float or a list of floats.")

    for i in dot_size:
        if not isinstance(i, float):
            raise ValueError("dot_size must be a float or a list of floats.")
        if i < 0 or i > 1:
            raise ValueError("dot_size must be between 0 and 1.")

    if isinstance(fill_color, str):
        fill_color = [fill_color]
    elif isinstance(fill_color, list):
        pass
    else:
        raise ValueError("fill_color must be a string or a list of strings.")

    for i in fill_color:
        if not isinstance(i, str):
            raise ValueError("fill_color must be a string or a list of strings.")

    matrix = get_qr_matrix(
        data,
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )

    qr_size = len(matrix)
    img_size = qr_size * box_size

    image = Image.new("RGBA", (img_size, img_size), back_color)
    draw = ImageDraw.Draw(image)

    for r in range(qr_size):
        for c in range(qr_size):
            if not matrix[r][c]:
                continue
            if is_finder_pattern(r, c, border, qr_size):
                continue

            dot_size_ = random.choice(dot_size)
            fill_color_ = random.choice(fill_color)

            x0 = c * box_size
            y0 = r * box_size
            x1 = x0 + box_size
            y1 = y0 + box_size

            draw.rounded_rectangle(
                [
                    x0 + box_size * (1 - dot_size_) / 2,
                    y0 + box_size * (1 - dot_size_) / 2,
                    x1 - box_size * (1 - dot_size_) / 2,
                    y1 - box_size * (1 - dot_size_) / 2,
                ],
                fill=fill_color_,
                radius=(box_size * dot_radius / 2),
            )

    # ファインダーパターンを描画
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

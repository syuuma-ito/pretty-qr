from typing import Literal

import qrcode

error_correction_level = {
    "L": qrcode.constants.ERROR_CORRECT_L,
    "M": qrcode.constants.ERROR_CORRECT_M,
    "Q": qrcode.constants.ERROR_CORRECT_Q,
    "H": qrcode.constants.ERROR_CORRECT_H,
}


def get_finder_pattern_location(border: int, qr_size: int) -> tuple[int, int, int, int]:
    """QRコードのファインダーパターンの位置を取得する関数

    Args:
        border (int): 余白のドット数。
        qr_size (int): QRコードのサイズ。

    Returns:
        tuple[int, int, int, int]: ファインダーパターンの位置。
    """
    finder_patterns = [
        (
            border,
            border,
            border + 7,
            border + 7,
        ),
        (
            border,
            (qr_size - border - 7),
            border + 7,
            qr_size - border,
        ),
        (
            (qr_size - border - 7),
            border,
            qr_size - border,
            border + 7,
        ),
    ]
    return finder_patterns


def is_finder_pattern(x: int, y: int, border: int, qr_size: int) -> bool:
    """指定した座標がファインダーパターンの位置にあるかどうかを判定する関数

    Args:
        x (int): 判定するx座標。
        y (int): 判定するy座標。
        border (int): 余白のドット数。
        qr_size (int): QRコードのサイズ。

    Returns:
        bool: ファインダーパターンの位置にあるかどうか
    """
    finder_patterns = get_finder_pattern_location(border, qr_size)

    for pattern in finder_patterns:
        if pattern[0] <= x < pattern[2] and pattern[1] <= y < pattern[3]:
            return True

    return False


def get_qr_matrix(
    data,
    version=None,
    error_correction: Literal["L", "M", "Q", "H"] = "L",
    box_size=10,
    border=4,
) -> list[list[bool]]:
    """
    QRコードのマトリックスを取得する関数

    Args:
        data (str): QRコードにするデータ。
        version (int): QRコードのバージョン。
        error_correction (str): エラー訂正レベル。"L", "M", "Q", "H"のいずれか。
        box_size (int): 1ドットあたりのピクセルサイズ。
        border (int): QRコード周囲の余白（ドット数）。

    Returns:
        list[list[bool]]: QRコードのマトリックス。
    """

    error_correction = error_correction_level.get(error_correction)
    if error_correction is None:
        raise ValueError(f"{error_correction} は無効なエラー訂正レベルです。")

    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.get_matrix()

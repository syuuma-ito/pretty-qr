from prettyqr.dot_qr import create_dot_qr
from prettyqr.normal_qr import create_qr
from prettyqr.rounded_qr import create_rounded_qr


def main():
    data = "https://example.com"
    error_correction = "L"
    box_size = 20
    border = 4

    normal_qr_image = create_qr(
        data,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
        fill_color="black",
        back_color="white",
        finder_color="black",
    )
    normal_qr_image.save("examples/normal_qr_code.png")

    rounded_qr_image = create_rounded_qr(
        data,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
        fill_color="black",
        back_color="white",
        finder_color="black",
    )
    rounded_qr_image.save("examples/rounded_qr_code.png")

    dot_qr_image = create_dot_qr(
        data,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
        dot_size=[0.7, 0.8, 0.9],
        fill_color=["#000", "#111", "#222"],
        back_color="white",
        finder_color="black",
    )
    dot_qr_image.save("examples/dot_qr_code.png")

    square_qr_image = create_dot_qr(
        data,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
        dot_size=[0.7, 0.8, 0.9],
        dot_radius=0,
        fill_color=["#000", "#111", "#222"],
        back_color="white",
        finder_color="black",
        finder_radius=0,
    )
    square_qr_image.save("examples/square_qr_code.png")


if __name__ == "__main__":
    main()

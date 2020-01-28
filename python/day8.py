import unittest

BLACK = 0
WHITE = 1
TRANSPARENT = 2


def parse(image_str):
    return list(map(int, image_str))


def chunks(L, n):
    """Yield successive n-sized chunks from L."""
    for i in range(0, len(L), n):
        yield L[i : i + n]


def checksum(digits, width=25, height=6):
    length = len(digits)
    layer_size = width * height
    num_layers = length // layer_size

    layers = []

    min_zeroes = layer_size
    l_with_min_zeroes = None

    for i, L in enumerate(chunks(digits, layer_size)):
        layers.append(L)
        assert len(L) == layer_size

        n_zeroes = L.count(BLACK)
        if n_zeroes < min_zeroes:
            min_zeroes = n_zeroes
            l_with_min_zeroes = i

    assert len(layers) == num_layers
    num_ones = layers[l_with_min_zeroes].count(WHITE)
    num_twos = layers[l_with_min_zeroes].count(TRANSPARENT)

    return num_ones * num_twos


def decode(digits, width=25, height=6):
    length = len(digits)
    layer_size = width * height
    num_layers = length // layer_size

    layers = []

    for i, L in enumerate(chunks(digits, layer_size)):
        layers.append(L)
        assert len(L) == layer_size

    final_layer = []
    for i in range(layer_size):
        pixel_stack = [layers[x][i] for x in range(num_layers)]

        final_pixel = None
        for p in pixel_stack:
            if p in [BLACK, WHITE]:
                final_pixel = p
                break
        else:
            final_pixel = TRANSPARENT
        final_layer.append(final_pixel)

    return final_layer


def print_image(digits, width=25, height=6, color=None):
    assert len(digits) == width * height
    for i, d in enumerate(digits):
        if color is not None:
            d = f"{d}{d}" if d == color else "  "
        end = "\n" if (i + 1) % width == 0 else ""
        print(d, end=end)


if __name__ == "__main__":
    unittest.main(exit=False)

    with open("../inputs/day8.input") as f:
        image_str = f.readline().strip()

    # Part I
    print(checksum(parse(image_str)))

    # Part II
    final_layer = decode(parse(image_str))
    print_image(final_layer)
    print_image(final_layer, color=BLACK)
    print_image(final_layer, color=WHITE)

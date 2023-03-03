example1 = "FOV27"


def h5name(h5name: str) -> str:
    index = h5name.removeprefix("FOV")
    return index

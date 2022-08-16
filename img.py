import requests
import cv2
import numpy
import asyncio
import time


def get_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    }


def to_hex(color, bgr=False):
    if bgr:
        return (
            "{:02x}".format(color[2])
            + "{:02x}".format(color[1])
            + "{:02x}".format(color[0])
        )
    else:
        return (
            "{:02x}".format(color[0])
            + "{:02x}".format(color[1])
            + "{:02x}".format(color[2])
        )


def send(params):
    response = requests.get(
        "https://r-paint.herokuapp.com/draw", headers=get_headers(), params=params
    )


resp = requests.get("https://r-paint.herokuapp.com/getimg", stream=True).raw
image = numpy.asarray(bytearray(resp.read()), dtype="uint8")
image_array = cv2.imdecode(image, cv2.IMREAD_COLOR)

img = cv2.imread("assets/img.jpg")
height = img.shape[0]
width = img.shape[1]


params = {
    "x": -1,
    "y": -1,
    "col": "000000",
}

for y in range(0, height, 4):
    params["x"] = -1
    params["y"] += 1

    for x in range(0, width, 4):
        params["x"] += 1
        imgBox = img[y, x]
        params["col"] = to_hex([int(imgBox[2]), int(imgBox[1]), int(imgBox[0])])
        if to_hex(image_array[params["y"], params["x"], :], True) != params["col"]:
            print(
                "replace: "
                + str(params["x"])
                + ","
                + str(params["y"])
                + " "
                + to_hex(image_array[params["y"], params["x"], :], True)
                + " "
                + params["col"]
            )
            asyncio.new_event_loop().run_in_executor(None, send, params)
            time.sleep(0.1)

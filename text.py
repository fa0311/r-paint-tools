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


# https://lazesoftware.com/tool/hugeaagen/
with open("assets/text.txt", "r") as f:
    text = f.read()


resp = requests.get("https://r-paint.herokuapp.com/getimg", stream=True).raw
image = numpy.asarray(bytearray(resp.read()), dtype="uint8")
image_array = cv2.imdecode(image, cv2.IMREAD_COLOR)

params = {
    "x": -1,
    "y": -1,
    "col": "000000",
}

for index in range(len(text)):

    if text[index] == "\n":
        params["y"] += 1
        params["x"] = 0
        continue

    if text[index] == " ":
        params["x"] += 1
        params["col"] = "000000"

    if text[index] == "■":
        params["x"] += 1
        params["col"] = "00ff00"

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

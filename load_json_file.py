import json

if __name__ == "__main__":
    with open("assets/elements.json") as elements_file:
        elements = json.load(elements_file)
        with open("assets/elements_rgb.json") as rgb_file:
            rgb_data = json.load(rgb_file)
            for symbol, rgb_code in rgb_data.items():
                for element in elements["elements"]:
                    if element["symbol"] == symbol:
                        element.pop("discovered_by")
                        element.pop("named_by")
                        element.pop("source")
                        element.pop("spectral_img")
                        element.pop("summary")
                        element.pop("xpos")
                        element.pop("ypos")
                        element["rgb"] = rgb_code["rgb"]
                        break
    with open("assets/result.json", "w") as result:
        string = json.dumps(elements, indent=4, sort_keys=True)
        result.write(string)


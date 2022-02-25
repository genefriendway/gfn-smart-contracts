import json


def read_json(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)


def write_json(file_path, data):
    # Serializing json
    json_object = json.dumps(data, indent=4)

    # Writing to sample.json
    with open(file_path, "w") as outfile:
        outfile.write(json_object)

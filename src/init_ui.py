def init(data, state):
    data["started"] = False
    data["finished"] = False
    data["tree"] = False
    data["connecting"] = False

    state["pathToVideos"] = "/video_from_images"

    state["selected"] = ""

    state["resultingProjectName"] = "my_project"

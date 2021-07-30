
def init_context(data, team_id, workspace_id):
    data["teamId"] = team_id
    data["workspaceId"] = workspace_id


def init(data, state):
    data["started"] = False
    data["finished"] = False
    data["tree"] = False
    data["connecting"] = False

    state["pathToVideos"] = "/video_from_images"

    state["selected"] = ""
    state["checked"] = True

    state["resultingProjectName"] = "my_project"

    state["dstProjectMode"] = "newProject"
    state["dstDatasetMode"] = "newDataset"
    state["dstProjectId"] = None
    state["selectedDatasetName"] = None
    state["dstProjectName"] = "my_project"


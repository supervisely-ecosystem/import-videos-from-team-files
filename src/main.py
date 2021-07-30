import os
import globals as g
import supervisely_lib as sly
import init_ui, init_ui_progress
from supervisely_lib.io.fs import get_file_name_with_ext, get_file_ext, get_file_name
import moviepy.editor as moviepy
from supervisely_lib.video.video import is_valid_ext, ALLOWED_VIDEO_EXTENSIONS


team_id = int(os.environ['context.teamId'])
workspace_id = int(os.environ['context.workspaceId'])


@g.my_app.callback("preview")
@sly.timeit
def preview(api: sly.Api, task_id, context, state, app_logger):
    global file_size
    file_size = {}

    path = state["pathToVideos"]
    try:
        files = api.file.list2(g.TEAM_ID, path)
    except Exception as e:
        g.my_app.show_modal_window("Can not find bucket or permission denied. Please, check if provider / bucket name are "
                              "correct or contact tech support", level="warning")
        fields = [
            {"field": "data.tree", "payload": None},
            {"field": "data.connecting", "payload": False},
        ]
        api.task.set_fields(task_id, fields)
        return

    tree_items = []
    for file in files:
        path = os.path.join(state["pathToVideos"], file.name)
        tree_items.append({
            "path": path,
            "size": file.sizeb
        })
        file_size[path] = file.sizeb

    fields = [
        {"field": "data.tree", "payload": tree_items},
        {"field": "data.connecting", "payload": False},
        {"field": "data.started", "payload": False},
    ]
    api.task.set_fields(task_id, fields)


@g.my_app.callback("import_videos")
@sly.timeit
def render_video_from_images(api: sly.Api, task_id, context, state, app_logger):

    team_id = state["teamId"]
    workspace_id = state["workspaceId"]
    project_name = state["resultingProjectName"]

    videos_pathes = state["selected"]
    #=============================================================================================================


    project = None
    if state["dstProjectMode"] == "newProject":
        project = api.project.create(workspace_id, state["dstProjectName"], sly.ProjectType.IMAGES,
                                     change_name_if_conflict=True)
    elif state["dstProjectMode"] == "existingProject":
        project = api.project.get_info_by_id(state["dstProjectId"])
    if project is None:
        sly.logger.error("Result project is None (not found or not created)")
        return

    dataset = None
    if state["dstDatasetMode"] == "newDataset":
        dataset = api.dataset.create(project.id, state["dstDatasetName"], change_name_if_conflict=True)
    elif state["dstDatasetMode"] == "existingDataset":
        dataset = api.dataset.get_info_by_name(project.id, state["selectedDatasetName"])
    if dataset is None:
        sly.logger.error("Result dataset is None (not found or not created)")
        return



    #=============================================================================================================
    new_project = api.project.create(workspace_id, project_name, type=sly.ProjectType.VIDEOS,
                                     change_name_if_conflict=True)
    new_dataset = api.dataset.create(new_project.id, g.dataset_name, change_name_if_conflict=True)

    for video_path in videos_pathes:
        if len(get_file_ext(video_path)) == 0:
            files_infos = api.file.list2(g.TEAM_ID, video_path)
            curr_video_pathes = [os.path.join(video_path, file_info.name) for file_info in files_infos]

        video_name = get_file_name_with_ext(video_path)
        if not is_valid_ext(get_file_ext(video_name)):
            app_logger.warn(
                'File with extention {} can not be processed. Allowed video extentions {}'.format(get_file_ext(video_name),
                                                                                           ALLOWED_VIDEO_EXTENSIONS))

        video_download_path = os.path.join(g.storage_dir, video_name)
        api.file.download(team_id, video_path, video_download_path)

        if get_file_ext(video_name) != g.video_ext:
            new_video_name = get_file_name(video_name) + g.video_ext
            clip = moviepy.VideoFileClip(video_download_path)
            video_download_path = video_download_path.split('.')[0] + g.video_ext
            clip.write_videofile(video_download_path)
            video_name = new_video_name

        file_info = g.api.video.upload_paths(new_dataset.id, [video_name], [video_download_path])

    g.my_app.stop()


    # work_dir = os.path.join(g.storage_dir, g.working_folder)
    #
    # meta_json = sly.io.json.load_json_file(os.path.join(work_dir, 'meta.json'))
    # meta = sly.ProjectMeta.from_json(meta_json)
    #
    # dataset_info = api.dataset.get_info_by_id(g.DATASET_ID)
    # dataset_path = os.path.join(work_dir, dataset_info.name)
    # imgs_path = os.path.join(dataset_path, 'img')
    # anns_path = os.path.join(dataset_path, 'ann')
    #
    # RESULT_DIR = os.path.join(g.storage_dir, g.working_folder)
    # mkdir(RESULT_DIR)
    # video_path = os.path.join(RESULT_DIR, dataset_info.name + g.video_ext)
    # file_remote = "/{}/{}_{}_{}".format(g.result_folder, g.TASK_ID, g.DATASET_ID, dataset_info.name + g.video_ext)
    #
    # images_infos = api.image.get_list(g.DATASET_ID, sort='name')
    #
    # if len(images_infos) == 0:
    #     app_logger.warn('There is no images in {} dataset'.format(dataset_info.name))
    #
    # for idx, image_info in enumerate(images_infos):
    #     if idx == 0:
    #         image_shape = (image_info.width, image_info.height)
    #     elif (image_info.width, image_info.height) != image_shape:
    #         app_logger.warn('Sizes of images in {} dataset are not the same. Check your input data.'.format(dataset_info.name))
    #         g.my_app.stop()
    #         return
    #
    # image_names = [image_info.name for image_info in images_infos]
    #
    # video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'MP4V'), int(g.frame_rate), image_shape)
    # for curr_im_name in image_names:
    #     curr_im_path = os.path.join(imgs_path, curr_im_name)
    #     curr_ann_path = os.path.join(anns_path, curr_im_name + g.ann_ext)
    #     ann_json = sly.io.json.load_json_file(curr_ann_path)
    #     ann = sly.Annotation.from_json(ann_json, meta)
    #     img = cv2.imread(curr_im_path)
    #     ann.draw_pretty(img, opacity=g.opacity / 100)
    #     video.write(img)
    # video.release()
    #
    # upload_progress = []
    #
    # def _print_progress(monitor, upload_progress):
    #     if len(upload_progress) == 0:
    #         upload_progress.append(sly.Progress(message="Upload {!r}".format(file_remote),
    #                                             total_cnt=monitor.len,
    #                                             ext_logger=app_logger,
    #                                             is_size=True))
    #     upload_progress[0].set_current_value(monitor.bytes_read)
    #
    # app_logger.info("Local video path: {!r}".format(video_path))
    # sly.fs.ensure_base_path(video_path)
    # file_info = api.file.upload(g.TEAM_ID, video_path, file_remote, lambda m: _print_progress(m, upload_progress))
    # api.task._set_custom_output(task_id, file_info.id, sly.fs.get_file_name_with_ext(file_remote),
    #                             description="Video from dataset images")
    #
    # app_logger.info("Local file successfully uploaded to team files")
    #
    # g.my_app.stop()


def main():
    sly.logger.info(
        "Script arguments",
        extra={
            "team_id": g.TEAM_ID,
            "workspace_id": g.WORKSPACE_ID,
            "task_id": g.TASK_ID
        }
    )

    data = {}
    state = {}

    init_ui.init_context(data, team_id, workspace_id)
    init_ui.init(data, state)
    init_ui_progress.init_progress(data,state)
    g.my_app.run(data=data, state=state)


if __name__ == "__main__":
    sly.main_wrapper("main", main)

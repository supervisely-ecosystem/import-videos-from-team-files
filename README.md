<div align="center" markdown>
<img src="https://i.imgur.com/Wo7XOMm.png"/>



# Import Videos from Team Files

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#How-To-Use">How To Use</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/import-videos)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-videos)
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-videos&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-videos&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-videos&counter=runs&label=runs&123)](https://supervise.ly)

</div>

## Overview

Application imports selected videos from `Team Files` to selected destination.

**Supported video formats:**

* `AVI`
* `MOV`
* `MKV`
* `WMV`
* `WEBM`
* `3GP`
* `MP4`
* `FLV`

**Note:** all videos will be converted to `MP4` format during import.

## How To Run 
**Step 1**: Add app to your team from [Ecosystem](https://app.supervise.ly/apps/ecosystem/import-videos) if it is not there.

**Step 2**: Open `Plugins & Apps` -> `Import Videos from Team Files` -> `Run` 

## How to use

**Step 1**: Choose path to folder in team files with videos.

**Step 2:** Select videos or folders with videos to download.

**Step 3:** Select result project and dataset names. You can download videos to new video project, add videos to existing video project by adding videos to existing dataset or creating new dataset.

After running the application, you can see videos download progress. Then progress is finished, you can find new videos in project you select in `step5`. 

**Note:**

After loading the videos, the application will continue its work, so you can choose another videos and continue work.
You can stop app session in `Plugins & Apps` -> `Import videos in MP4 format` by pressing the `STOP` button.

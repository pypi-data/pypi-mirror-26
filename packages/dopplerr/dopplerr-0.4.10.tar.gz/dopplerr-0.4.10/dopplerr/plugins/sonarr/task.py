# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from dopplerr.db import DopplerrDb
from dopplerr.descriptors.series import SeriesEpisodeUid
from dopplerr.notifications import emit_notifications
from dopplerr.notifications_types.series_subtitles_fetched import SubtitleFetchedNotification
from dopplerr.plugins.sonarr.filter import SonarrFilter
from dopplerr.tasks.download_subtitles import DownloadSubtitleTask
from dopplerr.tasks.manager import DopplerrTasksManager

log = logging.getLogger(__name__)


class DopplerrTask(object):
    def post_task(self, task):
        DopplerrTasksManager().post_task(task)


class TaskSonarrOnDownload(DopplerrTask):
    async def run(self, content):

        logging.debug("Sonarr notification received: %r", content)
        res = await SonarrFilter().filter(content)
        if res.is_unhandled:
            # event has been filtered out
            return res

        # processing ok, let's post our background task to the task queue
        self.post_task(self.task_sonarr_on_download_background(res))
        res.successful("Request successfully posted")
        return res.to_dict()

    async def task_sonarr_on_download_background(self, res):
        log.debug("Starting task_sonarr_on_download_background")
        res = await DownloadSubtitleTask().run(res)
        if not res.is_successful:
            return res

        for episode_info in res.sonarr_episode_infos:
            await emit_notifications(SubtitleFetchedNotification(series_episode_info=episode_info))
            DopplerrDb().update_fetched_series_subtitles(
                series_episode_uid=SeriesEpisodeUid(
                    episode_info['tv_db_id'],
                    episode_info['season_number'],
                    episode_info['episode_number'],
                ),
                subtitles_languages=episode_info['subtitles_languages'],
                dirty=False)
        logging.debug("Background task finished with result: %s", res.to_json())
        return res

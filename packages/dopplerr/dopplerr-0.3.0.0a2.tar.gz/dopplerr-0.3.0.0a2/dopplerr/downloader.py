# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import threading

# from subliminal import scan_videos
from babelfish import Language
from subliminal import Video
from subliminal import download_best_subtitles
from subliminal import region
from subliminal import save_subtitles
from subliminal.subtitle import get_subtitle_path
from txwebbackendbase.singleton import singleton
from txwebbackendbase.utils import recursive_iglob

from dopplerr.status import DopplerrStatus

log = logging.getLogger(__name__)


@singleton
class DopplerrDownloader(object):
    def __init__(self):
        # Avoid having 2 download at the same time, at least of the integrity of the cache file
        self.subliminal_download_lock = threading.Lock()

    @staticmethod
    def initialize_subliminal():
        log.info("Initializing Subliminal cache...")
        region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefile.dbm'})

    def search_file(self, root_dir, base_name):
        # This won't work with python < 3.5
        found = []
        protected_path = os.path.join(root_dir, "**", "*" + base_name + "*")
        protected_path = protected_path.replace("[", "[[]").replace("]", "[]]")
        log.debug("Searching %r", protected_path)
        for filename in recursive_iglob(protected_path):
            log.debug("Found: %s", filename)
            found.append(filename)
        return found

    def process_fullscan(self, _request):
        log.debug("Processing full scan of missing subtitle files...")
        res = {
            'status': 'unprocessed',
            'message': 'not implemented yet!',
        }
        # TODO: inspiration
        #   https://gist.github.com/alexsavio/9299716
        return res

    def download_missing_subtitles(self, res, files):
        log.info("Searching and downloading missing subtitles")
        res.update_status("downloading", "downloading missing subtitles")
        videos = []
        for fil in files:
            _, ext = os.path.splitext(fil)
            if ext in [".jpeg", ".jpg", ".nfo", ".srt", ".sub", ".nbz"]:
                log.debug("Ignoring %s because of extension: %s", fil, ext)
                continue
            videos.append(Video.fromname(fil))
        log.info("Video files: %r", videos)
        if not videos:
            log.debug("No subtitle to download")
            res.update_status("failed", "no video file found")
            return res
        res.update_status("fetching", "finding best subtitles")
        self.subliminal_download_lock.acquire()
        log.info("fetching subtitles...")
        try:
            provider_configs = DopplerrStatus().subliminal_provider_configs
            subtitles = download_best_subtitles(
                videos, {Language(l)
                         for l in DopplerrStatus().languages},
                provider_configs=provider_configs)
        except Exception as e:
            log.exception("subliminal raised an exception")
            res.update_status("failed", "subliminal exception")
            res.set("exception", repr(e))
            return res
        self.subliminal_download_lock.release()
        subtitles_info = []
        for vid in videos:
            log.info("Found subtitles for %s:", vid)
            for sub in subtitles[vid]:
                log.info("  %s from %s", sub.language, sub.provider_name)
                subtitles_info.append({
                    "language": str(sub.language),
                    "provider": sub.provider_name,
                    "filename": get_subtitle_path(vid.name, language=sub.language)
                })
            save_subtitles(vid, subtitles[vid])
        res.update_status("succeeded", "download successful")
        res.set("subtitles", subtitles_info)
        return res

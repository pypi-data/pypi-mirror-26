# coding: utf-8

# Standard Libraries
import asyncio
import logging

# Dopplerr
from dopplerr.config import DopplerrConfig

log = logging.getLogger(__name__)


class PeriodicTask(object):
    job_id: str = None
    job_type = 'interval'
    job_default_kwargs = {'max_instances': 1}
    scheduler = None
    seconds: int = None
    minutes: int = None
    hours: int = None
    active = False
    _interrupted = False
    enable_cfg: str = None
    forced = False
    force_start_required = False

    def __init__(self):
        self.init()

    def init(self):
        pass

    async def run(self):
        try:
            if self.force_start_required:
                self.forced = True
            elif self.forced:
                log.debug("Forced execution already started, skip this periodic schedule")
                return
            self.active = True
            return await self._run()
        finally:
            self.active = False

    async def _run(self):
        raise NotImplementedError

    @property
    def _add_job_kwargs(self):
        kw = self.job_default_kwargs.copy()
        if self.seconds:
            kw['seconds'] = self.seconds
        if self.minutes:
            kw['minutes'] = self.minutes
        if self.hours:
            kw['hours'] = self.hours
        return kw

    @property
    def job(self):
        if self.scheduler:
            return self.scheduler.get_job(self.job_id)

    def add_job(self, scheduler):
        if self.enable_cfg is not None and not DopplerrConfig().get_cfg_value(self.enable_cfg):
            log.info("Do not enable job '%s', it is disabled by configuration '%s'", self.job_id,
                     self.enable_cfg)
            return
        self.scheduler = scheduler
        scheduler.add_job(
            self.run, self.job_type, id=self.job_id, replace_existing=True, **self._add_job_kwargs)

    @property
    def next_run_time(self):
        job = self.job
        if job:
            return self.job.next_run_time

    @property
    def next_run_time_iso(self):
        t = self.next_run_time
        if t:
            return t.isoformat()

    @property
    def interval(self):
        # yapf: disable
        return (
            (self.seconds if self.seconds else 0) +
            (self.minutes * 60 if self.minutes else 0) +
            (self.hours * 60 * 60 if self.hours else 0) +
            0)
        # yapf: enable

    @property
    def started(self):
        return self.scheduler

    def stop(self):
        self.scheduler = None

    @property
    def stopped(self):
        return not self.scheduler

    def interrupt(self):
        self._interrupted = True

    @property
    def interrupted(self):
        return self._interrupted

    async def force_start(self):
        log.debug("Force start job: %s", self.job_id)
        self.force_start_required = True
        asyncio.ensure_future(self.run())

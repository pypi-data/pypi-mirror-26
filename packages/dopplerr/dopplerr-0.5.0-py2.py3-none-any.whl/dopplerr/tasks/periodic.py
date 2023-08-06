# coding: utf-8

import logging

log = logging.getLogger(__name__)


class PeriodicTask(object):
    job_id = NotImplementedError
    job_type = 'interval'
    job_default_kwargs = {'max_instances': 1}
    scheduler = None
    seconds = None
    minutes = None
    hours = None

    async def run(self):
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

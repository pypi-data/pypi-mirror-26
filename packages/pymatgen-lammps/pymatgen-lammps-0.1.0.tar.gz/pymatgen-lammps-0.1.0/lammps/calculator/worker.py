import urllib.parse
import asyncio
import multiprocessing

from zmq_legos.mdp import Worker as MDPWorker

from .process import LammpsProcess


class LammpsWorker:
    def __init__(self, stop_event, scheduler, command=None, num_workers=None, loop=None):
        self.command = command
        self.num_workers = num_workers or multiprocessing.cpu_count()
        if self.num_workers > multiprocessing.cpu_count():
            raise ValueError('cannot have more workers than cpus')

        parsed = urllib.parse.urlparse(scheduler)
        self.mdp_worker = MDPWorker(
            stop_event,
            max_messages=self.num_workers,
            protocol=parsed.scheme, port=parsed.port, hostname=parsed.hostname,
            loop=loop)

    async def create(self):
        self._processes = []
        for _ in range(self.num_workers):
            process = LammpsProcess(command=self.command)
            await process.create(self.mdp_worker.queued_messages, self.mdp_worker.completed_messages)
            self._processes.append(process)

    def shutdown(self):
        for process in self._processes:
            process.shutdown()

    async def run(self):
        await self.mdp_worker.run(b'lammps.job')

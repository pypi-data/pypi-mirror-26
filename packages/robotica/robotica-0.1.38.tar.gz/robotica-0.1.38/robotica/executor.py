""" Robotica Schedule. """
import asyncio
import datetime
import time
import logging
from typing import Dict, Set, List, Optional  # NOQA
from typing import TYPE_CHECKING

import math

from robotica.plugins.outputs import Output
from robotica.types import Action
if TYPE_CHECKING:
    from robotica.schedule import Schedule  # NOQA

logger = logging.getLogger(__name__)


class Timer:

    def __init__(
            self, *,
            loop: asyncio.AbstractEventLoop,
            executor: 'Executor',
            locations: Set[str],
            name: str) -> None:
        self._loop = loop
        self._executor = executor
        self._locations = locations
        self._name = name
        self._timer_running = False
        self._timer_stop = None  # type: Optional[float]
        self._early_warning = 3
        self._one_minute = 60
        self._task = None  # type: Optional[asyncio.Task[None]]

    @property
    def is_running(self) -> bool:
        return self._task is not None

    def cancel(self) -> None:
        if self._task is not None:
            self._task.cancel()

    async def _cancel(self, message: str):
        logger.info('timer %s: cancelled: %s', self._name, message)

        action = {
            'timer_cancel': {
                'name': self._name,
                'message': message,
            },
        }

        await self._executor.do_action(self._locations, action)

    async def _warn(
            self, *,
            time_left: int, time_total: int,
            epoch_minute: float,
            epoch_finish: float,
            action: Action):
        logger.info(
            "timer warn %s: time left %d, time total %s",
            self._name, time_left, time_total)

        new_action = {
            'timer_warn': {
                'name': self._name,
                'time_left': time_left,
                'time_total': time_total,
                'epoch_minute': epoch_minute,
                'epoch_finish': epoch_finish,
            },
        }
        new_action.update(action)

        await self._executor.do_action(self._locations, new_action)

    async def _update(
            self, *,
            time_left: int, time_total: int,
            epoch_minute: float,
            epoch_finish: float,
            action: Action):
        logger.info(
            "timer %s: time left %d, time total %s",
            self._name, time_left, time_total)

        new_action = {
            'timer_status': {
                'name': self._name,
                'time_left': time_left,
                'time_total': time_total,
                'epoch_minute': epoch_minute,
                'epoch_finish': epoch_finish,
            },
        }

        new_action.update(action)

        await self._executor.do_action(self._locations, new_action)

    async def _sleep_until_time(self, new_time: float):
        twait = max(new_time - time.time(), 0)
        logger.debug(
            "timer %s: waiting %.1f seconds.",
            self._name, twait)
        await asyncio.sleep(twait)

    def set_minutes(self, total_minutes: int) -> None:
        assert not self._timer_running
        current_time = time.time()
        self._timer_stop = current_time + total_minutes * self._one_minute

    def set_end_time(self, time_str: str) -> None:
        assert not self._timer_running
        hh, mm = time_str.split(":", maxsplit=1)
        hhmm = datetime.time(hour=int(hh), minute=int(mm))
        date = datetime.date.today()
        dt = datetime.datetime.combine(date=date, time=hhmm)
        self._timer_stop = dt.timestamp()

    async def _execute(self, action: Action) -> None:
        assert self._timer_stop is not None

        if self._timer_running:
            await self._cancel("already set.")
            raise RuntimeError(
                "timer %s: already running, cannot execute" % self._name)

        try:
            self._timer_running = True

            early_warning = self._early_warning
            one_minute = self._one_minute

            current_time = time.time()
            timer_stop = self._timer_stop
            next_minute = current_time
            total_minutes = int(
                math.ceil(
                    (timer_stop - current_time)
                    / one_minute
                )
            )

            logger.info(
                "timer %s: started at %d minutes.",
                self._name, total_minutes)

            while True:
                # calculate wait time
                current_time = time.time()
                twait = timer_stop - current_time

                logger.debug(
                    "timer %s: %.1f to go to.",
                    self._name, twait)

                if twait <= 0:
                    break

                # time: minute
                current_time = time.time()
                minutes_left = int(
                    math.ceil(
                        (timer_stop - current_time)
                        / one_minute
                    )
                )
                await self._update(
                    time_left=minutes_left,
                    time_total=total_minutes,
                    epoch_minute=next_minute,
                    epoch_finish=timer_stop,
                    action=action)
                action = {}

                # calculate absolute times
                current_time = time.time()
                twait = timer_stop - current_time
                seconds_to_next_minute = twait % one_minute
                if seconds_to_next_minute == 0:
                    seconds_to_next_minute = one_minute
                next_minute = current_time + seconds_to_next_minute
                next_warning = next_minute - early_warning

                # wait until early warning
                logger.debug(
                    "timer %s: waiting %.1f seconds to early warn, %.1f to go.",
                    self._name, next_warning - current_time, twait)
                await self._sleep_until_time(next_warning)

                # time: early_warning before minute
                current_time = time.time()
                minutes_left = int(
                    math.ceil(
                        (timer_stop - current_time - early_warning)
                        / one_minute
                    )
                )
                await self._warn(
                    time_left=minutes_left,
                    time_total=total_minutes,
                    epoch_minute=next_minute,
                    epoch_finish=timer_stop,
                    action={})

                # wait until minute
                current_time = time.time()
                twait = timer_stop - current_time
                logger.debug(
                    "timer %s: waiting %.1f seconds to minute, %.1f to go.",
                    self._name, next_minute - current_time, twait)
                await self._sleep_until_time(next_minute)

            logger.info(
                "timer %s: stopped after %d minutes.",
                self._name, total_minutes)

        except asyncio.CancelledError:
            await self._cancel("Cancelled.")
            raise
        except Exception as e:
            logger.exception("Timer encountered as error.")
            await self._cancel("Crashed.")
        finally:
            self._timer_running = False
            self._task = None

    async def execute(self, action: Action) -> None:
        self._task = self._loop.create_task(self._execute(action))
        await self._task


class Executor:
    def __init__(
            self, loop: asyncio.AbstractEventLoop, config: Dict) -> None:
        self._loop = loop
        self._config = config
        self._outputs = []  # type: List[Output]
        self._lock = asyncio.Lock()
        self._timers = {}  # type: Dict[str, Timer]
        self._schedule = None  # type: Optional['Schedule']

    def set_schedule(self, schedule: 'Schedule') -> None:
        self._schedule = schedule

    def add_output(self, output: Output) -> None:
        self._outputs.append(output)

    def action_required_for_locations(
            self, locations: Set[str], action: Action) -> Set[str]:

        # if timer action, we must process it everywhere.
        if 'timer' in action:
            return locations
        if 'template' in action:
            return locations

        required_locations = set([
            location
            for output in self._outputs
            for location in locations
            if output.is_action_required_for_location(location, action)
        ])

        return required_locations

    async def do_action(self, locations: Set[str], action: Action) -> None:
        required_locations = self.action_required_for_locations(locations, action)
        if len(required_locations) == 0:
            return

        if 'timer' in action:
            timer_details = action['timer']
            timer_name = timer_details.get('name', 'default')
            timer_replace = timer_details.get('replace', False)
            timer_cancel = timer_details.get('cancel', False)

            if (timer_name in self._timers and
                    self._timers[timer_name].is_running):
                if timer_replace or timer_cancel:
                    logger.info(
                        "timer %s: Already running, cancelling old one.",
                        timer_name)
                    self._timers[timer_name].cancel()
                else:
                    logger.info(
                        "timer %s: Already running, not starting.",
                        timer_name)
                    raise RuntimeError(
                        "timer %s: already running" % timer_name)

            # if request to cancel timer, don't start a new one
            if timer_cancel:
                return

            timer_action = dict(action)
            del timer_action['timer']

            self._timers[timer_name] = Timer(
                loop=self._loop,
                executor=self,
                locations=required_locations,
                name=timer_name,
            )
            if 'minutes' in timer_details:
                minutes = int(timer_details['minutes'])
                self._timers[timer_name].set_minutes(minutes)
            elif 'end_time' in timer_details:
                end_time = timer_details['end_time']
                self._timers[timer_name].set_end_time(end_time)
            else:
                assert False
            await self._timers[timer_name].execute(timer_action)
            return

        if 'template' in action and self._schedule is not None:
            template_details = action['template']
            template_name = template_details['name']
            await self._schedule.add_template(locations, template_name)
            return

        with await self._lock:
            coros = [
                output.execute(location, action)
                for output in self._outputs
                for location in locations
            ]
            await asyncio.gather(
                *coros,
                loop=self._loop
            )

    async def do_actions(self, locations: Set[str], actions: List[Action]) -> None:
        for action in actions:
            await self.do_action(locations, action)

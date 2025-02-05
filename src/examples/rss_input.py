#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 - 2023 Mewbot Developers <mewbot@quicksilver.london>
#
# SPDX-License-Identifier: BSD-2-Clause

# pylint: disable=duplicate-code
# this is an example - duplication for emphasis is desirable

# https://www.theguardian.com/world/rss

from typing import Any, Dict, Set, Type

from mewbot.api.v1 import Action
from mewbot.core import InputEvent, OutputEvent
from mewbot.io.rss import RSSInputEvent


class RSSPrintAction(Action):
    """
    Print every InputEvent.
    """

    @staticmethod
    def consumes_inputs() -> Set[Type[InputEvent]]:
        return {InputEvent}

    @staticmethod
    def produces_outputs() -> Set[Type[OutputEvent]]:
        return set()

    async def act(self, event: InputEvent, state: Dict[str, Any]) -> None:
        if not isinstance(event, RSSInputEvent):
            print(f"Unexpected event {event}")
            return

        rss_output_str = []
        rss_output_str.append(f"New event title - {event.title}")
        rss_output_str.append(f"New event author - {event.author}")
        rss_output_str.append(f"New event ... event - \n{event}")

        print("\n".join(rss_output_str))

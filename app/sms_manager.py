#  Copyright 2022 Pavel Suprunov
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import asyncio

from app.logger import log_critical
from app.logger import log_info
from app.models.domain.command import Command
from app.services.sms import send_sms_to_phone


async def sms_handler(queue: asyncio.Queue):
    while True:
        await log_info("Await new message from kafka")
        message: Command = await queue.get()

        await log_info("Get new message from queue")

        is_sent = await send_sms_to_phone("http://192.168.1.1", message.phone, message.message)
        if not is_sent:
            await log_critical("Sms has not sent")

        queue.task_done()
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

from aiokafka import AIOKafkaConsumer
from pydantic import ValidationError
from asyncio import Queue

from app.logger import log_error
from app.logger import log_info
from app.models.command import Command
from app.services.serializer import deserialize
from app.settings import AppSettings


async def get_message_from_kafka(settings: AppSettings, queue: Queue):
    consumer = AIOKafkaConsumer(
        "sms",
        bootstrap_servers=settings.kafka_host,
        key_deserializer=deserialize,
        value_deserializer=deserialize
    )

    await consumer.start()

    try:
        async for consumer_record in consumer:
            message = consumer_record.value

            try:
                new_command = Command(**message)

                await queue.put(new_command)
                await log_info("Put new message in queue")

            except TypeError as exception:
                await log_error(exception)
            except ValidationError as exception:
                await log_error(exception)

    finally:
        await consumer.stop()
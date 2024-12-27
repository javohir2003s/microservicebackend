from django.core.management.base import BaseCommand
from .myscript import parsing
import time
import asyncio


class Command(BaseCommand):
    help = "Web sahifani parsing qilib ma'lumotlar bazasiga saqlash"

    def handle(self, *args, **kwargs):
        start = time.perf_counter()
        async def main():
            await parsing()

        asyncio.run(main())

        stop = time.perf_counter()
        print(f"Funksiya ishlagan vaqt: {stop-start}")

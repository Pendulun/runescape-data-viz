from domain.repository.itemRepo import IItemRepo
from datetime import datetime


class ItemRepoMock(IItemRepo):

    def get_item_info(self, item_id: int) -> dict | None:
        if not isinstance(item_id, int):
            return dict()
        return dict()

    def get_item_prices(self, item_id: int) -> dict | None:
        if not isinstance(item_id, int):
            return dict()

        today_day = datetime.today().day
        today_month = datetime.today().month
        today_year = datetime.today().year
        today_datetime = datetime(today_year, today_month, today_day)
        # The API timecode comes in miliseconds, but today_datetime.timestamp
        # is in seconds
        today_timestamp = str(today_datetime.timestamp() * 1000).split(".")[0]
        items_prices = {
            'daily': {
                today_timestamp: 1
            },
            'average': {
                today_timestamp: 2
            }
        }
        return items_prices

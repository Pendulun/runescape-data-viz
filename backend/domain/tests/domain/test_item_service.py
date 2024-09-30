from unittest import main, TestCase
from domain.itemServiceImp import ItemServiceImp
from domain.tests.domain.mocks.item_repo_mock import ItemRepoMock
from datetime import datetime


class TestItemService(TestCase):

    def setUp(self):
        self.item_service = ItemServiceImp(ItemRepoMock())

    def test_can_get_item_info(self):
        item_id = 1
        item_info = self.item_service.get_item_info(item_id)
        self.assertIsInstance(item_info, dict)

    def test_get_empty_dict_invalid_id_item_info(self):
        item_id = 'a'
        item_info = self.item_service.get_item_info(item_id)
        self.assertDictEqual(item_info, dict())

    def test_get_empty_dict_invalid_id_item_prices(self):
        item_id = 'a'
        item_prices = self.item_service.get_item_prices(item_id)
        self.assertDictEqual(item_prices, dict())

    def test_get_item_price_date_as_date(self):
        item_id = 1
        item_prices = self.item_service.get_item_prices(item_id)
        curr_date = datetime.now().date()
        self.assertEqual(list(item_prices['daily'].keys())[0], curr_date)
        self.assertEqual(list(item_prices['average'].keys())[0], curr_date)


if __name__ == "__main__":
    main()

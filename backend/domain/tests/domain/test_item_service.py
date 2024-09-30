from unittest import main, TestCase
from domain.itemServiceImp import ItemServiceImp
from domain.tests.domain.mocks.item_repo_mock import ItemRepoMock


class TestItemService(TestCase):
    def setUp(self):
        self.item_service = ItemServiceImp(ItemRepoMock())

    def test_can_get_item_info(self):
        item_id = 1
        item_info = self.item_service.get_item_info(item_id)
        self.assertIsInstance(item_info, dict)
    
    def test_get_empty_dict_invalid_id(self):
        item_id = 'a'
        item_info = self.item_service.get_item_info(item_id)
        self.assertDictEqual(item_info, dict())

if __name__ == "__main__":
    main()
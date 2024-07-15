import unittest
from UnitTesting.unittesting import DeferrableTestCase
import sublime
import sublime_plugin
from Pieces.assets.assets_snapshot import AssetSnapshot
from Pieces.search.search_command import (PiecesSearchCommand,
    SearchTypeInputHandler,
    QueryInputHandler)


class TestPiecesSearchCommand(DeferrableTestCase):

    def setUp(self):
        # Set up any state specific to the test
        self.window = sublime.active_window()
        self.command = PiecesSearchCommand(self.window)
        yield 3000 # Wait 3 sec for everythin to load (websockets)

    def test_search_input_handler(self):
        items = SearchTypeInputHandler().list_items()
        self.assertIsInstance(items,list)
    
    def test_query_input_handler(self):
        SearchTypeInputHandler.search_type = "assets"
        asset = list(AssetSnapshot.identifiers_snapshot.values())[0]
        search_query = asset.name
        input = QueryInputHandler().next_input({"search_type":SearchTypeInputHandler.search_type,"query":search_query})
        items = input.list_items()
        self.assertIsInstance(items,list)
        self.assertGreater(len(items),0)

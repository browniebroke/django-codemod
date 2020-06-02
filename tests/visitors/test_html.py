from django_codemod.visitors import UnescapeEntitiesTransformer
from tests.visitors.base import BaseVisitorTest


class TestUnescapeEntitiesTransformer(BaseVisitorTest):

    transformer = UnescapeEntitiesTransformer

    def test_simple_substitution(self) -> None:
        before = """
            from django.utils.text import unescape_entities

            result = unescape_entities(content)
        """
        after = """
            from html import unescape

            result = unescape(content)
        """
        self.assertCodemod(before, after)

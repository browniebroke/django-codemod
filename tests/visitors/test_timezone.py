from django_codemod.visitors import FixedOffsetTransformer
from tests.visitors.base import BaseVisitorTest


class TestFixedOffsetTransformer(BaseVisitorTest):

    transformer = FixedOffsetTransformer

    def test_noop(self) -> None:
        """Test when nothing should change."""
        before = after = """
            from datetime import timedelta, timezone

            timezone(offset=timedelta(minutes=60))
        """

        self.assertCodemod(before, after)

    def test_without_name_kwargs(self) -> None:
        """Case with just offset given as kwarg."""
        before = """
            from django.utils.timezone import FixedOffset

            tz_info = FixedOffset(offset=60)
        """
        after = """
            from datetime import timedelta, timezone

            tz_info = timezone(offset=timedelta(minutes = 60))
        """

        self.assertCodemod(before, after)

    def test_without_name_args(self) -> None:
        """Case with just offset given as arg."""
        before = """
            from django.utils.timezone import FixedOffset

            tz_info = FixedOffset(60)
        """
        after = """
            from datetime import timedelta, timezone

            tz_info = timezone(timedelta(minutes = 60))
        """

        self.assertCodemod(before, after)

    def test_with_name_kwargs(self) -> None:
        """Case with both offset and name given as kwargs."""
        before = """
            from django.utils.timezone import FixedOffset

            tz_info = FixedOffset(offset=60, name="example")
        """
        after = """
            from datetime import timedelta, timezone

            tz_info = timezone(offset=timedelta(minutes = 60), name="example")
        """

        self.assertCodemod(before, after)

    def test_with_name_args(self) -> None:
        """Case with both offset and name given as args."""
        before = """
            from django.utils.timezone import FixedOffset

            tz_info = FixedOffset(60, "example")
        """
        after = """
            from datetime import timedelta, timezone

            tz_info = timezone(timedelta(minutes = 60), "example")
        """

        self.assertCodemod(before, after)

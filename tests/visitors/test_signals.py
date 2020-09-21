from parameterized import parameterized

from django_codemod.visitors import SignalDisconnectWeakTransformer
from tests.visitors.base import BaseVisitorTest


class TestSignalDisconnectWeakTransformer(BaseVisitorTest):

    transformer = SignalDisconnectWeakTransformer
    DJANGO_SIGNAL_NAMES = [
        "pre_init",
        "post_init",
        "pre_save",
        "post_save",
        "pre_delete",
        "post_delete",
        "m2m_changed",
        "pre_migrate",
        "post_migrate",
    ]

    @parameterized.expand(DJANGO_SIGNAL_NAMES)
    def test_noop(self, signal_name):
        before = after = f"""
            from django.db.models.signals import {signal_name}

            {signal_name}.disconnect(
                receiver=some_handler,
                sender=MyModel,
                dispatch_uid='something-unique',
            )
        """

        self.assertCodemod(before, after)

    @parameterized.expand(DJANGO_SIGNAL_NAMES)
    def test_with_kwargs(self, signal_name):
        before = f"""
            from django.db.models.signals import {signal_name}

            {signal_name}.disconnect(receiver=some_handler, sender=MyModel, weak=True)
        """

        after = f"""
            from django.db.models.signals import {signal_name}

            {signal_name}.disconnect(receiver=some_handler, sender=MyModel)
        """

        self.assertCodemod(before, after)

    @parameterized.expand(DJANGO_SIGNAL_NAMES)
    def test_with_kwargs_dispatch_uid(self, signal_name):
        before = f"""
            from django.db.models.signals import {signal_name}

            {signal_name}.disconnect(
                receiver=some_handler,
                sender=MyModel,
                weak=True,
                dispatch_uid='my-unique-id',
            )
        """

        after = f"""
            from django.db.models.signals import {signal_name}

            {signal_name}.disconnect(
                receiver=some_handler,
                sender=MyModel,
                dispatch_uid='my-unique-id',
            )
        """

        self.assertCodemod(before, after)

    @parameterized.expand(DJANGO_SIGNAL_NAMES)
    def test_imported_with_alias(self, signal_name):
        before = f"""
            from django.db.models.signals import {signal_name} as dj_{signal_name}

            dj_{signal_name}.disconnect(receiver=some_handler, weak=True)
        """

        after = f"""
            from django.db.models.signals import {signal_name} as dj_{signal_name}

            dj_{signal_name}.disconnect(receiver=some_handler)
        """

        self.assertCodemod(before, after)

    def test_multiple_signal_disconnected_single_import(self):
        before = """
            from django.db.models.signals import pre_save, post_save

            pre_save.disconnect(receiver=some_handler, weak=True)
            post_save.disconnect(receiver=some_handler, weak=True)
        """

        after = """
            from django.db.models.signals import pre_save, post_save

            pre_save.disconnect(receiver=some_handler)
            post_save.disconnect(receiver=some_handler)
        """

        self.assertCodemod(before, after)

    def test_multiple_signal_disconnected_separate_imports(self):
        before = """
            from django.db.models.signals import pre_save
            from django.db.models.signals import post_save

            pre_save.disconnect(receiver=some_handler, weak=True)
            post_save.disconnect(receiver=some_handler, weak=True)
        """

        after = """
            from django.db.models.signals import pre_save
            from django.db.models.signals import post_save

            pre_save.disconnect(receiver=some_handler)
            post_save.disconnect(receiver=some_handler)
        """

        self.assertCodemod(before, after)

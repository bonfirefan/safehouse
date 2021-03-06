from sms.tests.config import *
import sms.models as model
from django.test import TestCase
from django.utils.timezone import now
from datetime import timedelta


class ConfigTestCase(TestCase):

    def testConfigCreatesAConfigObject(self):
        model.config("key", "val")
        config = model.Config.objects.get(key='key')
        self.assertEquals(config.key, "key")
        self.assertEquals(config.val, "val")

    def testConfigUpdatesAConfigObject(self):
        model.config("key", "val")
        model.config("key", "val2")
        config = model.Config.objects.get(key='key')
        self.assertEquals(config.val, "val2")

    def testConfigDeletsAConfigObject(self):
        model.config("key", "val")
        model.config('key', None)
        with self.assertRaises(model.Config.DoesNotExist):
            model.Config.objects.get(key='key')


class StoreTaggedMessageTestCase(TestCase):

    def testCanSaveAMessage(self):
        model.save_tagged_message("a", "1", "3")


class PopMessageTagTestCase(TestCase):

    def setUp(self):
        self.sa1 = model.SavedMessage.objects.create(tag="a", message="a1")
        self.sa2 = model.SavedMessage.objects.create(tag="a", message="a2")
        self.sb1 = model.SavedMessage.objects.create(tag="b", message="b1")

    def testReturnsFirstMessage(self):
        output = model.pop_message_tag('a')
        self.assertEqual(self.sa1.message, output.message)

    def testReturnsTaggedMessage(self):
        output = model.pop_message_tag('b')
        self.assertEqual(self.sb1.message, output.message)

    def testDeletesMessageFromDatabase(self):
        output = model.pop_message_tag('a')
        self.assertEqual(model.SavedMessage.objects.count(), 2)

    def testReturnsNoneIfNoTag(self):
        output = model.pop_message_tag('c')
        self.assertIs(None, output)

class CreateFromDelayTestCase(TestCase):
    def testCreatesDelayedWithOffsetDelay(self):
        d1 = model.DelayedCommand.objects.create_from_delay(100, "bloog")
        offset = now().replace(microsecond=0) + timedelta(minutes=100)
        self.assertEqual(d1.send_at, offset)

    def testWorksWithStringOffset(self):
        d1 = model.DelayedCommand.objects.create_from_delay('100', "bloog")
        offset = now().replace(microsecond=0) + timedelta(minutes=100)
        self.assertEqual(d1.send_at, offset)

class DueCommandsTestCase(TestCase):
    def testGetsAllOverdueDelayedCommands(self):
        d1 = model.DelayedCommand.objects.create_from_delay(-100, "bloog")
        d2 = model.DelayedCommand.objects.create_from_delay(-100, "other")
        self.assertSequenceEqual(model.DelayedCommand.objects.due_commands(),
                                 [d1, d2])

    def testDoesNotGetUnderdueCommands(self):
        d1 = model.DelayedCommand.objects.create_from_delay(-100, "bloog")
        d2 = model.DelayedCommand.objects.create_from_delay(100, "other")
        self.assertSequenceEqual(model.DelayedCommand.objects.due_commands(),
                                 [d1])

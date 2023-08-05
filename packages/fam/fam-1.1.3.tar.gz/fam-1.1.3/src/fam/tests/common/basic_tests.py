
import unittest
import time
from fam.exceptions import *
from fam.tests.models.test01 import GenericObject, Dog, Cat, Person, JackRussell, Monkey, Monarch, NAMESPACE

"""
Wrapping the test case in BaseTestCases allows these base test to hide from the test runner and
only be called in the sub classes with specific databases

"""

class BasicBaseTestCases:

    class BasicTests(unittest.TestCase):

        db = None

       # Test the app
        def test_app(self):
            self.assertNotEqual(self.db, None)


        def test_make_an_object(self):
            dog = Dog(name="woofer")
            self.assertEqual(dog.namespace, NAMESPACE)
            self.assertEqual(dog.type, "dog")
            self.assertEqual(dog.name, "woofer")
            self.assertEqual(dog.__class__, Dog)


        def test_make_an_object2(self):
            dog = Dog(name="woofer")
            self.assertEqual(dog.talk(), "woof")


        def test_make_a_sub_object(self):
            jack = JackRussell()
            self.assertEqual(jack.talk(), "Yap")
            jack.name = "jack"
            jack.age = 12
            self.db.put(jack)


        def test_make_an_object_saved(self):
            dog = Dog(name="woofer")
            dog.save(self.db)
            self.assertEqual(dog.namespace, NAMESPACE)
            self.assertEqual(dog.type, "dog")
            self.assertEqual(dog.name, "woofer")
            self.assertEqual(dog.__class__, Dog)
            self.assertNotEqual(dog.key, None)
            # self.assertTrue(dog.schema.startswith("http://glowinthedark.co.uk/test/dog"))


        def test_make_an_object_double_dispatch_saved(self):
            dog = Dog(name="woofer")
            self.db.put(dog)
            self.assertEqual(dog.namespace, NAMESPACE)
            self.assertEqual(dog.type, "dog")
            self.assertEqual(dog.name, "woofer")
            self.assertEqual(dog.__class__, Dog)
            self.assertNotEqual(dog.key, None)


        def test_make_an_object_with_additional_properties(self):
            dog = Dog(name="woofer", collar="leather")
            dog.home = "hackney"
            self.db.put(dog)
            self.assertEqual(dog.home, "hackney")

        def test_fail_with_additional_properties(self):

            def wrong_monkey():
                return Monkey(name="bonzo", collar="leather")

            def collar_monkey(monkey):
                monkey.collar = "leather"

            self.assertRaises(FamValidationError, wrong_monkey)
            monkey = Monkey(name="bonzo")
            self.assertRaises(FamValidationError, collar_monkey, monkey)


        def test_make_an_object_saved_cas(self):
            paul = Person(name="paul")
            paul.save(self.db)
            cat = Cat(name="whiskers", owner_id=paul.key, legs=2)
            cat.save(self.db)
            self.assertEqual(cat.namespace, NAMESPACE)
            self.assertEqual(cat.type, "cat")
            self.assertNotEqual(cat.rev, None)


        def test_get_cat(self):
            paul = Person(name="paul")
            paul.save(self.db)
            cat = Cat(name="whiskers", owner_id=paul.key, legs=2)
            cat.save(self.db)
            another = Cat.get(self.db, cat.key)
            self.assertEqual(cat, another)


        def test_ref_to(self):
            paul = Person(name="paul")
            paul.save(self.db)
            cat = Cat(name="whiskers", owner_id=paul.key, legs=2)
            cat.save(self.db)
            self.assertEqual(cat.owner, paul)
            self.assertEqual(cat.owner.name, "paul")


        def test_ref_to_with_object(self):
            paul = Person(name="paul")
            self.db.put(paul)
            cat = Cat(name="whiskers", owner=paul, legs=2)
            cat.save(self.db)
            self.assertEqual(cat.owner, paul)
            self.assertEqual(cat.owner.name, "paul")
            catback = self.db.get(cat.key)
            self.assertEqual(cat, catback)


        def test_ref_from(self):
            paul = Person(name="paul")
            paul.save(self.db)
            cat = Cat(name="whiskers", owner_id=paul.key, legs=2)
            cat.save(self.db)
            cat2 = Cat(name="puss", owner_id=paul.key, legs=2)
            cat2.save(self.db)
            self.assertEqual(len(paul.cats), 2)
            self.assertTrue(paul.cats[0] == cat or paul.cats[1] == cat)


        def test_ref_from_multiple_index(self):
            paul = Person(name="paul")
            paul.save(self.db)
            cat = Cat(name="whiskers", owner_id=paul.key, legs=2)
            cat.save(self.db)
            dog = Dog(name="fly", owner=paul)
            self.db.put(dog)
            self.assertEqual(len(paul.cats), 1)
            self.assertEqual(len(paul.dogs), 1)
            self.assertEqual(len(paul.animals), 2)


        def test_refs_with_inheritance(self):
            paul = Person(name="paul")
            paul.save(self.db)
            jack = JackRussell()
            jack.owner_id = paul.key
            jack.name = "jack"
            jack.save(self.db)
            self.assertEqual(paul.dogs[0], jack)


        def test_refs_with_other_inheritance(self):
            paul = Monarch(name="paul")
            self.db.put(paul)
            jack = Dog()
            jack.owner = paul
            jack.name = "jack"
            self.db.put(jack)
            self.assertEqual(paul.dogs[0], jack)


        def test_delete_cat_dd(self):
            paul = Person(name="paul")
            self.db.put(paul)
            cat = Cat(name="whiskers", owner_id=paul.key, legs=2)
            self.db.put(cat)
            key = cat.key
            another = self.db.get(cat.key)
            self.assertEqual(cat, another)
            self.db.delete(cat)
            revivedcat = self.db.get(key)
            self.assertEqual(revivedcat, None)


        def test_delete_dog_to_refs(self):
            paul = Person(name="paul")
            paul.save(self.db)
            dog = Dog(name="rufus", owner_id=paul.key)
            dog.save(self.db)
            key = dog.key
            dog2 = Dog(name="fly", owner_id=paul.key)
            dog2.save(self.db)
            self.assertNotEqual(dog2.owner, None)
            key = paul.key
            dog.delete(self.db)
            revivedpaul = self.db.get(key)
            self.assertEqual(revivedpaul, None)
            refresheddog2 = Dog.get(self.db, dog2.key)
            self.assertEqual(refresheddog2.owner, None)


        def test_delete_cat_refs(self):
            paul = Person(name="paul")
            paul.save(self.db)
            cat = Cat(name="whiskers", owner_id=paul.key, legs=2)
            cat.save(self.db)
            key = cat.key
            cat2 = Cat(name="puss", owner_id=paul.key, legs=2)
            cat2.save(self.db)
            revivedcat1 = self.db.get(key)
            self.assertNotEqual(revivedcat1, None)
            paul.delete(self.db)
            revivedcat2 = self.db.get(key)
            self.assertEqual(revivedcat2, None)


        def test_delete_dog_refs(self):
            paul = Person(name="paul")
            paul.save(self.db)
            dog = Dog(name="rufus", owner_id=paul.key)
            dog.save(self.db)
            key = dog.key
            dog2 = Dog(name="fly", owner_id=paul.key)
            dog2.save(self.db)
            reviveddog1 = self.db.get(key)
            self.assertNotEqual(reviveddog1, None)
            paul.delete(self.db)
            reviveddog2 = self.db.get(key)
            self.assertNotEqual(reviveddog2, None)


        def test_update_cat(self):
            paul = Person(name="paul")
            paul.save(self.db)
            cat = Cat(name="whiskers", owner_id=paul.key, legs=2)
            cat.save(self.db)
            cat.name = "blackie"
            cat.save(self.db)
            self.assertEqual(cat.name, "blackie")
            self.assertEqual(cat._properties["name"], "blackie")
            self.assertFalse("name" in cat.__dict__.keys())


        def test_update_cat_fails(self):
            paul = Person(name="paul")
            paul.save(self.db)
            cat = Cat(name="whiskers", owner_id=paul.key, legs=2)
            cat.save(self.db)
            cat.colour = "black"
            cat.save(self.db)
            def change_colour():
                cat.colour = "white"
            self.assertRaises(FamImmutableError, change_colour)


        def setcatfood(self):
            self.cat.food = "biscuits"


        def test_update_catfood(self):
            paul = Person(name="paul")
            paul.save(self.db)
            cat = Cat(name="whiskers", owner_id=paul.key, legs=2)
            cat.save(self.db)
            self.assertRaises(Exception, self.setcatfood)


        def test_update_dogfood(self):
            dog = Dog(name="fly")
            dog.food = "biscuits"
            dog.save(self.db)


        def test_update_fails_without_rev(self):
            dog = Dog(name="fly")
            dog.save(self.db)
            dog.rev = None
            dog.name = "jess"
            self.assertRaises(FamResourceConflict, self.db.put, dog)


        def test_update_works_without_rev(self):
            monkey = Monkey(name="fly")
            monkey.save(self.db)
            monkey.rev = None
            monkey.name = "jess"
            self.db.put(monkey)

        def test_uniqueness(self):

            paul = Person(name="paul")
            self.db.put(paul)
            dog1 = Dog(name="rufus", owner_id=paul.key, kennel_club_membership="123456")

            dog1.save(self.db)
            # time.sleep(1)


            # print dog1.as_json()
            # dog2 = Dog(name="fly", owner_id=paul.key, kennel_club_membership="123456")
            # print dog2.as_json()
            # # self.db.put(dog2)
            # self.assertRaises(FamUniqueError, self.db.put, dog2)
            # # print "*********** end ***************"

    class RefNameTests(unittest.TestCase):

        # this test that refs whos name doesnt end with _id fail
        def test_misnamed_ref_to_fails(self):

            def duff_import():
                from fam.tests.models import test02
                print test02

            self.assertRaises(FamError, duff_import)
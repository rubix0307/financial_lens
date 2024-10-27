from django.test import TestCase
from django.contrib.auth import get_user_model
from section.models import Section, SectionUser
from section.services.base_section import UserSectionService

User = get_user_model()


class UserSectionServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_get_or_create_base_section_for_user_creates_section_if_none_exists(self):
        base_section = UserSectionService.get_or_create_base_section_for_user(self.user)
        self.assertIsNotNone(base_section)
        self.assertEqual(base_section.name, "Default Section")
        self.assertTrue(SectionUser.objects.filter(user=self.user, section=base_section, is_base=True).exists())

    def test_get_or_create_base_section_for_user_returns_existing_base_section(self):
        section = Section.objects.create(name="Existing Section")
        SectionUser.objects.create(user=self.user, section=section, is_base=True)

        base_section = UserSectionService.get_or_create_base_section_for_user(self.user)
        self.assertEqual(base_section, section)

    def test_assign_or_create_base_section_assigns_existing_section_as_base(self):
        section1 = Section.objects.create(name="Section 1")
        section2 = Section.objects.create(name="Section 2")
        SectionUser.objects.create(user=self.user, section=section1)
        SectionUser.objects.create(user=self.user, section=section2)

        base_section = UserSectionService.assign_or_create_base_section(self.user)
        self.assertEqual(base_section, section1)
        self.assertTrue(SectionUser.objects.filter(user=self.user, section=section1, is_base=True).exists())

    def test_create_default_section_creates_new_section(self):
        new_section = UserSectionService.create_default_section(self.user)
        self.assertIsNotNone(new_section)
        self.assertEqual(new_section.name, "Default Section")
        self.assertTrue(SectionUser.objects.filter(user=self.user, section=new_section, is_base=True).exists())

    def test_create_new_section_creates_section_with_given_name(self):
        section_name = "New Custom Section"
        new_section_user = UserSectionService.create_new_section(self.user, section_name)
        self.assertIsNotNone(new_section_user)
        self.assertEqual(new_section_user.section.name, section_name)
        self.assertTrue(new_section_user.is_owner)
        self.assertTrue(SectionUser.objects.filter(user=self.user, section=new_section_user.section, is_owner=True).exists())

    def test_get_existing_base_section_returns_none_if_no_base_section_exists(self):
        base_section = UserSectionService.get_existing_base_section(self.user)
        self.assertIsNone(base_section)

    def test_get_existing_base_section_returns_existing_base_section(self):
        section = Section.objects.create(name="Base Section")
        SectionUser.objects.create(user=self.user, section=section, is_base=True)

        base_section = UserSectionService.get_existing_base_section(self.user)
        self.assertEqual(base_section, section)

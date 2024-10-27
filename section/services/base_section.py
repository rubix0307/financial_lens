from typing import Optional

from django.contrib.auth import get_user_model
from section.models import Section, SectionUser


User = get_user_model()

class UserSectionService:
    @staticmethod
    def get_or_create_base_section_for_user(user: User) -> Section:
        """
        Get or create the base section for the given user.
        """
        base_section = UserSectionService.get_existing_base_section(user)
        if base_section:
            return base_section

        return UserSectionService.assign_or_create_base_section(user)

    @staticmethod
    def get_existing_base_section(user: User) -> Optional[Section]:
        """
        Retrieve the existing base section for the user if available.
        """
        base_section_user = SectionUser.objects.filter(user=user, is_base=True).first()
        if base_section_user:
            return base_section_user.section
        return None

    @staticmethod
    def assign_or_create_base_section(user: User) -> Section:
        """
        Assign the section with the lowest ID as base or create a new section if none exists.
        """
        user_sections = SectionUser.objects.filter(user=user).order_by('section_id')
        if user_sections.exists():
            base_section_user = user_sections.first()
            base_section_user.is_base = True
            base_section_user.save()
            return base_section_user.section

        return UserSectionService.create_default_section(user)

    @staticmethod
    def create_new_section(user: User, section_name: str) -> SectionUser:
        """
        Create a new section for the user and set SectionUser as is_owner.
        """
        new_section = Section.objects.create(name=section_name)
        return SectionUser.objects.create(user=user, section=new_section, is_owner=True)

    @staticmethod
    def create_default_section(user: User) -> Section:
        """
        Create a default section for the user and set it as base.
        """
        new_section_user = UserSectionService.create_new_section(user=user, section_name='Default Section')
        new_section_user.is_base = True
        new_section_user.save()
        return new_section_user.section

from django.test import TestCase
from accounts.models import Freelancer
from jobs.models import Skill
from django.contrib.auth.models import User
from django_countries import countries
import tempfile


class TestFreelancerModel(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            first_name='test_fn_1',
            last_name='test_ln_1',
            username='test_un_1'
        )
        self.skill1 = Skill.objects.create(
            name='skill1',
            abbr='skl1'
        )
        self.skill2 = Skill.objects.create(
            name='skill2',
            abbr='skl2'
        )

        self.freelancer1 = Freelancer.objects.create(
            profile_image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            mobile=1234567890,
            description='user_desc1',
            country=countries[0][0],
            address='address1',
            user=self.user1,
        )
        self.freelancer1.skills.add(self.skill1)
        self.freelancer1.skills.add(self.skill2)

    def test_freelancer_create(self):
        self.assertEquals(self.freelancer1.description, 'user_desc1')
        self.assertEquals(self.freelancer1.country, countries[0][0])
        self.assertEquals(self.freelancer1.address, 'address1')
        self.assertEquals(self.freelancer1.mobile, 1234567890)

    def test_freelancer_user_add(self):
        self.assertEquals(self.freelancer1.user.first_name, self.user1.first_name)
        self.assertEquals(self.freelancer1.user.last_name, self.user1.last_name)
        self.assertEquals(self.freelancer1.user.username, self.user1.username)

    def test_freelancer_skills_add(self):
        self.assertEquals(self.freelancer1.skills.all()[0].name, 'skill1')
        self.assertEquals(self.freelancer1.skills.all()[1].name, 'skill2')

    def test_freelancer_str_func(self):
        self.assertEquals(self.freelancer1.__str__(), self.user1.get_full_name())

    def test_mobile_less_equal_max_length(self):
        max_length = Freelancer._meta.get_field('mobile').max_length
        self.assertLessEqual(len(str(self.freelancer1.mobile)), max_length)

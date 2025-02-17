import random

from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum

from server.sponsors.models import Sponsor
from server.blog.models import BlogPost
from server.conferences.models import Place, Transport, Zosia
from server.lectures.models import Lecture
from server.organizers.models import OrganizerContact
from server.questions.models import QA
from server.rooms.models import Room
from server.users.models import Organization, User, UserPreferences
from server.utils.constants import FULL_DURATION_CHOICES, LECTURE_TYPE, MAX_BONUS_MINUTES, SponsorInternals, UserInternals
from server.utils.time_manager import now, time_point, timedelta_since, timedelta_since_now

FIRST_NAMES = ['Kasia', 'Marta', 'Julia', 'Ola', 'Natalia', 'Ania', 'Ewa', 'Alicja', 'Beata',
               'Dorota', 'Justyna', 'Weronika']


def create_question():
    data = {
        'question': lorem_ipsum.words(random.randint(5, 10)) + "?",
        'answer': ''.join(lorem_ipsum.paragraphs(1))[:400],
        'priority': random.randint(0, 100),
    }
    return QA.objects.create(**data)


def create_lecture(zosia, author):
    data = {
        'zosia': zosia,
        'requests': lorem_ipsum.words(60)[:750],
        'events': lorem_ipsum.words(60)[:750],
        'title': lorem_ipsum.sentence()[:255],
        'abstract': ' '.join(lorem_ipsum.paragraphs(3))[:1000],
        'duration': random.choice(FULL_DURATION_CHOICES)[0],
        'lecture_type': random.choice(LECTURE_TYPE)[0],
        'description': lorem_ipsum.words(random.randint(10, 20))[:255],
        'author': author,
        'accepted': random_bool(),
    }
    return Lecture.objects.create(**data)


def create_blogpost(author):
    data = {
        'title': lorem_ipsum.words(random.randint(5, 10)),
        'content': ''.join(lorem_ipsum.words(random.randint(10, 30)))[:500],
        'publication': now(),
        'author': author,
    }
    return BlogPost.objects.create(**data)


def random_date_before(date, range_days):
    return timedelta_since(date, days=-random.randint(1, range_days))


def create_place():
    data = {
        'name': 'Old Forest Inn',
        'url': 'http://google.com',
        'address': 'Bakery Street 23, Glasgow',
        'town': 'Glasgow'
    }
    return Place.objects.create(**data)


def create_transport(zosia):
    time = now()

    Transport.objects.create(
        zosia=zosia,
        departure_time=time_point(time.year, time.month, time.day, 16),
        capacity=45
    )

    Transport.objects.create(
        zosia=zosia,
        departure_time=time_point(time.year, time.month, time.day, 18),
        capacity=45
    )


def create_active_zosia(place, **kwargs):
    zosia_start = timedelta_since_now(days=60)
    start_date = now()
    end_date = timedelta_since(start_date, days=14)
    data = {
        'active': True,
        'place': place,
        'early_registration_start': None,
        'registration_start': start_date,
        'registration_end': end_date,
        'start_date': zosia_start,
        'rooming_start': start_date,
        'rooming_end': end_date,
        'lecture_registration_start': start_date,
        'lecture_registration_end': end_date,
        'description': 'Once upon a time there were apes',
        'price_accommodation': 50,
        'price_accommodation_breakfast': 60,
        'price_accommodation_dinner': 65,
        'price_whole_day': 70,
        'price_transport': 50,
        'price_transfer_baggage': 15,
        'account_number': 'PL59 1090 2402 4156 9594 3379 3484',
        'account_owner': 'Joan Doe',
        'account_bank': 'SuperBank',
        'account_address': 'ul. Fajna 42, 51-109, Wrocław'
    }
    data.update(kwargs)
    zosia = Zosia.objects.create(**data)
    create_transport(zosia)
    return zosia


def create_sample_staff_user():
    data = {
        'email': 'staff@example.com',
        'first_name': 'Zofia',
        'last_name': 'Ksiowa',
        'password': 'pass',
        'is_staff': True,
        'person_type': UserInternals.PERSON_PRIVILEGED,
    }

    return User.objects.create_user(**data)


def create_sample_organizer_user():
    data = {
        'email': 'organizator@example.com',
        'first_name': 'Organizator',
        'last_name': 'Ksiowy',
        'password': 'pass',
        'is_staff': False,
        'person_type': UserInternals.PERSON_ORGANIZER,
    }

    return User.objects.create_user(**data)


def create_contact_to_organizer(zosia, user):
    OrganizerContact.objects.create(
        zosia=zosia,
        user=user,
        phone_number=str(random.randint(500000000, 999999999))
    )


def random_bool():
    return random.random() < 0.5


def create_random_user_with_preferences(zosia, id):
    data = {
        'email': f'zosia{id}@example.com',
        'first_name': random.choice(FIRST_NAMES),
        'last_name': f'Testowa{id}',
        'password': 'pass',
        'person_type': UserInternals.PERSON_NORMAL,
    }
    u = User.objects.create_user(**data)

    org = Organization.objects.create(name=f"org_{id}", user=u, accepted=random_bool()) \
        if random_bool() else None

    accommodation_day_1 = random_bool()
    dinner_day_1 = random_bool() if accommodation_day_1 else False
    breakfast_day_2 = random_bool() if accommodation_day_1 else False

    accommodation_day_2 = random_bool()
    dinner_day_2 = random_bool() if accommodation_day_2 else False
    breakfast_day_3 = random_bool() if accommodation_day_2 else False

    accommodation_day_3 = random_bool()
    dinner_day_3 = random_bool() if accommodation_day_3 else False
    breakfast_day_4 = random_bool() if accommodation_day_3 else False

    phone_number = f'+48 {random.randint(100, 999)} {random.randint(100, 999)} ' \
                   f'{random.randint(100, 999)}'
    transport = random.choice(Transport.objects.find_with_free_places(zosia)) if random_bool() else None

    payment_acc = random_bool()
    bonus = random.randint(1, MAX_BONUS_MINUTES) if payment_acc else 0

    is_student = id % 2 == 1
    student_number = random.randint(100000, 999999) if is_student else ''

    discount_round = 0
    if is_student:
        # Not all student get a discounts
        discount_round = random.randint(0, 3)

    UserPreferences.objects.create(
        user=u,
        zosia=zosia,
        organization=org,
        transport=transport,
        accommodation_day_1=accommodation_day_1,
        dinner_day_1=dinner_day_1,
        accommodation_day_2=accommodation_day_2,
        breakfast_day_2=breakfast_day_2,
        dinner_day_2=dinner_day_2,
        accommodation_day_3=accommodation_day_3,
        breakfast_day_3=breakfast_day_3,
        dinner_day_3=dinner_day_3,
        breakfast_day_4=breakfast_day_4,
        contact=phone_number,
        payment_accepted=payment_acc,
        bonus_minutes=bonus,
        is_student=is_student,
        student_number=student_number,
        terms_accepted=True,
        discount_round=discount_round,
    )
    return u


def create_room(number, hidden):
    if random.random() < 0.1:
        data = {
            'name': f"Nr. {number}",
            'description': lorem_ipsum.words(random.randint(3, 6)),
            'beds_double': 1,
            'available_beds_double': 1,
            'hidden': hidden,
        }
    else:
        bed_single = random.randint(2, 6)
        data = {
            'name': f"Nr. {number}",
            'description': lorem_ipsum.words(random.randint(3, 6)),
            'beds_single': bed_single,
            'available_beds_single': random.randint(2, bed_single),
            'hidden': hidden,
        }
    return Room.objects.create(**data)


def create_sponsor(number):
    sponsor_type = random.choice(
        [SponsorInternals.TYPE_BRONZE,
         SponsorInternals.TYPE_SILVER,
         SponsorInternals.TYPE_GOLD])

    logo_path = 'https://s3.amazonaws.com/freebiesupply/large/2x/google-logo-transparent.png' if random.random() < 0.5 else None

    data = {
        'name': f"Sponsor {number}",
        'is_active': True,
        'url': 'http://google.com',
        'path_to_logo': logo_path,
        'sponsor_type': sponsor_type,
    }
    return Sponsor.objects.create(**data)


class Command(BaseCommand):
    help = 'Create custom data in database'

    def handle(self, *args, **kwargs):
        if Zosia.objects.filter(active=True).count() > 0:
            self.stdout.write('\033[1;91mThere is already active ZOSIA in database.'
                              '\033[0m Do you want to create data anyway? [y/n]')
            choice = input().lower()
            if choice not in {'yes', 'y'}:
                return

        place = create_place()
        self.stdout.write('Place for ZOSIA has been created!')

        zosia = create_active_zosia(place)
        self.stdout.write('Active ZOSIA has been created!')

        all_users = []

        sample_staff_user = create_sample_staff_user()
        all_users.append(sample_staff_user)
        self.stdout.write('Sample staff user has been created')

        sample_organizer_user = create_sample_organizer_user()
        all_users.append(sample_organizer_user)
        self.stdout.write('Sample organizer has been created')

        create_contact_to_organizer(zosia, sample_organizer_user)
        self.stdout.write('Contact to sample organizer created')

        user_num = 15
        for i in range(1, user_num + 1):
            user_with_prefs = create_random_user_with_preferences(zosia, i)
            self.stdout.write(f"Created random user #{i}")
            all_users.append(user_with_prefs)

        lectures_num = 5
        for i in range(1, lectures_num + 1):
            author = random.choice(all_users)
            create_lecture(zosia, author)
            self.stdout.write(f"Created lecture #{i}")

        blogposts_num = 5
        for i in range(1, blogposts_num + 1):
            create_blogpost(sample_staff_user)
            self.stdout.write(f"Created blogpost #{i}")

        question_num = random.randint(3, 10)
        for i in range(1, question_num + 1):
            create_question()
            self.stdout.write(f"Created question #{i}")

        room_num = random.randint(10, 25)
        for i in range(1, room_num + 1):
            create_room(i, False)
            self.stdout.write(f"Created room #{i}")

        hidden_room_num = random.randint(1, 4)
        for i in range(100, hidden_room_num + 100):
            create_room(i, True)
            self.stdout.write(f"Created hidden room #{i}")

        sponsor_num = random.randint(5, 10)
        for i in range(1, sponsor_num + 1):
            create_sponsor(i)
            self.stdout.write(f"Created sponsor #{i}")

        self.stdout.write(self.style.SUCCESS('Database has been filled with some data!'))

import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from shop.models import Product , ProductCategory ,ProductStatusType
from accounts.models import User,UserType
from pathlib import Path
from django.core.files import File
 

BASE_DIR= Path(__file__).resolve().parent

class Command(BaseCommand):
    help='Generate fake products'

    def handle(self , *args , **kwargs):
        fake=Faker(locale="fa_IR")
        user=User.objects.get(type=UserType.admin.value)

        image_list=[
            "./images/image 1.jpeg",
            "./images/image 2.jpeg",
            "./images/image 3.jpeg",
            "./images/image 4.jpeg",
            "./images/image 5.jpeg",
            "./images/image 6.jpeg",
            "./images/image 7.jpeg",
            "./images/image 8.jpg",
            "./images/image 9.jpeg",
            "./images/image 10.jpeg",


        ]

        categories=ProductCategory.objects.all()

        for _ in range(10):
            user=user
            num_categories = random.randint(1,4)
            selected_categories = random.sample(list(categories) , num_categories)
            title = ' '.join([fake.word() for _ in range(1,3)])
            slug=slugify(title, allow_unicode=True)
            selected_image = random.choice(image_list)
            image_obj = File(file=open(BASE_DIR / selected_image, "rb") , name=Path(selected_image).name)
            description = fake.paragraph(nb_sentences=0)
            brief_description =  fake.paragraph(nb_sentences=1)
            stock = fake.random_int(min=0 , max=10)
            status = random.choice(ProductStatusType.choices)[0]
            price = fake.random_int(min=100000 , max=100000)
            discount_percent = fake.random_int(min=0 , max=50)

            product = Product.objects.create(
                user=user,
                title=title,
                slug=slug,
                image=image_obj,
                description=description,
                brief_description=brief_description,
                stock=stock,
                status=status,
                price=price,
                discount_percent=discount_percent,
            )

            product.category.set(selected_categories)
            self.stdout.write(self.style.SUCCESS(
                'Successfully generated 10 fake products.'))
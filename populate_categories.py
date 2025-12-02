import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timebank.settings')
django.setup()

from mainapp.models import Category

# Define categories to create
categories_data = [
    {
        'category_name': 'Technology & IT',
        'description': 'Web development, programming, software, IT support, and technical services'
    },
    {
        'category_name': 'Education & Tutoring',
        'description': 'Academic tutoring, language lessons, music lessons, and educational services'
    },
    {
        'category_name': 'Arts & Crafts',
        'description': 'Painting, drawing, crafts, pottery, and creative artistic services'
    },
    {
        'category_name': 'Health & Wellness',
        'description': 'Yoga, fitness training, nutrition advice, and wellness coaching'
    },
    {
        'category_name': 'Home & Garden',
        'description': 'Gardening, home repairs, cleaning, organization, and maintenance'
    },
    {
        'category_name': 'Business & Professional',
        'description': 'Consulting, marketing, accounting, legal advice, and business services'
    },
    {
        'category_name': 'Creative Services',
        'description': 'Graphic design, video editing, photography, writing, and content creation'
    },
    {
        'category_name': 'Music & Performance',
        'description': 'Music lessons, singing, dance, theater, and performance arts'
    },
    {
        'category_name': 'Cooking & Food',
        'description': 'Cooking classes, meal prep, baking, and culinary services'
    },
    {
        'category_name': 'Transportation',
        'description': 'Rides, delivery, moving assistance, and transportation services'
    },
    {
        'category_name': 'Childcare & Elderly Care',
        'description': 'Babysitting, tutoring, elderly assistance, and caregiving services'
    },
    {
        'category_name': 'Pet Services',
        'description': 'Pet sitting, dog walking, grooming, and pet care'
    },
    {
        'category_name': 'Sports & Fitness',
        'description': 'Personal training, sports coaching, and fitness activities'
    },
    {
        'category_name': 'Language & Translation',
        'description': 'Language teaching, translation, interpretation services'
    },
    {
        'category_name': 'Other Services',
        'description': 'Miscellaneous services that don\'t fit other categories'
    }
]

# Create categories
created_count = 0
existing_count = 0

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        category_name=cat_data['category_name'],
        defaults={'description': cat_data['description']}
    )
    if created:
        created_count += 1
        print(f"✅ Created: {category.category_name}")
    else:
        existing_count += 1
        print(f"ℹ️  Already exists: {category.category_name}")

print(f"\n📊 Summary:")
print(f"   Created: {created_count}")
print(f"   Already existed: {existing_count}")
print(f"   Total categories: {Category.objects.count()}")
print(f"\n✨ Categories populated successfully!")

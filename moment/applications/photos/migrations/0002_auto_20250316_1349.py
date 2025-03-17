from datetime import timedelta
import random
from django.db import migrations
from django.utils import timezone
from django.core.files.base import ContentFile
from PIL import Image
import io

def create_mock_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Tag = apps.get_model('photos', 'Tag')
    Photo = apps.get_model('photos', 'Photo')
    PhotoRating = apps.get_model('photos', 'PhotoRating')
    Location = apps.get_model('photos', 'Location')

    # 创建测试用户
    test_user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    print(test_user)

    # 创建标签
    tags = [
        Tag.objects.create(name='风景'),
        Tag.objects.create(name='人像'),
        Tag.objects.create(name='美食'),
        Tag.objects.create(name='建筑'),
        Tag.objects.create(name='自然')
    ]

    # 创建位置
    locations = [
        Location.objects.create(
            name='西湖',
            latitude=30.2590,
            longitude=120.1485
        ),
        Location.objects.create(
            name='故宫',
            latitude=39.9163,
            longitude=116.3972
        ),
        Location.objects.create(
            name='长城',
            latitude=40.4319,
            longitude=116.5704
        )
    ]

    # 创建测试图片
    def create_test_image():
        img = Image.new('RGB', (800, 600), color='red')
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        return ContentFile(img_io.getvalue())

    photos = []
    for i in range(5000):
        random_date = timezone.now() - timedelta(days=random.randint(0, 365*10))
        photo = Photo.objects.create(
            title=f'测试照片 {i+1}',
            description=f'这是第 {i+1} 张测试照片的描述',
            file_path=f'test_photo_1.jpg',
            thumbnail_path=f'test_thumbnail_1.jpg',
            upload_time=timezone.now(),
            taken_time=random_date,
            size=1024*1024,  # 1MB
            width=800,
            height=600,
            format='JPEG',
            rating=4.5
        )
        photo.tags.add(tags[i % len(tags)])
        photo.locations.add(locations[i % len(locations)])
        photos.append(photo)

    # 创建评分
    for photo in photos:
        PhotoRating.objects.create(
            photo=photo,
            user=test_user,
            rating=4.5,
            comment=f'这是一张很棒的照片！'
        )

def remove_mock_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Tag = apps.get_model('photos', 'Tag')
    Photo = apps.get_model('photos', 'Photo')
    PhotoRating = apps.get_model('photos', 'PhotoRating')
    Location = apps.get_model('photos', 'Location')

    User.objects.filter(username='testuser').delete()
    Tag.objects.all().delete()
    Photo.objects.all().delete()
    PhotoRating.objects.all().delete()
    Location.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_mock_data, remove_mock_data),
    ]
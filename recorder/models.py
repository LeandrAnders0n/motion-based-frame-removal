# python manage.py makemigrations; python manage.py migrate
# python manage.py runserver
# delete from recorder_cameras; delete from recorder_video_stats; delete from recorder_contact;

from django.db import models
from django.utils import timezone

class Cameras(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    active_status = models.CharField(max_length=20)
    save_frequency = models.IntegerField(default=0)
    preferred_quality = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Video_Stats(models.Model):
    camera = models.ForeignKey(Cameras, on_delete=models.CASCADE)
    file = models.TextField()
    original_size = models.BigIntegerField(default=0)
    optimized_size = models.BigIntegerField(default=0)
    motion = models.DecimalField(max_digits=5, decimal_places=2, default=0)

class Contact(models.Model):
    subject = models.CharField(max_length=100)
    body = models.TextField()
    ref_id = models.TextField()

def initData():
        camera1 = Cameras.objects.create(name='Camera 1', description='This is the first camera', active_status='Active', save_frequency=60, preferred_quality=90)
        camera2 = Cameras.objects.create(name='Camera 2', description='This is the second camera', active_status='Inactive', save_frequency=120, preferred_quality=80)
        camera3 = Cameras.objects.create(name='Camera 3', description='This is the third camera', active_status='Active', save_frequency=180, preferred_quality=70)
        camera1.save()
        camera2.save()
        camera3.save()

        data1 = Video_Stats(
                camera_id=camera1.id,
                file='2022-12-15 12-00-00.webm',
                original_size=1000000000,
                optimized_size=500000000,
                motion=0.50,
        )
        data2 = Video_Stats(
                camera_id=camera2.id,
                file='2022-09-20 00-00-00.webm',
                original_size=2400000000,
                optimized_size=300000000,
                motion=0.9,
        )
        data3 = Video_Stats(
                camera_id=camera3.id,
                file='2022-01-12 15-00-00.webm',
                original_size=3000000000,
                optimized_size=10120000,
                motion=0.7,
        )
        data4 = Video_Stats(
                camera_id=camera3.id,
                file='2020-02-25 10-00-00.webm',
                original_size=2900000000,
                optimized_size=112000000,
                motion=0.4,
        )
        data5 = Video_Stats(
                camera_id=camera2.id,
                file='2021-03-30 18-00-00.webm',
                original_size=500000000,
                optimized_size=240000,
                motion=0.1,
        )
        data6 = Video_Stats(
                camera_id=camera1.id,
                file='2021-05-12 18-00-00.webm',
                original_size=9000000000,
                optimized_size=820000000,
                motion=0.85,
        )
        data7 = Video_Stats(
                camera_id=camera1.id,
                file='2020-01-22 15-00-00.webm',
                original_size=2200000000,
                optimized_size=250000000,
                motion=0.30,
        )
        data8 = Video_Stats(
                camera_id=camera1.id,
                file='2023-04-24 20-20-37.webm',
                original_size=1000000000,
                optimized_size=200000000,
                motion=0.20,
        )
        data9 = Video_Stats(
                camera_id=camera1.id,
                file='2023-03-01 23-00-00.webm',
                original_size=22000000000,
                optimized_size=90000000,
                motion=0.9,
        )
        data10 = Video_Stats(
                camera_id=camera3.id,
                file='2022-07-01 21-00-00.webm',
                original_size=8500000000,
                optimized_size=75000000,
                motion=0.55,
        )
        data11 = Video_Stats(
                camera_id=camera2.id,
                file='2022-12-31 22-00-00.webm',
                original_size=7000000000,
                optimized_size=575000000,
                motion=0.7,
        )
        data12 = Video_Stats(
                camera_id=camera3.id,
                file='2022-11-30 10-00-00.webm',
                original_size=3000000000,
                optimized_size=250000000,
                motion=0.25,
        )
        data1.save()
        data2.save()
        data3.save()
        data4.save()
        data5.save()
        data6.save()
        data7.save()
        data8.save()
        data9.save()
        data10.save()
        data11.save()
        data12.save()

# initData()
from django.shortcuts import render, redirect
from django.db.models import Sum, Avg
from .models import *
import time
import datetime
import cv2
import os
from django.conf import settings
from recorder.models import Video_Stats
import struct
from moviepy.video.io.VideoFileClip import VideoFileClip

# Dashboard
def lobby(request, filter='0'):
    # video = VideoFileClip('public/optimized/2023-04-25 18-48-46.webm')
    # duration = video.duration
    # video.close()
    # print("duration");
    # print(duration);


    if (filter == '0'):
        cameras = Cameras.objects.values('id', 'name').first()
    else:
        cameras = Cameras.objects.values('id', 'name').filter(id=filter).first()

    count = Cameras.objects.count()
    sum_optimized_size = Video_Stats.objects.aggregate(Sum('optimized_size'))['optimized_size__sum']
    sum_original_size = Video_Stats.objects.aggregate(Sum('original_size'))['original_size__sum']
    sum_motion = Video_Stats.objects.aggregate(Avg('motion'))['motion__avg']
    cameras_list = Cameras.objects.all()

    context = {
        'camera_count': count,
        'raw_storage': round(sum_original_size / (1024 * 1024 * 1024), 2),
        'storage': round(sum_optimized_size / (1024 * 1024 * 1024), 2),
        'optimized_perc': 100 - round((sum_optimized_size / sum_original_size) * 100, 2),
        'motion': round(sum_motion, 2),
        'cameras_list': cameras_list,
        'filter': cameras
    }
    return render(request, 'index.html', context=context)


# Webcam record | Modify it
def webcam(request):
    if request.method == 'POST' and request.FILES['video']:

        video_file = request.FILES['video']
        camera_id = request.POST.get('camera_id')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

        with open('public/raw/' + timestamp + '.webm', 'wb') as f:
            f.write(video_file.read())
            # pass camera_id from front-end
        
        camera_id = request.POST.get('camera_id', 'default_value')

    optimize(request,timestamp,camera_id)
    return render(request, 'webcam.html')


#optimize video and remove frames
def optimize(request,filename,camera_id):
        # Load the video capture object
    cap = cv2.VideoCapture('public/raw/' + filename + '.webm')
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Check if the video capture object was initialized correctly
    if not cap.isOpened():
        print("Error opening video stream or file")
    # Get the video frame dimensions
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    # Define the codec and create the video writer object
    fourcc = cv2.VideoWriter_fourcc(*'VP90')
    out = cv2.VideoWriter('public/optimized/' + filename + '.webm', fourcc, fps, (frame_width, frame_height))
    # Set the previous frame to None
    prev_frame = None
    # Start reading frames from the video
    # total_duration = cap.get(cv2.CAP_PROP_POS_MSEC)
    cap.set(cv2.CAP_PROP_POS_MSEC, 0)

    cap.set(cv2.CAP_PROP_FPS, fps)

    num_frames_read = 0
    # Start reading frames from the video
    while True:
        # Read the next frame
        ret, frame = cap.read()
        # Check if we've reached the end of the video
        if not ret:
            break

        num_frames_read = num_frames_read + 1
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Check if the previous frame is None
        if prev_frame is None:
            prev_frame = gray
            continue
        # Calculate the absolute difference between the current and previous frames
        diff = cv2.absdiff(prev_frame, gray)
        # Threshold the difference to get a binary mask
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        # Calculate the number of white pixels in the mask
        white_pixels = cv2.countNonZero(thresh)
        # If there are fewer than 1000 white pixels in the mask, it means the frame is redundant
        if white_pixels < 1000:
            continue
        # Write the non-redundant frame to the output video
        out.write(frame)
        # Set the current frame to be the previous frame for the next iteration
        prev_frame = gray
 
    # Release the video capture and video writer objects
    cap.release()

    cap = cv2.VideoCapture('public/optimized/' + filename + '.webm')
    total_duration = num_frames_read / fps
    total_duration_int = num_frames_read // fps

    with open("output.bin", "wb") as f:
        ebml_header = b'\x1a\x45\xdf\xa3'
        segment = b'\x42\x86\x81\x01'
        seek_head = b'\x42\xf7\x81\x01\x00\x00\x00\x00'
        segment_info = b'\x42\xf2\x81\x04\x00\x00\x00\x02'
        duration = b'\x44\x87\x81\x00' + struct.pack(">Q", int(total_duration_int))
        date_utc = b'\x44\x89\x81\x00\x00\x00\x00\x00'
        title = b'\x4d\x80\x67' + struct.pack(">H", len(filename)) + filename.encode('ascii')
        video = b'\x44\x7c\xb5\x00\x00\x00\x00\x00\x00\x00\x00\x22\xb5\x9c\x80'
        pixel_width = b'\x88\x83\x83\x82\x00' + struct.pack(">H", frame_width)
        pixel_height = b'\x88\x83\x83\x83\x00' + struct.pack(">H", frame_height)
        codec_id = b'\x9a\x22\xb5\x9c\x80\x00\x00\x00\x00'
        codec_name = b'\x86\x48\x83\x81\x01'
        # optimized_size = b'\x9b\x84\x80\x00\x00\x00\x00\x00' + struct.pack(">Q", optimized_size)

        f.write(ebml_header + segment + seek_head + segment_info + duration + date_utc + title + video + pixel_width + pixel_height + codec_id + codec_name + video)

        
    out.release()
    # Close all the windows
    cv2.destroyAllWindows()
    #add details of file to db
    #get file sizes
    original_size =os.path.getsize('public/raw/' + filename + '.webm')
    optimized_size = os.path.getsize('public/optimized/' + filename + '.webm')

    # get time
    diff = abs(original_size-optimized_size)
    motion = (round((diff/original_size),2))
    print(motion)

    stats = Video_Stats()
    stats.camera_id = camera_id
    stats.file = filename
    stats.original_size = original_size
    stats.optimized_size = optimized_size
    stats.motion = motion
    stats.save()
    print('done')
    return render(request, 'webcam.html')


# Contact us
def contact(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        description = request.POST.get('description')

        currTime = str(time.time())[:10]
        contact = Contact()
        contact.subject = subject
        contact.body = description
        contact.ref_id = currTime
        contact.save()

        context = {'ref_id': currTime}
        return render(request, 'ticket.html', context=context)
    else:
        return render(request, 'ticket.html')


# All raised tickets
def all_tickets(request):
    data = Contact.objects.all()
    for obj in data:
        obj.datetime = datetime.datetime.fromtimestamp(int(obj.ref_id))

    context = {'data': data}
    return render(request, 'tickets.html', context=context)


# Insert / modify camera
def camera(request, id=0):
    if request.method == 'POST':

        name = request.POST.get('camera_name')
        description = request.POST.get('camera_description')
        active_status = request.POST.get('active_status')
        save_frequency = request.POST.get('save_frequency')
        preferred_quality = request.POST.get('preferred_quality')

        if (id == 0):
            cameras = Cameras()
            cameras.name = name
            cameras.description = description
            cameras.active_status = active_status
            cameras.save_frequency = save_frequency
            cameras.preferred_quality = preferred_quality
            cameras.created_at = timezone.now()
            cameras.save()

        else:
            cameras = Cameras()
            cameras.id = id
            cameras.name = name
            cameras.description = description
            cameras.active_status = active_status
            cameras.save_frequency = save_frequency
            cameras.preferred_quality = preferred_quality
            cameras.created_at = timezone.now()
            cameras.save()

        context = {'camera_name': name}
        return render(request, 'camera.html', context=context)
    else:

        if (id == 0):
            return render(request, 'camera.html')
        else:
            data = Cameras.objects.filter(id=id).first()
            context = {'data': data}
            return render(request, 'camera.html', context=context)

# Delete camera
def camera_del(request, id=0):
    camera = Cameras.objects.get(id=id)
    camera.delete()
    return redirect('cameras')

# Camera list
def cameras(request):
    cameras = Cameras.objects.all()

    context = {'data': cameras}
    return render(request, 'cameras.html', context=context)

# Statistics
def data(request, filter='0'):
    cameras = Cameras.objects.all().values('id', 'name')
    if (filter == "0"):
        data = Video_Stats.objects.all()
    else:
        data = Video_Stats.objects.filter(camera_id=filter)

    context = {
        'data': data,
        'cameras': cameras,
        'filter': int(filter),
    }
    return render(request, 'data.html', context=context)

# Video page
def video(request,id):
    try:
        video = Video_Stats.objects.get(id=id)
        print(video.__dict__)
        filename = video.file+'.webm'
    except Video_Stats.DoesNotExist:
        video = None
    # context = {'data': 'video','video_url': 'filename'}
   
    # video_path = os.path.join(settings.MEDIA_ROOT, 'public/raw', filename)
    context = {'video_path': os.path.join(settings.MEDIA_URL, filename),'data':video}

    return render(request, 'video.html', context=context)
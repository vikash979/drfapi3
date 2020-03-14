#this class will hold the service logic for content
from content.models import Lecture
import datetime as dt
from datetime import timedelta
from institute.models import Batch, Phase
from common.choices import ObjectStatusChoices
import requests
import json

#d={'lectures': 1, 'duration': 2, 'time': '10:00', 'phase_id': '1', 'subject_id': '1', 'batches': ['1'], 'start_date': '2020-01-01'}
#from content.service import *
#create_lectures(**d)
def create_lectures(*args,**kwargs):
	classs_id = kwargs.get('classs_id')[0]
	subject_id = kwargs.get('subject_id')[0]
	session_id = kwargs.get('session_id')[0]
	program_id = kwargs.get('program_id')[0]
	no_of_lectures = kwargs.get('lectures')[0]
	duration = kwargs.get('duration')[0]
	time = kwargs.get('time')[0]
	phase_id = kwargs.get('phase_id')[0]
	batches = kwargs.get('batches')[0].split(",")
	# batches = get_batches(batches,phase_id)

	for batch in batches:
		last_lecture = Lecture.objects.filter(batch_id = batch)
		if last_lecture.exists():
			start_date_time = last_lecture.last().start_date_time
			start_date_time = get_next_eligible_date(start_date_time) 
			
		else: 
			start_date_time = get_date_time(Phase.objects.get(pk=phase_id).start_date, time)
			
		for lecture_counter in range(int(no_of_lectures)):
			create_lecture(classs_id, subject_id, session_id, program_id, phase_id, batch, \
				start_date_time, duration)
			start_date_time = get_next_eligible_date(start_date_time) 
			

# def get_batches(batches,phase_id):
# 	if 'all' in batches:
# 		batches = Batch.objects.filter(phase_id=phase_id).values_list('id',flat=True)
# 	return batches

def get_next_eligible_date(date_time,delta=1):
	'''
	This will provide the next working day skipping sunday
	'''
	if date_time.weekday() == 5:
		delta += 1
	return date_time + timedelta(delta)

def get_date_time(date,time):
	mydate = date#dt.datetime.strptime(date, "%Y-%m-%d")
	mytime = dt.datetime.strptime(time,'%H:%M').time()
	return dt.datetime.combine(mydate, mytime)

def create_lecture(classs_id, subject_id, session_id, program_id, phase_id, batch_id,start_date_time,duration):
	Lecture.objects.create(classs_id=classs_id, is_tentative=True, subject_id=subject_id, session_id=session_id, program_id=program_id, phase_id=phase_id, batch_id=batch_id, \
		start_date_time=start_date_time,duration_hrs=duration, object_status=ObjectStatusChoices.ACTIVE)


def doc_to_html(path,contentid,toc_type):
	files = {'content_file': open(path,'rb')}
	data={"content_id":contentid,"content_type":toc_type}
	url = "http://3.7.9.110:8000/api/v1/student_content"
	html_request = requests.post(url, files=files,data=data)
	return "completed"
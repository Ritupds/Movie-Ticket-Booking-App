from celery import shared_task
import requests
import json
from datetime import datetime
from models import User,Venue



@shared_task
def monthly_report():
    print("Monthly report task started")
    return True

@shared_task
def Daily_remainder():
    users=User.query.all()
    for user in users:
        response=requests.post("https://chat.googleapis.com/v1/spaces/AAAAOwSzyCM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=m_WAZWPIrHGCTlmjuzQsaZ8nkX36DfkTgAy9fntlPqs",data=json.dumps({"text":f"Hi{user.name},Have you booked your tickets for today's show?"}))
    return response.ok


@shared_task    
def UserTriggered_Job():
    venues=Venue.query.all()
    with open("venue.csv","w") as f:
        f.write("Name","Place","City","Capacity")
        for venue in venues:
            f.write(f"{venue.name},{venue.place},{venue.city},{venue.capacity}\n")
    return True        
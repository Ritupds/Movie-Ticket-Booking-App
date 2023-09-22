from celery import Celery,Task
from flask import Flask

def celery_init_app(app:Flask) -> Celery:
    class ContextTask(Task):
        def __call__(self,*args:object,**kwargs:object) -> object: 
            with app.app_context():
                return self.run(*args,**kwargs)
            
    my_celery_app=Celery(app.name,task_cls=ContextTask)
    my_celery_app.conf.broker_url="redis://localhost:6379/1"
    my_celery_app.conf.result_backend="redis://localhost:6379/2"
    my_celery_app.conf.timezone="Asia/Kolkata"
    my_celery_app.set_default()
    app.extensions["celery"]=my_celery_app
    return my_celery_app        
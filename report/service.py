from saas_com.core.service import get_content_type
from .repository import ReportRepo
from django.contrib.auth import get_user_model
from jobs.models import Job
from apps.models import App
from discussion.models import Discussion
from saas_com.core.exceptions import PermissionDenied , AlreadyExists , InvalidContentType , InvalidForm ,  ObjectNotFound

User = get_user_model()

class ReportService:
    repo = ReportRepo()
    CONTENT_TYPES = {
        "user":User,
        "app":App,
        "job":Job,
        "discussion":Discussion
    }

    def get_report(self , id):
        return self.repo.get_report(id = id)
    
    def get_reports(self , content_type , object_id):
        content_type = get_content_type(content_type , self.CONTENT_TYPES)
        return self.repo.get_reports(content_type , object_id)
    
    def has_user_report(self ,content_type ,  object_id , reporter):
        content_type = get_content_type(content_type , self.CONTENT_TYPES)
        return self.repo.has_user_report(content_type = content_type , object_id = object_id , reporter =  reporter)

    def add_report(self , reporter , content_type , id , form):

        content_object = self.CONTENT_TYPES[content_type].objects.filter(id = id).first()

        if content_object and content_object.user == reporter:
            raise PermissionDenied("You can't report on your {}".format(content_type))
        
        elif not content_type:
            raise ObjectNotFound(f"{content_type} not found")
        
        if self.has_user_report(content_type , object_id = id , reporter = reporter):
            raise AlreadyExists("You already report on this {}".format(content_type))
        
        content_type = get_content_type(content_type , self.CONTENT_TYPES)
        if form.is_valid():
            reason = form.cleaned_data.get("reason" , None)
            report_type = form.cleaned_data.get("report_type")
            return self.repo.add_report(reporter = reporter, content_type = content_type, id = id, reason = reason , report_type = report_type)
        raise InvalidForm("Invalid form data.")
    
    def del_report(self , id , user):
        report = self.get_report(id = id)
        if report.reporter == user:
            return self.repo.del_report(report)
        raise PermissionDenied("You can\'t delete this report")
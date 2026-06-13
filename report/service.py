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
    
    def get_reports(self , content_type_str , object_id):
        content_type_obj = get_content_type(content_type_str , self.CONTENT_TYPES)
        return self.repo.get_reports(content_type_obj , object_id)
    
    def has_user_report(self ,content_type_str ,  object_id , reporter):
        content_type_obj = get_content_type(content_type_str , self.CONTENT_TYPES)
        return self.repo.has_user_report(content_type = content_type_obj , object_id = object_id , reporter =  reporter)

    def add_report(self , reporter , content_type_str , id , form):
        
        # Validation phase
        content_type_obj = get_content_type(content_type_str , self.CONTENT_TYPES)

        if not form.is_valid():
            raise InvalidForm(form.errors)

        content_object = content_type_obj.model_class().objects.filter(id = id).first()

        if not content_object:
            raise ObjectNotFound(f"{content_type_str} not found")
        
        if isinstance(content_object , User):
            if content_object == reporter:
                raise PermissionDenied("You can't report on your profile")

        if hasattr(content_object , "user"):
            if content_object.user == reporter:
                raise PermissionDenied(f"You can't report on your {content_type_str}")
        
        if self.has_user_report(content_type_str , object_id = id , reporter = reporter):
            raise AlreadyExists(f"You have already reported this {content_type_str}")
        
        # Adding new report
        reason = form.cleaned_data.get("reason" , None)
        report_type = form.cleaned_data.get("report_type")
        return self.repo.add_report(reporter = reporter, content_type = content_type_obj , id = id, reason = reason , report_type = report_type)
    
    def del_report(self , id , user):
        report = self.get_report(id = id)
        if report.reporter == user:
            return self.repo.del_report(report)
        raise PermissionDenied("You can\'t delete this report")
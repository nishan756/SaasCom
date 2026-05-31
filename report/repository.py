from .models import Report
from saas_com.core.exceptions import ObjectNotFound

class ReportRepo:

    def get_report(self , id):
        try:
            return Report.objects.get(id = id)
        except Report.DoesNotExist:
            raise ObjectNotFound("Report not found")
    
    def get_reports(self , content_type , object_id):
        return Report.objects.filter(content_type = content_type , object_id = object_id)
    
    def has_user_report(self ,content_type , object_id , reporter):
        return Report.objects.filter(content_type = content_type , reporter = reporter , object_id = object_id).first()
    
    def add_report(self , reporter , report_type , content_type , id , reason = None):
        new_report = Report(
            reporter = reporter,
            content_type = content_type,
            object_id = id,
            reason = reason if reason else None,
            report_type = report_type
        )
        new_report.save()
    
    def del_report(self , report):
        report.delete()
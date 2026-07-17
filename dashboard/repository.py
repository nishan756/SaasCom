from discussion.models import Discussion
from discussion.service import DiscussionService
from comment.service import CommentService
from report.service import ReportService
from django.db.models import Count , Q
from bookmark.service import BookmarkService
from jobs.service import JobService
from jobs.models import Application

class DiscussionDashboardRepo:

    def main_dashboard(self , user , **query_param):
        discussions = Discussion.objects.prefetch_related("comments" , "tags" , "votes" , "reports").filter(user = user)

        date_from = query_param.get("date_from" , None)
        date_to = query_param.get("date_to" , None)
        title = query_param.get("title" , None)

        if date_from and date_to:
            discussions = discussions.filter(posted_at__gte = date_from , posted_at__lte = date_to)
        
        elif date_from:
            discussions = discussions.filter(posted_at__gte = date_from)
        
        elif date_to:
            discussions = discussions.filter(posted_at__lte = date_to)
        
        if title:
            discussions = discussions.filter(title__icontains = title)
        
        # Total discussions
        stats = discussions.aggregate(
            total_discussions = Count("id" , distinct = True),
            total_comments = Count("comments" , distinct = True),
            direct_comments = Count("comments" , filter = Q(comments__parent__isnull = True) , distinct = True),
            total_replies = Count("comments" , filter = Q(comments__parent__isnull = False) , distinct = True),
            total_reports = Count("reports" , distinct = True),

            total_votes = Count("votes" , distinct = True),
            total_upvote = Count("votes" , filter = Q(votes__vote_type = "upvote") , distinct = True),
            total_downvote = Count("votes" , filter = Q(votes__vote_type = "downvote") , distinct = True)
        )
        
        return {
            "stats": stats,
            "discussions": discussions
        }
    
    def discussion_stats_component(self , id , **query_param):

        comments = CommentService().get_comments("discussion" , id , **query_param)

        comment_stats = comments.aggregate(
            total_comment = Count("id" , distinct = True),
            direct_comment = Count("id" , distinct = True , filter = Q(parent__isnull = True)),
            total_replies = Count("id" , distinct = True , filter = Q(parent__isnull = False)),
        )

        reports = ReportService().get_reports("discussion" , id , **query_param)

        report_stats = reports.aggregate(
            total_report = Count("id" , distinct = True),
        )

        report_stats_by_category = reports.values("report_type").annotate(
            total_report = Count("id"),
        )

        bookmark_stats = BookmarkService().get_object_bookmarks("discussion" , id , **query_param).aggregate(
            total_bookmark = Count("id" , distinct = True)
        )

        return {
            "comment_stats":comment_stats , 
            "report_stats":report_stats,
            "comments":comments,
            "reports":reports,
            "bookmark_stats":bookmark_stats,
            "report_stats_by_category":report_stats_by_category
        }


class JobDashboardRepo:

    def main_dashboard(self , user , page , **query_param):
        jobs = JobService().get_user_jobs(user , page , **query_param)

        stats = jobs.object_list.aggregate(
            total_job = Count("id" , distinct = True),
            total_active_job = Count("id" , filter = Q(is_active = True) , distinct = True),
            total_inactive_job = Count("id" , filter = Q(is_active = False) , distinct = True),
        )

        application_stats = jobs.object_list.prefetch_related("applications").aggregate(
            total_application = Count("applications" , distinct = True),
        )

        for stat in application_stats:
            stats[stat] = application_stats[stat]
        
        return {
            "stats":stats,
            "jobs":jobs
        }

    def job_stats(self):
        pass


class ApplicationDashboardRepo:

    def main_dashboard(self , user , **query_param):
        applications = Application.objects.select_related("job" , "job__user" , "job__category").filter(user = user)
        
        # Query
        date_from = query_param.get("date_from" , None)
        date_to = query_param.get("date_to" , None)

        if date_from and date_to:
            applications = applications.filter(applied_at__gte = date_from , applied_at__lte = date_to)
        
        elif date_from:
            applications = applications.filter(applied_at__gte = date_from)
        
        elif date_to:
            applications = applications.filter(applied_at__lte = date_to)

        
        stats = applications.aggregate(

            # By Status
            total_active_application = Count("id" , filter = Q(status__in = {"pending" , "under_review" , "shortlisted" , "interview_scheduled"})),
            total_application = Count("id" , distinct = True),
            total_pending=Count("id", filter=Q(status="pending")),
            total_under_review=Count("id", filter=Q(status="under_review")),
            total_shortlisted=Count("id", filter=Q(status="shortlisted")),
            total_interview_scheduled=Count("id", filter=Q(status="interview_scheduled")),
            total_offered=Count("id", filter=Q(status="offered")),
            total_hired=Count("id", filter=Q(status="hired")),
            total_rejected_by_employer=Count("id", filter=Q(status="rejected_by_employer")),
            total_rejected_by_hr=Count("id", filter=Q(status="rejected_by_hr")),
            total_withdrawn=Count("id", filter=Q(status="withdrawn")),

            # By Job Type
            total_full_time = Count("id" , filter = Q(job__job_type = 'full_time')),
            total_intern = Count("id" , filter = Q(job__job_type = 'intern')),
            total_part_time = Count("id" , filter = Q(job__job_type = 'part_time')),
            total_contract = Count("id" , filter = Q(job__job_type = 'contract')),
            total_remote = Count("id" , filter = Q(job__job_type = 'remote')),
            total_hybrid = Count("id" , filter = Q(job__job_type = 'hybrid')),
            
        )


        job_title = query_param.get("job_title" , None)
        status = query_param.get("status" , None)
        category = query_param.get("category" , None)

        if job_title:
            applications = applications.filter(job__title__icontains = job_title)
        
        if status:
            applications = applications.filter(status = status)
        
        if category:
            applications = applications.filter(job__category__id = category)


        return {
            "applications":applications,
            "stats":stats,
        }
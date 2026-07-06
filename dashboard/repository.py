from discussion.models import Discussion
from discussion.service import DiscussionService
from comment.service import CommentService
from report.service import ReportService
from django.db.models import Count , Q
from bookmark.service import BookmarkService
from jobs.service import JobService

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
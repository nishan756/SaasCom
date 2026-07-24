from discussion.models import Discussion
from discussion.service import DiscussionService
from comment.service import CommentService
from report.service import ReportService
from django.db.models import Count , Q , Avg , Sum , F , FloatField , ExpressionWrapper
from django.db.models.functions import Coalesce , Round
from bookmark.service import BookmarkService
from jobs.service import JobService
from jobs.models import Application
from apps.models import App , Review
from vote.models import Vote
from report.models import Report
from django.contrib.contenttypes.models import ContentType
from saas_com.core.exceptions import ObjectNotFound
from bookmark.models import Bookmark


class AppsDashboardRepo:

    def main_dashboard(self, user, **query_param):
        content_type = ContentType.objects.get_for_model(App)

        apps = App.objects.filter(user=user).prefetch_related("category")

        app_ids = apps.values_list("id", flat=True)

        votes = Vote.objects.filter(
            content_type=content_type,
            object_id__in=app_ids,
        )

        reviews = Review.objects.filter(app__user=user)

        reports = Report.objects.filter(
            content_type=content_type,
            object_id__in=app_ids,
        )

        # Filter

        date_from = query_param.get("date_from" , None)
        date_to = query_param.get("date_to" , None)

        app_filter = {}
        vote_filter = {}
        review_filter = {}
        report_filter = {}

        if date_from:
            app_filter["added_at__gte"] = date_from
            vote_filter["added_at__gte"] = date_from
            review_filter["added_at__gte"] = date_from
            report_filter["reported_at__gte"] = date_from

        if date_to:
            app_filter["added_at__lte"] = date_to
            vote_filter["added_at__lte"] = date_to
            review_filter["added_at__lte"] = date_to
            report_filter["reported_at__lte"] = date_to

        votes = votes.filter(**vote_filter)
        reviews = reviews.filter(**review_filter)
        reports = reports.filter(**report_filter)

        # Statistics

        vote_stats = votes.aggregate(
            total_vote=Count("id"),
            total_upvote=Count("id", filter=Q(vote_type="upvote")),
            total_downvote=Count("id", filter=Q(vote_type="downvote")),
        )

        review_stats = reviews.aggregate(
            total_review=Count("id"),
            total_rating=Coalesce(Sum("rating"), 0),
            avg_rating=Coalesce(Avg("rating"), 0.0),
        )

        report_stats = reports.aggregate(
            total_report=Count("id"),
            total_spam=Count("id", filter=Q(report_type="spam")),
            total_fake=Count("id", filter=Q(report_type="fake")),
            total_harassment=Count("id", filter=Q(report_type="harassment")),
            total_copyright=Count("id", filter=Q(report_type="copyright")),
            total_scam=Count("id", filter=Q(report_type="scam")),
            total_other=Count("id", filter=Q(report_type="other")),
            total_nsfw=Count("id", filter=Q(report_type="nsfw")),
        )

        app_stats = apps.aggregate(
            total_app=Count("id"),
            total_approved_app=Count("id", filter=Q(status="approved")),
            total_pending_app=Count("id", filter=Q(status="pending")),
            total_rejected_app=Count("id", filter=Q(status="rejected")),
        )

        stats = {
            **app_stats,
            **vote_stats,
            **review_stats,
        }

        stats["report_stats"] = report_stats


        # App List

        apps = (
            apps.prefetch_related("votes", "reviews", "reports")
            .annotate(
                avg_rating=Coalesce(Avg("reviews__rating"), 0.0),
                total_review=Count("reviews", distinct=True),
                total_upvote=Count(
                    "votes",
                    filter=Q(votes__vote_type="upvote"),
                    distinct=True,
                ),
                total_downvote=Count(
                    "votes",
                    filter=Q(votes__vote_type="downvote"),
                    distinct=True,
                ),
            )
        )

        # Top Performing Apps

        apps.filter(**app_filter)
        
        top_apps = (
            apps.filter(status="approved")
            .annotate(
                performance_score=ExpressionWrapper(
                    (F("total_upvote") * 2)
                    + (F("avg_rating") * 10)
                    + (F("total_review") * 3),
                    output_field=FloatField(),
                )
            )
            .order_by("-performance_score")[:5]
        )

        if query_param.get("name"):
            apps = apps.filter(name__icontains=query_param["name"])

        if query_param.get("status"):
            apps = apps.filter(status=query_param["status"])


        return {
            "apps": apps,
            "stats": stats,
            "top_apps": top_apps,
        }

    def app_stats(self, user, id, **query_param):
        try:
            app = App.objects.get(id = id , user = user)
        
        except App.DoesNotExist:
            raise ObjectNotFound("App Not Found")
        
        content_type = ContentType.objects.get_for_model(App)

        votes = Vote.objects.filter(content_type = content_type , object_id = id)

        reports = Report.objects.filter(content_type = content_type , object_id = id)

        reviews = Review.objects.filter(app = app)

        bookmarks = Bookmark.objects.filter(content_type = content_type , object_id = id)

        query = {}

        date_from = query_param.get("date_from" , None)

        date_to = query_param.get("date_to" , None)

        if date_from:
            query["added_at__gte"] = date_from
        
        if date_to:
            query["added_at__lte"] = date_to

        if query:
            votes = votes.filter(**query)
            reports = reports.filter(**query)
            reviews = reviews.filter(**query)
            bookmarks = bookmarks.filter(**query)
        
        stats = {}

        vote_stats = votes.aggregate(
            total_vote = Count("id"),
            total_upvote = Count("id" , filter = Q(vote_type = "upvote")),
            total_downvote = Count("id" , filter = Q(vote_type = "downvote")),
            vote_score = F("total_upvote") - F("total_downvote")
        )        

        review_stats = reviews.aggregate(
                total_review = Count("id"),
                avg_rating = Round(Avg("rating") , 2),
                total_rating = Sum("rating"),
                total_0 = Count("id" , filter = Q(rating = 0)),
                total_1 = Count("id" , filter = Q(rating = 1)),
                total_2 = Count("id" , filter = Q(rating = 2)),
                total_3 = Count("id" , filter = Q(rating = 3)),
                total_4 = Count("id" , filter = Q(rating = 4)),
                total_5 = Count("id" , filter = Q(rating = 5)),

            )


        report_stats = reports.aggregate(
            total_report = Count("id"),
            total_spam=Count("id", filter=Q(report_type="spam")),
            total_fake=Count("id", filter=Q(report_type="fake")),
            total_harassment=Count("id", filter=Q(report_type="harassment")),
            total_copyright=Count("id", filter=Q(report_type="copyright")),
            total_scam=Count("id", filter=Q(report_type="scam")),
            total_other=Count("id", filter=Q(report_type="other")),
            total_nsfw=Count("id", filter=Q(report_type="nsfw")),
        )


        stats["bookmark_stats"] = bookmarks.aggregate(
            total_bookmark = Count("id"),
        )

        stats["vote_stats"] = vote_stats
        stats["review_stats"] = review_stats
        stats["report_stats"] = report_stats


        return {
            "app":app,
            "stats":stats,
        }


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
            total_offer_declined=Count("id", filter=Q(status="offer_declined")),
            total_offer_accepted=Count("id", filter=Q(status="offer_accepted")),
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
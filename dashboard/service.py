from .repository import DiscussionDashboardRepo
from django.core.paginator import Paginator
from django.db.models import Count , Q , Avg

class DiscussionDashboardService:

    def main_dashboard(self , user , **query_param):
        page = query_param.pop("page" , 1)
        discussions = DiscussionDashboardRepo().main_dashbaord(user , **query_param)

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

        # Comment and their ratios
        stats["direct_comments_ratio"] = f"{round(stats["direct_comments"]*100 / stats["total_comments"] if stats["total_comments"] > 0 else 0 , 2)}%"

        stats["reply_ratio"] = f"{round(stats["total_replies"]*100 / stats["total_comments"] , 2) if stats["total_comments"] > 0 else 0 }%"

        stats["avarage_comments"] = round(stats["total_comments"] / stats["total_discussions"] , 2)  if stats["total_comments"] > 0 else 0

        # Votes and their ratios
        stats["avarage_votes"] = round(stats["total_votes"] / stats["total_discussions"] , 2)  if stats["total_votes"] > 0 else 0

        stats["upvote_ratio"] = f"{round(stats["total_upvote"]*100 / stats["total_votes"] if stats["total_votes"] > 0 else 0 , 2)}%"

        stats["downvote_ratio"] = f"{round(stats["total_downvote"]*100 / stats["total_votes"] , 2) if stats["total_votes"] > 0 else 0 }%"

        stats["total_views"] = 0

        paginator = Paginator(discussions , 1)
        discussions = paginator.get_page(page)

        return {
            "stats":stats , 
            "discussions":discussions
        }
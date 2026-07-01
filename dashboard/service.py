from .repository import DiscussionDashboardRepo
from django.core.paginator import Paginator
from django.db.models import Count , Q , Avg
from vote.service import VoteService

class DiscussionDashboardService:

    repo = DiscussionDashboardRepo()

    def main_dashboard(self , user , **query_param):
        page = query_param.pop("page" , 1)
        
        result = DiscussionDashboardRepo().main_dashbaord(user , **query_param)

        stats = result["stats"]

        discussions = result["discussions"]

        # Comment and their ratios
        stats["direct_comments_ratio"] = f"{round(stats["direct_comments"]*100 / stats["total_comments"] if stats["total_comments"] > 0 else 0 , 2)}%"

        stats["reply_ratio"] = f"{round(stats["total_replies"]*100 / stats["total_comments"] , 2) if stats["total_comments"] > 0 else 0 }%"

        stats["avarage_comments"] = round(stats["total_comments"] / stats["total_discussions"] , 2)  if stats["total_comments"] > 0 else 0

        # Votes and their ratios
        stats["avarage_votes"] = round(stats["total_votes"] / stats["total_discussions"] , 2)  if stats["total_votes"] > 0 else 0

        stats["upvote_ratio"] = f"{round(stats["total_upvote"]*100 / stats["total_votes"] if stats["total_votes"] > 0 else 0 , 2)}%"

        stats["downvote_ratio"] = f"{round(stats["total_downvote"]*100 / stats["total_votes"] , 2) if stats["total_votes"] > 0 else 0 }%"

        stats["total_views"] = 0

        paginator = Paginator(discussions , 20)
        discussions = paginator.get_page(page)

        return {
            "stats":stats , 
            "discussions":discussions
        }
    
    def discussion_stats(self , id , **query_param):
        vote_stats = VoteService().get_object_votes_stats("discussion" , id , **query_param)

        components = self.repo.discussion_stats_component(id , **query_param)

        stats = {}

        comment_stats = components.pop("comment_stats")

        report_stats = components.pop("report_stats")

        bookmark_stats = components.pop("bookmark_stats")

        for key , value in comment_stats.items():
            stats[key] = value
        
        for key , value in report_stats.items():
            stats[key] = value
        
        for key , value in vote_stats.items():
            stats[key] = value
        
        for key , value in bookmark_stats.items():
            stats[key] = value

        return {
            "stats":stats,
            "comments":components["comments"],
            "reports":components["reports"],
        }
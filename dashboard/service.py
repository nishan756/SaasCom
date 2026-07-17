from .repository import DiscussionDashboardRepo, JobDashboardRepo , ApplicationDashboardRepo
from django.core.paginator import Paginator
from vote.service import VoteService
from django.core.paginator import Paginator

class DiscussionDashboardService:

    repo = DiscussionDashboardRepo()

    def main_dashboard(self , user , **query_param):
        page = query_param.pop("page" , 1)

        per_page = query_param.pop("per_page" , 20)
        
        result = self.repo.main_dashboard(user , **query_param)

        stats = result["stats"]

        discussions = result["discussions"]

        # Comment and their ratios
        stats["direct_comments_ratio"] = f"{round(stats["direct_comments"]*100 / stats["total_comments"] if stats["total_comments"] > 0 else 0 , 2)}%"

        stats["reply_ratio"] = f"{round(stats["total_replies"]*100 / stats["total_comments"] , 2) if stats["total_comments"] > 0 else 0 }%"

        stats["avarage_comments"] = round(stats["total_comments"] / stats["total_discussions"] , 2)  if stats["total_discussions"] > 0 else 0

        # Votes and their ratios
        stats["avarage_votes"] = round(stats["total_votes"] / stats["total_discussions"] , 2)  if stats["total_discussions"] > 0 else 0

        stats["upvote_ratio"] = f"{round(stats["total_upvote"]*100 / stats["total_votes"] , 2) if stats["total_votes"] > 0 else 0 }%"

        stats["downvote_ratio"] = f"{round(stats["total_downvote"]*100 / stats["total_votes"] , 2) if stats["total_votes"] > 0 else 0 }%"

        stats["total_views"] = 0

        paginator = Paginator(discussions , per_page)
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

        report_stats_by_category = components.pop("report_stats_by_category")

        
        temp_stats = {}
        
        for report in report_stats_by_category:
            temp_stats[report["report_type"].capitalize()] = report["total_report"]
        
        stats["report_stats_by_category"] = temp_stats

        stats["avg_reply_per_comment"] = round(comment_stats["total_replies"] / comment_stats["direct_comment"] if comment_stats["direct_comment"] > 0 else 0 , 2)

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


class JobDashboardService:

    repo = JobDashboardRepo()

    def main_dashboard(self , user , page , per_page , **query_param):
        jobs = self.repo.main_dashboard(user , page , **query_param).get("jobs")
        paginator = Paginator(jobs , per_page)
        jobs = paginator.get_page(page)
        result =  self.repo.main_dashboard(user , page , **query_param)
        result["jobs"] = jobs
        return result

    def job_stats(self):
        pass


class ApplicationDashboardService:

    repo = ApplicationDashboardRepo()

    def main_dashboard(self , user , per_page , page_num ,  **query_param):
        supported_query_field = {"date_from" , "date_to" , "job_title" , "status" , "category" , "job_type"}

        query_param = {key:value for key , value in query_param.items() if key in supported_query_field}

        result = self.repo.main_dashboard(user , **query_param)

        applications = result.pop("applications")

        paginator = Paginator(applications , per_page)

        applications = paginator.get_page(page_num)
        
        result["applications"] = applications

        total_full_time = result["stats"].pop("total_full_time")
        total_remote = result["stats"].pop("total_remote")
        total_intern = result["stats"].pop("total_intern")
        total_contract = result["stats"].pop("total_contract")
        total_hybrid = result["stats"].pop("total_hybrid")
        total_part_time = result["stats"].pop("total_part_time")

        total_application = result["stats"]["total_application"]

        temp_stats = {}

        temp_stats["full_time_ratio"] = f"{round(total_full_time*100 / total_application , 2) if total_application > 0 else 0 }%"

        temp_stats["part_time_ratio"] = f"{round(total_part_time*100 / total_application , 2) if total_application > 0 else 0 }%"

        temp_stats["contract_ratio"] = f"{round(total_contract*100 / total_application , 2) if total_application > 0 else 0 }%"

        temp_stats["hybrid_ratio"] = f"{round(total_hybrid *100 / total_application , 2) if total_application > 0 else 0 }%"

        temp_stats["intern_ratio"] = f"{round(total_intern *100 / total_application , 2) if total_application > 0 else 0 }%"

        temp_stats["remote_ratio"] = f"{round(total_remote *100 / total_application , 2) if total_application > 0 else 0 }%"

        result["stats"].update(temp_stats)

        return result
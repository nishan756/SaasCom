from .repository import DiscussionDashboardRepo, JobDashboardRepo , ApplicationDashboardRepo , AppsDashboardRepo
from django.core.paginator import Paginator
from vote.service import VoteService
from django.core.paginator import Paginator
from apps.models import App

class AppsDashboardService:

    repo = AppsDashboardRepo()

    def main_dashboard(self , user , page  , **query_param):

        per_page = query_param.pop("per_page" , 20)
        
        supported_query_param = {"date_from" , "date_to" , "category" , "name" , "status"}

        query_param = {key:value for key , value in query_param.items() if key in supported_query_param}

        result =  self.repo.main_dashboard(user , **query_param)
        
        apps = result.pop("apps")

        paginator = Paginator(apps , per_page)

        result["apps"] = paginator.get_page(page)

        return result

    def app_stats(self , user , id , **query_param):

        supported_query_param = {"date_from" , "date_to"}

        query_param = {key:value for key , value in query_param.items() if key in supported_query_param}

        result = self.repo.app_stats(user , id , **query_param)

        stats = result.pop("stats")
    
        review_stats = stats.pop("review_stats")

        temp_review_stats = {}

        total_review = review_stats.get("total_review")
        total_0 = review_stats.get("total_0")
        total_1 = review_stats.get("total_1")
        total_2 = review_stats.get("total_2")
        total_3 = review_stats.get("total_3")
        total_4 = review_stats.get("total_4")
        total_5 = review_stats.get("total_5")

        temp_review_stats["total_0_ratio"] = f"{round((total_0 * 100 / total_review) if total_review > 0 else 0)}%"
        temp_review_stats["total_1_ratio"] = f"{round((total_1 * 100 / total_review) if total_review > 0 else 0)}%"
        temp_review_stats["total_2_ratio"] = f"{round((total_2 * 100 / total_review) if total_review > 0 else 0)}%"
        temp_review_stats["total_3_ratio"] = f"{round((total_3 * 100 / total_review) if total_review > 0 else 0)}%"
        temp_review_stats["total_4_ratio"] = f"{round((total_4 * 100 / total_review) if total_review > 0 else 0)}%"
        temp_review_stats["total_5_ratio"] = f"{round((total_5 * 100 / total_review) if total_review > 0 else 0)}%"

        print(total_0)

        review_stats = {**review_stats , **temp_review_stats}
        stats["review_stats"] = review_stats
        result["stats"] = stats
        return result

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

    def main_dashboard(self , user , page_num , per_page , **query_param):

        supported_query_field = {"date_from" , "date_to" , "job_status"}

        query_param = {key:value for key , value in query_param.items() if key in supported_query_field}

        job_status_dict = {
            "active":"True",
            "inactive":"False",
        }

        job_status = query_param.pop("job_status" , None)

        if job_status:
            query_param["job_status"] = job_status_dict[job_status]

        result = self.repo.main_dashboard(user , **query_param)

        application_stats = result.get("stats").pop("application_stats")
        
        total_application = application_stats.get("total_application")
        total_pending = application_stats.get("total_pending")
        total_under_review = application_stats.get("total_under_review")
        total_shortlisted = application_stats.get("total_shortlisted")
        total_interview_scheduled = application_stats.get("total_interview_scheduled")
        total_offered = application_stats.get("total_offered")
        total_offer_declined = application_stats.get("total_offer_declined")
        total_offer_accepted = application_stats.get("total_offer_accepted")
        total_rejected_by_hr = application_stats.get("total_rejected_by_hr")
        total_withdrawn = application_stats.get("total_withdrawn")
        total_hired = application_stats.get("total_hired")
        
        temp_ratio_stats = {}
        if total_application != 0:
            temp_ratio_stats["pending_ratio"] = f"{round((total_pending * 100) / total_application , 2)}%"
            temp_ratio_stats["under_review_ratio"] = f"{round((total_under_review * 100) / total_application , 2)}%"
            temp_ratio_stats["shortlisted_ratio"] = f"{round((total_shortlisted * 100) / total_application , 2)}%"
            temp_ratio_stats["interview_scheduled_ratio"] = f"{round((total_interview_scheduled * 100) / total_application , 2)}%"
            temp_ratio_stats["offered_ratio"] = f"{round((total_offered * 100) / total_application , 2)}%"
            temp_ratio_stats["offer_declined_ratio"] = f"{round((total_offer_declined * 100) / total_application , 2)}%"
            temp_ratio_stats["offer_accepted_ratio"] = f"{round((total_offer_accepted * 100) / total_application , 2)}%"
            temp_ratio_stats["rejected_by_hr_ratio"] = f"{round((total_rejected_by_hr * 100) / total_application , 2)}%"
            temp_ratio_stats["withdrawn_ratio"] = f"{round((total_withdrawn * 100) / total_application , 2)}%"
            temp_ratio_stats["hired_ratio"] = f"{round((total_hired * 100) / total_application , 2)}%"
        
        application_stats = {**application_stats , **temp_ratio_stats}
        
        result["stats"]["application_stats"] = application_stats

        jobs = result.pop("jobs")

        paginator = Paginator(jobs , per_page)

        jobs = paginator.get_page(page_num)

        result["jobs"] = jobs

        return result

    def job_stats(self , id):
        result =  self.repo.job_stats(id)
        application_stats = result.get("stats").pop("application_stats")

        total_application = application_stats.get("total_application")
        total_pending = application_stats.get("total_pending")
        total_under_review = application_stats.get("total_under_review")
        total_shortlisted = application_stats.get("total_shortlisted")
        total_interview_scheduled = application_stats.get("total_interview_scheduled")
        total_offered = application_stats.get("total_offered")
        total_offer_declined = application_stats.get("total_offer_declined")
        total_offer_accepted = application_stats.get("total_offer_accepted")
        total_rejected_by_hr = application_stats.get("total_rejected_by_hr")
        total_withdrawn = application_stats.get("total_withdrawn")
        total_hired = application_stats.get("total_hired")

        temp_ratio_stats = {}
        if total_application != 0:
            temp_ratio_stats["pending_ratio"] = f"{round((total_pending * 100) / total_application , 2)}%"
            temp_ratio_stats["under_review_ratio"] = f"{round((total_under_review * 100) / total_application , 2)}%"
            temp_ratio_stats["shortlisted_ratio"] = f"{round((total_shortlisted * 100) / total_application , 2)}%"
            temp_ratio_stats["interview_scheduled_ratio"] = f"{round((total_interview_scheduled * 100) / total_application , 2)}%"
            temp_ratio_stats["offered_ratio"] = f"{round((total_offered * 100) / total_application , 2)}%"
            temp_ratio_stats["offer_declined_ratio"] = f"{round((total_offer_declined * 100) / total_application , 2)}%"
            temp_ratio_stats["offer_accepted_ratio"] = f"{round((total_offer_accepted * 100) / total_application , 2)}%"
            temp_ratio_stats["rejected_by_hr_ratio"] = f"{round((total_rejected_by_hr * 100) / total_application , 2)}%"
            temp_ratio_stats["withdrawn_ratio"] = f"{round((total_withdrawn * 100) / total_application , 2)}%"
            temp_ratio_stats["hired_ratio"] = f"{round((total_hired * 100) / total_application , 2)}%"

        application_stats = {**application_stats , **temp_ratio_stats}

        result["stats"]["application_stats"] = application_stats
        result["total_recent_application"] = len(result["recent_applications"])

        return result


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

        total_full_time = result["stats"].get("total_full_time")
        total_remote = result["stats"].get("total_remote")
        total_intern = result["stats"].get("total_intern")
        total_contract = result["stats"].get("total_contract")
        total_hybrid = result["stats"].get("total_hybrid")
        total_part_time = result["stats"].get("total_part_time")

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
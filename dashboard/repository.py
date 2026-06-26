from discussion.models import Discussion

class DiscussionDashboardRepo:

    def main_dashbaord(self , user , **query_param):
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
        
        return discussions

        
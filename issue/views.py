from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect

from .models import Issue, Status, Project, Tag, File
from .forms import IssueForm, ProjectForm, UploadFileForm

from comment.forms import CommentForm, Comment


class DashboardView(View):
    def get(self, request):
        context = {
            "issues": Issue.objects.all().order_by("-modified"),
            "view_data": {
                "user": request.user.username,
            }
        }
        return render(request, "issue/dashboard.html", context)


class IssueView(View):
    def get(self, request, issue_id):
        context = {
            "issue": get_object_or_404(Issue, id=issue_id),
            "comments": Comment.objects.filter(issue__id=issue_id).order_by("created"),
        }
        context["relations"] = [issue for issue in context["issue"].relations.all()] + [issue for issue in Issue.objects.filter(relations__in=[context["issue"]])]
        context["form"] = IssueForm(instance=context["issue"])
        context["file_form"] = UploadFileForm()
        context["comment_form"] = CommentForm()
        return render(request, "issue/issue.html", context)

    def post(self, request, issue_id):
        context = {
            "issue": get_object_or_404(Issue, id=issue_id)
        }
        action = request.POST.get("action")
        return {
            "create-relation": self.create_relation,
            "remove-relation": self.remove_relation,
            "delete-issue": self.delete_issue,
            "edit-issue": self.edit_issue,
            "upload-file": self.upload_file,
            "delete-file": self.delete_file,
            "create-comment": self.create_comment,
            "delete-comment": self.delete_comment,
        }.get(action, lambda context,request: redirect("issue", issue_id=context["issue"].id))(context, request)

    def create_relation(self, context, request):
        if request.POST.get("issue-id").isnumeric():
            related_issue = Issue.objects.filter(id=request.POST.get("issue-id")).first()
            if related_issue:
                context["issue"].relations.add(related_issue)
                context["issue"].save()
        return redirect("issue", issue_id=context["issue"].id)

    def remove_relation(self, context, request):
        relation_id = request.POST.get("relation-id")
        if relation_id.isnumeric():
            relation_id = int(relation_id)
            to_remove = set()
            for relation in context["issue"].relations.all():
                if relation.id == relation_id:
                    to_remove.add(relation)
            for relation in to_remove:
                context["issue"].relations.remove(relation)
            context["issue"].save()
        return redirect("issue", issue_id=context["issue"].id)

    def delete_issue(self, context, request):
        context["issue"].delete()
        return redirect("issues")

    def edit_issue(self, context, request):
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = context["issue"]
            issue.title = form.cleaned_data["title"]
            issue.description = form.cleaned_data["description"]
            issue.project = form.cleaned_data["project"]
            issue.status = form.cleaned_data["status"]

            # Remove tags based on form data
            for tag in issue.tags.all():
                if tag not in form.cleaned_data["tags"]:
                    issue.tags.remove(tag)

            # Add tags based on form data
            for tag in form.cleaned_data["tags"]:
                if tag not in issue.tags.all():
                    issue.tags.add(tag)
            
            issue.user = form.cleaned_data["user"]
            issue.save()
        return redirect("issue", issue_id=issue.id)

    def upload_file(self, context, request):
        file_form = UploadFileForm(request.POST, request.FILES)
        if file_form.is_valid():
            file_instance = File(file=file_form.files.get("file"))
            file_instance.save()
            context["issue"].files.add(file_instance)
            context["issue"].save()
        return redirect("issue", issue_id=context["issue"].id)

    def delete_file(self, context, request):
        file_id = request.POST.get("file-id")
        file = File.objects.filter(id=file_id).first()
        if file:
            file.delete()
        return redirect("issue", issue_id=context["issue"].id)

    def create_comment(self, context, request):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.username = request.user.username
            comment.issue = context["issue"]
            comment.save()
        return redirect("issue", issue_id=context["issue"].id)

    def delete_comment(self, context, request):
        comment_id = request.POST.get("comment-id")
        if comment_id.isnumeric():
            if comment := Comment.objects.filter(id=int(comment_id)).first():
                if comment.username == request.user.username or request.user.is_superuser:
                    comment.delete()
        return redirect("issue", issue_id=context["issue"].id)


class ProjectView(View):
    def get(self, request, project_id):
        context = {
            "project": get_object_or_404(Project, id=project_id),
        }
        context["form"] = ProjectForm(instance=context["project"])
        return render(request, "issue/project.html", context)

    def post(self, request, project_id):
        context = {
            "project": get_object_or_404(Project, id=project_id)
        }
        data = request.POST

        if data.get("form") == "delete-project":
            context["project"].delete()
            return redirect("issues")
        elif data.get("form") == "edit-project":
            form = ProjectForm(request.POST)
            if form.is_valid():
                project = context["project"]
                project.name = form.cleaned_data["name"]
                project.save()
                return redirect("project", project_id=project.id)
        return render(request, "issue/project.html", context)


class CreateIssueView(View):
    def get(self, request):
        context = {
            "form": IssueForm()
        }
        return render(request, "issue/create_issue.html", context)
    
    def post(self, request):
        context = {}
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.status,created = Status.objects.get_or_create(name="Open")
            issue.save()

            # Add tags based on form data
            for tag in form.cleaned_data["tags"]:
                issue.tags.add(tag)

            issue.save()
            return redirect("issue", issue_id=issue.id)
        redirect("create_issue")


class CreateProjectView(View):
    def get(self, request):
        context = {
            "form": ProjectForm()
        }
        return render(request, "issue/create_project.html", context)
    
    def post(self, request):
        context = {}
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return redirect("project", project_id=project.id)
        redirect("create_project")
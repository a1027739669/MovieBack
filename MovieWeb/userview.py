from django.shortcuts import render
from xadmin.views import CommAdminView


class TestView(CommAdminView):
    def get(self, request):
        context = super().get_context()
        return render(request, 'comment.html', context)
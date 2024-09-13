from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from ta_manager.forms.create import CreateSectionForm

from ta_manager.models import Section


class SectionView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'section.html', {"form": CreateSectionForm, "sectionList": self.List_All_Section()})
        # Check for permission in Sprint 2

    def post(self, request):
        # Check if the post is Removing or Create a section.
        # Create a Section
        message = None
        if 'create_section' in request.POST:
            form = CreateSectionForm(request.POST)
            if form.is_valid():
                form.save()
                message = "Section created successful"
            else:
                message = "Section failed to create"

        elif 'remove_section' in request.POST:
            selected_option = request.POST.getList('section_select')
            if len(selected_option) == 0:
                message = "No section is selected"
            elif not self.Remove_Section(selection_list=selected_option):
                message = "Section can not be deleted"
            else:
                message = "Section created successful"
        # List all the Section + re-print the form
        return render(request, 'section.html',
                      {"form": CreateSectionForm(), "message": message, "sectionList": self.List_All_Section()})

    def List_All_Section(self):
        return Section.objects.all()

    def Remove_Section(self, selection_list):
        for section in selection_list:
            try:
                section = Section.objects.get(section_name=section.name)
                section.delete()
            except Section.DoesNotExist:
                return False
        return True

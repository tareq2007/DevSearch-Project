from django.shortcuts import render, redirect
from .models import Project,Tag
from django.db.models import Q
from django.contrib import messages as message
from django.core.paginator import Paginator
from .utils import searchProjects
from .create_form import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required

def projects(request):
    projects, search = searchProjects(request)
    p = Paginator(projects, 3)
    page = request.GET.get('page')
    projects = p.get_page(page)
    context = {'projects': projects, 'search': search}
    return render(request, 'projects/projects.html', context)

def project(request,pk):
    projectobj = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectobj
        review.owner = request.user.profile
        review.save()
        projectobj.getVoteCount
        message.success(request, 'Your review was successfully submitted!')
        return redirect('pp', pk=projectobj.id)
    
    context = {'project': projectobj, 'form': form}
    return render(request, 'projects/single-project.html',context)

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/create_projects.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/create_projects.html', context)

@login_required(login_url='login')
def delete_Project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete.html', context)
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Message
from .utils import searchProfiles
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.decorators import login_required

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User not found')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'profiles')
        else:
             messages.error(request,'User or password did not match')

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.warning(request,'User logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,'User was created successfully')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request,'An error has occurred during registration')
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles, search = searchProfiles(request)
    p = Paginator(profiles, 3)
    page = request.GET.get('page')
    profiles = p.get_page(page)
    context = {'profiles': profiles, 'search': search}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkill = profile.skill_set.exclude(description__exact="")
    otherSkill = profile.skill_set.filter(description="")
    context = {'profile': profile, 'topSkill':topSkill, 'otherSkill': otherSkill}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def accountUser(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/account-form.html', context)

@login_required(login_url='login')
def addSkill(request,):
    form = SkillForm()
    profile = request.user.profile
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'Skill was added successfully')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/add-skill.html', context)

@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill.save()
            messages.success(request,'Skill was Updated successfully')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/add-skill.html', context)

def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request,'Skill was deleted successfully')
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete.html', context)

def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)

def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render (request, 'users/message.html', context)

def sendMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:  
                message.name = sender.name
                message.email = sender.email 
            message.save()
            messages.success(request,'Message was sent successfully')
            return redirect('user-profile', pk=recipient.id)
    context = {'recipient': recipient,'form': form}
    return render(request, 'users/message-form.html', context)

def home(request):
    return render(request, 'users/home.html')
def logoutView(request):
    logout(request)
    return redirect('/')
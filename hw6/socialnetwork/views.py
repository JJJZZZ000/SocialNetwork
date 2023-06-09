from django.db.models import FileField
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from socialnetwork.forms import LoginForm, RegisterForm

from socialnetwork.models import Post, Profile

from socialnetwork.forms import ProfileForm

from socialnetwork.models import Client

from socialnetwork.models import Comment

import json
# Create your views here.
def login_action(request):
    context = {}
    if request.method == 'GET':
        form = LoginForm()
        context['form'] = form
        return render(request, 'socialnetwork/login.html', context)
    form = LoginForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


def register_action(request):
    context = {}
    if request.method == 'GET':
        form = RegisterForm()
        context['form'] = form
        return render(request, 'socialnetwork/register.html', context)
    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request, new_user)
    profile = Profile(user=request.user)
    profile.save()
    client = Client(user=request.user)
    client.save()
    return redirect(reverse('home'))


@login_required
def global_stream_action(request):
    context = {}
    name = request.user.first_name + " " + request.user.last_name
    context['name'] = name
    user = request.user
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-date')
        context['posts'] = posts
        return render(request, 'socialnetwork/global_stream.html', context)
    if request.method == 'POST':
        content = request.POST["new_post"]
        post = Post(author=user, content=content)
        post.save()
        return redirect('global_stream')


def follower_stream_action(request):
    context = {}
    name = request.user.first_name + " " + request.user.last_name
    context['name'] = name
    user = request.user
    client = Client.objects.filter(user__id=user.id)[0]
    followings = client.followings.all()
    if request.method == 'GET':
        posts_ = Post.objects.all().order_by('-date')
        posts = []
        for post in posts_:
            if followings.contains(post.author):
                posts.append(post)
        context['posts'] = posts
        return render(request, 'socialnetwork/follower_stream.html', context)
    if request.method == 'POST':
        content = request.POST["new_post"]
        post = Post(author=user, content=content)
        post.save()
        return redirect('follower_stream')


def my_profile_action(request):
    context = {}
    user = request.user
    profile = Profile.objects.filter(user__id=user.id)[0]
    name = user.first_name + " " + user.last_name
    context['name'] = name
    context['bio'] = profile.bio
    context['profile_id'] = profile.id

    client = Client.objects.filter(user__id=user.id)[0]
    followings = client.followings.all()
    context['followings'] = followings
    # followings = []
    # for f_client in followings_client:
    #     followings.append(f_client.user)
    if request.method == 'GET':
        context['form'] = ProfileForm
        if not profile.profile_picture:
            context['hasPicture'] = False
        else:
            context['hasPicture'] = True
        return render(request, 'socialnetwork/my_profile.html', context)
    else:
        form = ProfileForm(request.POST, request.FILES)
        if not form.is_valid():
            context['form'] = form
            context['hasPicture'] = False
            return render(request, 'socialnetwork/my_profile.html', context)
        else:
            pic = form.cleaned_data['profile_picture']
            profile.profile_picture = pic
            profile.content_type = pic.content_type
            profile.bio = request.POST['bio']
            profile.save()
            context['form'] = ProfileForm
            context['hasPicture'] = True
            # return render(request, 'socialnetwork/my_profile.html', context)
            return redirect('my_profile')


# id is userid
def personal_profile_action(request, id):
    context = {}
    user = User.objects.filter(id=id)[0]
    my_user = request.user
    context['my_name'] = my_user.first_name+" "+my_user.last_name
    profile = Profile.objects.filter(user__id=user.id)[0]
    context['profile_id'] = profile.id
    if not profile.profile_picture:
        context['hasPicture'] = False
    else:
        context['hasPicture'] = True
    if my_user.id == id:
        return my_profile_action(request)
    profile = Profile.objects.filter(user__id=id)[0]
    name = user.first_name + " " + user.last_name
    context['name'] = name
    context['bio'] = profile.bio
    context['id'] = user.id
    client = Client.objects.filter(user__id=my_user.id)[0]

    if request.method == 'GET':
        context['picture'] = profile.profile_picture
        if client.followings.contains(user):
            context['isFollowing'] = True
        else:
            context['isFollowing'] = False
        return render(request, 'socialnetwork/personal_profile.html', context)
    else:
        if client.followings.contains(user):
            client.followings.remove(user)
        else:
            client.followings.add(user)
        return redirect('personal_profile', id=user.id)



    # else:
    #     print(request.POST['unfollow'])
    #     if request.POST['follow']:
    #         client.followings.add(user)
    #         context['isFollowing'] = True
    #     if request.POST['unfollow']:
    #         client.followings.remove(user)
    #         context['isFollowing'] = False
    #     print(context['isFollowing'])
    #     return redirect('personal_profile/'+id)

#
# def follow_unfollow(request, id1, id2):
#     user2 = User.objects.filter(id=id2)[0]
#     client = Client.objects.filter(user__id=id1)[0]
#     if client.followings.contains(user2):
#         client.followings.remove(user2)
#     else:
#         client.followings.add(user2)
#     return redirect('personal_profile/' + id2)


# id is userid
def get_photo_action(request, id):
    profile = get_object_or_404(Profile, id=id)
    if not profile.profile_picture:
        raise Http404
    return HttpResponse(profile.profile_picture, content_type=profile.content_type)



def json_dumps_serializer_global(request):
    if not request.user.id:
        return error_resp_json("You are not logged in", status=401)
    response_content = []
    for post in Post.objects.all().order_by('-date'):
        comments = []
        for comment in Comment.objects.filter(post__id=post.id).all().order_by('-date'):
            comment_item = {
                'id': comment.id,
                'texts': comment.content,
                'date': comment.date.isoformat(),
                'post_id': comment.post.id,
                'comment_first_name': comment.author.first_name,
                'comment_last_name': comment.author.last_name,
                'author_id': comment.author.id,
            }
            comments.append(comment_item)
        post_item = {
            'id': post.id,
            'texts': post.content,
            'first_name': post.author.first_name,
            'last_name': post.author.last_name,
            'author_id': post.author.id,
            'comments': comments,
            'date': post.date.isoformat(),
        }
        response_content.append(post_item)

    json_resp = json.dumps(response_content)

    return HttpResponse(json_resp, content_type='application/json')


def json_dumps_serializer_follower(request):
    if not request.user.id:
        return error_resp_json("You must be logged in to do this operation", status=401)
    response_data = []
    user = request.user
    # find the user and then get all the followers.
    client = Client.objects.filter(user__id=user.id)[0]
    followings = client.followings.all()
    for post in Post.objects.all().order_by('-date'):
        if not followings.contains(post.author):
            continue
        comments = []
        for comment in Comment.objects.filter(post__id=post.id).all().order_by('-date'):
            comment_item = {
                'id': comment.id,
                'texts': comment.content,
                'date': comment.date.isoformat(),
                'post_id': comment.post.id,
                'comment_first_name': comment.author.first_name,
                'comment_last_name': comment.author.last_name,
                'author_id': comment.author.id,
            }
            comments.append(comment_item)
        post_item = {
            'id': post.id,
            'texts': post.content,
            'first_name': post.author.first_name,
            'last_name': post.author.last_name,
            'author_id': post.author.id,
            'comments': comments,
            'date': post.date.isoformat(),
        }
        response_data.append(post_item)

    json_resp = json.dumps(response_data)

    return HttpResponse(json_resp, content_type='application/json')


def add_comment(request):
    if not request.user.id:
        return error_resp_json("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return error_resp_json("You must use a POST request for this operation", status=405)

    if not 'comment_text' in request.POST or not request.POST['comment_text'] \
            or not 'post_id' in request.POST or not request.POST['post_id']:
        return error_resp_json("You must enter an comment to add.", status=400)

    post_id = "" + request.POST.get('post_id', False)
    if not post_id.isdigit():
        return error_resp_json("The post id should be a digit.", status=400)

    res = Post.objects.filter(id=request.POST['post_id'])
    if not res:
        return error_resp_json("The post is not exist.", status=400)
    post = res[0]
    if not post:
        return error_resp_json("The post is not exist.", status=400)
    comment = Comment(author=request.user, content=request.POST["comment_text"], post=post)
    comment.save()
    req_type = request.POST.get('req_type', False)
    if req_type == '0':
        return json_dumps_serializer_global(request)
    return json_dumps_serializer_follower(request)


def error_resp_json(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)


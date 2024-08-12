from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import logging
from .models import Post, AboutUs, Category, SubCategory
from django.http import Http404
from django.core.paginator import Paginator
from .forms import ContactForm, PostForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout

# Create your views here.
            #EXAMPLE DATA.......
# posts = [
#         {'id':1, 'title':'post 1','content':'content of post 1'},
#         {'id':2, 'title':'post 2','content':'content of post 2'},
#         {'id':3, 'title':'post 3','content':'content of post 3'},
#         {'id':4, 'title':'post 4','content':'content of post 4'},
#     ]
def index(request):
    blog_title = 'Recent Jobs'
    allposts = Post.objects.all()


    paginator = Paginator(allposts, 5)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    
    
    return render(request,'index.html', {'blog_title':blog_title,'page_object':page_object})

def detail(request, slug):
    # post = next((item for item in posts if item['id'] == int(post_id)), None)

    try:
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category = post.category).exclude(pk=post.id)
        
    
    except Post.DoesNotExist:
        raise Http404("Post Does not Exist!!")


    # post = Post.objects.get(id=slug)

    # logger = logging.getLogger("TESTING")
    # logger.debug(f'post variable is {post}')
    return render(request,'detail.html', {'post':post, 'related_posts':related_posts})

def old_url_redirect(request):
    return redirect(reverse('blog:new_page_url'))

def new_url_view(request):
    return HttpResponse("This is new URL...")

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        logger = logging.getLogger("TESTING")
        # form.cleaned_data['name']
        if form .is_valid():            
            logger.debug(f' POST Data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            success_msg = "Your Email has been sent!!"
            return render(request,'contact.html', {'form':form, 'success_msg':success_msg}) 
        else:
            logger.debug(f' Form is not valid')
        return render(request,'contact.html', {'form':form, 'name':name, 'email':email, 'message':message}) 
    return render(request,'contact.html')

def about_view(request):
    about_content = AboutUs.objects.first().content
    return render(request,'about.html',{'about_content':about_content})

def add(request):
    if request.method == 'POST':
        print(request.POST)
        form = PostForm(request.POST)
        print("**********")
        print(form)
        if form.is_valid():
            print("**********")
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            img_url = form.cleaned_data['img_url']
            category = form.cleaned_data['category']
            status = form.cleaned_data['status']
            author = form.cleaned_data['author']
            subcategory = form.cleaned_data['subcategory']
            post = Post.objects.create(title=title, content=content, img_url=img_url, category_id = category, status = status, author = author, subcategory_id = subcategory)     
            return JsonResponse({'status':'success'})
            
        else:
            errors = {field:error.get_json_data() for field, error in form.errors.items()}
            return JsonResponse({'status':'error','form':errors})
    else:
        form = PostForm()
        category = Category.objects.all().values()
        subcategory = SubCategory.objects.all().values()
        return render(request,'add.html',{'form':form, 'categories':category, 'subcategories':subcategory})


@csrf_exempt
def edit(request, post_id):
    
    if request.method == 'POST':
        print("TGRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")

        form = PostForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
            content=form.cleaned_data['content']
            img_url = form.cleaned_data['img_url']
            category = form.cleaned_data['category']
            author = form.cleaned_data['author']
            status = form.cleaned_data['status']
            subcategory = form.cleaned_data['subcategory']
            post = Post.objects.get(id=post_id)
            post.title = title
            post.content = content
            post.img_url = img_url
            post.category_id = category
            post.author = author
            post.status = status
            post.subcategory_id = subcategory
            print(post)
            post.save()
            return JsonResponse({'status':'success','message':'Updated Successfully'})
        else:
            
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        post = Post.objects.get(id=post_id)
        form = PostForm(instance=post)
        print(post_id)
        categories = Category.objects.all()
        subcategory = SubCategory.objects.all()
        return render(request, 'edit.html', {'form': form, 'categories': categories ,'post_id':post_id, 'subcategories':subcategory})

    

def delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'error'})
    

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    data = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'img_url': post.img_url,
        'category': post.category.name,
    }
    return JsonResponse(data)

def grid(request):
    return render(request,'grid.html')

def get_grid(request):
    posts = Post.objects.select_related('category').values('id','title','content','category__name','img_url','author','status','subcategory__name').order_by('id')
    posts_list = list(posts)
    return JsonResponse(posts_list, safe=False)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        errors = {}
        
        # Validate username and password fields
        if not username:
            errors['username'] = 'Username is required.'
        if not password:
            errors['password'] = 'Password is required.'

        # Check if there are no errors and attempt authentication
        if not errors:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return JsonResponse({"status": 'success'})
                else:
                    errors['username'] = 'The user name is invalid.'
            else:
                errors['header'] = 'Invalid username or password.'

        return JsonResponse({"status": "error", "errors": errors})
    
    return render(request, 'registration/login.html',{'user': request.user})


def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('blog:login')
    return redirect('blog:grid')


def category_search(request):
    if request.method=='GET':
        q = request.GET.get('q')
        categories = Category.objects.filter(name__icontains=q)
        results = [{'id': category.id, 'text': category.name} for category in categories]
        return JsonResponse({'results': results})

    return JsonResponse({'results': []})

def subcategory(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        category_id = request.GET.get('category_id')
        if category_id:
            subcategories = SubCategory.objects.filter(name__icontains=q, category_id=category_id)
        results = [{'id': category.id, 'text': category.name} for category in subcategories]
        return JsonResponse({'results': results})

    return JsonResponse({'results': []})
       
        
    
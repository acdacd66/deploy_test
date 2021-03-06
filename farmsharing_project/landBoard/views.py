from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from accounts.models import *
from django.core.exceptions import ObjectDoesNotExist
# from .forms import SharingBoardForm
from django.core.paginator import Paginator
from django.utils import timezone

def SharingBoardRead(request):
    sharing_tmp = SharingBoard.objects.all()
    sharingboards=[]

    for sharingboard in sharing_tmp:
        sharingboards.append(sharingboard)
    sharingboards.reverse()

    paginator = Paginator(sharingboards,9)
    
    page = request.GET.get('page')
    sharingboards2 = paginator.get_page(page)
    region_list = Region.objects.all()
    return render(request, 'sharingboard_list.html', {'sharingboards': sharingboards, 'region_list':region_list, 'sharingboards2':sharingboards2})

# filter
def sharing_filter(request):
    region_list = Region.objects.all()
    filter_region = request.POST.get('region')
    filter_is_free = request.POST.get('is_free')

    search_mode = request.POST.get('search_mode')
    search_data = request.POST.get('search_data')

    #지역과 비용여부 필터링
    if(filter_region == "All" and filter_is_free == "All"):
        sharingboards = SharingBoard.objects.all()
    elif(filter_region == "All" and filter_is_free != "All"):
        sharingboards = SharingBoard.objects.filter(
            is_free = filter_is_free
        )
    elif(filter_region != "All" and filter_is_free == "All"):
        sharingboards = SharingBoard.objects.filter(
            region = filter_region
        )
    elif(filter_region != "All" and filter_is_free != "All"):
        sharingboards = SharingBoard.objects.filter(
            region = filter_region,
            is_free = filter_is_free
        )

    #위에서 필터링 된 내용 중 검색모드에 따른 제목, 내용, 작성자 검색 -> 리스트에 담아서 페이지네이터로 뿌림
    filter_result = []
    if search_mode == 'title' :
        for sb in sharingboards:
            if search_data in sb.title :
                filter_result.append(sb)
    elif search_mode == 'contents':
        for sb in sharingboards:
            if search_data in sb.content :
                filter_result.append(sb)
    else :
        for sb in sharingboards:
            if search_data in sb.writer.username :
                filter_result.append(sb)

    sharingboards = filter_result

    #페이지네이터
    paginator = Paginator(sharingboards,9)
    page = request.GET.get('page')
    sharingboards2 = paginator.get_page(page)

    return render(request, 'sharingboard_list.html', {'sharingboards': sharingboards, 'region_list':region_list, 'sharingboards2':sharingboards2})


def SharingBoardNew(request):
    regionM = Region.objects.all()
    user = request.user
    user_lands = user.user_land.all()
    return render(request, 'sharingboard_new.html', {'regionM': regionM, 'user_lands':user_lands})

def SharingBoardCreate(request):

    land_id = request.POST['choice_land']
    land = Land.objects.get(id = land_id)

    new_sb = SharingBoard() 
    new_sb.title = request.POST['title']
    new_sb.region = land.region
    new_sb.sharing_term = request.POST['sharing_term']
    new_sb.is_free = request.POST['is_free']
    new_sb.amount_period = request.POST['amount_period']
    new_sb.amount = request.POST['amount']
    new_sb.content = request.POST['content']
    new_sb.land_img = request.FILES.get('land_img')
    new_sb.writer = request.user
    new_sb.choice_land = land
    new_sb.pub_date=timezone.datetime.now()

    new_sb.save()
    return redirect('sharingboard')

def SharingBoardEdit(request,sb_id):
    regionM = Region.objects.all()
    edit_sb = SharingBoard.objects.get(pk=sb_id)
    user_lands = request.user.user_land.all()
    return render(request,'sharingboard_edit.html',{'sb':edit_sb , 'regionM': regionM, "user_lands":user_lands})

def SharingBoardUpdate(request,sb_id):
    land_id = request.POST['choice_land']
    land = Land.objects.get(id = land_id)

    update_sb = SharingBoard.objects.get(pk=sb_id) 
    update_sb.title = request.POST['title']
    update_sb.region = land.region
    update_sb.sharing_term = request.POST['sharing_term']
    update_sb.is_free = request.POST['is_free']
    update_sb.amount_period = request.POST['amount_period']

    if(request.POST['is_free'] == False):
        update_sb.amount = request.POST['amount']
    else:
        update_sb.amount = 0

    update_sb.content = request.POST['content']
    update_sb.choice_land = land
    update_sb.land_img = request.POST['land_img']
    update_sb.save()
    return redirect('sharingboard')

def SharingBoardDelete(request, sb_id):
    delete_post = SharingBoard.objects.get(pk= sb_id)
    delete_post.delete()
    return redirect('sharingboard')

def RequestBoardRead(request):
    request_tmp = RequestBoard.objects.all()
    request_list=[]
    for requestboard in request_tmp:
        request_list.append(requestboard)
    request_list.reverse()

    paginator = Paginator(request_list,9)
    page = request.GET.get('page')
    requestboards = paginator.get_page(page)
    region_list = Region.objects.all()
    return render(request, 'requestboard_list.html', {'requestboards': requestboards, 'region_list':region_list})

    # filter
def request_filter(request):
    region_list = Region.objects.all()
    filter_region = request.POST.get('region')
    filter_is_pay_for = request.POST.get('is_pay_for')

    search_mode = request.POST.get('search_mode')
    search_data = request.POST.get('search_data')

    if(filter_region == "All" and filter_is_pay_for == "All"):
        requestboards = RequestBoard.objects.all()
    elif(filter_region == "All" and filter_is_pay_for != "All"):
        requestboards = RequestBoard.objects.filter(
            is_pay_for = filter_is_pay_for
        )
    elif(filter_region != "All" and filter_is_pay_for == "All"):
        requestboards = RequestBoard.objects.filter(
            region = filter_region
        )
    elif(filter_region != "All" and filter_is_pay_for != "All"):
        requestboards = RequestBoard.objects.filter(
            region = filter_region,
            is_pay_for = filter_is_pay_for
        )

    filter_result = []
    if search_mode == 'title' :
        for rb in requestboards:
            if search_data in rb.title :
                filter_result.append(rb)
    elif search_mode == 'contents':
        for rb in requestboards:
            if search_data in rb.content :
                filter_result.append(rb)
    else :
        for rb in requestboards:
            if search_data in rb.writer.username :
                filter_result.append(rb)

    requestboards = filter_result

    return render(request, 'requestboard_list.html', {'requestboards': requestboards, 'region_list':region_list})


def SharingBoardDetail(request,sb_id):
    sb_detail = get_object_or_404(SharingBoard,pk= sb_id)
    comments = SB_comment.objects.filter(sbcomment = sb_id)
    me = request.user.username
    sb=SharingBoard.objects.get(id=sb_id)
    requested=False
    if sb.writer.username != request.user.username:
        try:
            land=Land_request.objects.get(land=sb.id, client=request.user.id)
            requested=land.status
        except ObjectDoesNotExist:
            pass
    

    return render(request, 'sharingboard_detail.html', {'sb':sb_detail, 'me':me, 'comments':comments,'requested':requested})

def RequestBoardDetail(request,rb_id):
    rb_detail = get_object_or_404(RequestBoard,pk= rb_id)
    comments = RB_comment.objects.filter(rbcomment = rb_id)
    land=""
    if request.user.is_authenticated :
        land = request.user.user_land.all()
    return render(request, 'requestboard_detail.html', {'rb':rb_detail, 'land':land,'comments':comments})

def RequestBoardNew(request):
    regionM = Region.objects.all()
    return render(request, 'requestboard_new.html', {'regionM': regionM})

def RequestBoardCreate(request):
    new_rb = RequestBoard() 
    new_rb.title = request.POST['title']
    new_rb.region = request.POST['region']
    new_rb.land_area = request.POST['land_area']
    new_rb.sharing_term_start = request.POST['sharing_term1']
    new_rb.sharing_term_end = request.POST['sharing_term2']
    new_rb.is_pay_for = request.POST['is_pay_for']
    new_rb.content = request.POST['content']
    new_rb.purpose = request.POST['purpose']
    new_rb.writer = request.user
    new_rb.pub_date=timezone.datetime.now()
    new_rb.save()
    return redirect('requestboard')

def RequestBoardEdit(request,rb_id):
    regionM = Region.objects.all()
    edit_rb = RequestBoard.objects.get(pk=rb_id)
    return render(request,'requestboard_edit.html',{'rb':edit_rb , 'regionM': regionM})

def RequestBoardUpdate(request,rb_id):
    update_rb = RequestBoard.objects.get(pk=rb_id) 
    update_rb.title = request.POST['title']
    update_rb.region = request.POST['region']
    update_rb.land_area = request.POST['land_area']
    update_rb.sharing_term = request.POST['sharing_term']
    update_rb.is_pay_for = request.POST['is_pay_for']
    update_rb.content = request.POST['content']
    update_rb.purpose = request.POST['purpose']
    update_rb.save()
    return redirect('requestboard')

def RequestBoardDelete(request, rb_id):
    delete_post = RequestBoard.objects.get(pk= rb_id)
    delete_post.delete()
    return redirect('requestboard')


def SharingBoardCommentNew(request,sb_id):
    comment = SB_comment()
    user = request.user
    comment.comment_writer = get_object_or_404(Profile , username= user)
    comment.comment_content = request.POST['content']
    comment.sbcomment = get_object_or_404(SharingBoard, pk = sb_id)
    comment.save()
    return redirect('sb_detail',sb_id)

def RequestBoardCommentNew(request,rb_id):
    comment = RB_comment()
    user = request.user
    comment.comment_writer = get_object_or_404(Profile, username=user)
    land_id = request.POST['l']
    land = Land.objects.get(id = land_id)
    comment.land_writer = land
    comment.comment_content = request.POST['content']
    comment.rbcomment = get_object_or_404(RequestBoard, pk=rb_id)
    comment.save()
    return redirect('rb_detail',rb_id)




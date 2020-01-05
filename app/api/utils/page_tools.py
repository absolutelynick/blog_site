from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_pagination_page(request, object_list, count=21):
    paginator = Paginator(object_list, count)
    page = request.GET.get("page")

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return page, posts

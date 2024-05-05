from django.urls import path
from .views import (home, post_create_view, post_delete_view,
                    post_edit_view, post_page_view, respone_sent,
                    response_delete, like_post, user_responses, accept_response, delete_response)

urlpatterns = [
    path('', home, name='home'),
    path('category/<category>/', home, name='category'),
    path('author/<str:author>/', home, name='author_posts'),
    path('create/', post_create_view, name='post_create'),
    path('delete/<int:pk>/', post_delete_view, name='post_delete'),
    path('edit/<int:pk>/', post_edit_view, name='post_edit'),
    path('post/<int:pk>/', post_page_view, name='post'),
    path('responsesent/<int:pk>/', respone_sent, name='response_sent'),
    path('response/delete/<int:pk>/', response_delete, name='response_delete'),
    path('like/<int:pk>/', like_post, name='like_post'),
    path('responses/', user_responses, name='user_responses'),
    path('responses/<int:pk>/accept', accept_response, name='accept_response'),
    path('responses/<int:pk>/delete', delete_response, name='delete_response')
   
    ]
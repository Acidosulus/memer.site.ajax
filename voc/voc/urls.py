"""voc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from vocapp import views

urlpatterns = [
	path('', views.index),
	path('login', views.PageLogIn),
	path('index', views.index),
    path('example', views.example),
    path('example/', views.example),
    path('dragTest', views.dragTest),
    path('dragTest/', views.dragTest),
	path('media_list/<str:folder_01>', views.media_list),
    path('media_list/<str:folder_01>/', views.media_list),
    path('media_list/<str:folder_01>/<str:folder_02>/', views.media_list_02),
    path('api/v1/media_list_create_new_volume/<str:folder>/<str:created_volume>/', views.create_user_media_folder),
    path('api/v1/media_list_delete_volume/<str:folder>/', views.delete_user_media_folder),
    path('api/v1/media_list_rename_volume/<str:current_folder>/<str:last_folder_name>/<str:new_folder_name>/', views.rename_user_media_folder),
    path('api/v1/media_cross_request/media_description/', views.media_cross_request_get),
	path('api/v1/cross_request/', views.cross_request),
	path('api/v1/media_cross_request/media_edit_comment/', views.media_edit_comment),
    #path('api/v1/media_list_rename_media/<str:folder>/<str:new_media_name>/', views.rename_user_media),
    path('api/v1/get_media_source/<str:folder>/<str:file>', views.get_user_media),
    path('media_upload/<str:user_folder>/', views.Upload_User_Media),
	path('hoster', views.hoster),
	path('hoster/<str:sitename>/', views.hoster_control),
	path('hoster/<str:sitename>/delete_all/', views.hoster_control_clear_all),
	path('test', views.test),
	path('test/', views.test),
	path('admin', admin.site.urls),
	path('word_in_progress/', views.word_in_progress),
    path('word_in_progress/<str:pc_word>/', views.word_in_progress),
	path('GetWoorhuntDataJSON/<str:pc_word>/', views.GetWoorhuntDataJSON),
	path('add_new_word/', views.add_new),
	path('add_new_word/<str:pc_new_word>/', views.add_new_with_parameter),
	path('ready_list/', views.ready_list),
	path('proceed_list/', views.proceed_list),
	path('next/<str:pc_last_word>/', views.next_with_last),
	path('ready/<str:pc_ready_word>/', views.ready),
	path('unready/<str:pc_unready_word>/', views.unready),
	path('book/<str:pc_book>/', views.book),
	path('books/', views.books),
	path('phrases/', views.phrases),
	path('phrases/ready_list/', views.phrases_ready_list),
	path('phrases/add_new/', views.phrases_add_new),
	path('phrases/add_new/<str:pc_phrase_id>/', views.phrases_add_new),
	path('phrases/in_progress/', views.phrases_in_progress),
    path('phrases/in_progress/<str:pc_phrase_id>/', views.phrases_in_progress_with_id),
	path('logout/', views.log_out),
	path('personal_page/', views.personal_page),
	path('accounts/', include('django.contrib.auth.urls')),
	path('accounts', include('django.contrib.auth.urls')),
	path('api/<str:pc_type>/<str:pc_book_id>/', views.json_response),
    path('restapi/v1/<str:pc_first>/<str:pc_second>/<str:pc_third>/', views.rest_response),
	path('sentence/<str:pc_sentence>/', views.get_sentence),# для генерации mp3 по переданному предложению

]


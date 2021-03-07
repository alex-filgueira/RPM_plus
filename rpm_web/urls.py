from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.frontpage, name='frontpage'),
    #url(r'^projects/$', views.ProjectListView.as_view(), name='projects'), # las vistas genéricas buscan plantillas en /application_name/the_model_name_list.html
    url(r'^projects/$', views.projectlist, name='projects'),
    url(r'^change_prj_select/$', views.change_prj_select, name='change_prj_select'),
    url(r'^update_prj_form/$', views.update_prj_form, name='update_prj_form'),
    url(r'^remove_project/$', views.remove_project, name='remove_project'),
    #url(r'^prj_vers_selected/$', views.prj_vers_selected, name='prj_vers_selected'),
    url(r'^prj_selected/$', views.prj_selected, name='prj_selected'),


    #url(r'^projects/$', views.ProjectListView.as_view(), name='projects'), # las vistas genéricas buscan plantillas en /application_name/the_model_name_list.html
    #url(r'^project/(?P<pk>\d+)$', views.ProjectDetailView.as_view(), name='project-detail'),
]

urlpatterns += [
    url(r'^projects/prj_/(?P<pk>[-\w]+)/$', views.rp_load, name='rp_load'),
    url(r'^update_ECU_list/$', views.update_ECU_list, name='update_ECU_list'),
    url(r'^update_Release_list/$', views.update_Release_list, name='update_Release_list'),
    
]


urlpatterns += [
    url(r'^projects_rp/$', views.projects_rp, name='projects_rp'),
    url(r'^projects/rp/(?P<pk>[-\w]+)/$', views.projects_rp_load, name='projects_rp_load'),
    url(r'^update_version_form/$', views.update_version_form, name='update_version_form'),
    url(r'^remove_version/$', views.remove_version, name='remove_version'),
    url(r'^updatedataproject/$', views.updatedataproject, name='updatedataproject'),                                                                                                                                      
]

urlpatterns += [
    url(r'^ppt/$', views.pptgen, name='pptgen'),    
    url(r'^generatepptdata/$', views.generatePptData, name='generatePptData'),
    url(r'^updatedatevalues/$', views.updatedatevalues, name='updatedatevalues'),                                                                                                                        
]





#  ('^(?P<first_name>[a-zA-Z]+)/(?P<last_name>[a-zA-Z]+)(?:/(?P<title>[a-zA-Z]+))?/$','some_method'),  
"""
urlpatterns += [
    url(r'^myprojects/$', views.LoanedProjectsByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
]
"""
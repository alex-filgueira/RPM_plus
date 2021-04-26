from django.urls import re_path

from . import views


urlpatterns = [
    #re_path(r'^$', views.frontpage_pre, name='frontpage_pre'),
    #re_path(r'^$', views.frontpage, name='frontpage'),
    #re_path(r'^$', views.frontpage_pre, name='frontpage'),
    re_path(r'^$', views.frontpage, name='frontpage'),


    #re_path(r'^projects/$', views.ProjectListView.as_view(), name='projects'), # las vistas genéricas buscan plantillas en /application_name/the_model_name_list.html
    
    #re_path(r'^projects/$', views.projectlist, name='projects'),
    #re_path(r'^change_prj_select/$', views.change_prj_select, name='change_prj_select'),
    #re_path(r'^update_prj_form/$', views.update_prj_form, name='update_prj_form'),
    re_path(r'^remove_project/$', views.remove_project, name='remove_project'),
    #re_path(r'^prj_vers_selected/$', views.prj_vers_selected, name='prj_vers_selected'),
    #re_path(r'^prj_selected/$', views.prj_selected, name='prj_selected'),


    #re_path(r'^projects/$', views.ProjectListView.as_view(), name='projects'), # las vistas genéricas buscan plantillas en /application_name/the_model_name_list.html
    #re_path(r'^project/(?P<pk>\d+)$', views.ProjectDetailView.as_view(), name='project-detail'),
]

urlpatterns += [
    #re_path(r'^projects/prj_/(?P<pk>[-\w]+)/$', views.rp_load, name='rp_load'),
    re_path(r'^update_ECU_list/$', views.update_ECU_list, name='update_ECU_list'),
    re_path(r'^update_Release_list/$', views.update_Release_list, name='update_Release_list'),

    re_path(r'^get_prj_list_user/$', views.get_prj_list_user, name='get_prj_list_user'),
    re_path(r'^copy_ecu_list/$', views.copy_ecu_list, name='copy_ecu_list'),
]


urlpatterns += [
    #re_path(r'^projects_rp/$', views.projects_rp, name='projects_rp'),
    re_path(r'^projects/rp/(?P<pk>[-\w]+)/$', views.projects_rp_load, name='projects_rp_load'),
    #re_path(r'^projects/$', views.projects_rp_load, name='projects_rp_load'),

    re_path(r'^update_project_metadata/$', views.update_project_metadata, name='update_project_metadata'),
    re_path(r'^update_version_form/$', views.update_version_form, name='update_version_form'),
    re_path(r'^remove_version/$', views.remove_version, name='remove_version'),
    re_path(r'^updatedataproject/$', views.updatedataproject, name='updatedataproject'),  

    re_path(r'^getprojectowner/$', views.getprojectowner, name='getprojectowner'),                                                                                                                        
]

urlpatterns += [
    #re_path(r'^ppt/$', views.pptgen, name='pptgen'),    
    re_path(r'^generatepptdata/$', views.generatePptData, name='generatePptData'),
    re_path(r'^updatedatevalues/$', views.updatedatevalues, name='updatedatevalues'),                                                                                                                        
]

urlpatterns += [
    re_path(r'^config_prj/$', views.config_prj, name='config_prj'),   
    re_path(r'^create_type/$', views.create_type, name='create_type'),       
    re_path(r'^create_plan/$', views.create_plan, name='create_plan'),      
    re_path(r'^remove_type/$', views.remove_type, name='remove_type'), 
    re_path(r'^remove_plan/$', views.remove_plan, name='remove_plan'),     
    re_path(r'^update_fig/$', views.update_fig, name='update_fig'),  
    #re_path(r'^create_basics/$', views.create_basics, name='create_basics'),
    re_path(r'^reset_basics_shapes/$', views.reset_basics_shapes, name='reset_basics_shapes'),
    re_path(r'^get_type/$', views.get_type, name='get_type'),
    re_path(r'^get_plan/$', views.get_plan, name='get_plan'),
]

urlpatterns += [
    re_path(r'^user_profile/$', views.user_profile, name='user_profile'),
    re_path(r'^change_pass/$', views.change_pass, name='change_pass'),
    re_path(r'^update_user_data/$', views.update_user_data, name='update_user_data'),
]

urlpatterns += [
    re_path(r'^ie_warning/$', views.ie_warning, name='ie_warning'),
]


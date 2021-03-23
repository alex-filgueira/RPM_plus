from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.frontpage, name='frontpage'),
    #url(r'^projects/$', views.ProjectListView.as_view(), name='projects'), # las vistas genéricas buscan plantillas en /application_name/the_model_name_list.html
    
    #url(r'^projects/$', views.projectlist, name='projects'),
    #url(r'^change_prj_select/$', views.change_prj_select, name='change_prj_select'),
    #url(r'^update_prj_form/$', views.update_prj_form, name='update_prj_form'),
    url(r'^remove_project/$', views.remove_project, name='remove_project'),
    #url(r'^prj_vers_selected/$', views.prj_vers_selected, name='prj_vers_selected'),
    #url(r'^prj_selected/$', views.prj_selected, name='prj_selected'),


    #url(r'^projects/$', views.ProjectListView.as_view(), name='projects'), # las vistas genéricas buscan plantillas en /application_name/the_model_name_list.html
    #url(r'^project/(?P<pk>\d+)$', views.ProjectDetailView.as_view(), name='project-detail'),
]

urlpatterns += [
    #url(r'^projects/prj_/(?P<pk>[-\w]+)/$', views.rp_load, name='rp_load'),
    url(r'^update_ECU_list/$', views.update_ECU_list, name='update_ECU_list'),
    url(r'^update_Release_list/$', views.update_Release_list, name='update_Release_list'),

    url(r'^get_prj_list_user/$', views.get_prj_list_user, name='get_prj_list_user'),
    url(r'^copy_ecu_list/$', views.copy_ecu_list, name='copy_ecu_list'),
    
]


urlpatterns += [
    #url(r'^projects_rp/$', views.projects_rp, name='projects_rp'),
    url(r'^projects/rp/(?P<pk>[-\w]+)/$', views.projects_rp_load, name='projects_rp_load'),
    url(r'^update_project_metadata/$', views.update_project_metadata, name='update_project_metadata'),
    url(r'^update_version_form/$', views.update_version_form, name='update_version_form'),
    url(r'^remove_version/$', views.remove_version, name='remove_version'),
    url(r'^updatedataproject/$', views.updatedataproject, name='updatedataproject'),                                                                                                                                      
]

urlpatterns += [
    #url(r'^ppt/$', views.pptgen, name='pptgen'),    
    url(r'^generatepptdata/$', views.generatePptData, name='generatePptData'),
    url(r'^updatedatevalues/$', views.updatedatevalues, name='updatedatevalues'),                                                                                                                        
]

urlpatterns += [
    url(r'^config_prj/$', views.config_prj, name='config_prj'),   
    url(r'^create_type/$', views.create_type, name='create_type'),       
    url(r'^create_plan/$', views.create_plan, name='create_plan'),      
    url(r'^remove_type/$', views.remove_type, name='remove_type'), 
    url(r'^remove_plan/$', views.remove_plan, name='remove_plan'),     
    url(r'^update_fig/$', views.update_fig, name='update_fig'),  
    url(r'^create_basics/$', views.create_basics, name='create_basics'),
    url(r'^get_type/$', views.get_type, name='get_type'),
    url(r'^get_plan/$', views.get_plan, name='get_plan'),
]

urlpatterns += [
    url(r'^user_profile/$', views.user_profile, name='user_profile'),
    url(r'^change_pass/$', views.change_pass, name='change_pass'),
    url(r'^update_user_data/$', views.update_user_data, name='update_user_data'),
]


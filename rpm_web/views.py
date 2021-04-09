from django.shortcuts import render

# Create your views here.
#Autentificaciones: https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Authentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from django.contrib.auth.models import User

from django.contrib.auth.decorators import permission_required
from django.views import generic

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.http import JsonResponse
import json

from datetime import date
from datetime import datetime

from django.contrib.auth.forms import UserCreationForm

#------------IE (internet Explorer) warning----------------------------------------
#------------------------------------------------------------------------
def ie_warning(request):
    print("ie_warning()")
    if request.user.is_authenticated:
        context = {
            'ok':True,
        } 
        # Renderiza la plantilla HTML index.html con los datos en la variable contexto
        return render(request,'ie_warning.html',context=context)
    else:
        return HttpResponseRedirect(reverse('login') )



#------------User profile----------------------------------------
#------------------------------------------------------------------------
def update_user_data(request):
    print("update_user_data()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)
            print("json_table:",json_table)

            if 'user_first_name' in json_table:
                u = User.objects.get(username= request.user)
                u.first_name= json_table['user_first_name']
                u.save()
            if 'user_email' in json_table:
                u = User.objects.get(username= request.user)
                u.email= json_table['user_email']
                u.save()
            
        return JsonResponse({
            'ok':True,
        })
    else:
        return HttpResponseRedirect(reverse('login') )


def change_pass(request):
    print("change_pass()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)
            print("json_table:",json_table)

            flag_pass_old = False
            flag_pass_new = False
            if 'old_pass' in json_table:
                #Check the old/actual pass
                if request.user.check_password(json_table['old_pass']): #Compare password
                    flag_pass_old = True
            if 'new_pass' in json_table:
                #Save the new pass
                u = User.objects.get(username= request.user)
                u.set_password(json_table['new_pass'])
                u.save()
                flag_pass_new = True

            
        return JsonResponse({
            'ok':True,
            'flag_pass_old':flag_pass_old,
            'flag_pass_new':flag_pass_new,
        })
    else:
        return HttpResponseRedirect(reverse('login') )


from django.core.mail import send_mail
from django.conf import settings

def user_profile(request):
    print("user_profile()")
    if request.user.is_authenticated:
        #if request.method == 'POST':
        print("user:",request.user)
        user_obj = User.objects.filter(username = request.user) # https://docs.djangoproject.com/en/3.1/ref/contrib/auth/
        print("obj:",user_obj)
        username = ""
        email = ""
        first_name = ""
        last_name = ""
        #groups = ""
        date_joined = ""

        for obj in user_obj:
            username = obj.username
            email = obj.email
            first_name = obj.first_name
            last_name = obj.last_name
            groups = obj.groups

            date_joined = obj.date_joined
            print("email:",obj.email)
            print("first_name:",obj.first_name)
            print("last_name:",obj.last_name)
            print("password:",obj.password)
            #print("groups:",obj.groups)
            print("user_permissions:",obj.user_permissions)
            print("is_staff:",obj.is_staff)
            print("is_active:",obj.is_active)
            print("is_superuser:",obj.is_superuser)
            print("last_login:",obj.last_login)
            print("date_joined:",obj.date_joined)

        #Get the groups for the user
        l = request.user.groups.values_list('name',flat = True) # QuerySet Object
        groups_list = list(l)
        """
        group = ""
        print("groups_list:",groups_list)
        if len(groups_list) > 0:
            group = groups_list[0]
        else:
            group = "no group"
        """
        #get first_time for tutorial
        flag_first_time_profile = False
        user_extra_list = MUser_extra.objects.filter(id_user = request.user.id)
        if user_extra_list.count() > 0:
             user_extra = MUser_extra.objects.get(id_user = request.user.id)
             flag_first_time_profile = user_extra.flag_first_time_profile
             user_extra.flag_first_time_profile = False
             user_extra.save()

        context = {
            'ok':True,
            'username':username,
            'email':email,
            'first_name':first_name,
            'last_name':last_name,
            #'groups':groups,
            'groups':groups_list,
            'date_joined':date_joined,
            #'group':group,
            'flag_first_time_profile':flag_first_time_profile,
        }

        #test send mails
        """
        print("test mail")

        subject = 'That’s your subject' 
        email_from = settings.EMAIL_HOST_USER
        to = 'alexandre.filgueira@seat.es'
        plain_message = "lalala"

        print(send_mail(subject, plain_message, email_from, [to], ))

        print("send mail")
        """
        # Renderiza la plantilla HTML index.html con los datos en la variable contexto
        return render(request,'user_profile.html',context=context)
    else:
        return HttpResponseRedirect(reverse('login') )


#------------Config projects----------------------------------------
#------------------------------------------------------------------------

def get_plan(request):
    print("get_plan()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)
            print("json_table:",json_table)

            plan_ = ""
            plan_fig1_color_1  = ""
            plan_fig1_color_2  = ""
            plan_fig1_color_3  = ""
            plan_fig1_border_w = 0
            if 'plan_id' in json_table:
                plan_ = MPlan2.objects.get(id=json_table['plan_id'])
                plan_fig1_color_1 = plan_.fig1_color_1
                plan_fig1_color_2 = plan_.fig1_color_2
                plan_fig1_color_3 = plan_.fig1_color_3
                plan_fig1_border_w = plan_.fig1_border_w


            
        return JsonResponse({
            'ok':True,
            'plan_fig1_color_1':plan_fig1_color_1,
            'plan_fig1_color_2':plan_fig1_color_2,
            'plan_fig1_color_3':plan_fig1_color_3,
            'plan_fig1_border_w':plan_fig1_border_w,
        })
    else:
        return HttpResponseRedirect(reverse('login') )

def get_type(request):
    print("get_type()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)
            print("json_table:",json_table)

            type_ = ""
            type_fig1_name = ""
            type_fig1_s = ""
            if 'type_id' in json_table:
                type_ = MType_input2.objects.get(id=json_table['type_id'])
                type_fig1_name = type_.fig1_name
                type_fig1_s = type_.fig1_s

            
        return JsonResponse({
            'ok':True,
            'type_fig1_name':type_fig1_name,
            'type_fig1_s':type_fig1_s,
        })
    else:
        return HttpResponseRedirect(reverse('login') )

def create_basics(request):
    print("create_basics()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)
            print("json_table:",json_table)
            print("type_list If is empty, create")
            #create diamond -> SW
            type_ = MType_input2()
            type_.id_user_id = request.user.id
            type_.name = "SW"
            type_.fig1_name = "pptx.ShapeType.diamond"
            type_.fig1_s = 0.28
            type_.save()
            #create diamond(triangle) -> HW
            type_ = MType_input2()
            type_.id_user_id = request.user.id
            type_.name = "HW"
            type_.fig1_name = "pptx.ShapeType.triangle"
            type_.fig1_s = 0.28
            type_.save()
            #create hexagon -> ZDC
            type_ = MType_input2()
            type_.id_user_id = request.user.id
            type_.name = "ZDC"
            type_.fig1_name = "pptx.ShapeType.hexagon"
            type_.fig1_s = 0.28
            type_.save()
        
            print("plan_list If is empty, create")
            #create vbv
            plan_ = MPlan2()
            plan_.id_user_id = request.user.id
            plan_.name = "vbv"
            plan_.fig1_color_1 = "#00b0f0" #fill color //azul
            plan_.fig1_color_2 = "#000000" #border color //negro
            plan_.fig1_border_w = 1.75 #border w
            plan_.save()
            #create te.vbv
            plan_ = MPlan2()
            plan_.id_user_id = request.user.id
            plan_.name = "te.vbv"
            plan_.fig1_color_1 = "#00b0f0" #fill color //azul
            plan_.fig1_color_2 = "#7f7f7f" #border color //gris oscuro
            plan_.fig1_border_w = 0.75 #border w
            plan_.save()
            #create planned
            plan_ = MPlan2()
            plan_.id_user_id = request.user.id
            plan_.name = "planned"
            plan_.fig1_color_1 = "#d9d9d9" #fill color //gris
            plan_.fig1_color_2 = "#7f7f7f" #border color //gris oscuro
            plan_.fig1_border_w = 0.75 #border w
            plan_.save()
            #create additional
            plan_ = MPlan2()
            plan_.id_user_id = request.user.id
            plan_.name = "additional"
            plan_.fig1_color_1 = "#d9d9d9" #fill color //gris
            plan_.fig1_color_2 = "#ff0000" #border color //rojo
            plan_.fig1_border_w = 1.75 #border w
            plan_.save()

            
        return JsonResponse({
            'ok':True,
        })
    else:
        return HttpResponseRedirect(reverse('login') )

def reset_basics_shapes(request):
    print("reset_basics_shapes()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)
            print("json_table:",json_table)
            print("type_list If is empty, create")
            #create diamond -> SW
            #type_ = MType_input2()
            type_list = MType_input2.objects.filter(id_user = request.user.id)
            for type_ in type_list:
                if type_.name == "SW":
                    type_.fig1_name = "pptx.ShapeType.diamond"
                    type_.fig1_s = 0.28
                    type_.save()
                #create diamond(triangle) -> HW
                if type_.name == "HW":
                    type_.fig1_name = "pptx.ShapeType.triangle"
                    type_.fig1_s = 0.28
                    type_.save()
                #create hexagon -> ZDC
                if type_.name == "ZDC":
                    type_.fig1_name = "pptx.ShapeType.hexagon"
                    type_.fig1_s = 0.28
                    type_.save()
        
            print("plan_list If is empty, create")
            #create vbv
            #plan_ = MPlan2()
            plan_list = MPlan2.objects.filter(id_user = request.user.id)
            for plan_ in plan_list:
                if plan_.name == "vbv":
                    plan_.fig1_color_1 = "#00b0f0" #fill color //azul
                    plan_.fig1_color_2 = "#000000" #border color //negro
                    plan_.fig1_border_w = 1.75 #border w
                    plan_.save()
            #create te.vbv
                if plan_.name == "te.vbv":
                    plan_.fig1_color_1 = "#00b0f0" #fill color //azul
                    plan_.fig1_color_2 = "#7f7f7f" #border color //gris oscuro
                    plan_.fig1_border_w = 0.75 #border w
                    plan_.save()
            #create planned
                if plan_.name == "planned":
                    plan_.fig1_color_1 = "#d9d9d9" #fill color //gris
                    plan_.fig1_color_2 = "#7f7f7f" #border color //gris oscuro
                    plan_.fig1_border_w = 0.75 #border w
                    plan_.save()
            #create additional
                if plan_.name == "additional":
                    plan_.fig1_color_1 = "#d9d9d9" #fill color //gris
                    plan_.fig1_color_2 = "#ff0000" #border color //rojo
                    plan_.fig1_border_w = 1.75 #border w
                    plan_.save()

            
        return JsonResponse({
            'ok':True,
        })
    else:
        return HttpResponseRedirect(reverse('login') )


def update_fig(request):
    print("update_fig()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)
            print("json_table:",json_table)

            if 'type_id' in json_table and  'plan_id' in json_table:
                type_ = MType_input2.objects.get(id=json_table['type_id'])
                plan_ = MPlan2.objects.get(id=json_table['plan_id'])
                if 'shape_name' in json_table:
                    type_.fig1_name = json_table['shape_name']
                if 'shape_s' in json_table:
                    type_.fig1_s = json_table['shape_s']
                if 'fill_color' in json_table:
                    plan_.fig1_color_1 = json_table['fill_color']
                if 'border_color' in json_table:
                    plan_.fig1_color_2 = json_table['border_color']
                if 'border_w' in json_table:
                    plan_.fig1_border_w = json_table['border_w']
                
                type_.save()
                plan_.save()

            
        return JsonResponse({
            'ok':True,
        })
    else:
        return HttpResponseRedirect(reverse('login') )

def remove_type(request):
    print("remove_type()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)
            print("json_table:",json_table)

            if 'type_id' in json_table:
                type_ = MType_input2.objects.get(id=json_table['type_id'])
                type_.delete()

            
        return JsonResponse({
            'ok':True,
        })
    else:
        return HttpResponseRedirect(reverse('login') )

def remove_plan(request):
    print("remove_plan()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)
            print("json_table:",json_table)

            if 'plan_id' in json_table:
                plan_ = MPlan2.objects.get(id=json_table['plan_id'])
                plan_.delete()

            
        return JsonResponse({
            'ok':True,
        })
    else:
        return HttpResponseRedirect(reverse('login') )

def create_type(request):
    print("create_type()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)
            print("json_table:",json_table)

            type_id = 0
            if 'type_name' in json_table:
                #save Type data
                type_ = MType_input2()
                type_.id_user_id = request.user.id
                type_.name = json_table['type_name']
                if 'fig1_name' in json_table:
                    type_.fig1_name = json_table['fig1_name']
                if 'fig1_s' in json_table:
                    type_.fig1_s = json_table['fig1_s']
                type_.save()
                type_id = type_.id
            
        return JsonResponse({
            'ok':True,
            'type_id':type_id,
        })
    else:
        return HttpResponseRedirect(reverse('login') )


def create_plan(request):
    print("create_plan()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)
            print("json_table:",json_table)

            plan_id = 0
            if 'plan_name' in json_table:
                #save Plan data
                plan_ = MPlan2()
                plan_.id_user_id = request.user.id
                plan_.name = json_table['plan_name']
                if 'fig1_color_1' in json_table:
                    plan_.fig1_color_1 = json_table['fig1_color_1']
                if 'fig1_color_2' in json_table:    
                    plan_.fig1_color_2 = json_table['fig1_color_2']
                if 'fig1_color_3' in json_table:
                    plan_.fig1_color_3 = json_table['fig1_color_3']
                if 'fig1_border_w' in json_table:
                    plan_.fig1_border_w = json_table['fig1_border_w']
                plan_.save()
                plan_id = plan_.id
            
        return JsonResponse({
            'ok':True,
            'plan_id':plan_id,
        })
    else:
        return HttpResponseRedirect(reverse('login') )


def config_prj(request):
    print("config_prj()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)
            print("json_table:",json_table)

            #save Config project data
            config_prj = MConfig_prj.objects.get(id_user=request.user.id)
            if 'marked1_color' in json_table:
                config_prj.marked1_color = json_table['marked1_color']
            if 'marked1_w' in json_table:
                config_prj.marked1_w = json_table['marked1_w']
            if 'marked2_color' in json_table:
                config_prj.marked2_color = json_table['marked2_color']
            if 'marked2_w' in json_table:
                config_prj.marked2_w = json_table['marked2_w']
            if 'marked3_color' in json_table:
                config_prj.marked3_color = json_table['marked3_color']
            if 'marked3_w' in json_table:
                config_prj.marked3_w = json_table['marked3_w']

            if 'week_color' in json_table:
                config_prj.week_color = json_table['week_color']
            if 'week_s' in json_table:
                config_prj.week_s = json_table['week_s']

            if 'flag_head' in json_table:
                config_prj.flag_head = json_table['flag_head']
            if 'flag_footer' in json_table:
                config_prj.flag_footer = json_table['flag_footer']
            if 'flag_title' in json_table:
                config_prj.flag_title = json_table['flag_title']
            if 'flag_legend' in json_table:
                config_prj.flag_legend = json_table['flag_legend']
            if 'flag_logo' in json_table:
                config_prj.flag_logo = json_table['flag_logo']
            if 'flag_status_date' in json_table:
                config_prj.flag_status_date = json_table['flag_status_date']

            if 'title' in json_table:
                config_prj.title = json_table['title']
            if 'created_by' in json_table:
                config_prj.created_by = json_table['created_by']
            if 'logo_url' in json_table:
                config_prj.logo_url = json_table['logo_url']

            config_prj.save()

        #get first_time for tutorial
        flag_first_time_conf = False
        user_extra_list = MUser_extra.objects.filter(id_user = request.user.id)
        if user_extra_list.count() > 0:
             user_extra = MUser_extra.objects.get(id_user = request.user.id)
             flag_first_time_conf = user_extra.flag_first_time_conf
             user_extra.flag_first_time_conf = False
             user_extra.save()

        print("request.user.id:",request.user.id)
        config_prj_list = MConfig_prj.objects.filter(id_user=request.user.id)
        if(len(config_prj_list) == 0):
            print("config_prj If is empty, create")
            config_prj = MConfig_prj()
            config_prj.id_user_id = request.user.id
            config_prj.save()

        #Check
        config_prj_list = MConfig_prj.objects.get(id_user=request.user.id)
        print("config_prj_list.id:",config_prj_list.id)

        #type_list = []
        create_predef_type(request.user.id)
        type_list = MType_input2.objects.filter(id_user=request.user.id)
        #plan_list = []
        create_predef_plan(request.user.id)
        plan_list = MPlan2.objects.filter(id_user=request.user.id)

        context = {
            'ok':True,
            'config_prj':config_prj_list,
            'type_list':type_list,
            'plan_list':plan_list,
            'flag_first_time_conf':flag_first_time_conf,
        } 

        # Renderiza la plantilla HTML index.html con los datos en la variable contexto
        return render(request,'config_prj.html',context=context)
    else:
        return HttpResponseRedirect(reverse('login') )





#------------PPT generation----------------------------------------
#------------------------------------------------------------------------

def updatedatevalues(request):
    print("updatedatevalues()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)
            print("json_table:",json_table)

            date_ini = json_table['date_ini']
            date_status = json_table['date_status']
            date_end = json_table['date_end']
            #print("date_status:",date_status)

            factor_weeks = json_table['factor_weeks']
            max_ecu_slide = json_table['max_ecu_slide']

            prj_id = json_table['prj_id']
            MProject_objt_selected = MProject.objects.get(id=prj_id)

            MProject_objt_selected.date_ini = date_ini
            MProject_objt_selected.date_status = date_status
            MProject_objt_selected.date_end = date_end

            MProject_objt_selected.factor_weeks = factor_weeks
            MProject_objt_selected.max_ecu_slide = max_ecu_slide

            MProject_objt_selected.save()

            # Take date_ini (date) to CW
            print("date_ini:",date_ini)
            
            date_ini_obj = datetime.strptime(date_ini,'%Y-%m-%d')
            #print("date_ini_obj:",date_ini_obj)

            cw_ini = datetime.date(date_ini_obj).strftime("%V")
            print("cw_ini:",cw_ini)

            y_ini = datetime.date(date_ini_obj).strftime("%Y")
            print("y_ini:",y_ini)

            date_status_obj = datetime.strptime(date_status,'%Y-%m-%d')
            cw_status = datetime.date(date_status_obj).strftime("%V")
            y_status = datetime.date(date_status_obj).strftime("%Y")
        
            date_end_obj = datetime.strptime(date_end,'%Y-%m-%d')
            cw_end = datetime.date(date_end_obj).strftime("%V")
            y_end = datetime.date(date_end_obj).strftime("%Y")

        return JsonResponse({
            'ok':True,
            'date_ini': date_ini, #new
            'date_status': date_status, #new
            'date_end': date_end, #new

            'cw_ini': cw_ini, #new
            'y_ini': y_ini, #new
            'cw_status': cw_status, #new
            'y_status': y_status, #new
            'cw_end': cw_end, #new
            'y_end': y_end, #new

            'factor_weeks': factor_weeks, #new
            'max_ecu_slide': max_ecu_slide, #new
        })
    else:
        return HttpResponseRedirect(reverse('login') )
            

def generatePptData(request):
    print("generatePptData()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)

            prj_id = json_table['prj_id']
            print("prj_id:",prj_id)

            MProject_objt_selected = MProject.objects.filter(id=prj_id)
            for obj in MProject_objt_selected:
                prj_name = obj.name

            version_id = json_table['version_id']
            print("version_id:",version_id)

            ecuList_name = []
            ecuList_id = []#Extra
            ecuList_comment = []#Extra
            ecuList_dx = []#Extra

            RelInList_id = []
            RelInList_id_ecu = []
            RelInList_id_type = []

            RelInList_n_version = []
            RelInList_date = []
            RelInList_plan = []
            RelInList_id_plan = []
            RelInList_visual = []
            RelInList_dx = []
            RelInList_comment = []
            RelInList_marked1 = []

            RelInList_ecu_name = []#Extra
            RelInList_type_name = []#Extra

            RelInList_type_fig1_name = []#Extra
            RelInList_type_fig1_s = []#Extra

            RelInList_plan_fig1_color_1 = []#extra
            RelInList_plan_fig1_color_2 = []#extra
            RelInList_plan_fig1_color_3 = []#extra
            RelInList_plan_fig1_border_w = []#extra


            nECU = 0
            ecu_id = 0
            #Get ECU list
            ECUlist_objt_selected = MECU.objects.filter(id_version=version_id)
            #flag_new_ecu = True


            ecuList_name_pre = []
            ecuList_id_pre = []#Extra
            ecuList_comment_pre = []#Extra
            ecuList_dx_pre = []#Extra
            ecuList_order_pre = []
            for elt in ECUlist_objt_selected:
                #print("name eculist: ",elt.name)
                ecuList_name_pre.append(elt.name)
                ecuList_comment_pre.append(elt.comment)
                ecuList_dx_pre.append(elt.dx_ecu)
                ecuList_id_pre.append(str(elt.id))
                ecuList_order_pre.append(elt.order)


            ecuList_name_sorted = []
            ecuList_comment_sorted  = []
            ecuList_dx_sorted  = []
            ecuList_id_sorted  = []

            ecuList_order_sorted = sorted(ecuList_order_pre)
            for i in ecuList_order_sorted:
                #print(ecuList_order_sorted[i-1])
                cont_j = 0
                for j in ecuList_order_pre:
                    cont_j += 1
                    if i == j:
                        ecuList_name_sorted.append(ecuList_name_pre[cont_j-1])
                        ecuList_comment_sorted.append(ecuList_comment_pre[cont_j-1])
                        ecuList_dx_sorted.append(ecuList_dx_pre[cont_j-1])
                        ecuList_id_sorted.append(ecuList_id_pre[cont_j-1])




            #for obj in ECUlist_objt_selected:
            cont_i = 0
            for i in ecuList_id_sorted:
                cont_i += 1
                #ecuList_name.append(obj.name)
                #ecu_id = obj.id
                flag_new_ecu = True

                #Get sw/hw/zdc inputs for each ECU -> MRelease_input
                #MR_inputlist_objt_selected = MRelease_input.objects.filter(id_ecu=obj.id).filter(flag_visual=True)

                MR_inputlist_objt_selected = MRelease_input.objects.filter(id_ecu=i).filter(flag_visual=True)
                for elt in MR_inputlist_objt_selected:
                    if flag_new_ecu == True:
                        nECU = nECU + 1
                        flag_new_ecu = False
                        """
                        ecuList_comment.append(obj.comment)
                        ecuList_dx.append(obj.dx_ecu)
                        ecuList_name.append(obj.name)
                        ecuList_id.append(obj.id)
                        ecu_id = obj.id
                        """
                        ecuList_comment.append(ecuList_comment_sorted[cont_i-1])
                        ecuList_dx.append(ecuList_dx_sorted[cont_i-1])
                        ecuList_name.append(ecuList_name_sorted[cont_i-1])
                        ecuList_id.append(ecuList_id_sorted[cont_i-1])
                        ecu_id = ecuList_id_sorted[cont_i-1]
                        print("nECU:",nECU)

                        
                    print("founded id:",elt.id)
                    RelInList_id.append(str(elt.id))
                    RelInList_id_ecu.append(str(elt.id_ecu_id))
                    RelInList_id_type.append(str(elt.id_type_input_id))
                    RelInList_n_version.append(elt.n_version)
                    RelInList_date.append(elt.date_beantragt)
                    #RelInList_plan.append(elt.plan)
                    RelInList_id_plan.append(str(elt.id_plan_id))
                    RelInList_visual.append(str(elt.flag_visual))
                    #print("visual:",elt.flag_visual) #¿?¿?¿?

                    #RelInList_dx.append(elt.dx_ecu)
                    RelInList_comment.append(elt.comment)
                    RelInList_marked1.append(str(elt.flag_marked1))

                    ecu_name = MECU.objects.get(id=ecu_id).name #Get ecu name for this Ri
                    print("ecu_name:",ecu_name)
                    RelInList_ecu_name.append(ecu_name)
                    #print("elt.id_ecu:",elt.id_ecu_id)
                    type_name = MType_input2.objects.get(id=elt.id_type_input_id).name 
                    RelInList_type_name.append(type_name)

                    type_fig1_name = MType_input2.objects.get(id=elt.id_type_input_id).fig1_name 
                    RelInList_type_fig1_name.append(type_fig1_name)

                    type_fig1_s = MType_input2.objects.get(id=elt.id_type_input_id).fig1_s 
                    RelInList_type_fig1_s.append(type_fig1_s)

                    plan_name = MPlan2.objects.get(id=elt.id_plan_id).name 
                    RelInList_plan.append(plan_name)

                    plan_fig1_color_1 = MPlan2.objects.get(id=elt.id_plan_id).fig1_color_1 
                    RelInList_plan_fig1_color_1.append(plan_fig1_color_1)

                    plan_fig1_color_2 = MPlan2.objects.get(id=elt.id_plan_id).fig1_color_2 
                    RelInList_plan_fig1_color_2.append(plan_fig1_color_2)

                    plan_fig1_color_3 = MPlan2.objects.get(id=elt.id_plan_id).fig1_color_3 
                    RelInList_plan_fig1_color_3.append(plan_fig1_color_3)

                    plan_fig1_border_w = MPlan2.objects.get(id=elt.id_plan_id).fig1_border_w 
                    RelInList_plan_fig1_border_w.append(plan_fig1_border_w)

                    ecu_obj = MECU.objects.get(id=elt.id_ecu_id) 
                    RelInList_dx.append(ecu_obj.dx_ecu)


        #Config project model
        if MConfig_prj.objects.filter(id_user_id=request.user.id).count() == 0:                    
            #If not exist, create it
            new_MConfig = MConfig_prj()
            new_MConfig.id_user = request.user.id
            new_MConfig.save()


        prj_marked1_color = MConfig_prj.objects.get(id_user_id=request.user.id).marked1_color
        prj_marked1_w = MConfig_prj.objects.get(id_user_id=request.user.id).marked1_w
        prj_marked2_color = MConfig_prj.objects.get(id_user_id=request.user.id).marked2_color
        prj_marked2_w = MConfig_prj.objects.get(id_user_id=request.user.id).marked2_w
        prj_marked3_color = MConfig_prj.objects.get(id_user_id=request.user.id).marked3_color
        prj_marked3_w = MConfig_prj.objects.get(id_user_id=request.user.id).marked3_w

        prj_week_color = MConfig_prj.objects.get(id_user_id=request.user.id).week_color
        prj_week_s = MConfig_prj.objects.get(id_user_id=request.user.id).week_s

        prj_flag_head= MConfig_prj.objects.get(id_user_id=request.user.id).flag_head
        prj_flag_footer= MConfig_prj.objects.get(id_user_id=request.user.id).flag_footer 
        prj_flag_title= MConfig_prj.objects.get(id_user_id=request.user.id).flag_title 
        prj_flag_legend= MConfig_prj.objects.get(id_user_id=request.user.id).flag_legend 
        prj_flag_logo= MConfig_prj.objects.get(id_user_id=request.user.id).flag_logo 
        prj_flag_status_date= MConfig_prj.objects.get(id_user_id=request.user.id).flag_status_date
        
        prj_title= MConfig_prj.objects.get(id_user_id=request.user.id).title 
        prj_created_by= MConfig_prj.objects.get(id_user_id=request.user.id).created_by 
        prj_logo_url= MConfig_prj.objects.get(id_user_id=request.user.id).logo_url 



        #type list
        type_list = []
        type_obj_list = MType_input2.objects.filter(id_user_id=request.user.id)
        for elem in type_obj_list:
            type_list.append(elem.name)
            type_list.append(elem.fig1_name)
            type_list.append(elem.fig1_s)

        #plan list
        plan_list = []
        plan_obj_list = MPlan2.objects.filter(id_user_id=request.user.id)
        for elem in plan_obj_list:
            plan_list.append(elem.name)
            plan_list.append(elem.fig1_color_1)
            plan_list.append(elem.fig1_color_2)
            plan_list.append(elem.fig1_color_3)
            plan_list.append(elem.fig1_border_w)


        return JsonResponse({
                    'RelInList_id': RelInList_id,
                    'RelInList_id_ecu': RelInList_id_ecu,
                    'RelInList_id_type': RelInList_id_type,
                    'RelInList_n_version': RelInList_n_version,
                    'RelInList_date': RelInList_date,
                    'RelInList_plan': RelInList_plan,
                    'RelInList_plan_fig1_color_1':RelInList_plan_fig1_color_1,
                    'RelInList_plan_fig1_color_2':RelInList_plan_fig1_color_2,
                    'RelInList_plan_fig1_color_3':RelInList_plan_fig1_color_3,
                    'RelInList_plan_fig1_border_w':RelInList_plan_fig1_border_w,
                    'RelInList_id_plan': RelInList_id_plan,
                    'RelInList_type_name': RelInList_type_name,
                    'RelInList_type_fig1_name':RelInList_type_fig1_name,
                    'RelInList_type_fig1_s':RelInList_type_fig1_s,
                    'RelInList_visual': RelInList_visual,
                    'RelInList_dx': RelInList_dx,
                    'RelInList_comment': RelInList_comment,
                    'RelInList_marked1': RelInList_marked1,

                    'RelInList_ecu_name': RelInList_ecu_name,
                    
                    'ecuList_comment': ecuList_comment,
                    'ecuList_dx': ecuList_dx,
                    'ecuList_name': ecuList_name,
                    'ecuList_id': ecuList_id,
                    'nECU': nECU,

                    'prj_name': prj_name,

                    'plan_list': plan_list,
                    'type_list': type_list,

                    'prj_marked1_color': prj_marked1_color,
                    'prj_marked1_w': prj_marked1_w,
                    'prj_marked2_color': prj_marked2_color,
                    'prj_marked2_w': prj_marked2_w,
                    'prj_marked3_color': prj_marked3_color,
                    'prj_marked3_w': prj_marked3_w,

                    'prj_week_color': prj_week_color,
                    'prj_week_s': prj_week_s,

                    'prj_flag_head': prj_flag_head,
                    'prj_flag_footer': prj_flag_footer,
                    'prj_flag_title': prj_flag_title,
                    'prj_flag_legend': prj_flag_legend,
                    'prj_flag_logo': prj_flag_logo,
                    'prj_flag_status_date': prj_flag_status_date,

                    'prj_title': prj_title,
                    'prj_created_by': prj_created_by,
                    'prj_logo_url': prj_logo_url,

        })

    else:
        return HttpResponseRedirect(reverse('login') )


#------------Users----------------------------------------
#------------------------------------------------------------------------
from .forms import CustomUserCreationForm
from django.contrib import messages

def create_predef_type(user_id):
            type_list = MType_input2.objects.filter(id_user=user_id)
            if(len(type_list) == 0):
                print("type_list If is empty, create")
                #create diamond -> SW
                type_ = MType_input2()
                type_.id_user_id = user_id
                type_.name = "SW"
                type_.fig1_name = "pptx.ShapeType.diamond"
                type_.fig1_s = 0.28
                type_.save()
                #create diamond(triangle) -> HW
                type_ = MType_input2()
                type_.id_user_id = user_id
                type_.name = "HW"
                type_.fig1_name = "pptx.ShapeType.triangle"
                type_.fig1_s = 0.28
                type_.save()
                #create hexagon -> ZDC
                type_ = MType_input2()
                type_.id_user_id = user_id
                type_.name = "ZDC"
                type_.fig1_name = "pptx.ShapeType.hexagon"
                type_.fig1_s = 0.28
                type_.save()

def create_predef_plan(user_id):
            plan_list = MPlan2.objects.filter(id_user=user_id)
            if(len(plan_list) == 0):
                print("plan_list If is empty, create")
                #create vbv
                plan_ = MPlan2()
                plan_.id_user_id = user_id
                plan_.name = "vbv"
                plan_.fig1_color_1 = "00b0f0" #fill color //azul
                plan_.fig1_color_2 = "000000" #border color //negro
                plan_.fig1_border_w = 1.75 #border w
                plan_.save()
                #create te.vbv
                plan_ = MPlan2()
                plan_.id_user_id = user_id
                plan_.name = "te.vbv"
                plan_.fig1_color_1 = "00b0f0" #fill color //azul
                plan_.fig1_color_2 = "7f7f7f" #border color //gris oscuro
                plan_.fig1_border_w = 0.75 #border w
                plan_.save()
                #create planned
                plan_ = MPlan2()
                plan_.id_user_id = user_id
                plan_.name = "planned"
                plan_.fig1_color_1 = "d9d9d9" #fill color //gris
                plan_.fig1_color_2 = "7f7f7f" #border color //gris oscuro
                plan_.fig1_border_w = 0.75 #border w
                plan_.save()
                #create additional
                plan_ = MPlan2()
                plan_.id_user_id = user_id
                plan_.name = "additional"
                plan_.fig1_color_1 = "d9d9d9" #fill color //gris
                plan_.fig1_color_2 = "ff0000" #border color //rojo
                plan_.fig1_border_w = 1.75 #border w
                plan_.save()





def register(request):
    notes = []
    flag_ok = False
    if request.method == 'POST':
        json_table = json.loads(request.body)
        print("json_table:",json_table)
        
        if User.objects.filter(email = json_table['email']).count() > 0:
            notes.append("This email is in use for other user")

        print("notes:",notes)

        if len(notes) == 0:
            print("save user")

            user = User.objects.create_user(json_table['user'],json_table['email'],json_table['pass1'] )

            user.save()

            messages.success(request, 'Account created successfully')

            #Create first inputs in BBDD
            #Populate the first project config
            config_prj_list = MConfig_prj.objects.filter(id_user=user.id)
            if(len(config_prj_list) == 0):
                print("config_prj If is empty, create")
                config_prj = MConfig_prj()
                config_prj.id_user_id = user.id
                config_prj.save()
            
            type_list = MType_input2.objects.filter(id_user=user.id)
            if(len(type_list) == 0):
                print("type_list If is empty, create")
                #create diamond -> SW
                type_ = MType_input2()
                type_.id_user_id = user.id
                type_.name = "SW"
                type_.fig1_name = "pptx.ShapeType.diamond"
                type_.fig1_s = 0.28
                type_.save()
                #create diamond(triangle) -> HW
                type_ = MType_input2()
                type_.id_user_id = user.id
                type_.name = "HW"
                type_.fig1_name = "pptx.ShapeType.triangle"
                type_.fig1_s = 0.28
                type_.save()
                #create hexagon -> ZDC
                type_ = MType_input2()
                type_.id_user_id = user.id
                type_.name = "ZDC"
                type_.fig1_name = "pptx.ShapeType.hexagon"
                type_.fig1_s = 0.28
                type_.save()
            
            plan_list = MPlan2.objects.filter(id_user=user.id)
            if(len(plan_list) == 0):
                print("plan_list If is empty, create")
                #create vbv
                plan_ = MPlan2()
                plan_.id_user_id = user.id
                plan_.name = "vbv"
                plan_.fig1_color_1 = "00b0f0" #fill color //azul
                plan_.fig1_color_2 = "000000" #border color //negro
                plan_.fig1_border_w = 1.75 #border w
                plan_.save()
                #create te.vbv
                plan_ = MPlan2()
                plan_.id_user_id = user.id
                plan_.name = "te.vbv"
                plan_.fig1_color_1 = "00b0f0" #fill color //azul
                plan_.fig1_color_2 = "7f7f7f" #border color //gris oscuro
                plan_.fig1_border_w = 0.75 #border w
                plan_.save()
                #create planned
                plan_ = MPlan2()
                plan_.id_user_id = user.id
                plan_.name = "planned"
                plan_.fig1_color_1 = "d9d9d9" #fill color //gris
                plan_.fig1_color_2 = "7f7f7f" #border color //gris oscuro
                plan_.fig1_border_w = 0.75 #border w
                plan_.save()
                #create additional
                plan_ = MPlan2()
                plan_.id_user_id = user.id
                plan_.name = "additional"
                plan_.fig1_color_1 = "d9d9d9" #fill color //gris
                plan_.fig1_color_2 = "ff0000" #border color //rojo
                plan_.fig1_border_w = 1.75 #border w
                plan_.save()

            print("Create user_extra")
            user_extra = MUser_extra()
            user_extra.id_user_id = user.id
            user_extra.save()

            flag_ok = True

        
        return JsonResponse({
            'notes': notes,
            'flag_ok':flag_ok,
        })


    return render(request, 'registration/register.html', {
        'notes': notes
        })

"""
def register2(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')

            #Create first inputs in BBDD
            #Populate the first project config
            config_prj_list = MConfig_prj.objects.filter(id_user=user.id)
            if(len(config_prj_list) == 0):
                print("config_prj If is empty, create")
                config_prj = MConfig_prj()
                config_prj.id_user_id = user.id
                config_prj.save()
            
            type_list = MType_input2.objects.filter(id_user=user.id)
            if(len(type_list) == 0):
                print("type_list If is empty, create")
                #create diamond -> SW
                type_ = MType_input2()
                type_.id_user_id = user.id
                type_.name = "SW"
                type_.fig1_name = "pptx.ShapeType.diamond"
                type_.fig1_s = 0.28
                type_.save()
                #create diamond(triangle) -> HW
                type_ = MType_input2()
                type_.id_user_id = user.id
                type_.name = "HW"
                type_.fig1_name = "pptx.ShapeType.triangle"
                type_.fig1_s = 0.28
                type_.save()
                #create hexagon -> ZDC
                type_ = MType_input2()
                type_.id_user_id = user.id
                type_.name = "ZDC"
                type_.fig1_name = "pptx.ShapeType.hexagon"
                type_.fig1_s = 0.28
                type_.save()
            
            plan_list = MPlan2.objects.filter(id_user=user.id)
            if(len(plan_list) == 0):
                print("plan_list If is empty, create")
                #create vbv
                plan_ = MPlan2()
                plan_.id_user_id = user.id
                plan_.name = "vbv"
                plan_.fig1_color_1 = "00b0f0" #fill color //azul
                plan_.fig1_color_2 = "000000" #border color //negro
                plan_.fig1_border_w = 1.75 #border w
                plan_.save()
                #create te.vbv
                plan_ = MPlan2()
                plan_.id_user_id = user.id
                plan_.name = "te.vbv"
                plan_.fig1_color_1 = "00b0f0" #fill color //azul
                plan_.fig1_color_2 = "7f7f7f" #border color //gris oscuro
                plan_.fig1_border_w = 0.75 #border w
                plan_.save()
                #create planned
                plan_ = MPlan2()
                plan_.id_user_id = user.id
                plan_.name = "planned"
                plan_.fig1_color_1 = "d9d9d9" #fill color //gris
                plan_.fig1_color_2 = "7f7f7f" #border color //gris oscuro
                plan_.fig1_border_w = 0.75 #border w
                plan_.save()
                #create additional
                plan_ = MPlan2()
                plan_.id_user_id = user.id
                plan_.name = "additional"
                plan_.fig1_color_1 = "d9d9d9" #fill color //gris
                plan_.fig1_color_2 = "ff0000" #border color //rojo
                plan_.fig1_border_w = 1.75 #border w
                plan_.save()

            return HttpResponseRedirect(reverse('login') )

    else:
        f = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': f})
"""   
"""
def register_old(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Si el usuario se crea correctamente 
            if user is not None:

                #Populate the first project config
                config_prj_list = MConfig_prj.objects.filter(id_user=user.id)
                if(len(config_prj_list) == 0):
                    print("config_prj If is empty, create")
                    config_prj = MConfig_prj()
                    config_prj.id_user_id = user.id
                    config_prj.save()
                

                type_list = MType_input2.objects.filter(id_user=user.id)
                if(len(type_list) == 0):
                    print("type_list If is empty, create")
                    #create diamond -> SW
                    type_ = MType_input2()
                    type_.id_user_id = user.id
                    type_.name = "SW"
                    type_.fig1_name = "pptx.ShapeType.diamond"
                    type_.fig1_s = 0.28
                    type_.save()

                    #create diamond(triangle) -> HW
                    type_ = MType_input2()
                    type_.id_user_id = user.id
                    type_.name = "HW"
                    type_.fig1_name = "pptx.ShapeType.triangle"
                    type_.fig1_s = 0.28
                    type_.save()

                    #create hexagon -> ZDC
                    type_ = MType_input2()
                    type_.id_user_id = user.id
                    type_.name = "ZDC"
                    type_.fig1_name = "pptx.ShapeType.hexagon"
                    type_.fig1_s = 0.28
                    type_.save()

                
                plan_list = MPlan2.objects.filter(id_user=user.id)
                if(len(plan_list) == 0):
                    print("plan_list If is empty, create")
                    #create vbv
                    plan_ = MPlan2()
                    plan_.id_user_id = user.id
                    plan_.name = "vbv"
                    plan_.fig1_color_1 = "00b0f0" #fill color //azul
                    plan_.fig1_color_2 = "000000" #border color //negro
                    plan_.fig1_border_w = 1.75 #border w
                    plan_.save()

                    #create te.vbv
                    plan_ = MPlan2()
                    plan_.id_user_id = user.id
                    plan_.name = "te.vbv"
                    plan_.fig1_color_1 = "00b0f0" #fill color //azul
                    plan_.fig1_color_2 = "7f7f7f" #border color //gris oscuro
                    plan_.fig1_border_w = 0.75 #border w
                    plan_.save()

                    #create planned
                    plan_ = MPlan2()
                    plan_.id_user_id = user.id
                    plan_.name = "planned"
                    plan_.fig1_color_1 = "d9d9d9" #fill color //gris
                    plan_.fig1_color_2 = "7f7f7f" #border color //gris oscuro
                    plan_.fig1_border_w = 0.75 #border w
                    plan_.save()

                    #create additional
                    plan_ = MPlan2()
                    plan_.id_user_id = user.id
                    plan_.name = "additional"
                    plan_.fig1_color_1 = "d9d9d9" #fill color //gris
                    plan_.fig1_color_2 = "ff0000" #border color //rojo
                    plan_.fig1_border_w = 1.75 #border w
                    plan_.save()
                  
                # Hacemos el login manualmente
                #do_login(request, user)
                # Y le redireccionamos a la portada
                return HttpResponseRedirect(reverse('login') )

    # Si llegamos al final renderizamos el formulario
    return render(request, "registration/register.html", {'form': form})
"""

#------------FrontPage----------------------------------------
#------------------------------------------------------------------------
import os
import glob
def frontpage(request):
    if request.user.is_authenticated:
        # Genera contadores de algunos de los objetos principales
        num_users=User.objects.all().count()
        num_projects=MProject.objects.all().count()

        # uso de sesiones: https://docs.djangoproject.com/en/3.1/topics/http/sessions/
        # Numero de visitas a esta view, como está contado en la variable de sesión.
        num_visits = request.session.get('num_visits', 0)
        request.session['num_visits'] = num_visits + 1

        #get the flag_first_time if exist
        flag_first_time = False
        user_extra_list = MUser_extra.objects.filter(id_user = request.user.id)
        if user_extra_list.count() > 0:
             user_extra = MUser_extra.objects.get(id_user = request.user.id)
             flag_first_time = user_extra.flag_first_time
             user_extra.flag_first_time = False
             user_extra.save()

        print("flag_first_time:",flag_first_time)
        context = {
            'num_users':num_users,
            'num_projects':num_projects,
            'num_visits':num_visits,
            'flag_first_time':flag_first_time,
        } 

        # Renderiza la plantilla HTML index.html con los datos en la variable contexto
        return render(request,'frontpage.html',context=context)

    else:
        return HttpResponseRedirect(reverse('login') )

#------------Configurar proyectos----------------------------------------
#------------------------------------------------------------------------


def remove_project(request):
    print("remove_project()")
    if request.user.is_authenticated:
        if request.method == "POST":
                print("POST")
                #print("body:",request.body)

                json_request= json.loads(request.body)
                select_value = json_request['select_value'] #ID project to return
                print("Remove project with ID: ",select_value)

                project_objt_selected = MProject.objects.filter(id=select_value)
                project_objt_selected.delete()

                project_list = MProject.objects.filter(id_user=request.user.id)
                #print(project_list)
                #print(project_list[0].id)

                return JsonResponse({
                    'id_removed':select_value,
                    'id_first_prj':project_list[0].id,
                })

    else:
        return HttpResponseRedirect(reverse('login') )


def prj_selected(request):
    print("prj_selected()")
    if request.user.is_authenticated:
        if request.method == "POST":
                print("POST")
                print("body:",request.body)

                json_request= json.loads(request.body)
                select_value = json_request['prj_id'] #ID project to return
                print("Project ID: ",select_value)
                prj_id = select_value

                v_objt_selected = MVersion.objects.filter(id_project=prj_id)
                len(v_objt_selected)

                if len(v_objt_selected) < 1:
                    print("no hay version para este proyecto -> crear!")
                    new_v = MVersion()
                    new_v.id_project_id = prj_id
                    new_v.name = "automatic_name"
                    new_v.save()

                return JsonResponse({
                    'flag_ok':True,
                    'prj_id': prj_id,
                    })

    else:
        return HttpResponseRedirect(reverse('login') )



#--- news project master
"""
def projects_rp(request):
    print("projects_rp()")
    if request.user.is_authenticated:
        project_list = MProject.objects.filter(id_user=request.user.id)
        context = {
            'mproject_list':project_list,
        } 
        # Renderiza la plantilla HTML index.html con los datos en la variable contexto
        return render(request,'project_rp.html',context=context)

    else:
        return HttpResponseRedirect(reverse('login') )
"""
def projects_rp_load(request,pk):
    print("projects_rp_load()")
    
    print("project pk: ",pk)
    #pk = '-1'
    flag_disabled = False
    if request.user.is_authenticated:
        print("user.id:",request.user.id)

        project_list = MProject.objects.filter(id_user_id=request.user.id)
        print("project_list:",project_list)

        project_list_extra = MProject.objects.exclude(id_user_id=request.user.id)

        flag_first_time_prj = False
        if pk != "-1" and pk != "0": #Is here because if pk= -1 or pk = 0 the page will be reload and the tutorial aborted
            #get first_time for tutorial
            user_extra_list = MUser_extra.objects.filter(id_user = request.user.id)
            if user_extra_list.count() > 0:
                user_extra = MUser_extra.objects.get(id_user = request.user.id)
                flag_first_time_prj = user_extra.flag_first_time_prj
                user_extra.flag_first_time_prj = False
                user_extra.save()


        #Get the groups for the user
        l = request.user.groups.values_list('name',flat = True) # QuerySet Object
        groups_list = list(l)
        print("groups_list:",groups_list)

        flag_integradores = False
        flag_administradores = False
        for group in groups_list:
            if group == 'integradores':
                flag_integradores = True
            if group == 'administradores':
                flag_administradores = True


        if flag_integradores == True:
            if pk == "-1":#Select the first or create new
                print("Select first project")
                if len(project_list) > 0:
                    pk = project_list[0].id
                else:
                    pk = "0"

            if pk == "0":#Crea nuevo project
                print("Create new project")
                new_prj = MProject()
                dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                new_prj.name = "Auto-"+dt_string
                new_prj.id_user_id = request.user.id #need id_user_id not id_user
                new_prj.date_created = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                new_prj.save()

                pk = new_prj.id
        else:
            if pk == "-1":#Select the first in project_list_extra
                print("Select first project")
                if len(project_list_extra) > 0:
                    pk = project_list_extra[0].id
                else:
                    pk = "0"


        #Check if the user is the owner for the project
        prj_list = MProject.objects.filter(id=pk)
        if prj_list.count() > 0:
            prj_objt_selected = MProject.objects.get(id=pk)
            print(prj_objt_selected.id_user_id )
            if prj_objt_selected.id_user_id != request.user.id:
                print("Este project NO pertenece al usuario")
                #return HttpResponseRedirect(reverse('frontpage') )
                #Añadir aquí control de editar
                flag_disabled = True
                #Check if the user is a admin
                if flag_administradores == True:
                    flag_disabled = False
                
            else:
                print("Este project SI pertenece al usuario")
        else:
            print("Este project id NO existe")
            return HttpResponseRedirect(reverse('frontpage') )

        #version list-----------------
        #Get the LAST version for the project with id = rp_load
        v_objt_selected = MVersion.objects.filter(id_project=pk)
        if len(v_objt_selected) > 0:
            print(v_objt_selected[len(v_objt_selected)-1])
        else:
            print("Crear nueva version")
            new_v = MVersion()
            new_v.id_project_id = pk
            new_v.name = "automatic_name"
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            new_v.date = dt_string
            new_v.save()
        
        v_objt_selected = MVersion.objects.filter(id_project=pk)

        #select the last version
        version_name = v_objt_selected[v_objt_selected.count()-1].name

        # Take date_ini (date) to CW
        date_ini = prj_objt_selected.date_ini
        print("date_ini:",date_ini)

        date_ini_obj = datetime.strptime(date_ini,'%Y-%m-%d')
        #print("date_ini_obj:",date_ini_obj)

        cw_ini = datetime.date(date_ini_obj).strftime("%V")
        print("cw_ini:",cw_ini)

        y_ini = datetime.date(date_ini_obj).strftime("%Y")
        print("y_ini:",y_ini)

        date_status = prj_objt_selected.date_status
        date_status_obj = datetime.strptime(date_status,'%Y-%m-%d')
        cw_status = datetime.date(date_status_obj).strftime("%V")
        y_status = datetime.date(date_status_obj).strftime("%Y")

        date_end = prj_objt_selected.date_end
        date_end_obj = datetime.strptime(date_end,'%Y-%m-%d')
        cw_end = datetime.date(date_end_obj).strftime("%V")
        y_end = datetime.date(date_end_obj).strftime("%Y")

        date_created = prj_objt_selected.date_created



        print("context")
        context = {
            'project_list':project_list,
            'project_list_extra':project_list_extra,
            'prj_id': pk,
            'prj_name': prj_objt_selected.name,
            'prj_comment': prj_objt_selected.comment,
            'date_ini': prj_objt_selected.date_ini, #new
            'date_status': prj_objt_selected.date_status, #new
            'date_end': prj_objt_selected.date_end, #new
            'cw_ini': cw_ini, #new
            'y_ini': y_ini, #new
            'cw_status': cw_status, #new
            'y_status': y_status, #new
            'cw_end': cw_end, #new
            'y_end': y_end, #new

            'factor_weeks': prj_objt_selected.factor_weeks, #new
            'max_ecu_slide': prj_objt_selected.max_ecu_slide, #new

            'version_list': v_objt_selected,
            'version_name': version_name,

            'flag_disabled': flag_disabled,
            'flag_integradores':flag_integradores,

            'date_created':date_created,

            'flag_first_time_prj':flag_first_time_prj,
        }

        return render(request,'project_rp.html',context=context)
    else:
        return HttpResponseRedirect(reverse('login') )

def getprojectowner(request):
    print("getprojectowner()")
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_table = json.loads(request.body)
            print("json_table:",json_table)

            prj_owner = ""
            if 'prj_id' in json_table:
                prj = MProject.objects.get(id=json_table['prj_id'])
                prj_owner = prj.id_user.username
                print(prj_owner)

            
        return JsonResponse({
            'ok':True,
            'prj_owner':prj_owner,
        })
    else:
        return HttpResponseRedirect(reverse('login') )


def update_project_metadata(request):
    print("update_project_metadata()")
    if request.user.is_authenticated:
        if request.method == "POST":
            print("POST")
            print("body:",request.body)
                
            json_request= json.loads(request.body)
            print("json_request:",json_request)

            if 'prj_id' in json_request:
                prj = MProject.objects.get(pk=json_request['prj_id'])
                prj.name = json_request['prj_name']
                prj.comment= json_request['prj_comment']
                prj.save()

            return JsonResponse({
                'flag_ok':True,

            })

    else:
        return HttpResponseRedirect(reverse('login') )            



def update_version_form(request):
    print("update_version_form()")
    if request.user.is_authenticated:
        if request.method == "POST":
            print("POST")
            print("body:",request.body)
                
            json_request= json.loads(request.body)
            vers_id = json_request['version_id']
            print("vers_id:",vers_id)

            new_version = json_request['new_version']
            project_id = json_request['project_id']

            version_name = json_request['version_name']

            print("new_version:",new_version)
            print("project_id:",project_id)

            print("version_name:",version_name)
            reload = False

            if version_name == "":
                version_name = "automatic_name"

            if new_version == 1:
                print("Crear nueva version") #Copia las ECUs y entradas de la versión seleccionada (vers_id)
                new_v = MVersion()
                new_v.id_project_id = project_id
                new_v.name = version_name
                dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                new_v.date = dt_string
                new_v.save()

                #Copy all ECUs to new version
                ECU_objt_selected = MECU.objects.filter(id_version=vers_id)
                print("Copia lista ECUs para nueva version_id:",new_v.id) 
                for elt in ECU_objt_selected:
                    new_ecu = MECU()
                    new_ecu.name = elt.name
                    new_ecu.dx_ecu = elt.dx_ecu
                    new_ecu.comment = elt.comment
                    new_ecu.id_version_id = new_v.id
                    new_ecu.created_by = elt.created_by
                    new_ecu.save()

                    #Copy all MRelease_input to new version for each ecu
                    MRelease_objt_selected = MRelease_input.objects.filter(id_ecu=elt.id)
                    print("Copia lista R_inputs para cada nueva ECU_id:", new_ecu.id, " desde la anterior ECU_id:", elt.id) 
                    for obj in MRelease_objt_selected:
                        new_Ri = MRelease_input()
                        new_Ri.id_ecu_id = new_ecu.id
                        new_Ri.id_type_input = obj.id_type_input
                        new_Ri.n_version = obj.n_version
                        new_Ri.date_beantragt = obj.date_beantragt
                        new_Ri.id_plan = obj.id_plan
                        new_Ri.flag_visual = obj.flag_visual
                        new_Ri.comment = obj.comment
                        new_Ri.flag_marked1 = obj.flag_marked1
                        new_Ri.flag_marked2 = obj.flag_marked2
                        new_Ri.flag_marked3 = obj.flag_marked3
                        new_Ri.created_by = obj.created_by
                        new_Ri.date_created = obj.date_created
                        

                        new_Ri.save()

                vers_id = new_v.id
                reload = True

            if new_version == -1:
                print("Update version")
                version_objt_selected = MVersion.objects.get(id=vers_id)
                version_objt_selected.name = version_name
                version_objt_selected.save()
                reload = True
            
            return JsonResponse({
                    'reload':reload,
                    'vers_id':vers_id,
            })

    else:
        return HttpResponseRedirect(reverse('login') )


def remove_version(request):
    print("remove_project()")
    if request.user.is_authenticated:
        if request.method == "POST":
                print("POST")
                #print("body:",request.body)

                json_request= json.loads(request.body)
                select_value = json_request['select_value'] #ID project to return
                print("Remove version with ID: ",select_value)

                version_objt_selected = MVersion.objects.filter(id=select_value)
                version_objt_selected.delete()

                return JsonResponse({
                    'id_removed':select_value,
                })

    else:
        return HttpResponseRedirect(reverse('login') )

def updatedataproject(request):
    print("updatedataproject()")
    if request.user.is_authenticated:
        if request.method == "POST":
                print("POST")
                #print("body:",request.body)

                json_request= json.loads(request.body)
                prj_id = json_request['prj_id'] 
                print("prj_id: ",prj_id)

                vers_id = json_request['vers_id']
                print("vers_id: ",vers_id)

                #Get the ECU list for the version ID
                ECUlist_objt_selected = MECU.objects.filter(id_version=vers_id)
                ecuList_name = []
                ecuList_comment = []
                ecuList_dx = []
                ecuList_id = []
                ecuList_created_by = []
                ecuList_created_by_name = []
                ecuList_order = []

                for elt in ECUlist_objt_selected:
                    #print("name eculist: ",elt.name)
                    ecuList_name.append(elt.name)
                    ecuList_comment.append(elt.comment)
                    ecuList_dx.append(elt.dx_ecu)
                    ecuList_id.append(str(elt.id))
                    ecuList_order.append(elt.order)

                    #print(elt.created_by)
                    if elt.created_by != None:
                        ecuList_created_by.append(str(elt.created_by.id))
                        ecuList_created_by_name.append(elt.created_by.username)
                    else:
                        ecuList_created_by.append("")
                        ecuList_created_by_name.append("")

                print("ecuList_name:",ecuList_name)
                #print("ecuList_comment:",ecuList_comment)
                #print("ecuList_dx:",ecuList_dx)
                #print("ecuList_id:",ecuList_id)
                #print("ecuList_created_by:",ecuList_created_by)
                #order lists -> sorted
                ecuList_name_sorted = []
                ecuList_comment_sorted  = []
                ecuList_dx_sorted  = []
                ecuList_id_sorted  = []
                ecuList_created_by_sorted  = []
                ecuList_created_by_name_sorted  = []
                ecuList_order_sorted = sorted(ecuList_order)
                cont_i = 0
                for i in ecuList_order_sorted:
                    cont_i += 1
                    #print(ecuList_order_sorted[i-1])
                    cont_j = 0
                    if i != 0: #order = 0 -> no inicializados
                        for j in ecuList_order:
                            cont_j += 1
                            if j == i:
                                ecuList_name_sorted.append(ecuList_name[cont_j-1])
                                ecuList_comment_sorted.append(ecuList_comment[cont_j-1])
                                ecuList_dx_sorted.append(ecuList_dx[cont_j-1])
                                ecuList_id_sorted.append(ecuList_id[cont_j-1])
                                ecuList_created_by_sorted.append(ecuList_created_by[cont_j-1])
                                ecuList_created_by_name_sorted.append(ecuList_created_by_name[cont_j-1])
                    else:
                         ecuList_name_sorted.append(ecuList_name[cont_i-1])
                         ecuList_comment_sorted.append(ecuList_comment[cont_i-1])
                         ecuList_dx_sorted.append(ecuList_dx[cont_i-1])
                         ecuList_id_sorted.append(ecuList_id[cont_i-1])
                         ecuList_created_by_sorted.append(ecuList_created_by[cont_i-1])
                         ecuList_created_by_name_sorted.append(ecuList_created_by_name[cont_i-1])
                            
                print("ecuList_name_sorted:",ecuList_name_sorted)


                return JsonResponse({
                    'ecuList_name': ecuList_name_sorted,
                    'ecuList_comment': ecuList_comment_sorted,
                    'ecuList_dx': ecuList_dx_sorted,
                    'ecuList_id': ecuList_id_sorted,
                    'ecuList_created_by':ecuList_created_by_sorted,
                    'ecuList_created_by_name':ecuList_created_by_name_sorted,
                })

    else:
        return HttpResponseRedirect(reverse('login') )



#------------Configurar ECU + Release Plan----------------------------------------
#------------------------------------------------------------------------


def update_ECU_list(request):
    print("update_ECU_list()")
    if request.user.is_authenticated:
        if request.method == "POST":
                print("POST")
                print("body:",request.body)


                json_table = json.loads(request.body)
                print("json_table:",json_table)
                json_allData = json_table['ecu_list']
                print("json_allData:",json_allData)

                json_id_v = json_table['version_id']
                print("json_id_v:",json_id_v)

                ECUlist_objt_selected = MECU.objects.filter(id_version=json_id_v)

                #Recoje y elimina todas las entradas de la BBDD
                #all_entries_remove = ECU_model.objects.filter(id_version=json_id_v)
                #all_entries = ECU_model.objects.all()
                #all_entries_remove.delete()

                #Busca entradas eliminadas
                print("Check for delete")
                for elt in ECUlist_objt_selected:
                    flag_salvado = False
                    for row in json_allData:
                        #print("elt.id:",elt.id)
                        #print("row['id']:",row['id'])
                        if int(row['id']) == elt.id:
                            flag_salvado = True
                    if flag_salvado == False:
                        print("Remove: ",elt.id)
                        elt.delete()


                #Guarda entradas nuevas
                cont_ecu = 0
                for row in json_allData:
                    cont_ecu = cont_ecu + 1
                    print("cont_ecu:",cont_ecu)
                    flag_empty_row = True
                    print("row:",row)


                    for prop in row:
                        #print(prop)
                        #print(row[prop])
                        if prop != "id":#Esto limpia las row en blanco (pero con ID)
                            if row[prop] == None:
                                row[prop] = ""
                            if row[prop] != "":
                                flag_empty_row = False

                    #print("flag_empty_row:",flag_empty_row)
                    if flag_empty_row == False:
                        if int(row['id'])!= 0:
                            print("update value")
                            #print("int(row['id']): ",int(row['id']))
                            ecu_obj = MECU.objects.get(id=int(row['id'])) 
                            aux_string =  row['name'].replace('\n', ' ').replace('\r', '')
                            ecu_obj.name = aux_string
                            aux_string =  row['comment'].replace('\n', ' ').replace('\r', '')
                            ecu_obj.comment = aux_string
                            aux_string =  row['dx'].replace('\n', ' ').replace('\r', '')
                            ecu_obj.dx_ecu = row['dx']
                            ecu_obj.order = cont_ecu

                            if row['created_by'] != 'null' and row['created_by'] != '':
                                #get user by id and save it
                                user = User.objects.get(id=int(row['created_by'])) 
                                ecu_obj.created_by = user
                            else:
                                ecu_obj.created_by = request.user
                            ecu_obj.save()
                        else:
                            print("create new")
                            aux_string_name =  row['name'].replace('\n', ' ').replace('\r', '')
                            aux_string_com =  row['comment'].replace('\n', ' ').replace('\r', '')
                            aux_string_dx =  row['dx'].replace('\n', ' ').replace('\r', '')
                            ecu_model = MECU(
                                name = aux_string_name,
                                comment = aux_string_com,
                                dx_ecu = aux_string_dx,
                                id_version_id = json_id_v,
                                created_by = request.user,
                                order = cont_ecu,
                            )
                            ecu_model.save()

                
                ecuList_name = []
                ecuList_comment = []
                ecuList_dx = []
                ecuList_id = []
                ecuList_created_by = []
                ecuList_created_by_name = []
                ecuList_order = []

                #load ecu_list
                ECUlist_objt_selected = MECU.objects.filter(id_version=json_id_v)
                #ECUlist_objt_selected.count()
                
                for elt in ECUlist_objt_selected:
                    #print("order:",elt.order, " name:",elt.name)
                    ecuList_name.append(elt.name)
                    ecuList_comment.append(elt.comment)
                    ecuList_dx.append(elt.dx_ecu)
                    ecuList_id.append(str(elt.id))
                    ecuList_created_by.append(elt.created_by.id)
                    ecuList_created_by_name.append(elt.created_by.username)
                    ecuList_order.append(elt.order)

                print("ecuList_name:",ecuList_name)
                #print("ecuList_comment:",ecuList_comment)
                #print("ecuList_dx:",ecuList_dx)
                #print("ecuList_id:",ecuList_id)
                #print("ecuList_created_by:",ecuList_created_by)

                #order lists -> sorted
                ecuList_name_sorted = []
                ecuList_comment_sorted  = []
                ecuList_dx_sorted  = []
                ecuList_id_sorted  = []
                ecuList_created_by_sorted  = []
                ecuList_created_by_name_sorted  = []

                ecuList_order_sorted = sorted(ecuList_order)
                cont_i = 0
                for i in ecuList_order_sorted:
                    cont_i += 1
                    #print(ecuList_order_sorted[i-1])
                    cont_j = 0
                    if i != 0: #order = 0 -> no inicializados
                        for j in ecuList_order:
                            cont_j += 1
                            if j == i:
                                ecuList_name_sorted.append(ecuList_name[cont_j-1])
                                ecuList_comment_sorted.append(ecuList_comment[cont_j-1])
                                ecuList_dx_sorted.append(ecuList_dx[cont_j-1])
                                ecuList_id_sorted.append(ecuList_id[cont_j-1])
                                ecuList_created_by_sorted.append(ecuList_created_by[cont_j-1])
                                ecuList_created_by_name_sorted.append(ecuList_created_by_name[cont_j-1])
                    else:
                         ecuList_name_sorted.append(ecuList_name[cont_i-1])
                         ecuList_comment_sorted.append(ecuList_comment[cont_i-1])
                         ecuList_dx_sorted.append(ecuList_dx[cont_i-1])
                         ecuList_id_sorted.append(ecuList_id[cont_i-1])
                         ecuList_created_by_sorted.append(ecuList_created_by[cont_i-1])
                         ecuList_created_by_name_sorted.append(ecuList_created_by_name[cont_i-1])
                            
                #print("ecuList_name_sorted:",ecuList_name_sorted)

                
                #----------------
                #found the [release_inputs -> Release_input_model] for all ECUs for this version
                RelInList_id = []
                RelInList_id_ecu = []
                RelInList_id_type = []
                RelInList_n_version = []
                RelInList_date = []
                RelInList_plan = []
                RelInList_id_plan = []
                RelInList_visual = []
                RelInList_dx = []
                RelInList_comment = []
                RelInList_marked1 = []
                RelInList_marked2 = []
                RelInList_marked3 = []

                RelInList_created_by = []
                RelInList_created_by_name = []
                RelInList_date_created = []
                
                RelInList_ecu_name = []#Extra
                RelInList_type_name = []#Extra
                
                for ecu_id in ecuList_id:
                    print("filter id:",ecu_id)
                    RelInputs_objt_selected = MRelease_input.objects.filter(id_ecu=ecu_id)
                    for elt in RelInputs_objt_selected:
                        RelInList_id.append(str(elt.id))
                        RelInList_id_ecu.append(str(elt.id_ecu_id))
                        RelInList_id_type.append(str(elt.id_type_input_id))
                        RelInList_n_version.append(elt.n_version)
                        RelInList_date.append(elt.date_beantragt)
                        #RelInList_plan.append(elt.plan)
                        RelInList_id_plan.append(str(elt.id_plan_id))
                        RelInList_visual.append(str(elt.flag_visual))
                        print("visual:",elt.flag_visual) #¿?¿?¿?

                        #RelInList_dx.append(elt.dx_ecu)
                        RelInList_comment.append(elt.comment)
                        RelInList_marked1.append(str(elt.flag_marked1))
                        RelInList_marked2.append(str(elt.flag_marked2))
                        RelInList_marked3.append(str(elt.flag_marked3))

                        if elt.created_by != None:
                            RelInList_created_by.append(str(elt.created_by.id))
                            RelInList_created_by_name.append(str(elt.created_by.username))
                        else:
                            RelInList_created_by.append("")
                            RelInList_created_by_name.append("")

                        RelInList_date_created.append(elt.date_created)

                        ecu_name = MECU.objects.get(id=ecu_id).name #Get ecu name for this Ri
                        RelInList_ecu_name.append(ecu_name)
                        #print("elt.id_ecu:",elt.id_ecu_id)
                        #type_name = MType_input.objects.get(id=elt.id_type_input_id).name 
                        if MType_input2.objects.filter(id = elt.id_type_input_id).count() > 0:
                            type_name = MType_input2.objects.get(id=elt.id_type_input_id).name
                            RelInList_type_name.append(type_name)
                        else:
                            #RelInList_type_name.append("null")
                            RelInList_type_name.append("")

                        #plan_name = MPlan.objects.get(id=elt.id_plan_id).name
                        if MPlan2.objects.filter(id = elt.id_plan_id).count() > 0:
                            plan_name = MPlan2.objects.get(id=elt.id_plan_id).name
                            RelInList_plan.append(plan_name)
                        else:
                            #RelInList_plan.append("null")
                            RelInList_plan.append("")
                        #print("RelInList_plan: ",RelInList_plan)

                        ecu_obj = MECU.objects.get(id=elt.id_ecu_id) 
                        RelInList_dx.append(ecu_obj.dx_ecu)


                #Get the all list of types
                type_list_id = []#Extra
                type_list_name = []#Extra
                type_list_comment = []#Extra
                #type_list_obj = MType_input2.objects.all()
                #type_list_obj = MType_input2.objects.filter(id_user = request.user.id)
                type_list_obj = MType_input2.objects.filter(id_user = request.user.id)

                for elt in type_list_obj:
                    type_list_id.append(str(elt.id))
                    type_list_name.append(elt.name)
                    type_list_comment.append(elt.comment)

                print("type_list_name: ",type_list_name)
                #Get the all list of plans
                plan_list_id = []#Extra
                plan_list_name = []#Extra
                plan_list_comment = []#Extra
                #plan_list_obj = MPlan2.objects.all()
                plan_list_obj = MPlan2.objects.filter(id_user = request.user.id)
                
                for elt in plan_list_obj:
                    plan_list_id.append(str(elt.id))
                    plan_list_name.append(elt.name)
                    plan_list_comment.append(elt.comment)
                print("plan_list_name: ",plan_list_name)
                    
                #----------

                # redirect to a new URL: ¿?
                return JsonResponse({
                    'flag_ok' : True,
                    'ecuList_name': ecuList_name_sorted ,
                    'ecuList_comment': ecuList_comment_sorted ,
                    'ecuList_dx': ecuList_dx_sorted ,
                    'ecuList_id': ecuList_id_sorted ,
                    'ecuList_created_by':ecuList_created_by_sorted ,
                    'ecuList_created_by_name':ecuList_created_by_name_sorted ,

                    'id_v' : json_id_v,

                    'RelInList_id': RelInList_id,
                    'RelInList_id_ecu': RelInList_id_ecu,
                    'RelInList_id_type': RelInList_id_type,
                    'RelInList_n_version': RelInList_n_version,
                    'RelInList_date': RelInList_date,
                    'RelInList_plan': RelInList_plan,
                    'RelInList_id_plan': RelInList_id_plan,
                    'RelInList_visual': RelInList_visual,
                    'RelInList_dx': RelInList_dx,
                    'RelInList_comment': RelInList_comment,
                    'RelInList_marked1': RelInList_marked1,
                    'RelInList_marked2': RelInList_marked2,
                    'RelInList_marked3': RelInList_marked3,

                    'RelInList_created_by': RelInList_created_by,
                    'RelInList_created_by_name':RelInList_created_by_name,
                    'RelInList_date_created': RelInList_date_created,

                    'RelInList_ecu_name': RelInList_ecu_name,
                    'RelInList_type_name': RelInList_type_name,

                    'type_list_id': type_list_id,
                    'type_list_name': type_list_name,
                    'type_list_comment': type_list_comment,

                    'plan_list_id': plan_list_id,
                    'plan_list_name': plan_list_name,
                    'planlist_comment': plan_list_comment,
                })

        else:
                print("NO POST")
                #return HttpResponseRedirect(reverse('rp_load', args=(json_id_v)))

    else:
        return HttpResponseRedirect(reverse('login') )


def update_Release_list(request):
   print("update_Release_list()")
   if request.user.is_authenticated:
   
        if request.method == "POST":
            print("POST")
            #print(request.POST)
            #print("body:",request.body)

            json_table = json.loads(request.body)
            json_allData = json_table['all_data']
            print("json_allData:",json_allData)

            #Busca entradas eliminadas
            json_id_v = json_table['id_v']
            print("json_id_v:",json_id_v)
            
            print("Check for delete")
            ECUlist_objt_selected = MECU.objects.filter(id_version=json_id_v)
            for elt in ECUlist_objt_selected:
                #Busca para cada ECU las RI asociadas
                RIlist_objt_selected = MRelease_input.objects.filter(id_ecu=elt.id)
                for obj in RIlist_objt_selected:
                    flag_salvado = False
                    for row in json_allData:
                        #print("obj.id:",obj.id)
                        #print("row['RelInList_id']:",row['RelInList_id'])
                        if int(row['RelInList_id']) == obj.id:
                            flag_salvado = True
                    if flag_salvado == False:
                        print("Remove: ",obj.id)
                        obj.delete()
            
            #Guarda entradas nuevas
            for row in json_allData:
                flag_empty_row = True
                print("row:",row)

                for prop in row:
                    #print(row[prop])
                    if prop != "ID":#Esto limpia las row en blanco (pero con ID)
                        if row[prop] == None:
                            row[prop] = ""
                    if row[prop] != "":
                        flag_empty_row = False

                #print("flag_empty_row:",flag_empty_row)
                if flag_empty_row == False:
                    #Find id_ecu, por si se cambió de ECU
                    #Clean value if have: name - dx
                    #list_filter = row['RelInList_ecu_name'].split("-")
                    #name_clean = list_filter[0].rstrip() #rstrip() elimina los ultimos espacios si los hay
                    name_clean = row['RelInList_ecu_name']
                    #print("name_clean:->",name_clean,"<-")
                    print("name_ecu:->",name_clean,"<-")

                    ECU_selected = MECU.objects.filter(name=name_clean, id_version=json_id_v)
                    ecu_id = 0
                    for elt in ECU_selected:
                        ecu_id = elt.id
                        print("ecu_id:",ecu_id)

                    #Find type, por si se cambió
                    user_type_list = MType_input2.objects.filter(id_user = request.user.id)
                    type_id = 0
                    for t in user_type_list:
                        if t.name == row['RelInList_type_name']:
                            type_id = t.id
                            print("type_id:",type_id)

                    #Find plan, por si se cambió
                    user_plan_list = MPlan2.objects.filter(id_user = request.user.id)
                    plan_id = 0
                    for p in user_plan_list:
                        if p.name == row['RelInList_plan']:
                            plan_id = p.id
                            print("plan_id: ",plan_id)

                    #Adecua booleans
                    flag_visual = True
                    if row['RelInList_visual'] == None:
                        flag_visual = False
                    if row['RelInList_visual'] == "":
                        flag_visual = False
                    if row['RelInList_visual'] == False:
                        flag_visual = False
                    if row['RelInList_visual'] == 'False':
                        flag_visual = False

                    flag_marked1 = True
                    if row['RelInList_marked1'] == None:
                        flag_marked1 = False
                    if row['RelInList_marked1'] == "":
                        flag_marked1 = False
                    if row['RelInList_marked1'] == False:
                        flag_marked1 = False
                    if row['RelInList_marked1'] == 'False':
                        flag_marked1 = False

                    if int(row['RelInList_id'])!= 0: #añadir checkeo de vacio ""
                        print("update value")
                        RI_selected = MRelease_input.objects.get(id = int(row['RelInList_id']))

                        RI_selected.id_ecu_id = int(ecu_id)
                        RI_selected.id_type_input_id = type_id
                        aux_string =  row['RelInList_n_version'].replace('\n', ' ').replace('\r', '')
                        RI_selected.n_version = aux_string
                        RI_selected.date_beantragt = row['RelInList_date']
                        #RI_selected.plan = row['RelInList_plan']
                        RI_selected.id_plan_id = plan_id

                        RI_selected.flag_visual = flag_visual
                        aux_string =  row['RelInList_comment'].replace('\n', ' ').replace('\r', '')
                        RI_selected.comment = aux_string
                        RI_selected.flag_marked1= flag_marked1
                        RI_selected.save()

                        #RI_model.save()
                        
                    else:
                        print("create new:")
                        print("ecu_id:",ecu_id)
                        aux_string_ver =  row['RelInList_n_version'].replace('\n', ' ').replace('\r', '')
                        aux_string_com =  row['RelInList_comment'].replace('\n', ' ').replace('\r', '')

                        RI_model = MRelease_input(
                            #id = row['RelInList_id'],
                            id_ecu_id = ecu_id,
                            id_type_input_id = type_id,
                            n_version = aux_string_ver,
                            date_beantragt = row['RelInList_date'],
                            #plan = row['RelInList_plan'],
                            id_plan_id = plan_id,
                            flag_visual = flag_visual,
                            comment = aux_string_com,
                            flag_marked1 = flag_marked1,
                            created_by = request.user,
                            date_created = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        )
                        RI_model.save()

            #Return valores actualizados a la tabla -> ID------------------
            RelInList_id = []
            RelInList_id_ecu = []
            RelInList_id_type = []
            RelInList_n_version = []
            RelInList_date = []
            RelInList_plan = []
            RelInList_id_plan = []
            RelInList_visual = []
            RelInList_dx = []
            RelInList_comment = []
            RelInList_marked1 = []
            RelInList_marked2 = []
            RelInList_marked3 = []

            RelInList_created_by = []
            RelInList_created_by_name = []
            RelInList_date_created = []
                
            RelInList_ecu_name = []#Extra
            RelInList_type_name = []#Extra

            ecuList_name = []
            ecuList_dx = []
                
            ECUlist_objt_selected = MECU.objects.filter(id_version=json_id_v)
            for obj in ECUlist_objt_selected:
                ecu_id = obj.id
                ecuList_name.append(obj.name)
                ecuList_dx.append(obj.dx_ecu)
                print("filter id:",ecu_id)

                RelInputs_objt_selected = MRelease_input.objects.filter(id_ecu=ecu_id)
                for elt in RelInputs_objt_selected:
                    print("founded id:",elt.id)
                    RelInList_id.append(str(elt.id))
                    RelInList_id_ecu.append(str(elt.id_ecu_id))
                    RelInList_id_type.append(str(elt.id_type_input_id))
                    RelInList_n_version.append(elt.n_version)
                    RelInList_date.append(elt.date_beantragt)
                    #RelInList_plan.append(elt.plan)
                    RelInList_id_plan.append(str(elt.id_plan_id))
                    RelInList_visual.append(str(elt.flag_visual))
                    #print("visual:",elt.flag_visual) #¿?¿?¿?

                    #RelInList_dx.append(elt.dx_ecu)
                    RelInList_comment.append(elt.comment)
                    RelInList_marked1.append(str(elt.flag_marked1))
                    RelInList_marked2.append(str(elt.flag_marked2))
                    RelInList_marked3.append(str(elt.flag_marked3))

                    if elt.created_by != None:
                        RelInList_created_by.append(str(elt.created_by.id))
                        RelInList_created_by_name.append(str(elt.created_by.username))
                    else:
                        RelInList_created_by.append("")
                        RelInList_created_by_name.append("")

                    RelInList_date_created.append(elt.date_created)

                    ecu_name = MECU.objects.get(id=ecu_id).name #Get ecu name for this Ri
                    RelInList_ecu_name.append(ecu_name)
                    #print("elt.id_ecu:",elt.id_ecu_id)
                    type_name = MType_input2.objects.get(id=elt.id_type_input_id).name 
                    RelInList_type_name.append(type_name)

                    plan_name = MPlan2.objects.get(id=elt.id_plan_id).name 
                    RelInList_plan.append(plan_name)

                    ecu_obj = MECU.objects.get(id=elt.id_ecu_id) 
                    RelInList_dx.append(ecu_obj.dx_ecu)

            #Get the all list of types
            type_list_id = []#Extra
            type_list_name = []#Extra
            type_list_comment = []#Extra
            type_list_obj = MType_input2.objects.filter(id_user = request.user.id)
                
            for elt in type_list_obj:
                type_list_id.append(str(elt.id))
                type_list_name.append(elt.name)
                type_list_comment.append(elt.comment)

            #Get the all list of plans
            plan_list_id = []#Extra
            plan_list_name = []#Extra
            plan_list_comment = []#Extra
            #plan_list_obj = MPlan2.objects.all()
            plan_list_obj = MPlan2.objects.filter(id_user = request.user.id)
            
            for elt in plan_list_obj:
                plan_list_id.append(str(elt.id))
                plan_list_name.append(elt.name)
                plan_list_comment.append(elt.comment)

            print("SEND")
            return JsonResponse({
                    'ecuList_name': ecuList_name,
                    #'ecuList_comment': ecuList_comment,
                    'ecuList_dx': ecuList_dx,
                    #'ecuList_id': ecuList_id,
                    'id_v' : json_id_v,

                    'RelInList_id': RelInList_id,
                    'RelInList_id_ecu': RelInList_id_ecu,
                    'RelInList_id_type': RelInList_id_type,
                    'RelInList_n_version': RelInList_n_version,
                    'RelInList_date': RelInList_date,
                    'RelInList_plan': RelInList_plan,
                    'RelInList_id_plan': RelInList_id_plan,
                    'RelInList_visual': RelInList_visual,
                    'RelInList_dx': RelInList_dx,
                    'RelInList_comment': RelInList_comment,
                    'RelInList_marked1': RelInList_marked1,
                    'RelInList_marked2': RelInList_marked2,
                    'RelInList_marked3': RelInList_marked3,

                    'RelInList_created_by': RelInList_created_by,
                    'RelInList_created_by_name':RelInList_created_by_name,
                    'RelInList_date_created':RelInList_date_created,

                    'RelInList_ecu_name': RelInList_ecu_name,
                    'RelInList_type_name': RelInList_type_name,

                    #'type_list_id': type_list_id,
                    'type_list_name': type_list_name,
                    #'type_list_comment': type_list_comment,

                    #'plan_list_id': plan_list_id,
                    'plan_list_name': plan_list_name,
                    #'planlist_comment': plan_list_comment
            })


        else:
            print("NO_POST")
            #json_id_v = 3
            #return HttpResponseRedirect(reverse('rp_load', args=(json_id_v)))

   else:
       return HttpResponseRedirect(reverse('login') )


def get_prj_list_user(request):
   print("get_prj_list_user()")
   if request.user.is_authenticated:
        if request.method == "POST":
            print("POST")
            #print(request.POST)
            #print("body:",request.body)

            #get the proyects for the user
            #prj_list = MProject.objects.filter(id_user=request.user.id)
            prj_list = MProject.objects.all()
            prj_name_list = []
            prj_id_list = []
            for obj in prj_list:
                prj_name_list.append(obj.name)
                prj_id_list.append(obj.id)

            return JsonResponse({
                    'ok': True,
                    'prj_name_list': prj_name_list,
                    'prj_id_list': prj_id_list
            })
        else:
            print("NO_POST")
            #json_id_v = 3
            #return HttpResponseRedirect(reverse('rp_load', args=(json_id_v)))
   else:
       return HttpResponseRedirect(reverse('login') )

def copy_ecu_list(request):
   print("copy_ecu_list()")
   if request.user.is_authenticated:
        if request.method == "POST":
            print("POST")
            #print(request.POST)
            #print("body:",request.body)
            json_table = json.loads(request.body)
            print("json_table:",json_table)
            prj_id = json_table['prj_id']
            
            #get the MVersion by prj id
            ver_list = MVersion.objects.filter(id_project=prj_id)

            #Take the last version
            print(ver_list[ver_list.count()-1].name)

            #get the ecu_list for the id version selected
            ecu_list = MECU.objects.filter(id_version=ver_list[ver_list.count()-1].id)

            #get the actual version in the actual project
            version_id = json_table['version_id']

            #Iterate the ecu_list
            for obj in ecu_list:
                #Create new ecu objt
                new_ecu = MECU()
                new_ecu.id_version_id = version_id
                #copy values
                new_ecu.name = obj.name
                new_ecu.dx_ecu = obj.dx_ecu
                new_ecu.comment = obj.comment
                new_ecu.created_by = obj.created_by
                #save
                new_ecu.save()


            return JsonResponse({
                    'ok': True,
            })
        else:
            print("NO_POST")
            #json_id_v = 3
            #return HttpResponseRedirect(reverse('rp_load', args=(json_id_v)))
   else:
       return HttpResponseRedirect(reverse('login') )



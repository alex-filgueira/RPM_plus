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
        
        return JsonResponse({
            'ok':True,
            'date_ini': date_ini, #new
            'date_status': date_status, #new
            'date_end': date_end, #new

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
            RelInList_ecu_name = []#Extra
            RelInList_type_name = []#Extra


            nECU = 0
            ecu_id = 0
            #Get ECU list
            ECUlist_objt_selected = MECU.objects.filter(id_version=version_id)
            #flag_new_ecu = True
            for obj in ECUlist_objt_selected:
                #ecuList_name.append(obj.name)
                #ecu_id = obj.id
                flag_new_ecu = True

                #Get sw/hw/zdc inputs for each ECU -> MRelease_input
                MR_inputlist_objt_selected = MRelease_input.objects.filter(id_ecu=obj.id).filter(flag_visual=True)
                for elt in MR_inputlist_objt_selected:
                    if flag_new_ecu == True:
                        nECU = nECU + 1
                        flag_new_ecu = False
                        ecuList_comment.append(obj.comment)
                        ecuList_dx.append(obj.dx_ecu)
                        ecuList_name.append(obj.name)
                        ecuList_id.append(obj.id)
                        ecu_id = obj.id
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

                    ecu_name = MECU.objects.get(id=ecu_id).name #Get ecu name for this Ri
                    print("ecu_name:",ecu_name)
                    RelInList_ecu_name.append(ecu_name)
                    #print("elt.id_ecu:",elt.id_ecu_id)
                    type_name = MType_input.objects.get(id=elt.id_type_input_id).name 
                    RelInList_type_name.append(type_name)

                    plan_name = MPlan.objects.get(id=elt.id_plan_id).name 
                    RelInList_plan.append(plan_name)

                    ecu_obj = MECU.objects.get(id=elt.id_ecu_id) 
                    RelInList_dx.append(ecu_obj.dx_ecu)




        return JsonResponse({
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

                    'RelInList_ecu_name': RelInList_ecu_name,
                    'RelInList_type_name': RelInList_type_name,

                    'ecuList_comment': ecuList_comment,
                    'ecuList_dx': ecuList_dx,
                    'ecuList_name': ecuList_name,
                    'ecuList_id': ecuList_id,
                    'nECU': nECU,

                    'prj_name': prj_name,
        })

    else:
        return HttpResponseRedirect(reverse('login') )

def pptgen(request):
    if request.user.is_authenticated:
        # Genera contadores de algunos de los objetos principales
        num_users=User.objects.all().count()
        num_projects=MProject.objects.all().count()

        # uso de sesiones: https://docs.djangoproject.com/en/3.1/topics/http/sessions/
        # Numero de visitas a esta view, como está contado en la variable de sesión.
        num_visits = request.session.get('num_visits', 0)
        request.session['num_visits'] = num_visits + 1

        context = {
            'num_users':num_users,
            'num_projects':num_projects,
            'num_visits':num_visits,
        } 

        # Renderiza la plantilla HTML index.html con los datos en la variable contexto
        return render(request,'pptgen.html',context=context)

    else:
        return HttpResponseRedirect(reverse('login') )



#------------Users----------------------------------------
#------------------------------------------------------------------------
from .forms import CustomUserCreationForm
from django.contrib import messages


#...
def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return HttpResponseRedirect(reverse('login') )

    else:
        f = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': f})

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
                # Hacemos el login manualmente
                #do_login(request, user)
                # Y le redireccionamos a la portada
                return HttpResponseRedirect(reverse('login') )

    # Si llegamos al final renderizamos el formulario
    return render(request, "registration/register.html", {'form': form})


#------------FrontPage----------------------------------------
#------------------------------------------------------------------------

def frontpage(request):
    if request.user.is_authenticated:
        # Genera contadores de algunos de los objetos principales
        num_users=User.objects.all().count()
        num_projects=MProject.objects.all().count()

        # uso de sesiones: https://docs.djangoproject.com/en/3.1/topics/http/sessions/
        # Numero de visitas a esta view, como está contado en la variable de sesión.
        num_visits = request.session.get('num_visits', 0)
        request.session['num_visits'] = num_visits + 1

        context = {
            'num_users':num_users,
            'num_projects':num_projects,
            'num_visits':num_visits,
        } 

        # Renderiza la plantilla HTML index.html con los datos en la variable contexto
        return render(request,'frontpage.html',context=context)

    else:
        return HttpResponseRedirect(reverse('login') )

#------------Configurar proyectos----------------------------------------
#------------------------------------------------------------------------
def projectlist(request):
    print("projectlist()")
    if request.user.is_authenticated:
        project_list = MProject.objects.filter(id_user=request.user.id)
        context = {
            'mproject_list':project_list,
        } 
        # Renderiza la plantilla HTML index.html con los datos en la variable contexto
        return render(request,'project_manager.html',context=context)

    else:
        return HttpResponseRedirect(reverse('login') )


def update_prj_form(request):
    print("update_prj_form()")
    if request.user.is_authenticated:
        if request.method == "POST":
                print("POST")
                #print("body:",request.body)

                prjname = request.POST.get("prjname")#Viene de un FORM
                print("prjname: ",prjname)

                prjcomment = request.POST.get("prjcomment")
                print("prjcomment: ",prjcomment)

                prjid = request.POST.get("prjid")
                print("prjid: ",prjid)

                #If id != "" -> update. Else -> create new
                if prjid != "":
                    project_objt_selected = MProject.objects.get(pk=prjid)
                    #print(project_objt_selected.name)
                    project_objt_selected.name = prjname
                    project_objt_selected.comment = prjcomment
                    project_objt_selected.save()

                """
                else:
                    if prjname != "":
                        print("Create new")
                        new_prj = MProject()
                        new_prj.name = prjname
                        new_prj.comment = prjcomment
                        new_prj.id_user_id = request.user.id #need id_user_id not id_user
                        new_prj.save()
                    else:
                        print("Need a name")
                """

        return HttpResponseRedirect(reverse('projects_rp_load', kwargs={'pk':prjid}))

        #return HttpResponseRedirect(reverse('projects', args=("")))
    else:
        return HttpResponseRedirect(reverse('login') )


def change_prj_select(request):
    print("change_prj_select()")
    if request.user.is_authenticated:
        #Search the projects that belong to the user selected (Test -> id_user=1)
        project_objt = MProject.objects.filter(id_user_id=request.user.id)
        prj_id = 0

        #take the first
        if len(project_objt) > 0:
            prj_id = project_objt[0].id
            version_obj = MVersion.objects.filter(id_project_id=prj_id)
            #for elt in version_obj:
                #print("Vname: ",elt.name)

        if request.method == "POST":
                print("POST")
                print("body:",request.body)

                json_request= json.loads(request.body)
                select_value = json_request['select_value'] #ID project to return

                project_objt_selected = MProject.objects.filter(id=select_value)
                prj_name = ""
                prj_comment = ""
                prj_id = ""
                for elt in project_objt_selected:
                    print("name: ",elt.name)
                    prj_name = elt.name
                    prj_comment = elt.comment
                    prj_id = elt.id

                """
                version_obj = MVersion.objects.filter(id_project_id=select_value)
                v_name = []
                v_comment = []
                v_id = []
                for elt in version_obj:
                    print("name: ",elt.name)
                    v_name.append(elt.name)
                    v_comment.append(elt.comment)
                    v_id.append(elt.id)
                """

                return JsonResponse({
                    'prj_name':prj_name,
                    'prj_comment':prj_comment,
                    'prj_id' : prj_id,
                    #'v_name' : v_name,
                    #'v_comment' : v_comment,
                    #'v_id' : v_id,
                    })
                

        else:
                print("NO POST")

                return render(request, "project_manager.html", {
                    #"project_objt" : project_objt,
                    #"version_obj" : version_obj,
                    })




    else:
        return HttpResponseRedirect(reverse('login') )

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


        
        #return HttpResponseRedirect(reverse('projects', args=("")))
    else:
        return HttpResponseRedirect(reverse('login') )

"""
def prj_vers_selected(request):
    print("prj_vers_selected()")
    if request.user.is_authenticated:
        if request.method == "POST":
                print("POST")
                print("body:",request.body)

                json_request= json.loads(request.body)
                select_value = json_request['v_list_id'] #ID project to return
                v_id = select_value
                print("Version ID: ",select_value)

                select_value = json_request['prj_id'] #ID project to return
                print("Project ID: ",select_value)
                prj_id = select_value

                if v_id == "":
                    print("no hay id de version -> crear!")
                    new_v = MVersion()
                    new_v.id_project_id = prj_id
                    new_v.name = "XXX"
                    new_v.save()
                    v_id = new_v.id


                return JsonResponse({
                    'flag_ok':True,
                    'v_id':v_id,
                    })

    else:
        return HttpResponseRedirect(reverse('login') )
"""

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


def projects_rp_load(request,pk):
    print("projects_rp_load()")
    print("project pk: ",pk)
    if request.user.is_authenticated:

        project_list = MProject.objects.filter(id_user=request.user.id)

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
            new_prj.save()

            pk = new_prj.id

        #if pk != 0:#Esto significa que hay project
            #prj_objt_selected = MProject.objects.get(id=pk)

        prj_objt_selected = MProject.objects.get(id=pk)


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

        context = {
            'mproject_list':project_list,
            'prj_id': pk,
            'prj_comment': prj_objt_selected.comment,
            'date_ini': prj_objt_selected.date_ini, #new
            'date_status': prj_objt_selected.date_status, #new
            'date_end': prj_objt_selected.date_end, #new

            'factor_weeks': prj_objt_selected.factor_weeks, #new
            'max_ecu_slide': prj_objt_selected.max_ecu_slide, #new

            'version_list': v_objt_selected,
        } 
        return render(request,'project_rp.html',context=context)
    else:
        return HttpResponseRedirect(reverse('login') )

def update_version_form(request):
    print("update_version_form()")
    if request.user.is_authenticated:
        if request.method == "POST":
            print("POST")
            print("body:",request.body)
                
            json_request= json.loads(request.body)
            version_id = json_request['version_id']
            print("version_id:",version_id)
            vers_id = version_id

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

                ECU_objt_selected = MECU.objects.filter(id_version=vers_id)
                for elt in ECU_objt_selected:
                    new_ecu = MECU()
                    new_ecu.name = elt.name
                    new_ecu.comment = elt.comment
                    new_ecu.id_version_id = new_v.id
                    new_ecu.save()

                vers_id = new_v.id
                reload = True

            if new_version == -1:
                print("Update version")
                version_objt_selected = MVersion.objects.get(id=vers_id)
                version_objt_selected.name = version_name
                version_objt_selected.save()
                reload = True
            
            #return HttpResponseRedirect(reverse('projects_rp_load', kwargs={'pk':project_id}))
            return JsonResponse({
                    'reload':reload,
                    'vers_id':vers_id,
            })

        #return HttpResponseRedirect(reverse('projects', args=("")))
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

        #return HttpResponseRedirect(reverse('projects', args=("")))
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
                for elt in ECUlist_objt_selected:
                    print("name eculist: ",elt.name)
                    ecuList_name.append(elt.name)
                    ecuList_comment.append(elt.comment)
                    ecuList_dx.append(elt.dx_ecu)
                    ecuList_id.append(str(elt.id))
                print("ecuList_name:",ecuList_name)


                return JsonResponse({
                    'ecuList_name': ecuList_name,
                    'ecuList_comment': ecuList_comment,
                    'ecuList_dx': ecuList_dx,
                    'ecuList_id': ecuList_id,
                })

        #return HttpResponseRedirect(reverse('projects', args=("")))
    else:
        return HttpResponseRedirect(reverse('login') )



#------------Configurar ECU + Release Plan----------------------------------------
#------------------------------------------------------------------------
def rp_load(request,pk):
    print("rp_load()")
    print("project pk: ",pk)
    if request.user.is_authenticated:

        #Get the LAST version for the project with id = rp_load
        v_objt_selected = MVersion.objects.filter(id_project=pk)

        v_id = 0
        if len(v_objt_selected) > 0:
            for elt in v_objt_selected:
                print("name v: ",elt.name)
                v_id = elt.id
        else:
            print("Este proyecto no tiene ninguna versión!")



        #Get the ECU list for the version ID
        ECUlist_objt_selected = MECU.objects.filter(id_version=v_id)
        ecuList_name = []
        ecuList_comment = []
        ecuList_dx = []
        ecuList_id = []
        for elt in ECUlist_objt_selected:
            print("name eculist: ",elt.name)
            ecuList_name.append(elt.name)
            ecuList_comment.append(elt.comment)
            ecuList_dx.append(elt.dx_ecu)
            ecuList_id.append(str(elt.id))
        print("ecuList_name:",ecuList_name)

        if request.method == "POST":
                print("POST")
                print("body:",request.body)

                # redirect to a new URL: ¿?
                return JsonResponse({
                    'ecuList_name': ecuList_name,
                    'ecuList_comment': ecuList_comment,
                    'ecuList_dx': ecuList_dx,
                    'ecuList_id': ecuList_id,
                })

        else:
                print("NO POST")

        #found the [release_inputs -> MRelease_input] for all ECUs for this version
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

                ecu_name = MECU.objects.get(id=ecu_id).name #Get ecu name for this Ri
                RelInList_ecu_name.append(ecu_name)
                #print("elt.id_ecu:",elt.id_ecu_id)
                type_name = MType_input.objects.get(id=elt.id_type_input_id).name 
                RelInList_type_name.append(type_name)

                plan_name = MPlan.objects.get(id=elt.id_plan_id).name 
                RelInList_plan.append(plan_name)

                ecu_obj = MECU.objects.get(id=elt.id_ecu_id) 
                RelInList_dx.append(ecu_obj.dx_ecu)


        #Get the all list of types
        type_list_id = []#Extra
        type_list_name = []#Extra
        type_list_comment = []#Extra
        type_list_obj = MType_input.objects.all()
        
        for elt in type_list_obj:
            type_list_id.append(str(elt.id))
            type_list_name.append(elt.name)
            type_list_comment.append(elt.comment)

        #Get the all list of plans
        plan_list_id = []#Extra
        plan_list_name = []#Extra
        plan_list_comment = []#Extra
        plan_list_obj = MPlan.objects.all()
        
        for elt in plan_list_obj:
            plan_list_id.append(str(elt.id))
            plan_list_name.append(elt.name)
            plan_list_comment.append(elt.comment)


        #Add (;)
        RelInList_id = ';'.join(RelInList_id)
        RelInList_id_ecu = ';'.join(RelInList_id_ecu)
        RelInList_id_type = ';'.join(RelInList_id_type)
        RelInList_n_version = ';'.join(RelInList_n_version)
        RelInList_date = ';'.join(RelInList_date)
        RelInList_plan = ';'.join(RelInList_plan)
        RelInList_id_plan = ';'.join(RelInList_id_plan)
        RelInList_visual = ';'.join(RelInList_visual)
        RelInList_dx = ';'.join(RelInList_dx)
        RelInList_comment = ';'.join(RelInList_comment)
        
        RelInList_ecu_name = ';'.join(RelInList_ecu_name)
        RelInList_type_name = ';'.join(RelInList_type_name)

        type_list_id = ';'.join(type_list_id)
        type_list_name = ';'.join(type_list_name)
        type_list_comment = ';'.join(type_list_comment)

        ecuList_name = ';'.join(ecuList_name)
        ecuList_comment = ';'.join(ecuList_comment)
        ecuList_dx = ';'.join(ecuList_dx)
        ecuList_id = ';'.join(ecuList_id)
        

        return render(request, "rp.html", {
            'ecuList_name': ecuList_name,
            'ecuList_comment': ecuList_comment,
            'ecuList_dx': ecuList_dx,
            'ecuList_id': ecuList_id,
            'id_v' : v_id,

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

            'RelInList_ecu_name': RelInList_ecu_name,
            'RelInList_type_name': RelInList_type_name,

            'type_list_id': type_list_id,
            'type_list_name': type_list_name,
            'type_list_comment': type_list_comment,

            'plan_list_id': plan_list_id,
            'plan_list_name': plan_list_name,
            'planlist_comment': plan_list_comment,
        
        })   #Search the projects that belong to the user selected (Test -> id_user=1)
        #id_user=1

        #Get the ECU list for the version ID
        ECUlist_objt_selected = MECU.objects.filter(id_version=v_id)
        ecuList_name = []
        ecuList_comment = []
        ecuList_dx = []
        ecuList_id = []
        for elt in ECUlist_objt_selected:
            print("name eculist: ",elt.name)
            ecuList_name.append(elt.name)
            ecuList_comment.append(elt.comment)
            ecuList_dx.append(elt.dx_ecu)
            ecuList_id.append(str(elt.id))
        print("ecuList_name:",ecuList_name)

        if request.method == "POST":
                print("POST")
                print("body:",request.body)

                # redirect to a new URL: ¿?
                return JsonResponse({
                    'ecuList_name': ecuList_name,
                    'ecuList_comment': ecuList_comment,
                    'ecuList_dx': ecuList_dx,
                    'ecuList_id': ecuList_id,
                })

        else:
                print("NO POST")

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

                ecu_name = MECU.objects.get(id=ecu_id).name #Get ecu name for this Ri
                RelInList_ecu_name.append(ecu_name)
                #print("elt.id_ecu:",elt.id_ecu_id)
                type_name = MType_input.objects.get(id=elt.id_type_input_id).name 
                RelInList_type_name.append(type_name)

                plan_name = MPlan.objects.get(id=elt.id_plan_id).name 
                RelInList_plan.append(plan_name)

                ecu_obj = MECU.objects.get(id=elt.id_ecu_id) 
                RelInList_dx.append(ecu_obj.dx_ecu)


        #Get the all list of types
        type_list_id = []#Extra
        type_list_name = []#Extra
        type_list_comment = []#Extra
        type_list_obj = MType_input.objects.all()
        
        for elt in type_list_obj:
            type_list_id.append(str(elt.id))
            type_list_name.append(elt.name)
            type_list_comment.append(elt.comment)

        #Get the all list of plans
        plan_list_id = []#Extra
        plan_list_name = []#Extra
        plan_list_comment = []#Extra
        plan_list_obj = MPlan.objects.all()
        
        for elt in plan_list_obj:
            plan_list_id.append(str(elt.id))
            plan_list_name.append(elt.name)
            plan_list_comment.append(elt.comment)


        #Add (;)
        RelInList_id = ';'.join(RelInList_id)
        RelInList_id_ecu = ';'.join(RelInList_id_ecu)
        RelInList_id_type = ';'.join(RelInList_id_type)
        RelInList_n_version = ';'.join(RelInList_n_version)
        RelInList_date = ';'.join(RelInList_date)
        RelInList_plan = ';'.join(RelInList_plan)
        RelInList_id_plan = ';'.join(RelInList_id_plan)
        RelInList_visual = ';'.join(RelInList_visual)
        RelInList_dx = ';'.join(RelInList_dx)
        RelInList_comment = ';'.join(RelInList_comment)
        
        RelInList_ecu_name = ';'.join(RelInList_ecu_name)
        RelInList_type_name = ';'.join(RelInList_type_name)

        type_list_id = ';'.join(type_list_id)
        type_list_name = ';'.join(type_list_name)
        type_list_comment = ';'.join(type_list_comment)

        ecuList_name = ';'.join(ecuList_name)
        ecuList_comment = ';'.join(ecuList_comment)
        ecuList_dx = ';'.join(ecuList_dx)
        ecuList_id = ';'.join(ecuList_id)
        

        return render(request, "rp.html", {
            'ecuList_name': ecuList_name,
            'ecuList_comment': ecuList_comment,
            'ecuList_dx': ecuList_dx,
            'ecuList_id': ecuList_id,
            'id_v' : v_id,

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
        return HttpResponseRedirect(reverse('login') )


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
                for row in json_allData:
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
                            ecu_obj.name = row['name']
                            ecu_obj.comment = row['comment']
                            ecu_obj.dx_ecu = row['dx']
                            ecu_obj.save()
                            """
                            ecu_model = MECU(
                                id = row['id'],
                                name = row['name'],
                                comment = row['comment'],
                                id_version_id = json_id_v
                            )
                            ecu_model.save()
                            """
                        else:
                            print("create new")
                            ecu_model = MECU(
                                name = row['name'],
                                comment = row['comment'],
                                dx_ecu = row['dx'],
                                id_version_id = json_id_v
                            )
                            ecu_model.save()

                
                ecuList_name = []
                ecuList_comment = []
                ecuList_dx = []
                ecuList_id = []
                ECUlist_objt_selected = MECU.objects.filter(id_version=json_id_v)
                for elt in ECUlist_objt_selected:
                    print("name: ",elt.name)
                    ecuList_name.append(elt.name)
                    ecuList_comment.append(elt.comment)
                    ecuList_dx.append(elt.dx_ecu)
                    ecuList_id.append(str(elt.id))
                print("ecuList_name:",ecuList_name)
                print("ecuList_comment:",ecuList_comment)
                print("ecuList_dx:",ecuList_dx)
                print("ecuList_id:",ecuList_id)
                
                
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

                        ecu_name = MECU.objects.get(id=ecu_id).name #Get ecu name for this Ri
                        RelInList_ecu_name.append(ecu_name)
                        #print("elt.id_ecu:",elt.id_ecu_id)
                        type_name = MType_input.objects.get(id=elt.id_type_input_id).name 
                        RelInList_type_name.append(type_name)

                        plan_name = MPlan.objects.get(id=elt.id_plan_id).name 
                        RelInList_plan.append(plan_name)
                        print("RelInList_plan: ",RelInList_plan)

                        ecu_obj = MECU.objects.get(id=elt.id_ecu_id) 
                        RelInList_dx.append(ecu_obj.dx_ecu)


                #Get the all list of types
                type_list_id = []#Extra
                type_list_name = []#Extra
                type_list_comment = []#Extra
                type_list_obj = MType_input.objects.all()
                
                for elt in type_list_obj:
                    type_list_id.append(str(elt.id))
                    type_list_name.append(elt.name)
                    type_list_comment.append(elt.comment)

                #Get the all list of plans
                plan_list_id = []#Extra
                plan_list_name = []#Extra
                plan_list_comment = []#Extra
                plan_list_obj = MPlan.objects.all()
                
                for elt in plan_list_obj:
                    plan_list_id.append(str(elt.id))
                    plan_list_name.append(elt.name)
                    plan_list_comment.append(elt.comment)
                print("plan_list_name: ",plan_list_name)
                    
                #----------

                # redirect to a new URL: ¿?
                return JsonResponse({
                    'flag_ok' : True,
                    'ecuList_name': ecuList_name,
                    'ecuList_comment': ecuList_comment,
                    'ecuList_dx': ecuList_dx,
                    'ecuList_id': ecuList_id,
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

                    'RelInList_ecu_name': RelInList_ecu_name,
                    'RelInList_type_name': RelInList_type_name,

                    'type_list_id': type_list_id,
                    'type_list_name': type_list_name,
                    'type_list_comment': type_list_comment,

                    'plan_list_id': plan_list_id,
                    'plan_list_name': plan_list_name,
                    'planlist_comment': plan_list_comment,
                })

                """
                return JsonResponse({
                    'flag_ok' : True,
                    'ecuList_name': ecuList_name,
                    'ecuList_comment': ecuList_comment,
                    'ecuList_dx': ecuList_dx,
                    'ecuList_id': ecuList_id,
                })
                """
        else:
                print("NO POST")
                return HttpResponseRedirect(reverse('rp_load', args=(json_id_v)))

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
                    list_filter = row['RelInList_ecu_name'].split("-")
                    name_clean = list_filter[0].rstrip() #rstrip() elimina los ultimos espacios si los hay
                    print("name_clean:->",name_clean,"<-")

                    ECU_selected = MECU.objects.filter(name=name_clean)
                    ecu_id = 0
                    for elt in ECU_selected:
                        ecu_id = elt.id
                        print("ecu_id:",ecu_id)

                    #Find type, por si se cambió
                    type_selected = MType_input.objects.filter(name=row['RelInList_type_name'])
                    type_id = 0
                    for elt in type_selected:
                        type_id = elt.id
                        print("type_id:",type_id)

                    #Find plan, por si se cambió
                    plan_selected = MPlan.objects.filter(name=row['RelInList_plan'])
                    plan_id = 0
                    for elt in plan_selected:
                        plan_id = elt.id
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

                    if int(row['RelInList_id'])!= 0: #añadir checkeo de vacio ""
                        print("update value")
                        RI_selected = MRelease_input.objects.get(id = int(row['RelInList_id']))

                        RI_selected.id_ecu_id = int(ecu_id)
                        RI_selected.id_type_input_id = type_id
                        RI_selected.n_version = row['RelInList_n_version']
                        RI_selected.date_beantragt = row['RelInList_date']
                        #RI_selected.plan = row['RelInList_plan']
                        RI_selected.id_plan_id = plan_id

                        RI_selected.flag_visual = flag_visual
                        RI_selected.comment = row['RelInList_comment']
                        RI_selected.save()
                        """
                        #Otro método
                        RI_model = Release_input_model(
                            id = row['RelInList_id'],
                            id_ecu_id = ecu_id,
                            id_type_input_id = type_id,
                            n_version = row['RelInList_n_version'],
                            date_beantragt = row['RelInList_date'],
                            plan = row['RelInList_plan'],
                            flag_visual = flag_visual,
                            comment = row['RelInList_comment'],
                        )
                        """
                        #RI_model.save()
                        
                    else:
                        print("create new")
                        RI_model = MRelease_input(
                            #id = row['RelInList_id'],
                            id_ecu_id = ecu_id,
                            id_type_input_id = type_id,
                            n_version = row['RelInList_n_version'],
                            date_beantragt = row['RelInList_date'],
                            #plan = row['RelInList_plan'],
                            id_plan_id = plan_id,
                            flag_visual = flag_visual,
                            comment = row['RelInList_comment'],
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

                    ecu_name = MECU.objects.get(id=ecu_id).name #Get ecu name for this Ri
                    RelInList_ecu_name.append(ecu_name)
                    #print("elt.id_ecu:",elt.id_ecu_id)
                    type_name = MType_input.objects.get(id=elt.id_type_input_id).name 
                    RelInList_type_name.append(type_name)

                    plan_name = MPlan.objects.get(id=elt.id_plan_id).name 
                    RelInList_plan.append(plan_name)

                    ecu_obj = MECU.objects.get(id=elt.id_ecu_id) 
                    RelInList_dx.append(ecu_obj.dx_ecu)

            #Get the all list of types
            type_list_id = []#Extra
            type_list_name = []#Extra
            type_list_comment = []#Extra
            type_list_obj = MType_input.objects.all()
                
            for elt in type_list_obj:
                type_list_id.append(str(elt.id))
                type_list_name.append(elt.name)
                type_list_comment.append(elt.comment)

            #Get the all list of plans
            plan_list_id = []#Extra
            plan_list_name = []#Extra
            plan_list_comment = []#Extra
            plan_list_obj = MPlan.objects.all()
            
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
            json_id_v = 3
            return HttpResponseRedirect(reverse('rp_load', args=(json_id_v)))

   else:
       return HttpResponseRedirect(reverse('login') )








#Vistas genéricas-----------
"""
def index(request):

    # Genera contadores de algunos de los objetos principales
    num_users=User.objects.all().count()
    num_projects=MProject.objects.all().count()

    # uso de sesiones: https://docs.djangoproject.com/en/3.1/topics/http/sessions/
    # Numero de visitas a esta view, como está contado en la variable de sesión.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_users':num_users,
        'num_projects':num_projects,
        'num_visits':num_visits,
    } 

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(request,'index.html',context=context)


#Vistas genéricas-----------
from django.views import generic

class ProjectListView(generic.ListView):
    model = MProject
    paginate_by = 2 #más de X registros la vista comenzará a paginar la información que envía a la plantilla. A las diferentes páginas se accede usando parámetros GET -- para acceder a la página 2 usarías la URL: /rpm_web/projects/?page=2

class ProjectDetailView(generic.DetailView):
    model = MProject

#La siguiente función permite limitar el acceso a los usuarios logueados. si n oestás, se te remite a la pag de login.
class LoanedProjectsByUserListView(LoginRequiredMixin,generic.ListView):

    model = MProject
    template_name ='catalog/project_model_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self):
        return MProject.objects.filter(borrower=self.request.user)

#Forms----------
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookModelForm

#@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):

    book_inst=get_object_or_404(MProject, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            #book_inst.due_back = form.cleaned_data['renewal_date']
            #book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'name': 'testname',})

    return render(request, 'rpm_web/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
"""
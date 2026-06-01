from tkinter import *
from tkinter import ttk
from faker import Faker
from datetime import datetime
import random
import re
import html
import json
fake = Faker("ES")


def ubicarVentana(ventana,ancho,largo):
    """
    Funcionamiento: Esta funcion se encarga de ubicar la ventana en el centro de la pantalla
    Entradas:
    - ventana: es la ventana que se desea ubicar
    - ancho: es el ancho que se le asignara a la ventana
    - largo: es el largo que se le asignara a la ventana
    """
    pantallaAncho=ventana.winfo_screenwidth()
    pantallaLargo=ventana.winfo_screenheight()
    x=int((pantallaAncho/2)-(ancho/2))
    y=int((pantallaLargo/2)-(largo/2))-50
    ventana.geometry(f"{ancho}x{largo}+{x}+{y}")

# ---------------- VENTANA PRINCIPAL ----------------
ventana = Tk()
ventana.title("Banco de Sangre")
ubicarVentana(ventana,700,600)
ventana.config(bg="#f4f7fb")
ventana.resizable(False,False)
# ---------------- TITULO ----------------

titulo = Label(ventana,text="DONAR SANGRE, ES DONAR VIDA",
    font=("Arial",24,"bold"),bg="#ffffff",fg="black")
titulo.pack(pady=30)
# ---------------- SUBTITULO ----------------
subtitulo = Label(ventana,text="Sistema de Información - Banco de Sangre",
    font=("Arial",14),bg="white",fg="black")
subtitulo.pack(pady=5)
# ---------------- MARCO DEL MENU ----------------
frameMenu = Frame(ventana,bg="#ffffff",bd=4,relief="ridge")
frameMenu.pack(pady=40)
# Inicializaciones 

def cargarDatos():
    try:
        with open("Donantes.json", "r") as f:
            return json.load(f)
    except:
        return []

def guardarDatos(donantes):
    with open("Donantes.json", "w") as f:
        json.dump(donantes, f, indent=4, ensure_ascii=False)

donantes = cargarDatos()


lugaresDonacion={
    "San Jose":["Banco Nacional de Sangre","Hospital Mexico","Hospital San Juan de Dios"],
    "Alajuela":["Hospital San Rafael de Alajuela","Hospital de San Ramon","Hospital del Canton Norteno"],
    "Cartago":["Hospital Max Peralta"],
    "Heredia":["Hospital San Vicente de Paul"],
    "Guanacaste":["Hospital La Anexion en Nicoya","Hospital Enrique Baltodano de Liberia"],
    "Puntarenas":["Hospital Monsenor Sanabria"],
    "Limon":["Hospital Tony Facio","Hospital de Guapiles"]}
# ================================ FUNCIONES ========================================
# =============Funcione de uso general para todas las funciones====================

def cedulaInser(frameInsertar):
    """
    Funcionamiento: Esta funcion se encarga de crear la entrada para la cedula en la ventana de insertar donante
    Entradas:
    - frameInsertar: es el frame donde se desea crear la entrada
    Salidas:
    - cedula: es la variable que contiene el valor de la cedula ingresada por el usuario
    """
    Label(frameInsertar, text = "Cedula", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 0,column=0,pady=5)
    cedula = StringVar()
    Entry(frameInsertar,textvariable=cedula).grid(row=0,column=1)
    return cedula
    
def cedulaInserAux(cedula):
    """
    Funcionamiento: Esta funcion se encarga de validar la cedula ingresada por el usuario en la ventana de insertar donante
    Entradas:
    - cedula: es la variable que contiene el valor de la cedula ingresada por el usuario
    Salidas:
    - (True, cedula): si la cedula es valida
    - (False, mensaje): si la cedula no es valida
    """
    formato=r"[1-9]{1}-[0-9]{4}-[0-9]{4}"
    numeros=cedula.replace("-","")
    if numeros=="":
        return(False,"Debe ingresar una cedula")
    for i in numeros:
        if i.isdigit()==False:
            return(False,"Los datos ingresados en cedula nada mas deben ser numeros")
    if re.fullmatch(formato,cedula) is None:
        return(False,"Formato invalido en cedula, ejemplo de formato correcto #-####-####")
    return(True,cedula)
    
def nombreInser(frameInsertar):
    """
    Funcionamiento: Esta funcion se encarga de crear la entrada para el nombre en la ventana de insertar donante
    Entradas:
    - frameInsertar: es el frame donde se desea crear la entrada
    Salidas:
    - nombre: es la variable que contiene el valor del nombre ingresado por el usuario
    """
    Label(frameInsertar, text = "Nombre completo", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 1,column=0,pady=5)
    nombre = StringVar()
    Entry(frameInsertar,textvariable=nombre).grid(row=1,column=1)
    return nombre   

def normalizarNombre(pnombre):
    """
    Funcinamiento: Esta funcion se encarga de validar el nombre ingresado por el usuario en la ventana de insertar donante, ademas de normalizarlo para que tenga la primera letra en mayuscula y el resto en minuscula
    Entradas:
    - pnombre: es la variable que contiene el valor del nombre ingresado por el usuario
    Salidas:
    - (True, resultado): si el nombre es valido, resultado es el nombre normalizado
    """
    if pnombre == "":
        return (False,"Debe incluir un nombre")
    for letra in pnombre:
        if letra.isalpha() == False and letra != " ":
            return(False,"Debe ingresar solamente letras en el nombre")
    palabras = pnombre.split()
    if len(palabras) != 3:
        return (False, "Debe ingresar un nombre y dos apellidos")
    resultado = []
    for p in palabras:                           
        palabra = p[0].upper() + p[1:].lower() 
        resultado += [palabra]
    return (True,resultado)

def fechaNacimientoInser(frameInsertar):
    """
    Funcionamiento: Esta funcion se encarga de crear la entrada para la fecha de nacimiento en la ventana de insertar donante
    Entradas:
    - frameInsertar: es el frame donde se desea crear la entrada
    Salidas:
    - fechaNacimiento: es la variable que contiene el valor de la fecha de nacimiento ingresada por el usuario
    """
    Label(frameInsertar, text = "Fecha de nacimiento", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 2,column=0,pady=5)
    fechaNacimiento = StringVar()
    Entry(frameInsertar,textvariable= fechaNacimiento).grid(row=2,column=1)
    return fechaNacimiento

def validarFechaAux(fechaNacimiento):
    """
    Funcionamiento: Esta funcion se encarga de validar la fecha de nacimiento ingresada por el usuario en la ventana de insertar donante, ademas de verificar que la fecha sea valida teniendo en cuenta los dias de cada mes y los años bisiestos
    Entradas:
    - fechaNacimiento: es la variable que contiene el valor de la fecha de nacimiento ingresada por el usuario
    Salidas:
    - (True, fechaNacimiento): si la fecha de nacimiento es valida
    """
    formato=r"\d{2}/\d{2}/\d{4}"
    if re.fullmatch(formato,fechaNacimiento)is None :
        return(False,"Formato invalido en fecha de nacimiento use el formato DD/MM/AAAA")
    fecha=fechaNacimiento.split("/")
    dia=int(fecha[0])
    mes=int(fecha[1])
    anno=int(fecha[2])
    if mes<1 or mes>12:
        return(False,"El mes ingresado en fecha de nacimiento no existe")
    if anno<1900:
        return(False,"El año ingresado en fecha de nacimiento no es valido")
    if mes in [1,3,5,7,8,10,12]:
        if dia<1 or dia>31:
            return(False,"Ese mes ingredago en fecha de nacimiento solo tiene 31 dias")
    elif mes in [4,6,9,11]:
        if dia<1 or dia>30:
            return(False,"Ese mes ingresado en fecha de nacimiento solo tiene 30 dias")
    elif mes==2:
        bisiesto=False
        if anno%4==0 and anno%100!=0:
            bisiesto=True
        elif anno%400==0:
            bisiesto=True
        if bisiesto==True:
            if dia<1 or dia>29:
                return(False,"Fecha de nacimiento:  febrero en año bisiesto solo tiene 29 dias")
        else:
            if dia<1 or dia>28:
                return(False,"Fecha de nacimiento: febrero solo tiene 28 dias")
    return(True,fechaNacimiento)

def tipoSangreInser(frameInsertar):
    """
    Funcionamiento: Esta funcion se encarga de crear la entrada para el tipo de sangre en la ventana de insertar donante
    Entradas:
    - frameInsertar: es el frame donde se desea crear la entrada
    Salidas:
    - tipoSangre: es la variable que contiene el valor del tipo de sangre ingresado por el usuario
    """
    Label(frameInsertar, text = "Tipo de sangre", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 3,column=0,pady=5)
    tipoSangre = StringVar()
    ttk.Combobox(frameInsertar,textvariable=tipoSangre,
        values=["O+","O-","A+","A-","B+","B-","AB+","AB-"]
        ).grid(row=3, column = 1)
    return tipoSangre

def sexoInser(frameInsertar):
    """
    Funcionamiento: Esta funcion se encarga de crear la entrada para el sexo en la ventana de insertar donante
    Entradas:
    - frameInsertar: es el frame donde se desea crear la entrada
    Salidas:
    - sexo: es la variable que contiene el valor del sexo ingresado por el usuario
    """
    frameSexo = Frame(frameInsertar, bg = "#ffffff", bd = 5)
    Label(frameSexo, text = "Sexo", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 0,column=0,pady=5)
    sexo = BooleanVar(value=True)
    Radiobutton(frameSexo, text= "Femenino",variable=sexo,value = False).grid(row=0,column=2)
    Radiobutton(frameSexo, text= "Masculino",variable=sexo,value = True).grid(row=0,column=1)
    frameSexo.grid(row=4)
    return sexo

def pesoInser(frameInsertar):
    """Funcionamiento: Esta funcion se encarga de crear la entrada para el peso en la ventana de insertar donante
    Entradas:
    - frameInsertar: es el frame donde se desea crear la entrada
    Salidas:
    - peso: es la variable que contiene el valor del peso ingresado por el usuario
    """
    Label(frameInsertar, text = "Peso(kg)", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 5,column=0,pady=5)
    peso = StringVar()
    Entry(frameInsertar,textvariable=peso).grid(row=5,column=1)
    return peso

def validarPesoAux(peso):
    """
    Funcionamiento: Esta funcion se encarga de validar el peso ingresado por el usuario en la ventana de insertar donante, ademas de verificar que el peso sea un numero entero positivo
    Entradas:
    - peso: es la variable que contiene el valor del peso ingresado por el usuario
    Salidas:
    - (True, peso): si el peso es valido
    - (False, mensaje): si el peso no es valido
    """
    if peso.isdigit()==False:
        return(False,"El peso solo debe contener numeros")
    return(True,peso)

def telefonoInser(frameInsertar):
    """
    Funcionamiento: Esta funcion se encarga de crear la entrada para el telefono en la ventana de insertar donante
    Entradas:
    - frameInsertar: es el frame donde se desea crear la entrada
    Salidas:
    - telefono: es la variable que contiene el valor del telefono ingresado por el usuario
    """
    Label(frameInsertar, text = "Telefono", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 6,column=0,pady=5)
    telefono = StringVar()
    Entry(frameInsertar,textvariable= telefono).grid(row=6,column=1)
    return telefono

def validarTelefonoAux(telefono):
    """
    Funcionamiento: Esta funcion se encarga de validar el telefono ingresado por el usuario en la ventana de insertar donante, ademas de verificar que el telefono tenga el formato correcto y que solo contenga numeros y un '-' como separador
    Entradas:
    - telefono: es la variable que contiene el valor del telefono ingresado por el usuario
    Salidas:
    - (True, telefono): si el telefono es valido
    - (False, mensaje): si el telefono no es valido
    """
    formato=r"[0-9]{4}-[0-9]{4}"
    if telefono == "":
        return(False,"Debe ingresar un numero de telefono")
    elif re.fullmatch(formato,telefono)==None:
        return(False,"Formato invalido en el numero de telefono, ejemplo correcto de formato ####-####")
    telefono=telefono.replace("-","")
    if telefono.isdigit()==False:
        return(False,"El numero de telefono solo debe contener numeros y un '-' como separador.")
    if telefono[0] in ["0","1","3","5"]:
        return(False,"El numero telefonico no puede iniciar con 0,1,3 o 5")
    return(True,telefono)

def correoInser(frameInsertar):
    """
    Funcionamiento: Esta funcion se encarga de crear la entrada para el correo en la ventana de insertar donante
    Entradas:
    - frameInsertar: es el frame donde se desea crear la entrada
    Salidas:
    - correo: es la variable que contiene el valor del correo ingresado por el usuario
    """
    Label(frameInsertar, text = "Correo", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 7,column=0,pady=5)
    correo = StringVar()
    Entry(frameInsertar,textvariable=correo).grid(row=7,column=1)
    return correo

def validarCorreoAux(correo):
    """
    Funcionamiento: Esta funcion se encarga de validar el correo ingresado por el usuario en la ventana de insertar donante, ademas de verificar que el correo tenga el formato correcto y que solo contenga letras, numeros y los caracteres permitidos en un correo
    Entradas:
    - correo: es la variable que contiene el valor del correo ingresado por el usuario
    Salidas:
    - (True, correo): si el correo es valido
    - (False, mensaje): si el correo no es valido
    """
    if correo == "":
        return(False,"Debe ingresar un correo")
    formato=r"[a-zA-Z0-9%+-]+@(gmail\.com|racsa\.go\.cr|costarricense\.cr|ccss\.sa\.cr)$"
    if re.fullmatch(formato,correo)==None:
        return(False,"Correo invalido ejemplo formato de correo correcto ejemplo@gmail.com")
    return(True,correo)

#===============================Funciones para la fa funcion de insertar donadores======================================

def definirProvincia(n):
    """
    Funcionamiento: Esta funcion se encarga de definir la provincia a partir del primer numero de la cedula ingresada por el usuario en la ventana de insertar donante
    Entradas:
    - n: es el primer numero de la cedula ingresada por el usuario
    Salidas:
    - provincia: es la provincia correspondiente al numero ingresado por el usuario
    """
    n = int(n)
    if n==1:
        return "San Jose"
    elif n==2:
        return "Alajuela"
    elif n==3:
        return "Cartago"
    elif n == 4:
        return "Heredia"
    elif n == 5:
        return "Guanacaste"
    elif n == 6:
        return "Puntarenas"
    elif n == 7:
        return "Limon"

def calcularEdad(fechaNacimiento):
    """
    Funcionamiento: Esta funcion se encarga de calcular la edad a partir de la fecha de nacimiento ingresada por el usuario en la ventana de insertar donante, ademas de verificar si el mes y el dia de nacimiento ya pasaron en el año actual para calcular la edad correctamente
    Entradas:
    - fechaNacimiento: es la variable que contiene el valor de la fecha de nacimiento ingresada por el usuario
    Salidas:
    - edad: es la edad calculada a partir de la fecha de nacimiento ingresada por el usuario
    """
    fecha=fechaNacimiento.split("/")
    diaNacimiento=int(fecha[0])
    mesNacimiento=int(fecha[1])
    annoNacimiento=int(fecha[2])
    diaActual=17
    mesActual=5
    annoActual=2026
    edad=annoActual-annoNacimiento
    if mesNacimiento>mesActual:
        edad=edad-1
    elif mesNacimiento==mesActual:
        if diaNacimiento>diaActual:
            edad=edad-1
    return edad

def mayorEdad(fechaNacimiento):
    """
    Funcionamiento: Esta funcion se encarga de verificar si la edad calculada a partir de la fecha de nacimiento ingresada por el usuario en la ventana de insertar donante es mayor o igual a 18 años para determinar si el usuario puede ser donante o no
    Entradas:
    - fechaNacimiento: es la variable que contiene el valor de la fecha de nacimiento ingresada por el usuario
    Salidas:
    - mensaje: es un mensaje que indica si el usuario puede ser donante o no a partir de su edad calculada
    """
    if calcularEdad(fechaNacimiento) >= 18:
        return "Dado su fecha de nacimineto usted ya puede ser donador"
    return"Dado su fecha de nacimiento usted aun no puede ser donador"

def compatibilidadSangre(tipoSangre):
    """
    Funcionamiento: Esta funcion se encarga de determinar la compatibilidad de sangre a partir del tipo de sangre ingresado por el usuario en la ventana de insertar donante, ademas de retornar una lista con los tipos de sangre a los que el usuario puede donar
    Entradas:
    - tipoSangre: es la variable que contiene el valor del tipo de sangre ingresado por el usuario
    Salidas:
    - compatibilidad[tipoSangre]: es una lista con los tipos de sangre a los que el usuario puede donar a partir del tipo de sangre ingresado por el usuario
    """
    compatibilidad = {"O-":["O+","O-","A+","A-","B-","B+","AB-","AB+"],
               "O+":["O+","A+","B+","AB+"],
               "A-":["A+","A-","AB-","AB+"],
               "A+":["A+","AB+"],
               "B-":["B-","B+","AB-","AB+"],
               "B+":["B+","AB+"],
               "AB-":["AB-","AB+"],
               "AB+":["AB+"]}
    return compatibilidad[tipoSangre]

def recomendacionSangre(tipoSangre):
    """
    Funcionamiento: Esta funcion se encarga de retornar una recomendacion a partir del tipo de sangre ingresado por el usuario en la ventana de insertar donante, ademas de recomendar un video sobre las particularidades de la sangre tipo A si el usuario tiene ese tipo de sangre
    Entradas:
    - tipoSangre: es la variable que contiene el valor del tipo de sangre ingresado por el usuario
    Salidas:
    - mensaje: es un mensaje que contiene una recomendacion a partir del tipo de sangre ingresado por el usuario, si el tipo de sangre es A+ o A- se recomienda un video sobre las particularidades de la sangre tipo A
    """
    if tipoSangre in ["A+","A-"]:
        return "Se le recomienda ver este video sobre las particularidades de la sangre tipo 'A'"
    return None

def validarLugarNacimiento(cedula,lugaresDonacion):
    """
    Funcionamiento: Esta funcion se encarga de validar el lugar de nacimiento a partir de la cedula ingresada por el usuario en la ventana de insertar donante
    Entradas:
    - cedula: es la variable que contiene el valor de la cedula ingresada por el usuario
    - lugaresDonacion: es la variable que contiene los lugares de donacion disponibles
    Salidas:
    - mensaje: es un mensaje que indica el lugar de nacimiento del usuario y los lugares donde puede donar a partir de la cedula ingresada por el usuario
    """
    cedula = cedula.split("-")
    provincia = definirProvincia(cedula[0])
    ubicacion = str(lugaresDonacion[provincia])
    return "Dado que usted nació en la provincia de: "+provincia+"\n usted podria donar en: "+ubicacion

def recomendaccionPeso(peso):
    """
    Funcionamiento: Esta funcion se encarga de recomendar si el usuario tiene un peso adecuado para donar sangre a partir del peso ingresado por el usuario en la ventana de insertar donante, ademas de indicar el motivo por el cual el usuario no puede donar sangre si su peso es menor a 50 kg o mayor a 120 kg
    Entradas:
    - peso: es la variable que contiene el valor del peso ingresado por el usuario
    Salidas:
    - mensaje: es un mensaje que indica si el usuario tiene un peso adecuado para donar sangre a partir del peso ingresado por el usuario, si el peso es menor a 50 kg o mayor a 120 kg se indica el motivo por el cual el usuario no puede donar sangre
    """
    mensaje = ""
    if int(peso)<=50:
        mensaje = "No puede donar sangre por bajo peso\n"
    elif int(peso) >=120:
        mensaje = "No puede donar sangre por sobrepeso\n"
    else:
        mensaje = "usted posee un peso adecuado para donar sangre.\n"
    return mensaje

def generarAnalisisDonante(cedula,fechaNacimiento,tipoSangre,peso,lugaresDonacion):
    """
    Funcionamiento: Esta funcion se encarga de generar un analisis del donante a partir de la cedula, fecha de nacimiento, tipo de sangre y peso ingresados por el usuario en la ventana de insertar donante, ademas de retornar un mensaje con el analisis generado
    Entradas:
    - cedula: es la variable que contiene el valor de la cedula ingresada por el usuario
    - fechaNacimiento: es la variable que contiene el valor de la fecha de nacimiento ingresada por el usuario
    - tipoSangre: es la variable que contiene el valor del tipo de sangre ingresado por el usuario
    - peso: es la variable que contiene el valor del peso ingresado por el usuario
    Salidas:
    - mensaje: es un mensaje que contiene el analisis del donante generado a partir de los datos ingresados
    """
    resultadoProvincia=validarLugarNacimiento(cedula,lugaresDonacion)
    edad=mayorEdad(fechaNacimiento)
    comenPeso = recomendaccionPeso(peso)
    compatibilidad=compatibilidadSangre(tipoSangre)
    recomendacion=recomendacionSangre(tipoSangre)
    mensaje=""
    mensaje+=edad+"\n"
    mensaje+= resultadoProvincia+"\n"
    mensaje += comenPeso+"\n"
    mensaje+="Puede donar a:\n"
    for i in compatibilidad:
        mensaje+=i+"\n"
    if recomendacion != None:
        mensaje+="\nRecomendacion:\n"
        mensaje+=recomendacion
    return mensaje

def validarDatos(donantes,cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo):
    """
    Funcionamiento: Esta funcion se encarga de validar los datos ingresados por el usuario en la ventana de insertar donante, ademas de agregar el donante a la lista de donantes si todos los datos son validos
    Entradas:
    - donantes: es la variable que contiene la lista de donantes
    - cedula: es la variable que contiene el valor de la cedula ingresada por el usuario
    - nombre: es la variable que contiene el valor del nombre ingresado por el usuario
    - fechaNacimiento: es la variable que contiene el valor de la fecha de nacimiento ingresada por el usuario
    - tipoSangre: es la variable que contiene el valor del tipo de sangre ingresado por el usuario
    - sexo: es la variable que contiene el valor del sexo ingresado por el usuario
    - peso: es la variable que contiene el valor del peso ingresado por el usuario
    - telefono: es la variable que contiene el valor del telefono ingresado por el usuario
    - correo: es la variable que contiene el valor del correo ingresado por el usuario
    Salidas:
    - (True, mensaje): si todos los datos son validos, mensaje es un mensaje que indica que el donante fue registrado correctamente
    - (False, mensaje): si algun dato no es valido, mensaje es un mensaje que indica el error encontrado
    """
    resultadoCedula=cedulaInserAux(cedula)
    if resultadoCedula[0]==False:
        return resultadoCedula
    resultadoNombre = normalizarNombre(nombre)
    if resultadoNombre[0] == False:
        return resultadoNombre
    resultadoFecha=validarFechaAux(fechaNacimiento)
    if resultadoFecha[0]==False:
        return resultadoFecha
    resultadoPeso=validarPesoAux(peso)
    if resultadoPeso[0]==False:
        return resultadoPeso
    resultadoTelefono=validarTelefonoAux(telefono)
    if resultadoTelefono[0]==False:
        return resultadoTelefono
    resultadoCorreo=validarCorreoAux(correo)
    if resultadoCorreo[0]==False:
        return resultadoCorreo
    donantes.append([nombre,cedula,fechaNacimiento,tipoSangre,
        sexo,peso,telefono,correo,1,0])
    guardarDatos(donantes)
    return(True,"Donante registrado correctamente")

def registrar(mensajeRegistrar,donantes,cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo,mensaje,lugaresDonacion):
    """
    Funcionamiento: Esta funcion se encarga de registrar el donante a partir de los datos ingresados por el usuario en la ventana de insertar donante, ademas de validar los datos ingresados y mostrar un mensaje con el resultado del registro
    Entradas:
    - mensajeRegistrar: es la variable que contiene el mensaje donde se mostrara el analisis del donante registrado
    - donantes: es la variable que contiene la lista de donantes
    - cedula: es la variable que contiene el valor de la cedula ingresada por el usuario
    - nombre: es la variable que contiene el valor del nombre ingresado por el usuario
    - fechaNacimiento: es la variable que contiene el valor de la fecha de nacimiento ingresada por el usuario
    - tipoSangre: es la variable que contiene el valor del tipo de sangre ingresado por el usuario
    - sexo: es la variable que contiene el valor del sexo ingresado por el usuario
    - peso: es la variable que contiene el valor del peso ingresado por el usuario
    - telefono: es la variable que contiene el valor del telefono ingresado por el usuario
    - correo: es la variable que contiene el valor del correo ingresado por el usuario
    - mensaje: es la variable que contiene el mensaje donde se mostrara el resultado del registro
    Salidas:
    - mensaje: es un mensaje que indica el resultado del registro, si el registro fue exitoso se muestra un mensaje con el analisis del donante registrado, si el registro no fue exitoso se muestra un mensaje con el error encontrado
    """
    resultado=validarDatos(donantes,cedula.get(),nombre.get(),fechaNacimiento.get(),tipoSangre.get(),
        sexo.get(),peso.get(),telefono.get(),correo.get())
    if resultado[0]==False:
        mensaje.config(text=resultado[1],fg="red")
        return
    mensaje.config(text=resultado[1],fg="green")
    mensajeRegistrar.config(text= generarAnalisisDonante(cedula.get(),fechaNacimiento.get(),tipoSangre.get(),peso.get(),lugaresDonacion),font=("calibri",11,"bold"))
    mensajeRegistrar.pack()

def limpiar(cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo):
    """
    Funcionamiento: Esta funcion se encarga de limpiar las entradas de la ventana de insertar donante, ademas de limpiar el mensaje donde se muestra el resultado del registro
    Entradas:
    - cedula: es la variable que contiene el valor de la cedula ingresada por el usuario
    - nombre: es la variable que contiene el valor del nombre ingresado por el usuario
    - fechaNacimiento: es la variable que contiene el valor de la fecha de nacimiento ingresada
    - tipoSangre: es la variable que contiene el valor del tipo de sangre ingresado por el usuario
    - sexo: es la variable que contiene el valor del sexo ingresado por el usuario
    - peso: es la variable que contiene el valor del peso ingresado por el usuario
    - telefono: es la variable que contiene el valor del telefono ingresado por el usuario
    - correo: es la variable que contiene el valor del correo ingresado por el usuario
    Salidas:
    - cedula: se limpia el valor de la cedula ingresada por el usuario
    - nombre: se limpia el valor del nombre ingresado por el usuario
    - fechaNacimiento: se limpia el valor de la fecha de nacimiento ingresada por el usuario
    - tipoSangre: se limpia el valor del tipo de sangre ingresado por el usuario
    - sexo: se limpia el valor del sexo ingresado por el usuario
    - peso: se limpia el valor del peso ingresado por el usuario
    - telefono: se limpia el valor del telefono ingresado por el usuario
    - correo: se limpia el valor del correo ingresado por el usuario
    """
    cedula.set("")
    nombre.set("")
    fechaNacimiento.set("")
    tipoSangre.set("")
    sexo.set(True)
    peso.set("")
    telefono.set("")
    correo.set("")

def salirInser(ventana,ventanaInsertar):
    """
    Funcionamiento: Esta funcion se encarga de cerrar la ventana de insertar donante y mostrar la ventana principal
    Entradas:
    - ventana: es la variable que contiene la ventana principal
    - ventanaInsertar: es la variable que contiene la ventana de insertar donante
    Salidas:
    - ventana: se muestra la ventana principal
    - ventanaInsertar: se cierra la ventana de insertar donante
    """
    ventana.deiconify()
    ventanaInsertar.destroy()

def crearBotones(ventana,frameBotones,ventanaInsertar,mensaje,mensajeRegistrar,donantes,cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo,lugaresDonacion):
    """
    Funcionamiento: Esta funcion se encarga de crear los botones de la ventana de insertar donante, ademas de asignarles la funcionalidad correspondiente a cada uno
    Entradas:
    - ventana: es la variable que contiene la ventana principal
    - frameBotones: es la variable que contiene el frame donde se desean crear los botones
    - ventanaInsertar: es la variable que contiene la ventana de insertar donante
    - mensaje: es la variable que contiene el mensaje donde se mostrara el resultado del registro
    - mensajeRegistrar: es la variable que contiene el mensaje donde se mostrara el analisis del donante registrado
    - donantes: es la variable que contiene la lista de donantes
    - cedula: es la variable que contiene el valor de la cedula ingresada por el usuario
    - nombre: es la variable que contiene el valor del nombre ingresado por el usuario
    - fechaNacimiento: es la variable que contiene el valor de la fecha de nacimiento ingresada por el usuario
    - tipoSangre: es la variable que contiene el valor del tipo de sangre ingresado por el usuario
    - sexo: es la variable que contiene el valor del sexo ingresado por el usuario
    - peso: es la variable que contiene el valor del peso ingresado por el usuario
    - telefono: es la variable que contiene el valor del telefono ingresado por el usuario
    - correo: es la variable que contiene el valor del correo ingresado por el usuario
    Salidas:
    - sin salidas, se crean los botones en la ventana de insertar donante y se les asigna la funcionalidad correspondiente a cada uno
    """
    Button(frameBotones,text="Registrar",font=("Arial",12,"bold"),
        bg="#4773C3",fg="white",
        command=lambda: registrar(mensajeRegistrar,donantes,cedula,nombre,fechaNacimiento,
            tipoSangre,sexo,peso,telefono,correo,mensaje,lugaresDonacion)
    ).grid(row=0,column=0,padx=10)
    Button(frameBotones,text="Limpiar",
        font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda: limpiar(cedula,nombre,fechaNacimiento,
        tipoSangre,sexo,peso,telefono,correo)
        ).grid(row=0,column=1,padx=10)
    Button(frameBotones,text="Regresar",font=("Arial",12,"bold"),
        bg="#43C345",fg="white",
        command=lambda: salirInser(ventana,ventanaInsertar)
    ).grid(row=0,column=2,padx = 10)

def crearEntradas(frameInsertar):
    """
    Funcionamiento: Esta funcion se encarga de crear las entradas de la ventana de insertar donante, ademas de retornar las variables que contienen los valores ingresados por el usuario en cada una de las entradas
    Entradas:
    - frameInsertar: es la variable que contiene el frame donde se desean crear las entradas
    Salidas:
    - nombre: es la variable que contiene el valor del nombre ingresado por el usuario
    - fechaNacimiento: es la variable que contiene el valor de la fecha de nacimiento ingresada por el usuario
    - tipoSangre: es la variable que contiene el valor del tipo de sangre ingresado por el usuario
    - sexo: es la variable que contiene el valor del sexo ingresado por el usuario
    - peso: es la variable que contiene el valor del peso ingresado por el usuario
    - telefono: es la variable que contiene el valor del telefono ingresado por el usuario
    - correo: es la variable que contiene el valor del correo ingresado por el usuario
    """
    nombre=nombreInser(frameInsertar)
    fechaNacimiento=fechaNacimientoInser(frameInsertar)
    tipoSangre=tipoSangreInser(frameInsertar)
    sexo=sexoInser(frameInsertar)
    peso=pesoInser(frameInsertar)
    telefono=telefonoInser(frameInsertar)
    correo=correoInser(frameInsertar)
    return(nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo)

#===========funciones usadas principalmente para actualizar donadores==========

def buscarDonante(donantes, cedulaBuscar):
    """
    Funcionamiento: Esta funcion se encarga de buscar un donante en la lista de donantes a partir de la cedula ingresada por el usuario en la ventana de buscar donante para actualizar, ademas de retornar un mensaje con el resultado de la busqueda
    Entradas:
    - donantes: es la variable que contiene la lista de donantes
    - cedulaBuscar: es la variable que contiene el valor de la cedula ingresada
    Salidas:
    - (True, donante, i): si el donante fue encontrado, donante es la variable que contiene los datos del donante encontrado y i es la variable que contiene la posicion del donante en la lista de donantes
    - (False, mensaje, -1): si el donante no fue encontrado, mensaje es un mensaje que indica que no se encontro el donante y -1 es la variable que indica que no se encontro el donante
    """
    for i, donante in enumerate(donantes):
        if donante[1] == cedulaBuscar:
            return (True, donante, i) 
    return (False, "No se encontro el donante", -1)

def limpiarActualizacion(nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo,mensajeActualizar):
    """
    Funcionamiento: Esta funcion se encarga de limpiar las entradas de la ventana de actualizar donante, ademas de limpiar el mensaje donde se muestra el resultado de la actualizacion
    Entradas:
    - nombre: es la variable que contiene el valor del nombre ingresado por el usuario
    - fechaNacimiento: es la variable que contiene el valor de la fecha de nacimiento ingresada por el usuario
    - tipoSangre: es la variable que contiene el valor del tipo de sangre ingresado por el usuario
    - sexo: es la variable que contiene el valor del sexo ingresado por el usuario
    - peso: es la variable que contiene el valor del peso ingresado por el usuario
    - telefono: es la variable que contiene el valor del telefono ingresado por el usuario
    - correo: es la variable que contiene el valor del correo ingresado por el usuario
    - mensajeActualizar: es la variable que contiene el mensaje donde se mostrara el resultado de la actualizacion
    Salidas:
    - limpiar las entradas de la ventana de actualizar donante y limpiar el mensaje donde se muestra el resultado de la actualizacion
    """
    nombre.set("")
    fechaNacimiento.set("")
    tipoSangre.set("")
    sexo.set(True)
    peso.set("")
    telefono.set("")
    correo.set("")
    mensajeActualizar.config(text="")

def guardarActualizacion(donantes, posicion, cedula, nombre, fechaNacimiento, tipoSangre, sexo, peso, telefono, correo, mensajeActualizar, mensaje,lugaresDonacion):
    """
    Funcionamiento: Esta funcion se encarga de guardar la actualizacion del donante a partir de los datos ingresados por el usuario en la ventana de actualizar donante, ademas de validar los datos ingresados y mostrar un mensaje con el resultado de la actualizacion
    Entradas:
    - donantes: es la variable que contiene la lista de donantes
    - posicion: es la variable que contiene la posicion del donante en la lista de donantes
    - cedula: es la variable que contiene el valor de la cedula ingresada por el usuario
    - nombre: es la variable que contiene el valor del nombre ingresado por el usuario
    - fechaNacimiento: es la variable que contiene el valor de la fecha de nacimiento ingresada por el usuario
    - tipoSangre: es la variable que contiene el valor del tipo de sangre ingresado por el usuario
    - sexo: es la variable que contiene el valor del sexo ingresado por el usuario
    - peso: es la variable que contiene el valor del peso ingresado por el usuario
    - telefono: es la variable que contiene el valor del telefono ingresado por el usuario
    - correo: es la variable que contiene el valor del correo ingresado por el usuario
    - mensajeActualizar: es la variable que contiene el mensaje donde se mostrara el resultado de la actualizacion
    - mensaje: es la variable que contiene el mensaje donde se mostrara el analisis del donante actualizado
    Salidas:
    - guarda la actualizacion del donante en la lista de donantes y muestra un mensaje con el resultado de la actualizacion, si la actualizacion fue exitosa se muestra un mensaje con el analisis del donante actualizado, si la actualizacion no fue exitosa se muestra un mensaje con el error encontrado
    """
    resultado = validarDatos([], cedula, nombre.get(), fechaNacimiento.get(), tipoSangre.get(), sexo.get(), peso.get(), telefono.get(), correo.get())
    if resultado[0] == False:
        mensajeActualizar.config(text=resultado[1], fg="red")
        return
    donantes[posicion] = [
        normalizarNombre(nombre.get())[1],
        cedula,
        fechaNacimiento.get(),
        tipoSangre.get(),
        sexo.get(),
        peso.get(),
        telefono.get(),
        correo.get(),1,0]
    mensajeActualizar.config(text="Donante actualizado correctamente", fg="green")
    mensaje.config(text=generarAnalisisDonante(cedula, fechaNacimiento.get(), tipoSangre.get(), peso.get(), lugaresDonacion), font=("calibri", 11, "bold"))
    mensaje.pack()

def cargarDatosActualizar(donantes, posicion, nombre, fechaNacimiento, tipoSangre, sexo, peso, telefono, correo):
    """
    Funcionamiento: Esta funcion se encarga de cargar los datos del donante encontrado en la ventana de actualizar donante, ademas de mostrar los datos del donante en las entradas correspondientes para que el usuario pueda editarlos
    Entradas:
    - donantes: es la variable que contiene la lista de donantes
    - posicion: es la variable que contiene la posicion del donante en la lista de donantes
    - nombre: es la variable que contiene el valor del nombre ingresado por el usuario
    - fechaNacimiento: es la variable que contiene el valor de la fecha de nacimiento ingresada por el usuario
    - tipoSangre: es la variable que contiene el valor del tipo de sangre ingresado por el usuario
    - sexo: es la variable que contiene el valor del sexo ingresado por el usuario
    - peso: es la variable que contiene el valor del peso ingresado por el usuario
    - telefono: es la variable que contiene el valor del telefono ingresado por el usuario
    - correo: es la variable que contiene el valor del correo ingresado por el usuario
    Salidas:
    - carga los datos del donante encontrado en las entradas correspondientes de la ventana de actualizar donante para que el usuario pueda editarlos
    """
    donante = donantes[posicion] 
    nombre.set(donante[0])
    fechaNacimiento.set(donante[2]) 
    tipoSangre.set(donante[3])
    sexo.set(donante[4])
    peso.set(donante[5])
    telefono.set(donante[6])
    correo.set(donante[7])

def abrirVentanaActualizar(ventana, ventanaBuscarActualizar, donantes, posicion, cedula, lugaresDonacion):
    """
    Funcionamiento: Esta funcion se encarga de abrir la ventana de actualizar donante a partir del donante encontrado en la ventana de buscar donante para actualizar, ademas de cerrar la ventana de buscar donante para actualizar y mostrar la ventana de actualizar donante
    Entradas:
    - ventana: es la variable que contiene la ventana principal
    - ventanaBuscarActualizar: es la variable que contiene la ventana de buscar donante para actualizar
    - donantes: es la variable que contiene la lista de donantes
    - posicion: es la variable que contiene la posicion del donante en la lista de donantes
    - cedula: es la variable que contiene el valor de la cedula ingresada por el usuario
    - lugaresDonacion: es la variable que contiene la lista de lugares de donacion disponibles
    Salidas:
    - ventanaBuscarActualizar: se cierra la ventana de buscar donante para actualizar
    - ventanaActualizar: se muestra la ventana de actualizar donante con los datos del donante encontrado cargados en las entradas correspondientes para que el usuario pueda editarlos
    """
    ventanaBuscarActualizar.destroy()
    ventanaActualizar = Toplevel()
    ventanaActualizar.title("Actualizar donador")
    ubicarVentana(ventanaActualizar, 900, 900)
    ventanaActualizar.config(bg="#FFFFFF")
    frameInsertar = Frame(ventanaActualizar, bg="#BB4242", bd=5)
    frameInsertar.pack(pady=20)
    nombre, fechaNacimiento, tipoSangre, sexo, peso, telefono, correo = crearEntradas(frameInsertar)
    cargarDatosActualizar(donantes, posicion, nombre, fechaNacimiento, tipoSangre, sexo, peso, telefono, correo)
    mensajeActualizar = Label(ventanaActualizar, text="", font=("Arial", 12, "bold"), bg="white", fg="red")
    mensajeActualizar.pack(pady=10)
    frameBotones = Frame(ventanaActualizar, bg="#FFFFFF", bd=5)
    frameBotones.pack(pady=20)
    mensaje = Label(ventanaActualizar, text="", font=("Arial", 12, "bold"), bg="white", fg="red")
    mensaje.pack(pady=10)
    Button(frameBotones, text="Actualizar", font=("Arial", 12, "bold"), bg="#4773C3", fg="white",
        command=lambda: guardarActualizacion(donantes, posicion, cedula, nombre, fechaNacimiento, tipoSangre, sexo, peso, telefono, correo, mensajeActualizar, mensaje,lugaresDonacion)).grid(row=0, column=0, padx=10)
    Button(frameBotones, text="Limpiar", font=("Arial", 12, "bold"), bg="#4773C3", fg="white",
        command=lambda: limpiarActualizacion(nombre, fechaNacimiento, tipoSangre, sexo, peso, telefono, correo, mensajeActualizar)).grid(row=0, column=1, padx=10)
    Button(frameBotones, text="Regresar", font=("Arial", 12, "bold"), bg="#43C345", fg="white",
        command=lambda: [ventanaActualizar.destroy(), ventana.deiconify()]).grid(row=0, column=2, padx=10)

def buscarDonanteActualizar(ventana, ventanaBuscarActualizar, donantes, cedulaBuscar, mensaje, lugaresDonacion):
    """
    Funcionamiento: Esta funcion se encarga de buscar un donante en la lista de donantes a partir de la cedula ingresada por el usuario en la ventana de buscar donante para actualizar, ademas de mostrar un mensaje con el resultado de la busqueda y abrir la ventana de actualizar donante si el donante fue encontrado
    Entradas:
    - ventana: es la variable que contiene la ventana principal
    - ventanaBuscarActualizar: es la variable que contiene la ventana de buscar donante para actualizar
    - donantes: es la variable que contiene la lista de donantes
    - cedulaBuscar: es la variable que contiene el valor de la cedula ingresada por el usuario
    - mensaje: es la variable que contiene el mensaje donde se mostrara el resultado de la busqueda
    - lugaresDonacion: es la variable que contiene la lista de lugares de donacion disponibles
    Salidas:
    - mensaje: es un mensaje que indica el resultado de la busqueda, si el donante fue encontrado se muestra un mensaje indicando que el donante fue encontrado correctamente, si el donante no fue encontrado se muestra un mensaje indicando que no se encontro el donante
    - ventanaActualizar: se muestra la ventana de actualizar donante con los datos del donante encontrado cargados en las entradas correspondientes para que el usuario pueda editarlos, si el donante fue encontrado correctamente
    """
    resultado = buscarDonante(donantes, cedulaBuscar.get())
    if resultado[0] == False:
        mensaje.config(text=resultado[1], fg="red")
        return
    mensaje.config(text="Donante encontrado correctamente", fg="green")
    abrirVentanaActualizar(ventana, ventanaBuscarActualizar, donantes, resultado[2], cedulaBuscar.get(), lugaresDonacion)

#==============Generar Donadores==============

def generarNombreSexo():
    """
    Funcionamiento: Esta funcion se encarga de generar un nombre completo y un sexo aleatorio para un donante, utilizando la libreria Faker para generar los nombres y apellidos, ademas de retornar el nombre completo y el sexo generado
    Salidas:
    - nombreCompleto: es la variable que contiene el nombre completo generado para el donante
    - sexo: es la variable que contiene el sexo generado para el donante, True para masculino y False para femenino
    """
    sexo=random.choice([True,False])
    if sexo==True:
        nombre=fake.first_name_male()
    else:
        nombre=fake.first_name_female()
    apellido1=fake.last_name()
    apellido2=fake.last_name()
    nombreCompleto = nombre+" "+apellido1+" "+apellido2 
    return nombreCompleto,sexo

def generarCedula():
    """
    Funcionamiento: Esta funcion se encarga de generar una cedula aleatoria para un donante, utilizando la libreria random para generar los numeros de la cedula, ademas de retornar la cedula generada
    Salidas:
    - cedula: es la variable que contiene la cedula generada para el donante, con el formato "provincia-parte2-parte3"
    """
    provincia=random.randint(1,7)
    parte2=random.randint(1000,9999)
    parte3=random.randint(1000,9999)
    cedula=f"{provincia}-{parte2}-{parte3}"
    return cedula

def generarFecha():
    """
    Funcionamiento: Esta funcion se encarga de generar una fecha de nacimiento aleatoria para un donante, utilizando la libreria random para generar el año, mes y dia de la fecha, ademas de retornar la fecha generada con el formato "dd/mm/aaaa"
    Salidas:
    - fecha: es la variable que contiene la fecha de nacimiento generada para el donante, con el formato "dd/mm/aaaa"
    """
    anno=random.randint(1961,2008)
    mes=random.randint(1,12)
    if mes in [1,3,5,7,8,10,12]:
        maxDias=31
    elif mes in [4,6,9,11]:
        maxDias=30
    else:
        if anno%4==0 and mes == 2:
            maxDias=29
        else:
            maxDias=28
    dia=random.randint(1,maxDias)
    fecha=f"{dia:02d}/{mes:02d}/{anno}"
    return fecha

def generarTipoSangre():
    """
    Fucionamiento: Esta funcion se encarga de generar un tipo de sangre aleatorio para un donante, utilizando la libreria random para seleccionar un tipo de sangre de una lista predefinida, ademas de retornar el tipo de sangre generado
    Salidas:
    - sangre: es la variable que contiene el tipo de sangre generado para el donante, seleccionada aleatoriamente de una lista predefinida de tipos de sangre
    """
    sangre = random.choice(["O+","O-","A+","A-","B+","B-","AB+","AB-"])
    return sangre

def generarPeso():
    """
    Funcionamiento: Esta funcion se encarga de generar un peso aleatorio para un donante, utilizando la libreria random para generar un numero entero entre 30 y 300, ademas de retornar el peso generado
    Salidas:
    - peso: es la variable que contiene el peso generado para el donante, con un valor entero entre 30 y 300
    """
    peso = random.randint(50,120)
    return peso

def generarTelefono():
    """
    Fuionamiento: Esta funcion se encarga de generar un numero de telefono aleatorio para un donante, utilizando la libreria random para generar los numeros del telefono, ademas de retornar el numero de telefono generado con el formato "inicio-parte1-parte2"
    Salidas:
    - telefono: es la variable que contiene el numero de telefono generado para el donante, con el formato "inicio-parte1-parte2", donde inicio es un numero entre 2 y 9, parte1 es un numero entre 100 y 999, y parte2 es un numero entre 1000 y 9999
    """
    inicio=random.choice([2,4,6,7,8,9])
    parte1=random.randint(100,999)
    parte2=random.randint(1000,9999)
    telefono=f"{inicio}{parte1}-{parte2}"
    return telefono

def generarCorreo(nombreCompleto):
    """
    Funcionamiento: Esta funcion se encarga de generar un correo electronico aleatorio para un donante, utilizando la libreria random para seleccionar un dominio de correo de una lista predefinida y generar un numero aleatorio para agregar al correo, ademas de retornar el correo generado con el formato "nombreCompletoNumero@dominio"
    Entradas:
    - nombreCompleto: es la variable que contiene el nombre completo del donante, que se utilizara para generar el correo electronico
    Salidas:
    - correo: es la variable que contiene el correo electronico generado para el donante, con el formato "nombreCompletoNumero@dominio", donde nombreCompleto es el nombre completo del donante sin espacios y en minusculas, numero es un numero aleatorio entre 1 y 999, y dominio es un dominio de correo seleccionado aleatoriamente de una lista predefinida de dominios de correo
    """
    dominios=["gmail.com","racsa.go.cr","costarricense.cr","ccss.sa.cr"]
    numero=random.randint(1,999)
    dominio=random.choice(dominios)
    nombreCompleto = nombreCompleto.replace(" ","")
    nombreCompleto = nombreCompleto.replace('á','a').replace('é',
        'e').replace('í','i').replace('ó','o').replace('ú','u').replace('Á',
        'A').replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U')
    correo=nombreCompleto.lower()+str(numero)+"@"+dominio
    return correo

def crearDonadores(mensaje,donantes,cantidad):
    """
    Funcionamiento: Esta funcion se encarga de crear una cantidad especificada de donantes, utilizando las funciones auxiliares para generar sus datos
    Entradas:
    - mensaje: es la variable que contiene el mensaje donde se mostrara el resultado de la creacion de los donantes
    - donantes: es la variable que contiene la lista de donantes, donde se agregaran los donantes generados
    - cantidad: es la variable que contiene el valor de la cantidad de donantes que se desea generar, ingresada por el usuario
    Salidas:
    - mensaje: es un mensaje que indica el resultado de la creacion de los donantes, si la cantidad ingresada es valida se muestra un mensaje indicando que los donantes fueron generados correctamente, si la cantidad ingresada no es valida se muestra un mensaje indicando el error encontrado
    - donantes: se agregan a la lista de donantes los donantes generados
    """
    if cantidad.isdigit() == True:
        cantidad=int(cantidad)
        contador = 0
        if cantidad<=0:
            mensaje.config(text="Debe ingresar un numero mayor a cero",fg="red")
            mensaje.pack()
        else:
            while contador < cantidad:
                nombre,sexo=generarNombreSexo()
                donantes.append([nombre,generarCedula(),generarFecha(),generarTipoSangre(),sexo,generarPeso(),
                    generarTelefono(),generarCorreo(nombre),1,0])
                contador+=1
            guardarDatos(donantes)
            mensaje.config(text="Donadores generados correctamente",fg="green")
            mensaje.pack()
    else:
        mensaje.config(text="Unicamente debe ingresar numeros enteros",fg="red")
        mensaje.pack()

#==================Eliminar donadores=======================
def confirmarInactivacionEspecifica(donantes, posicion, ventanaJustificar, comboRazon, mensajeOriginal):
    """
    Funcionamiento: Esta funcion se encarga de confirmar la inactivacion de un donante a partir de la seleccion del motivo de inactivacion realizada por el usuario en la ventana de justificacion de inactivacion, ademas de actualizar el estado del donante a inhabilitado y guardar el codigo de justificacion en la lista de donantes, cerrar la ventana de justificacion de inactivacion y mostrar un mensaje con el resultado de la inactivacion
    Entradas:
    - donantes: es la variable que contiene la lista de donantes
    - posicion: es la variable que contiene la posicion del donante en la lista de donantes
    - ventanaJustificar: es la variable que contiene la ventana de justificacion de inactivacion, que se cerrara despues de confirmar la inactivacion
    - comboRazon: es la variable que contiene el combobox donde el usuario selecciona el motivo de inactivacion, que se utilizara para obtener el codigo de justificacion seleccionado por el usuario
    - mensajeOriginal: es la variable que contiene el mensaje donde se mostrara el resultado de la inactivacion, que se actualizara despues de confirmar la inactivacion
    Salidas:
    - donantes: se actualiza el estado del donante a inhabilitado y se guarda el codigo de justificacion en la lista de donantes
    - ventanaJustificar: se cierra la ventana de justificacion de inactivacion
    - mensajeOriginal: se muestra un mensaje indicando que el donante fue inhabilitado satisfactoriamente, con el estado actualizado a 0, si la inactivacion fue confirmada correctamente, si no se selecciono un motivo de inactivacion valido se muestra un mensaje indicando que se debe seleccionar un motivo valido para confirmar la inactivacion
    - comboRazon: se obtiene el codigo de justificacion seleccionado por el usuario en el combobox para guardar en la lista de donantes, si no se selecciono un motivo de inactivacion valido se muestra un mensaje indicando que se debe seleccionar un motivo valido para confirmar la inactivacion
    """
    seleccion = comboRazon.get()
    if not seleccion:
        Label(ventanaJustificar, text="¡Debe seleccionar un motivo válido!", fg="red", bg="white").pack()
        return
    codigoJustificacion = int(seleccion[0])
    donantes[posicion][-2] = 0 
    donantes[posicion][-1] = codigoJustificacion 
    ventanaJustificar.destroy()
    mensajeOriginal.config(text="Donador inhabilitado satisfactoriamente (Estado: 0)", fg="green")

def eliminarDonanteAux(donantes, cedulaBuscar, mensaje):
    """
    Funcionamiento: Esta funcion se encarga de eliminar un donante a partir de la cedula ingresada por el usuario en la ventana de eliminar donante, ademas de mostrar un mensaje con el resultado de la eliminacion
    Entradas:
    - donantes: es la variable que contiene la lista de donantes
    - cedulaBuscar: es la variable que contiene el valor de la cedula ingresada
    - mensaje: es la variable que contiene el mensaje donde se mostrara el resultado de la eliminacion
    Salidas:
    - mensaje: es un mensaje que indica el resultado de la eliminacion, si el donante fue encontrado y se inhabilito correctamente se muestra un mensaje indicando que el donante fue inhabilitado satisfactoriamente, si el donante no fue encontrado se muestra un mensaje indicando que no se encontro el donante, si el donante ya se encuentra inhabilitado se muestra un mensaje indicando que el donante ya se encuentra inhabilitado
    - ventanaJustificar: se muestra la ventana de justificacion de inactivacion para que el usuario seleccione el motivo de inactivacion, si el donante fue encontrado y se encuentra habilitado, si el donante no fue encontrado o ya se encuentra inhabilitado no se muestra la ventana de justificacion de inactivacion
    """
    resultadoCedula = cedulaInserAux(cedulaBuscar.get())
    if resultadoCedula[0] == False:
        mensaje.config(text=resultadoCedula[1], fg="red")
        return
    resultado = buscarDonante(donantes, cedulaBuscar.get())
    if resultado[0] == False:
        mensaje.config(text=resultado[1], fg="red")
        return
    posicion = resultado[2]
    if donantes[posicion][-2] == 0:
        mensaje.config(text="Este donante ya se encuentra inhabilitado", fg="orange")
        return
    ventanaJustificar = Toplevel()
    ventanaJustificar.title("Causa de Inhabilitación")
    ventanaJustificar.geometry("550x300")
    ventanaJustificar.config(bg="white")
    ventanaJustificar.resizable(False, False)
    Label(ventanaJustificar, text=f"Seleccione el motivo de rechazo para:\n{donantes[posicion][0]}", 
          font=("Arial", 11, "bold"), bg="white", fg="#0D1764").pack(pady=15)
    causasRechazo = [
        "1. Enfermedades Infecciosas/Crónicas (VIH, Hepatitis, Diabetes...)",
        "2. Conductas de Riesgo (Nuevas parejas, etc.)",
        "3. Factores de Salud Física (Hemoglobina, presión, fiebre...)",
        "4. Procedimientos Médicos (Transfusiones, tatuajes recientes...)",
        "5. Uso de Medicamentos (Fármacos sin receta...)",
        "6. Estilo de Vida y Viajes (Drogas, alcohol, zonas endémicas...)",
        "7. Situaciones Específicas (Embarazo, lactancia, menstruación)",
        "0. sin justificacion"]
    comboRazon = ttk.Combobox(ventanaJustificar, values=causasRechazo, width=55, state="readonly")
    comboRazon.pack(pady=15)
    comboRazon.current(0)
    Button(ventanaJustificar, text="Confirmar Inactivación (0)", font=("Arial", 11, "bold"), bg="#C62828", fg="white",
           command=lambda: (confirmarInactivacionEspecifica(donantes, posicion, ventanaJustificar, comboRazon, mensaje), ventanaJustificar.destroy())).pack(pady=20)

#===============Funciones para Insertar lugar de donacion====================

def insertarLugar(frame, lugares, datos, provincia):
    formulario = Frame(frame, bg="#cfcfcf")
    formulario.pack(pady=10)
    texto_lugares = f"Lugares en {provincia}:\n"
    for i in datos:
        texto_lugares += i + "\n"
    mensaje = Label(formulario, text=texto_lugares, font=("Arial", 11, "bold"), bg="white", fg="#0D1764")
    mensaje.pack()
    Label(formulario, text="Ingrese el nuevo Lugar", font=("Arial", 11, "bold"), bg="white", fg="#0D1764").pack(pady=15)
    entradaLugar = Text(formulario, height=4, width=35, font=("Arial", 10))
    entradaLugar.pack(pady=15)
    frameBotones = Frame(formulario, bg="#ffffff")
    frameBotones.pack()
    Button(frameBotones, text="Agregar Lugar", font=("Arial", 11, "bold"), bg="#C62828", fg="white", 
           command=lambda: [
               lugares[provincia].append(entradaLugar.get("1.0", "end-1c")), 
               formulario.destroy(), 
               insertarLugar(frame, lugares, lugares[provincia], provincia)
           ]).grid(row=0, column=0, padx=10)
    Button(frameBotones, text="Cancelar", font=("Arial", 11, "bold"), bg="#C62828", fg="white", command=lambda: formulario.destroy()).grid(row=0, column=1, padx=10)

def nuevoLugarDonacion(frame, lugares, provincia):
    for clave, datos in lugares.items():
        if provincia == clave:
            insertarLugar(frame, lugares, datos, provincia)
        

#==================Funciones para reportes=======================

def generarHTMLReportes(filasHTML,mensaje):
    """
    Funcionamiento: Esta funcion se encarga de generar un reporte en formato HTML a partir de las filas HTML generadas para cada donante, ademas de mostrar un mensaje con el resultado de la generacion del reporte
    Entradas:
    - filasHTML: es la variable que contiene la lista de filas HTML generadas para cada donante, que se utilizara para construir el contenido del reporte en formato HTML
    - mensaje: es la variable que contiene el mensaje donde se mostrara el resultado de la generacion del reporte, que se actualizara despues de generar el reporte
    Salidas:
    - mensaje: es un mensaje que indica el resultado de la generacion del reporte, si el reporte fue generado correctamente se muestra un mensaje indicando que el reporte fue generado correctamente, si hubo un error al generar el reporte se muestra un mensaje indicando que hubo un error al generar el reporte
    - reporte HTML: se genera un archivo HTML con el contenido del reporte construido a partir de las filas HTML generadas para cada donante, si el reporte fue generado correctamente, si hubo un error al generar el reporte no se genera el archivo HTML
    """
    inicio=datetime.now()
    ahora=datetime.now()
    nombreArchivo="reporteDonant"+ahora.strftime("%d-%m-%H-%M-%S")+".html"
    try:
        with open(nombreArchivo,"w",encoding="utf-8") as archivo:
            archivo.write("<!DOCTYPE html>\n")
            archivo.write("<html lang='es'>\n")
            archivo.write("<head>\n")
            archivo.write("<meta charset='UTF-8'>\n")
            archivo.write("<title>Reporte Donantes</title>\n")
            archivo.write("</head>\n")
            archivo.write("<body style='font-family: Arial, sans-serif;'>\n")
            archivo.write("<h1>Reporte de Donantes</h1>\n")
            archivo.write(f"<h2>Generado el {ahora.strftime('%d/%m/%y %H:%M:%S')}</h2>\n")
            final=datetime.now()
            duracion=final-inicio
            archivo.write(f"<p><strong>Duración total:</strong> {duracion}</p>\n")
            archivo.write(f"<p><strong>Cantidad total de donantes:</strong> {len(filasHTML)}</p>\n")
            archivo.write("<table border='1' style='border-collapse:collapse; text-align:center; width:100%;'>\n")
            archivo.write("<tr style='background-color:#cccccc;'>\n")
            archivo.write("<th>Cedula</th>\n")
            archivo.write("<th>Nombre</th>\n")
            archivo.write("<th>Fecha nacimiento</th>\n")
            archivo.write("<th>Tipo sangre</th>\n")
            archivo.write("<th>Sexo</th>\n")
            archivo.write("<th>Peso</th>\n")
            archivo.write("<th>Telefono</th>\n")
            archivo.write("<th>Correo</th>\n")
            archivo.write("<th>justificacion</th>\n")
            archivo.write("</tr>\n")
            for filas in filasHTML:
                archivo.write(filas)
            archivo.write("</table>\n")
            archivo.write("</body>\n")
            archivo.write("</html>\n")
        mensaje.config(text="Reporte generado correctamente",fg="green")
    except:
        print("ERROR")

def crearFilaHTML(cedula,datos,color):
    """
    Funcionamiento: Esta funcion se encarga de crear una fila en formato HTML para un donante a partir de sus datos, ademas de retornar la fila HTML generada
    Entradas:
    - cedula: es la variable que contiene el valor de la cedula del donante, que se utilizara para mostrar en la fila HTML
    - datos: es la variable que contiene la lista de datos del donante, que se utilizara para mostrar en la fila HTML
    - color: es la variable que contiene el valor del color de fondo que se utilizara para la fila HTML, que se asignara de forma alternada para cada fila para mejorar la legibilidad del reporte
     Salidas:
    - fila: es la variable que contiene la fila en formato HTML generada para el donante, que incluye las celdas con los datos del donante y el color de fondo asignado, que se utilizara para construir el contenido del reporte en formato HTML
    """
    if datos[4] == True:
        sexo = "Masculino"
    else:
        sexo = "Femenino"
    fila=f"""
    <tr style="background-color:{color};">
        <td>{html.escape(str(cedula))}</td>
        <td>{html.escape(str(datos[0]))}</td>
        <td>{html.escape(str(datos[2]))}</td>
        <td>{html.escape(str(datos[3]))}</td>
        <td>{sexo}</td>
        <td>{html.escape(str(datos[5]))}</td>
        <td>{html.escape(str(datos[6]))}</td>
        <td>{html.escape(str(datos[7]))}</td>
        <td>{html.escape(str(datos[9]))}</td>
    </tr>
    """
    return fila

def crearFilasProvincia(numeroProvincia, donantes):
    """
    Funcionamiento: Esta funcion se encarga de crear una lista de filas en formato HTML para los donantes que pertenecen a una provincia especifica, a partir de sus datos, ademas de retornar la lista de filas HTML generadas
    Entradas:
    - numeroProvincia: es la variable que contiene el valor del numero de la provincia seleccionada
    - donantes: es la variable que contiene la lista de donantes, que se utilizara para filtrar los donantes que pertenecen a la provincia seleccionada y generar las filas HTML correspondientes para cada uno de ellos
    Salidas:
    - filas: es la variable que contiene la lista de filas en formato HTML generadas para los donantes que pertenecen a la provincia seleccionada, que se utilizara para construir el contenido del reporte en formato HTML, si no se encontraron donantes para la provincia seleccionada se retorna una lista vacia
    """
    filas = []
    i = 0
    for datos in donantes:
        cedula = datos[1]
        provincia = int(cedula.split("-")[0])
        if provincia == numeroProvincia:
            if i % 2 == 0:
                color = "#85a9cc"
            else:
                color = "#9C8FE6"
            filas.append(crearFilaHTML(cedula, datos, color))
            i += 1
    return filas

def reportePorProvincia(ventanaReporte,donantes):
    """
    Funcionamiento: Esta funcion se encarga de mostrar una ventana para que el usuario seleccione la provincia de la que desea generar un reporte, ademas de generar el reporte en formato HTML para los donantes que pertenecen a la provincia seleccionada y mostrar un mensaje con el resultado de la generacion del reporte
    Entradas:
    - ventanaReporte: es la variable que contiene la ventana principal de reportes, que se ocultara para mostrar la ventana de seleccion de provincia y se mostrara nuevamente despues de cerrar la ventana de seleccion de provincia
    - donantes: es la variable que contiene la lista de donantes, que se utilizara para filtrar los donantes que pertenecen a la provincia seleccionada y generar el reporte en formato HTML correspondiente para cada uno de ellos
     Salidas:
    - ventanaReporte: se oculta la ventana principal de reportes para mostrar la ventana de seleccion de provincia, y se muestra nuevamente despues de cerrar la ventana de seleccion de provincia
    - mensaje: es un mensaje que indica el resultado de la generacion del reporte, si el reporte fue generado correctamente se muestra un mensaje indicando que el reporte fue generado correctamente, si hubo un error al generar el reporte se muestra un mensaje indicando que hubo un error al generar el reporte
    - reporte HTML: se genera un archivo HTML con el contenido del reporte construido a partir de las filas HTML generadas para los donantes que pertenecen a la provincia seleccionada, si el reporte fue generado correctamente, si hubo un error al generar el reporte no se genera el archivo HTML
    """
    ventanaReporte.withdraw()
    ventanaReporteProvincia = Toplevel()
    ventanaReporteProvincia.title("Reporte por provincia")
    ubicarVentana(ventanaReporteProvincia,500,350)
    ventanaReporteProvincia.config(bg="#ffffff")
    frameProvincia = Frame(ventanaReporteProvincia,bg="#ffffff")
    frameProvincia.pack(pady=20)
    Label(frameProvincia,text="Escoja la provincia de la que quiere generar el reporte").pack(pady=20)
    provincias={"San Jose":1,"Alajuela":2,"Cartago":3,"Heredia":4,
        "Guanacaste":5,"Puntarenas":6,"Limon":7}
    opcion = ttk.Combobox(frameProvincia,values=list(provincias.keys()))
    opcion.pack()
    mensaje = Label(frameProvincia,text="")
    mensaje.pack()
    frameBotones = Frame(ventanaReporteProvincia,bg="#ffffff")
    frameBotones.pack()
    Button(frameBotones,text="Generar reporte",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda:generarHTMLReportes(crearFilasProvincia(provincias[opcion.get()],donantes),mensaje)).grid(row=0,column=0,padx=5)
    Button(frameBotones,text="Salir",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda:[ventanaReporteProvincia.destroy(),ventanaReporte.deiconify()]).grid(row=0,column=1,padx=5)

def crearFilasEdad(edadInicial, edadFinal, donantes):
    """
    Funcionamiento: Esta funcion se encarga de crear una lista de filas en formato HTML para los donantes que se encuentran dentro de un rango de edad especifico, a partir de sus datos, ademas de retornar la lista de filas HTML generadas
    Entradas:
    - edadInicial: es la variable que contiene el valor de la edad inicial del rango de edad seleccionado por el usuario, que se utilizara para filtrar los donantes que se encuentran dentro del rango de edad seleccionado y generar las filas HTML correspondientes para cada uno de ellos
    - edadFinal: es la variable que contiene el valor de la edad final del rango de edad seleccionado por el usuario, que se utilizara para filtrar los donantes que se encuentran dentro del rango de edad seleccionado y generar las filas HTML correspondientes para cada uno de ellos
    - donantes: es la variable que contiene la lista de donantes, que se utilizara para filtrar los donantes que se encuentran dentro del rango de edad seleccionado y generar las filas HTML correspondientes para cada uno de ellos
    Salidas:
    - filas: es la variable que contiene la lista de filas en formato HTML generadas para los donantes que se encuentran dentro del rango de edad seleccionado, que se utilizara para construir el contenido del reporte en formato HTML, si no se encontraron donantes para el rango de edad seleccionado se retorna una lista vacia
    """
    filas = []
    i = 0
    fechaActual = datetime.now()
    for datos in donantes:
        cedula = datos[1]
        fechaNacimiento = datetime.strptime(datos[2], "%d/%m/%Y") 
        edad = fechaActual.year - fechaNacimiento.year
        if (fechaActual.month, fechaActual.day) < (fechaNacimiento.month, fechaNacimiento.day):
            edad -= 1
        if edad >= edadInicial and edad <= edadFinal:
            if i % 2 == 0:
                color = "#85a9cc"
            else:
                color = "#9C8FE6"
            filas.append(crearFilaHTML(cedula, datos, color))
            i += 1
    return filas

def reportePorEdad(ventanaReporte,donantes):
    """
    Funcionamiento: Esta funcion se encarga de mostrar una ventana para que el usuario ingrese el rango de edad del que desea generar un reporte, ademas de generar el reporte en formato HTML para los donantes que se encuentran dentro del rango de edad ingresado y mostrar un mensaje con el resultado de la generacion del reporte
    Entradas:
    - ventanaReporte: es la variable que contiene la ventana principal de reportes, que se ocultara para mostrar la ventana de ingreso de rango de edad y se mostrara nuevamente despues de cerrar la ventana de ingreso de rango de edad
    - donantes: es la variable que contiene la lista de donantes, que se utilizara para filtrar los donantes que se encuentran dentro del rango de edad ingresado y generar el reporte en formato HTML correspondiente para cada uno de ellos
    Salidas:
    - ventanaReporte: se oculta la ventana principal de reportes para mostrar la ventana de ingreso de rango de edad, y se muestra nuevamente despues de cerrar la ventana de ingreso de rango de edad
    - mensaje: es un mensaje que indica el resultado de la generacion del reporte, si el reporte fue generado correctamente se muestra un mensaje indicando que el reporte fue generado correctamente, si hubo un error al generar el reporte se muestra un mensaje indicando que hubo un error al generar el reporte
    - reporte HTML: se genera un archivo HTML con el contenido del reporte construido a partir de las filas HTML generadas para los donantes que se encuentran dentro del rango de edad ingresado, si el reporte fue generado correctamente, si hubo un error al generar el reporte no se genera el archivo HTML
    """
    ventanaReporte.withdraw()
    ventanaReporteEdad=Toplevel()
    ventanaReporteEdad.title("Reporte por edad")
    ubicarVentana(ventanaReporteEdad,500,350)
    ventanaReporteEdad.config(bg="#ffffff")
    frameEdad=Frame(ventanaReporteEdad,bg="#ffffff")
    frameEdad.pack(pady=20)
    Label(frameEdad,text="Ingrese el rango de edad",bg="#ffffff").grid(row=0,column=0,columnspan=2,pady=20)
    Label(frameEdad,text="Edad inicial",bg="#ffffff").grid(row=1,column=0,pady=10)
    edadInicial=StringVar()
    Entry(frameEdad,textvariable=edadInicial).grid(row=1,column=1,pady=10)
    Label(frameEdad,text="Edad final",bg="#ffffff").grid(row=2,column=0,pady=10)
    edadFinal=StringVar()
    Entry(frameEdad,textvariable=edadFinal).grid(row=2,column=1,pady=10)
    mensaje=Label(frameEdad,text="",bg="#ffffff")
    mensaje.grid(row=3,column=0,columnspan=2,pady=10)
    frameBotones=Frame(ventanaReporteEdad,bg="#ffffff")
    frameBotones.pack(pady=20)
    Button(frameBotones,text="Generar reporte",font=("Arial",12,"bold"),
        bg="#4773C3",fg="white",
        command=lambda:generarHTMLReportes(crearFilasEdad(int(edadInicial.get()),int(edadFinal.get()),
                donantes),mensaje)).grid(row=0,column=0,padx=5)
    Button(frameBotones,text="Regresar",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda:generarHTMLReportes(crearFilasEdad(int(edadInicial.get()),int(edadFinal.get()),donantes),mensaje)).grid(row=0,column=0,padx=5)
    Button(frameBotones,text="Generar reporte",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda: generarHTMLReportes(crearFilasEdad(int(edadInicial.get()),int(edadFinal.get()),donantes),mensaje)).grid(row=0,column=0,padx=5)
    Button(frameBotones,text="Salir",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda:[ventanaReporteEdad.destroy(),ventanaReporte.deiconify()]).grid(row=0,column=1,padx=5)

def crearFilasTipoSangreProvincia(tipoSangre, numeroProvincia, donantes):
    """
    Funcionamiento: Esta funcion se encarga de crear una lista de filas en formato HTML para los donantes que tienen un tipo de sangre especifico y pertenecen a una provincia especifica, a partir de sus datos, ademas de retornar la lista de filas HTML generadas
    Entradas:
    - tipoSangre: es la variable que contiene el valor del tipo de sangre seleccionado por el usuario, que se utilizara para filtrar los donantes que tienen el tipo de sangre seleccionado y generar las filas HTML correspondientes para cada uno de ellos
    - numeroProvincia: es la variable que contiene el valor del numero de la provincia seleccionada por el usuario, que se utilizara para filtrar los donantes que pertenecen a la provincia seleccionada y generar las filas HTML correspondientes para cada uno de ellos
    - donantes: es la variable que contiene la lista de donantes, que se utilizara para filtrar los donantes que tienen el tipo de sangre seleccionado y pertenecen a la provincia seleccionada, y generar las filas HTML correspondientes para cada uno de ellos
    Salidas:
    - filas: es la variable que contiene la lista de filas en formato HTML generadas para los donantes que tienen el tipo de sangre seleccionado y pertenecen a la provincia seleccionada, que se utilizara para construir el contenido del reporte en formato HTML, si no se encontraron donantes para el tipo de sangre y provincia seleccionados se retorna una lista vacia
    """
    filas = []
    i = 0
    for datos in donantes:
        cedula = datos[1]
        provincia = int(cedula.split("-")[0])
        if datos[3] == tipoSangre and provincia == numeroProvincia:
            if i % 2 == 0:
                color = "#85a9cc"
            else:
                color = "#9C8FE6"
            filas.append(crearFilaHTML(cedula, datos, color))
            i += 1
    return filas

def reporteTipoSangreProvincia(ventanaReporte,donantes):
    """
    Funcionamiento: Esta funcion se encarga de mostrar una ventana para que el usuario seleccione el tipo de sangre y la provincia de la que desea generar un reporte, ademas de generar el reporte en formato HTML para los donantes que tienen el tipo de sangre seleccionado y pertenecen a la provincia seleccionada, y mostrar un mensaje con el resultado de la generacion del reporte
    Entradas:
    - ventanaReporte: es la variable que contiene la ventana principal de reportes, que se ocultara para mostrar la ventana de seleccion de tipo de sangre y provincia, y se mostrara nuevamente despues de cerrar la ventana de seleccion de tipo de sangre y provincia
    - donantes: es la variable que contiene la lista de donantes, que se utilizara para filtrar los donantes que tienen el tipo de sangre seleccionado y pertenecen a la provincia seleccionada, y generar el reporte en formato HTML correspondiente para cada uno de ellos
    Salidas:
    - ventanaReporte: se oculta la ventana principal de reportes para mostrar la ventana de seleccion de tipo de sangre y provincia, y se muestra nuevamente despues de cerrar la ventana de seleccion de tipo de sangre y provincia
    - mensaje: es un mensaje que indica el resultado de la generacion del reporte, si el reporte fue generado correctamente se muestra un mensaje indicando que el reporte fue generado correctamente, si hubo un error al generar el reporte se muestra un mensaje indicando que hubo un error al generar el reporte
    - reporte HTML: se genera un archivo HTML con el contenido del reporte construido a partir de las filas HTML generadas para los donantes que tienen el tipo de sangre seleccionado y pertenecen a la provincia seleccionada, si el reporte fue generado correctamente, si hubo un error al generar el reporte no se genera el archivo HTML
    """
    ventanaReporte.withdraw()
    ventanaReporteSangre=Toplevel()
    ventanaReporteSangre.title("Reporte tipo sangre provincia")
    ubicarVentana(ventanaReporteSangre,500,350)
    ventanaReporteSangre.config(bg="#ffffff")
    frameReporte=Frame(ventanaReporteSangre,bg="#ffffff")
    frameReporte.pack(pady=20)
    Label(
        frameReporte,
        text="Seleccione el tipo de sangre y provincia",
        bg="#ffffff"
    ).grid(row=0,column=0,columnspan=2,pady=20)
    Label(
        frameReporte,
        text="Tipo sangre",
        bg="#ffffff"
    ).grid(row=1,column=0,pady=10)
    tiposSangre=["O+","O-","A+","A-","B+","B-","AB+","AB-"]
    opcionSangre=ttk.Combobox(frameReporte,values=tiposSangre)
    opcionSangre.grid(row=1,column=1,pady=10)
    Label(frameReporte,text="Provincia",bg="#ffffff").grid(row=2,column=0,pady=10)
    provincias={"San Jose":1,"Alajuela":2,"Cartago":3,"Heredia":4,"Guanacaste":5,"Puntarenas":6,"Limon":7}
    opcionProvincia=ttk.Combobox(frameReporte,values=list(provincias.keys()))
    opcionProvincia.grid(row=2,column=1,pady=10)
    mensaje=Label(frameReporte,text="",bg="#ffffff")
    mensaje.grid(row=3,column=0,columnspan=2,pady=10)
    frameBotones=Frame(ventanaReporteSangre,bg="#ffffff")
    frameBotones.pack(pady=20)
    Button(frameBotones,text="Generar reporte",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda:generarHTMLReportes(crearFilasTipoSangreProvincia(opcionSangre.get(),provincias[opcionProvincia.get()],donantes),mensaje)
    ).grid(row=0,column=0,padx=5)
    Button(frameBotones,text="Regresar",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda:[ventanaReporteSangre.destroy(),ventanaReporte.deiconify()]).grid(row=0,column=1,padx=5)

def crearFilasCompletaDonadores(donantes):
    """
    Funcionamiento: Esta funcion se encarga de crear una lista de filas en formato HTML para todos los donantes registrados, a partir de sus datos, ademas de retornar la lista de filas HTML generadas
    Entradas:
    - donantes: es la variable que contiene la lista de donantes, que se utilizara para generar las filas HTML correspondientes para cada uno de ellos, sin aplicar ningun filtro, ya que se generaran filas HTML para todos los donantes registrados
    Salidas:
    - filas: es la variable que contiene la lista de filas en formato HTML generadas para todos los donantes registrados, que se utilizara para construir el contenido del reporte en formato HTML, si no se encontraron donantes registrados se retorna una lista vacia
    """
    filas = []
    i = 0
    for datos in donantes:
        cedula = datos[1]
        if i % 2 == 0:
            color = "#85a9cc"
        else:
            color = "#9C8FE6"
        filas.append(crearFilaHTML(cedula, datos, color))
        i += 1
    return filas

def reporteCompleto(ventanaReporte,donantes):
    """
    Funcionamiento: Esta funcion se encarga de generar un reporte completo de todos los donantes registrados en formato HTML, a partir de sus datos, ademas de mostrar un mensaje con el resultado de la generacion del reporte
    Entradas:
    - ventanaReporte: es la variable que contiene la ventana principal de reportes, que se ocultara para mostrar la ventana de confirmacion de generacion de reporte completo, y se mostrara nuevamente despues de cerrar la ventana de confirmacion de generacion de reporte completo
    - donantes: es la variable que contiene la lista de donantes, que se utilizara para generar el reporte completo en formato HTML para todos los donantes registrados, sin aplicar ningun filtro, ya que se generaran filas HTML para todos los donantes registrados
     Salidas:
    - ventanaReporte: se oculta la ventana principal de reportes para mostrar la ventana de confirmacion de generacion de reporte completo, y se muestra nuevamente despues de cerrar la ventana de confirmacion de generacion de reporte completo
    - mensaje: es un mensaje que indica el resultado de la generacion del reporte completo, si el reporte completo fue generado correctamente se muestra un mensaje indicando que el reporte completo fue generado correctamente, si hubo un error al generar el reporte completo se muestra un mensaje indicando que hubo un error al generar el reporte completo
    - reporte HTML: se genera un archivo HTML con el contenido del reporte completo construido a partir de las filas HTML generadas para todos los donantes registrados, si el reporte completo fue generado correctamente, si hubo un error al generar el reporte completo no se genera el archivo HTML
    """
    frameFinal= Frame(ventanaReporte,bg="white")
    frameFinal.pack(pady=10)
    Label(frameFinal, text="Esta seguro que desea hacer el reporte completo").pack()
    mensaje = Label(frameFinal,text="")
    mensaje.pack()
    Button(frameFinal,text="Generar reporte",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda:generarHTMLReportes(crearFilasCompletaDonadores(donantes),mensaje)
    ).pack(pady=10)
    Button(frameFinal,text="Regresar",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda: frameFinal.destroy()).pack(pady=10)

def crearFilaHTMLMujeresO(datos,color):
    fila=f"""
    <tr style="background-color:{color};">
        <td>{html.escape(str(datos[1]))}</td>
        <td>{html.escape(str(datos[0]))}</td>
        <td>{html.escape(str(datos[2]))}</td>
        <td>{html.escape(str(datos[6]))}</td>
        <td>{html.escape(str(datos[7]))}</td>
    </tr>
    """
    return fila

def crearFilasMujeresO(donantes):
    filas = []
    i = 0
    for datos in donantes:
        cedula = datos[1]
        if datos[4] == False and datos[3] == "O-":
            if i % 2 == 0:
                color = "#85a9cc"
            else:
                color = "#9C8FE6"
            filas.append(crearFilaHTMLMujeresO(cedula,datos, color))
            i += 1
    return filas

def generarHTMLMujeresO(filasHTML,mensaje):
    inicio=datetime.now()
    ahora=datetime.now()
    nombreArchivo="reporteMujeresO-"+ahora.strftime("%d-%m-%H-%M-%S")+".html"
    try:
        with open(nombreArchivo,"w",encoding="utf-8") as archivo:
            archivo.write("<!DOCTYPE html>\n")
            archivo.write("<html lang='es'>\n")
            archivo.write("<head>\n")
            archivo.write("<meta charset='UTF-8'>\n")
            archivo.write("<title>Reporte Mujeres O-</title>\n")
            archivo.write("</head>\n")
            archivo.write("<body style='font-family: Arial, sans-serif;'>\n")
            archivo.write("<h1>Reporte Mujeres Donantes O-</h1>\n")
            archivo.write(f"<h2>Generado el {ahora.strftime('%d/%m/%y %H:%M:%S')}</h2>\n")
            final=datetime.now()
            duracion=final-inicio
            archivo.write(f"<p><strong>Duración total:</strong> {duracion}</p>\n")
            archivo.write(f"<p><strong>Cantidad total de donantes:</strong> {len(filasHTML)}</p>\n")
            archivo.write("<table border='1' style='border-collapse:collapse; text-align:center; width:100%;'>\n")
            archivo.write("<tr style='background-color:#cccccc;'>\n")
            archivo.write("<th>Cedula</th>\n")
            archivo.write("<th>Nombre</th>\n")
            archivo.write("<th>Fecha nacimiento</th>\n")
            archivo.write("<th>Telefono</th>\n")
            archivo.write("<th>Correo</th>\n")
            archivo.write("</tr>\n")
            for fila in filasHTML:
                archivo.write(fila)
            archivo.write("</table>\n")
            archivo.write("</body>\n")
            archivo.write("</html>\n")
        mensaje.config(text="Reporte generado correctamente",fg="green")
    except:
        mensaje.config(text="Error al generar el reporte",fg="red")

def reporteMujeresO(ventanaReporte,donantes):
    frameFinal = Frame(ventanaReporte,bg="white")
    frameFinal.pack(pady=10)
    Label(frameFinal,text="generar reporte de mujeres donantes O-",bg="white",font=("Arial",12)).pack(pady=10)
    mensaje = Label(frameFinal,text="",bg="white")
    mensaje.pack()
    Button(frameFinal,text="Generar reporte",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda:generarHTMLMujeresO(crearFilasMujeresO(donantes),mensaje)).pack(pady=10)
    Button(frameFinal,text="Cancelar",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda:frameFinal.destroy()).pack(pady=10)

def crearFilaHTMLDonacion(cedula,datos,color):
    fila=f"""
    <tr style="background-color:{color};">
        <td>{html.escape(str(cedula))}</td>
        <td>{html.escape(str(datos[0]))}</td>
        <td>{html.escape(str(datos[3]))}</td>
        <td>{html.escape(str(datos[6]))}</td>
        <td>{html.escape(str(datos[7]))}</td>
    </tr>
    """
    return fila

def crearFilasDonacion(tipoSangre,donantes):
    filas=[]
    contador=0
    compatibilidad={"O-":["O-","O+","A-","A+","B-","B+","AB-","AB+"],
        "O+":["O+","A+","B+","AB+"],
        "A-":["A-","A+","AB-","AB+"],
        "A+":["A+","AB+"],
        "B-":["B-","B+","AB-","AB+"],
        "B+":["B+","AB+"],
        "AB-":["AB-","AB+"],
        "AB+":["AB+"]}
    for provincia in range(1,8):
        for datos in donantes:
            provinciaDonante=int(datos[1].split("-")[0])
            if provinciaDonante==provincia and datos[3] in compatibilidad[tipoSangre]:
                if contador % 2 == 0:
                    color="#85a9cc"
                else:
                    color="#9C8FE6"
                filas.append(crearFilaHTMLDonacion(datos[1],datos,color))
                contador+=1
    return filas

def generarHTMLDonacion(filasHTML,mensaje):
    inicio=datetime.now()
    ahora=datetime.now()
    nombreArchivo="reporteDonacion"+ahora.strftime("%d-%m-%H-%M-%S")+".html"
    try:
        with open(nombreArchivo,"w",encoding="utf-8") as archivo:
            archivo.write("<!DOCTYPE html>\n")
            archivo.write("<html lang='es'>\n")
            archivo.write("<head>\n")
            archivo.write("<meta charset='UTF-8'>\n")
            archivo.write("<title>Reporte Donacion</title>\n")
            archivo.write("</head>\n")
            archivo.write("<body style='font-family: Arial, sans-serif;'>\n")
            archivo.write("<h1>Reporte de compatibilidad sanguínea</h1>\n")
            archivo.write(f"<h2>Generado el {ahora.strftime('%d/%m/%y %H:%M:%S')}</h2>\n")
            final=datetime.now()
            duracion=final-inicio
            archivo.write(f"<p><strong>Duración total:</strong> {duracion}</p>\n")
            archivo.write("<table border='1' style='border-collapse:collapse; text-align:center; width:100%;'>\n")
            archivo.write("<tr style='background-color:#cccccc;'>\n")
            archivo.write("<th>Cedula</th>\n")
            archivo.write("<th>Nombre completo</th>\n")
            archivo.write("<th>Tipo de sangre</th>\n")
            archivo.write("<th>Telefono</th>\n")
            archivo.write("<th>Correo</th>\n")
            archivo.write("</tr>\n")
            for fila in filasHTML:
                archivo.write(fila)
            archivo.write("</table>\n")
            archivo.write("</body>\n")
            archivo.write("</html>\n")
        mensaje.config(text="Reporte creado satisfactoriamente",fg="green")
    except:
        mensaje.config(text="Reporte no creado",fg="red")

def reporteDonacion(ventanaReporte,donantes):
    ventanaReporte.withdraw()
    ventanaDonacion=Toplevel()
    ventanaDonacion.title("¿A quién puede donar?")
    ubicarVentana(ventanaDonacion,700,600)
    ventanaDonacion.config(bg="#ffffff")
    frameReporte=Frame(ventanaDonacion,bg="#ffffff")
    frameReporte.pack(pady=20)
    Label(frameReporte,text="Seleccione el tipo de sangre",bg="#ffffff").grid(row=0,column=0,pady=10)
    tiposSangre=["O+","O-","A+","A-","B+","B-","AB+","AB-"]
    opcionSangre=ttk.Combobox(frameReporte,values=tiposSangre)
    opcionSangre.grid(row=0,column=1,pady=10)
    mensaje=Label(frameReporte,text="",bg="#ffffff")
    mensaje.grid(row=1,column=0,columnspan=2,pady=10)
    frameBotones=Frame(ventanaDonacion,bg="#ffffff")
    frameBotones.pack(pady=20)
    Button(frameBotones,text="Generar reporte",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda:generarHTMLDonacion(crearFilasDonacion(opcionSangre.get(),donantes),mensaje)).grid(row=0,column=0,padx=5)
    Button(frameBotones,text="Regresar",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda:[ventanaDonacion.destroy(), ventanaReporte.deiconify()]).grid(row=0,column=1,padx=5)

def crearFilasRecibir(tipoSangre,donantes):
    filas=[]
    contador=0
    compatibilidad={
        "O-":["O-"],
        "O+":["O-","O+"],
        "A-":["O-","A-"],
        "A+":["O-","O+","A-","A+"],
        "B-":["O-","B-"],
        "B+":["O-","O+","B-","B+"],
        "AB-":["O-","A-","B-","AB-"],
        "AB+":["O-","O+","A-","A+","B-","B+","AB-","AB+"]}
    for provincia in range(7,0,-1): 
        for datos in donantes:
            provinciaDonante=int(datos[1].split("-")[0])
            if provinciaDonante == provincia and datos[3] in compatibilidad[tipoSangre]:
                if contador % 2 == 0:
                    color="#85a9cc"
                else:
                    color="#9C8FE6"
                filas.append(
                    crearFilaHTMLDonacion(datos[1],datos,color)
                )
                contador += 1
    return filas

def reporteRecibir(ventanaReporte,donantes):
    ventanaReporte.withdraw()
    ventanaRecibir=Toplevel()
    ventanaRecibir.title("¿De quien puede recibir?")
    ubicarVentana(ventanaRecibir,700,600)
    ventanaRecibir.config(bg="#ffffff")
    frameReporte=Frame(ventanaRecibir,bg="#ffffff")
    frameReporte.pack(pady=20)
    Label(frameReporte,text="Seleccione el tipo de sangre",bg="#ffffff").grid(row=0,column=0,pady=10)
    tiposSangre=["O+","O-","A+","A-","B+","B-","AB+","AB-"]
    opcionSangre=ttk.Combobox(frameReporte,values=tiposSangre)
    opcionSangre.grid(row=0,column=1,pady=10)
    mensaje=Label(frameReporte,text="",bg="#ffffff")
    mensaje.grid(row=1,column=0,columnspan=2,pady=10)
    frameBotones=Frame(ventanaRecibir,bg="#ffffff")
    frameBotones.pack(pady=20)
    Button(frameBotones,text="Generar reporte",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda:generarHTMLDonacion(crearFilasRecibir(opcionSangre.get(),donantes),mensaje)).grid(row=0,column=0,padx=5)
    Button(frameBotones,text="Regresar",font=("Arial",12,"bold"),bg="#4773C3",fg="white",
        command=lambda:[ventanaRecibir.destroy(),ventanaReporte.deiconify()]).grid(row=0,column=1,padx=5)

def opcionesReportes(opcion,ventanaReporte,donantes):
    """
    Funcionamiento: Esta funcion se encarga de redirigir a la funcion correspondiente para generar el reporte seleccionado por el usuario, a partir de la opcion seleccionada en la ventana de reportes, ademas de mostrar un mensaje con el resultado de la generacion del reporte
    Entradas:
    - opcion: es la variable que contiene el valor de la opcion seleccionada por el usuario en la ventana de reportes, que se utilizara para redirigir a la funcion correspondiente para generar el reporte seleccionado por el usuario
    - ventanaReporte: es la variable que contiene la ventana principal de reportes, que se ocultara para mostrar la ventana de seleccion de opciones de reporte, y se mostrara nuevamente despues de cerrar la ventana de seleccion de opciones de reporte
    - donantes: es la variable que contiene la lista de donantes, que se utilizara para generar el reporte seleccionado por el usuario en formato HTML para los donantes correspondientes, dependiendo de la opcion seleccionada por el usuario
    Salidas:
    - Llama a la funcion correspondiente para generar el reporte seleccionado por el usuario, dependiendo de la opcion seleccionada por el usuario, si la opcion seleccionada por el usuario no corresponde a ninguna opcion valida se muestra un mensaje indicando que la opcion seleccionada no es valida
    """
    if opcion == 1:
        reportePorProvincia(ventanaReporte,donantes)
    elif opcion ==2:
        reportePorEdad(ventanaReporte,donantes)
    elif opcion == 3:
        reporteTipoSangreProvincia(ventanaReporte,donantes)
    elif opcion == 4:
        reporteCompleto(ventanaReporte,donantes)
    elif opcion == 5:
        reporteMujeresO(ventanaReporte,donantes)
    elif opcion == 6:
        reporteDonacion(ventanaReporte,donantes)
    elif opcion == 7:
        reporteRecibir(ventanaReporte,donantes)
    

#=======Funcion principal=======

def insertarDonador(ventana,donantes,lugaresDonacion):
    """
    Funcionamiento: Esta funcion se encarga de mostrar una ventana para que el usuario ingrese los datos de un nuevo donante, ademas de validar los datos ingresados, registrar el nuevo donante en la lista de donantes, y mostrar un mensaje con el resultado del registro del nuevo donante
    Entradas:
    - ventana: es la variable que contiene la ventana principal del programa, que se ocultara para mostrar la ventana de ingreso de datos del nuevo donante, y se mostrara nuevamente despues de cerrar la ventana de ingreso de datos del nuevo donante
    - donantes: es la variable que contiene la lista de donantes, que se utilizara para registrar el nuevo donante ingresado por el usuario, agregando los datos del nuevo donante a la lista de donantes, y para validar los datos ingresados por el usuario, verificando que la cedula ingresada no se encuentre registrada en la lista de donantes, y que los datos ingresados cumplan con los formatos requeridos
    - lugaresDonacion: es la variable que contiene la lista de lugares de donacion, que se utilizara para validar el lugar de donacion ingresado por el usuario, verificando que el lugar de donacion ingresado se encuentre registrado en la lista de lugares de donacion
    Salidas:
    - ventana: se oculta la ventana principal del programa para mostrar la ventana de ingreso de datos del nuevo donante, y se muestra nuevamente despues de cerrar la ventana de ingreso de datos del nuevo donante
    - mensaje: es un mensaje que indica el resultado del registro del nuevo donante, si el nuevo donante fue registrado correctamente se muestra un mensaje indicando que el nuevo donante fue registrado correctamente, si hubo un error al registrar el nuevo donante se muestra un mensaje indicando que hubo un error al registrar el nuevo donante, como por ejemplo si la cedula ingresada ya se encuentra registrada en la lista de donantes, o si los datos ingresados no cumplen con los formatos requeridos
    - nuevo donante registrado: se agrega el nuevo donante a la lista de donantes con los datos ingresados por el usuario, si el nuevo donante fue registrado correctamente, si hubo un error al registrar el nuevo donante no se agrega el nuevo donante a la lista de donantes
    """
    ventana.withdraw()
    ventanaInsertar=Toplevel()
    ventanaInsertar.title("Insertar donador")
    ubicarVentana(ventanaInsertar,900,900)
    ventanaInsertar.config(bg="#FFFFFF")
    frameInsertar=Frame(ventanaInsertar,bg="#BB4242",bd=5)
    frameInsertar.pack(pady=20)
    cedula=cedulaInser(frameInsertar)
    nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo=crearEntradas(frameInsertar)
    mensaje = Label(ventanaInsertar,text = "",font= ("arial",12,"bold"), bg = "white",fg= "red")
    mensaje.pack(pady=10)
    frameBotones=Frame(ventanaInsertar,bg="#FFFFFF",bd=5)
    frameBotones.pack(pady=20)
    mensajeRegistrar = Label(ventanaInsertar,text = "")
    mensajeRegistrar.pack(pady=20)
    crearBotones(ventana,frameBotones,ventanaInsertar,mensaje,mensajeRegistrar,donantes,cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo,lugaresDonacion)

def generar(ventana,donantes):
    """
    Funcionamiento: Esta funcion se encarga de mostrar una ventana para que el usuario ingrese la cantidad de donadores que desea generar, ademas de generar la cantidad de donadores ingresada por el usuario, registrar los nuevos donadores en la lista de donadores, y mostrar un mensaje con el resultado de la generacion de los nuevos donadores
    Entradas:
    - ventana: es la variable que contiene la ventana principal del programa, que se ocultara para mostrar la ventana de ingreso de cantidad de donadores a generar, y se mostrara nuevamente despues de cerrar la ventana de ingreso de cantidad de donadores a generar
    - donantes: es la variable que contiene la lista de donantes, que se utilizara para registrar los nuevos donadores generados por el programa, agregando los datos de los nuevos donadores a la lista de donantes, y para validar la cantidad de donadores ingresada por el usuario, verificando que la cantidad de donadores ingresada sea un numero entero positivo
    Salidas:
    - ventana: se oculta la ventana principal del programa para mostrar la ventana de ingreso de cantidad de donadores a generar, y se muestra nuevamente despues de cerrar la ventana de ingreso de cantidad de donadores a generar
    - mensaje: es un mensaje que indica el resultado de la generacion de los nuevos donadores, si los nuevos donadores fueron generados correctamente se muestra un mensaje indicando que los nuevos donadores fueron generados correctamente, si hubo un error al generar los nuevos donadores se muestra un mensaje indicando que hubo un error al generar los nuevos donadores, como por ejemplo si la cantidad de donadores ingresada no es un numero entero positivo
    - nuevos donadores generados: se generan la cantidad de nuevos donadores ingresada por el usuario, con datos aleatorios, y se agregan a la lista de donantes, si los nuevos donadores fueron generados correctamente, si hubo un error al generar los nuevos donadores no se generan los nuevos donadores ni se agregan a la lista de donantes
    """
    ventana.withdraw()
    ventanaGenerar= Toplevel()
    ventanaGenerar.title("Generar Donadores")
    ubicarVentana(ventanaGenerar,700,600)
    ventanaGenerar.config(bg="#ffffff")
    frameGenerar= Frame(ventanaGenerar,bg="#ffffff",bd=5)
    frameGenerar.pack(pady=5)
    Label(frameGenerar,text="Ingrese la cantidad de donadores que desea generar",bg="#ffffff",font=("Arial",12,"bold")).grid(row=0,pady=20)
    cantidad= StringVar()
    Entry(frameGenerar,textvariable=cantidad).grid(row=1,pady=20)
    mensaje = Label(ventanaGenerar,text = "",font= ("arial",12,"bold"), bg = "white",fg= "red")
    mensaje.pack(pady=5)
    frameBotones= Frame(ventanaGenerar,bg="#ffffff",bd=5)
    frameBotones.pack(pady=5)
    Button(frameBotones,text="generar",font=("Arial",12,"bold"),bg="#4773C3",fg="white",command=lambda:crearDonadores(mensaje,donantes,cantidad.get())).grid(row=0,column=0,padx=5)
    Button(frameBotones, text="Limpiar", font=("Arial", 12, "bold"), bg="#555555", fg="white", command=lambda: [cantidad.set(""), mensaje.config(text="")]).grid(row=0, column=1, padx=5)
    Button(frameBotones,text="Regresar",font=("Arial",12,"bold"),bg="#BB3535",fg="white",command=lambda:salirInser(ventana,ventanaGenerar)).grid(row=0,column=2,padx=5)

def actualizarDonador(ventana,donantes,lugaresDonacion):
    """
    Funcionamiento: Esta funcion se encarga de mostrar una ventana para que el usuario ingrese la cedula del donante que desea actualizar, ademas de validar la cedula ingresada, buscar el donante correspondiente a la cedula ingresada en la lista de donantes, mostrar los datos actuales del donante encontrado, permitir al usuario ingresar los nuevos datos del donante, validar los nuevos datos ingresados, actualizar los datos del donante en la lista de donantes, y mostrar un mensaje con el resultado de la actualizacion del donante
    Entradas:
    - ventana: es la variable que contiene la ventana principal del programa, que se ocultara para mostrar la ventana de ingreso de cedula del donante a actualizar, y se mostrara nuevamente despues de cerrar la ventana de ingreso de cedula del donante a actualizar
    - donantes: es la variable que contiene la lista de donantes, que se utilizara para buscar el donante correspondiente a la cedula ingresada por el usuario, verificando que la cedula ingresada se encuentre registrada en la lista de donantes, y para actualizar los datos del donante encontrado en la lista de donantes, reemplazando los datos actuales del donante con los nuevos datos ingresados por el usuario, si la actualizacion del donante fue realizada correctamente
    - lugaresDonacion: es la variable que contiene la lista de lugares de donacion, que se utilizara para validar el nuevo lugar de donacion ingresado por el usuario, verificando que el nuevo lugar de donacion ingresado se encuentre registrado en la lista de lugares de donacion
    Salidas:
    - ventana: se oculta la ventana principal del programa para mostrar la ventana de ingreso de cedula del donante a actualizar, y se muestra nuevamente despues de cerrar la ventana de ingreso de cedula del donante a actualizar
    - mensaje: es un mensaje que indica el resultado de la actualizacion del donante, si el donante fue actualizado correctamente se muestra un mensaje indicando que el donante fue actualizado correctamente, si hubo un error al actualizar el donante se muestra un mensaje indicando que hubo un error al actualizar el donante, como por ejemplo si la cedula ingresada no se encuentra registrada en la lista de donantes, o si los nuevos datos ingresados no cumplen con los formatos requeridos
    - donante actualizado: se actualizan los datos del donante encontrado en la lista de donantes con los nuevos datos ingresados por el usuario, si el donante fue actualizado correctamente, si hubo un error al actualizar el donante no se actualizan los datos del donante en la lista de donantes
    """
    ventana.withdraw()
    ventanaBuscarActualizar=Toplevel()
    ventanaBuscarActualizar.title("Buscar donador")
    ubicarVentana(ventanaBuscarActualizar,700,600)
    ventanaBuscarActualizar.config(bg="#ffffff")
    Label(ventanaBuscarActualizar,text="Ingrese la cedula del donante a actualizar\npara asi poder confirmar si el donante esta registrado",bg="#ffffff",font=("Arial",12,"bold")).pack(pady=20)
    frameBuscar=Frame(ventanaBuscarActualizar,bg="#ffffff")
    frameBuscar.pack(pady=10)
    cedulaBuscar=cedulaInser(frameBuscar)
    mensaje=Label(ventanaBuscarActualizar,text="",bg="#ffffff",font=("Arial",11,"bold"))
    mensaje.pack(pady=10)
    frameBotones = Frame(ventanaBuscarActualizar, bg="#ffffff")
    frameBotones.pack()
    Button(frameBotones,text="Buscar",font=("Arial",12,"bold"),bg="#4773C3",fg="white",command=lambda:buscarDonanteActualizar(ventana,ventanaBuscarActualizar,donantes,cedulaBuscar,mensaje,lugaresDonacion)).grid(row=0,column=0,padx=10)
    Button(frameBotones, text="Limpiar", font=("Arial", 12, "bold"), bg="#555555", fg="white", command=lambda: [cedulaBuscar.delete(0, 'end') if hasattr(cedulaBuscar, 'delete') else cedulaBuscar.set(""), mensaje.config(text="")]).grid(row=0,column=1,padx=10)
    Button(frameBotones,text="Regresar",font=("Arial",12,"bold"),bg="#43C345",fg="white",command=lambda:[ventanaBuscarActualizar.destroy(),ventana.deiconify()]).grid(row=0,column=2,padx=10)

def eliminarDonador(ventana,donantes):
    """
    Funcionamiento: Esta funcion se encarga de mostrar una ventana para que el usuario ingrese la cedula del donante que desea eliminar, ademas de validar la cedula ingresada, buscar el donante correspondiente a la cedula ingresada en la lista de donantes, eliminar el donante encontrado de la lista de donantes, y mostrar un mensaje con el resultado de la eliminacion del donante
    Entradas:
    - ventana: es la variable que contiene la ventana principal del programa, que se ocultara para mostrar la ventana de ingreso de cedula del donante a eliminar, y se mostrara nuevamente despues de cerrar la ventana de ingreso de cedula del donante a eliminar
    - donantes: es la variable que contiene la lista de donantes, que se utilizara para buscar el donante correspondiente a la cedula ingresada por el usuario, verificando que la cedula ingresada se encuentre registrada en la lista de donantes, y para eliminar el donante encontrado de la lista de donantes, si la eliminacion del donante fue realizada correctamente
    Salidas:
    - ventana: se oculta la ventana principal del programa para mostrar la ventana de ingreso de cedula del donante a eliminar, y se muestra nuevamente despues de cerrar la ventana de ingreso de cedula del donante a eliminar
    - mensaje: es un mensaje que indica el resultado de la eliminacion del donante, si el donante fue eliminado correctamente se muestra un mensaje indicando que el donante fue eliminado correctamente, si hubo un error al eliminar el donante se muestra un mensaje indicando que hubo un error al eliminar el donante, como por ejemplo si la cedula ingresada no se encuentra registrada en la lista de donantes
    - donante eliminado: se elimina el donante encontrado de la lista de donantes, si el donante fue eliminado correctamente, si hubo un error al eliminar el donante no se elimina el donante de la lista de donantes
    """
    ventana.withdraw()
    ventanaEliminar=Toplevel()
    ventanaEliminar.title("Eliminar donador")
    ubicarVentana(ventanaEliminar,500,500)
    ventanaEliminar.config(bg="#ffffff")
    Label(ventanaEliminar,text="Ingrese la cedula del donante a eliminar",bg="#ffffff",font=("Arial",12,"bold")).pack(pady=20)
    frameBuscar=Frame(ventanaEliminar,bg="#ffffff")
    frameBuscar.pack(pady=10)
    cedulaBuscar=cedulaInser(frameBuscar)
    mensaje=Label(ventanaEliminar,text="",bg="#ffffff",font=("Arial",11,"bold"))
    mensaje.pack(pady=10)
    frameBotones = Frame(ventanaEliminar,bg="#FFFFFF")
    frameBotones.pack()
    Button(frameBotones,text="Eliminar",font=("Arial",12,"bold"),bg="#C62828",fg="white",command=lambda:eliminarDonanteAux(donantes,cedulaBuscar,mensaje)).grid(row=0,column=0,padx=10)
    Button(frameBotones,text="Regresar",font=("Arial",12,"bold"),bg="#43C345",fg="white",command=lambda:[ventanaEliminar.destroy(),ventana.deiconify()]).grid(row=0,column=1,padx=10)

def lugaresDeDonacion(ventana,lugares):
    ventana.withdraw()
    ventanaLugares = Toplevel()
    ventanaLugares.title("Lugar de donacion")
    ubicarVentana(ventanaLugares,700,600)
    ventanaLugares.config(bg="#ffffff")
    frameLugares = Frame(ventanaLugares,bg="#ffffff")
    frameLugares.pack(pady=20)
    Label(frameLugares,text="Provincias",bg="#ffffff",font=("Arial",12,"bold")).grid(row=0,column=0,pady=10,padx=10)
    provincia = ttk.Combobox(frameLugares, values=list(lugares.keys()), state="readonly")
    provincia.grid(row=0, column=1, pady=10, padx=10)
    frameBotones = Frame(ventanaLugares,bg= "#ffffff")
    frameBotones.pack(pady=20)
    frameNuevoLugar = Frame(ventanaLugares,bg= "#ffffff")
    frameNuevoLugar.pack(pady=20)
    Button(frameBotones,text="Agregar",font=("Arial",12,"bold"),bg="#C62828",fg="white",command=lambda:nuevoLugarDonacion(frameNuevoLugar,lugares,provincia.get())).grid(row=0,column=0,padx=10)
    Button(frameBotones,text="Regresar",font=("Arial",12,"bold"),bg="#43C345",fg="white",command=lambda:[ventanaLugares.destroy(),ventana.deiconify()]).grid(row=0,column=1,padx=10)

def reportes(ventana,donantes):
    """
    Funcionamiento: Esta funcion se encarga de mostrar una ventana para que el usuario seleccione la opcion de reporte que desea generar, ademas de redirigir a la funcion correspondiente para generar el reporte seleccionado por el usuario, y mostrar un mensaje con el resultado de la generacion del reporte
    Entradas:
    - ventana: es la variable que contiene la ventana principal del programa, que se ocultara para mostrar la ventana de seleccion de opciones de reporte, y se mostrara nuevamente despues de cerrar la ventana de seleccion de opciones de reporte
    - donantes: es la variable que contiene la lista de donantes, que se utilizara para generar el reporte seleccionado por el usuario en formato HTML para los donantes correspondientes, dependiendo de la opcion seleccionada por el usuario
     Salidas:
    - ventana: se oculta la ventana principal del programa para mostrar la ventana de seleccion de opciones de reporte, y se muestra nuevamente despues de cerrar la ventana de seleccion de opciones de reporte
    - mensaje: es un mensaje que indica el resultado de la generacion del reporte seleccionado por el usuario, si el reporte seleccionado por el usuario fue generado correctamente se muestra un mensaje indicando que el reporte seleccionado por el usuario fue generado correctamente, si hubo un error al generar el reporte seleccionado por el usuario se muestra un mensaje indicando que hubo un error al generar el reporte seleccionado por el usuario, como por ejemplo si la opcion seleccionada por el usuario no corresponde a ninguna opcion valida
    - reporte HTML: se genera un archivo HTML con el contenido del reporte seleccionado por el usuario construido a partir de las filas HTML generadas para los donantes correspondientes, dependiendo de la opcion seleccionada por el usuario, si el reporte seleccionado por el usuario fue generado correctamente, si hubo un error al generar el reporte seleccionado por el usuario no se genera el archivo HTML
    """
    ventana.withdraw()
    ventanaReportes = Toplevel()
    ventanaReportes.title("Reporte de donadores")
    ubicarVentana(ventanaReportes,700,600)
    ventanaReportes.config(bg="#ffffff")
    frameReporte= Frame(ventanaReportes,bg="#ffffff")
    frameReporte.pack()
    Label(frameReporte,text="Ingrese la opcion de reporte:").pack(pady=10)
    opcion = {"Donantes por provincia":1,"Rango de edad":2,"Tipo de sangre por provincia":3,
            "Lista completa de donadores":4,"Mujeres donantes O-":5,"A quien puede donar":6,"De quien puede recibir":7,"Donantes no activos":8}
    opciones=ttk.Combobox(frameReporte,textvariable=opcion,values=list(opcion.keys()))
    opciones.pack(pady=10)
    frameBotones = Frame(ventanaReportes,bg="#ffffff")
    frameBotones.pack()
    Button(frameBotones,text="Aceptar",font=("Arial",12,"bold"),bg="#5ab86a",fg="white",command= lambda:opcionesReportes(opcion[opciones.get()],ventanaReportes,donantes)).grid(row = 0,column= 0, padx = 10)
    Button(frameBotones, text="Limpiar",font=("Arial",12,"bold"),bg="#f44336", fg="white", command=lambda: opciones.set("")).grid(row = 0,column= 1, padx = 10)
    Button(frameBotones,text="Regresar",font=("Arial",12,"bold"),bg="#43C345",fg="white",command=lambda:[ventanaReportes.destroy(),ventana.deiconify()]).grid(row=0,column= 2, padx = 10)

def salir():
    ventana.destroy()
# ---------------- BOTONES ----------------
Button(frameMenu,text="1. Insertar donador",font=("Arial",14),
    width=30,height=2,bg="#1565c0",fg="white",
    command=lambda:insertarDonador(ventana,donantes,lugaresDonacion)).grid(row=1,column=0)
Button(frameMenu,text="2. Generar donadores",font=("Arial",14),
    width=30,height=2,bg="#1565c0",fg="white",command=lambda:generar(ventana,donantes)).grid(row=1,column=1)
Button(frameMenu,text="3. Actualizar datos",font=("Arial",14),
    width=30,height=2,bg="#1565c0",fg="white",command=lambda:actualizarDonador(ventana,donantes,lugaresDonacion)).grid(row=2,column=0)
Button(frameMenu,text="4. Eliminar donador",font=("Arial",14),
    width=30,height=2,bg="#1565c0",fg="white",
    command=lambda:eliminarDonador(ventana,donantes)).grid(row=2,column=1)
Button(frameMenu,text="5. Insertar lugar",font=("Arial",14),
    width=30,height=2,bg="#1565c0",fg="white",command=lambda:lugaresDeDonacion(ventana,lugaresDonacion)).grid(row=3,column=0)
Button(frameMenu,text="6. Reportes",font=("Arial",14),width=30,
    height=2,bg="#1565c0",fg="white",command=lambda:reportes(ventana,donantes)).grid(row=3,column=1)
Button(frameMenu,text="7. Salir",font=("Arial",14),width=30,
    height=2,bg="#2e7d32",fg="white",command=salir).grid(row=4,column=0,columnspan=2)
# ---------------- FOOTER ----------------
footer = Label(ventana,text="TEC - Taller de Programación",
    font=("Arial black",12),bg="#1f255c",fg="white")
footer.pack(side="bottom",pady=20, padx= 20)
# ---------------- EJECUTAR ----------------
ventana.mainloop()
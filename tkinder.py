from tkinter import *
from tkinter import ttk
import re

def ubicarVentana(ventana,ancho,largo):
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
donantes = [] #Crear diccionario que la llave sea la cedula y la otra informacion sean los datos que se guardan en esa llave
# ================================ FUNCIONES ========================================
# =============Funcione de uso general para todas las funciones====================

def cedulaInser(frameInsertar):
    Label(frameInsertar, text = "Cedula", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 0,column=0,pady=5)
    cedula = StringVar()
    Entry(frameInsertar,textvariable=cedula).grid(row=0,column=1)
    return cedula
    
def cedulaInserAux(cedula):
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
    Label(frameInsertar, text = "Nombre completo", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 1,column=0,pady=5)
    nombre = StringVar()
    Entry(frameInsertar,textvariable=nombre).grid(row=1,column=1)
    return nombre   

def normalizarNombre(pnombre):
    if pnombre == "":
        return (False,"Debe incluir un nombre")
    for letra in pnombre:
        if letra.isalpha() == False and letra != " ":
            return(False,"Debe ingresar solamente letras en el nombre")
    palabras = pnombre.split()     
    resultado = ""
    for p in palabras:                           
        palabra = p[0].upper() + p[1:].lower() 
        resultado = resultado + palabra + " "     
    return (True,resultado)

def fechaNacimientoInser(frameInsertar):
    Label(frameInsertar, text = "Fecha de nacimiento", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 2,column=0,pady=5)
    fechaNacimiento = StringVar()
    Entry(frameInsertar,textvariable= fechaNacimiento).grid(row=2,column=1)
    return fechaNacimiento

def validarFechaAux(fechaNacimiento):
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
    Label(frameInsertar, text = "Tipo de sangre", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 3,column=0,pady=5)
    tipoSangre = StringVar()
    ttk.Combobox(frameInsertar,textvariable=tipoSangre,
        values=["O+","O-","A+","A-","B+","B-","AB+","AB-"]
        ).grid(row=3, column = 1)
    return tipoSangre


def sexoInser(frameInsertar):
    frameSexo = Frame(frameInsertar, bg = "#ffffff", bd = 5)
    Label(frameSexo, text = "Sexo", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 0,column=0,pady=5)
    sexo = BooleanVar(value=True)
    Radiobutton(frameSexo, text= "Femenino",variable=sexo,value = False).grid(row=0,column=2)
    Radiobutton(frameSexo, text= "Masculino",variable=sexo,value = True).grid(row=0,column=1)
    frameSexo.grid(row=4)
    return sexo

def pesoInser(frameInsertar):
    Label(frameInsertar, text = "Peso(kg)", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 5,column=0,pady=5)
    peso = StringVar()
    Entry(frameInsertar,textvariable=peso).grid(row=5,column=1)
    return peso

def validarPesoAux(peso):
    if peso.isdigit()==False:
        return(False,"El peso solo debe contener numeros")
    return(True,peso)

def telefonoInser(frameInsertar):
    Label(frameInsertar, text = "Telefono", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 6,column=0,pady=5)
    telefono = StringVar()
    Entry(frameInsertar,textvariable= telefono).grid(row=6,column=1)
    return telefono

def validarTelefonoAux(telefono):
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
    Label(frameInsertar, text = "Correo", font=("Arial",14,"bold"),fg="#0D1764").grid(row= 7,column=0,pady=5)
    correo = StringVar()
    Entry(frameInsertar,textvariable=correo).grid(row=7,column=1)
    return correo

def validarCorreoAux(correo):
    if correo == "":
        return(False,"Debe ingresar un correo")
    formato=r"[a-zA-Z0-9._%+-]+@(gmail\.com|racsa\.go\.cr|costarricense\.cr|ccss\.sa\.cr)$"
    if re.fullmatch(formato,correo)==None:
        return(False,"Correo invalido ejemplo formato de correo correcto ejemplo@gmail.com")
    return(True,correo)

#===============================Funciones para la fa funcion de insertar donadores======================================
#==============================Comentario despues de registrar los datos del donador===========================================

def definirProvincia(n):
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
    if calcularEdad(fechaNacimiento) >= 18:
        return "Dado su fecha de nacimineto usted ya puede ser donador"
    return"Dado su fecha de nacimiento usted aun no puede ser donador"

def compatibilidadSangre(tipoSangre):
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
    if tipoSangre in ["A+","A-"]:
        return "Se le recomienda ver este video sobre las particularidades de la sangre tipo 'A'"
    return None

def validarLugarNacimiento(cedula):
    cedula = cedula.split("-")
    provincia = definirProvincia(cedula[0])
    lugaresDonacion={
    "San Jose":["Banco Nacional de Sangre","Hospital Mexico","Hospital San Juan de Dios"],
    "Alajuela":["Hospital San Rafael de Alajuela","Hospital de San Ramon","Hospital del Canton Norteno"],
    "Cartago":["Hospital Max Peralta"],
    "Heredia":["Hospital San Vicente de Paul"],
    "Guanacaste":["Hospital La Anexion en Nicoya","Hospital Enrique Baltodano de Liberia"],
    "Puntarenas":["Hospital Monsenor Sanabria"],
    "Limon":["Hospital Tony Facio","Hospital de Guapiles"]}
    ubicacion = str(lugaresDonacion[provincia])
    return "Dado que usted nació en la provincia de: "+provincia+"\n usted podria donar en: "+ubicacion

def recomendaccionPeso(peso):
    mensaje = ""
    if int(peso)>=50:
        mensaje = "usted posee un peso adecuado para donar sangre.\n"
    elif int(peso) >120:
        mensaje = "No puede donar sangre por sobrepeso\n"
    else:
        mensaje = "No puede donar sangre por bajo peso\n"
    return mensaje

def generarAnalisisDonante(cedula,fechaNacimiento,tipoSangre,peso):
    resultadoProvincia=validarLugarNacimiento(cedula)
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
    donantes.append([cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo]) # Agregar una validacion para que no se repitan datos
    return(True,"Donante registrado correctamente")

def registrar(mensajeRegistrar,donantes,cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo,mensaje):
    resultado=validarDatos(donantes,cedula.get(),nombre.get(),fechaNacimiento.get(),tipoSangre.get(),
        sexo.get(),peso.get(),telefono.get(),correo.get())
    if resultado[0]==False:
        mensaje.config(text=resultado[1],fg="red")
        return
    mensaje.config(text=resultado[1],fg="green")
    mensajeRegistrar.config(text= generarAnalisisDonante(cedula.get(),fechaNacimiento.get(),tipoSangre.get(),peso.get()),font=("calibri",11,"bold"))
    mensajeRegistrar.pack()

def limpiar(cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo):
    cedula.set("")
    nombre.set("")
    fechaNacimiento.set("")
    tipoSangre.set("")
    sexo.set(True)
    peso.set("")
    telefono.set("")
    correo.set("")

def salirInser(ventana,ventanaInsertar):
    ventana.deiconify()
    ventanaInsertar.destroy()

def crearBotones(ventana,frameBotones,ventanaInsertar,mensaje,mensajeRegistrar,donantes,cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo):
    Button(frameBotones,text="Registrar",font=("Arial",12,"bold"),
        bg="#4773C3",fg="white",
        command=lambda: registrar(mensajeRegistrar,donantes,cedula,nombre,fechaNacimiento,
            tipoSangre,sexo,peso,telefono,correo,mensaje)
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
    nombre=nombreInser(frameInsertar)
    fechaNacimiento=fechaNacimientoInser(frameInsertar)
    tipoSangre=tipoSangreInser(frameInsertar)
    sexo=sexoInser(frameInsertar)
    peso=pesoInser(frameInsertar)
    telefono=telefonoInser(frameInsertar)
    correo=correoInser(frameInsertar)
    return(nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo)

#===========funciones usadas principalmente para actualizar donadores==========

def buscarDonante(donantes,cedulaBuscar):
    for i in range(len(donantes)):
        if donantes[i][0]==cedulaBuscar:
            return(True,donantes[i],i)
    return(False,"No se encontro el donante",-1)

def limpiarActualizacion(nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo,mensajeActualizar):
    nombre.set("")
    fechaNacimiento.set("")
    tipoSangre.set("")
    sexo.set(True)
    peso.set("")
    telefono.set("")
    correo.set("")
    mensajeActualizar.config(text="")

def guardarActualizacion(donantes,posicion,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo,mensajeActualizar):
    resultado=validarDatos([],donantes[posicion][0],nombre.get(),fechaNacimiento.get(),tipoSangre.get(),sexo.get(),peso.get(),telefono.get(),correo.get())
    if resultado[0]==False:
        mensajeActualizar.config(text=resultado[1],fg="red")
        return
    donantes[posicion]=[
        donantes[posicion][0],
        normalizarNombre(nombre.get())[1],
        fechaNacimiento.get(),
        tipoSangre.get(),
        sexo.get(),
        peso.get(),
        telefono.get(),
        correo.get()
    ]
    mensajeActualizar.config(text="Donante actualizado correctamente",fg="green")

def actualizardatos(ventanaBuscar,cedula,donantes):
    ventanaBuscar.withdraw()
    ventanaActualizar=Toplevel()
    ventanaActualizar.title("Insertar donador")
    ubicarVentana(ventanaActualizar,900,900)
    ventanaActualizar.config(bg="#FFFFFF")
    frameInsertar=Frame(ventanaActualizar,bg="#E6E6E6",bd=5)
    frameInsertar.pack(pady=20)
    nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo=crearEntradas(frameInsertar)
    mensaje = Label(ventanaActualizar,text = "",font= ("arial",12,"bold"), bg = "white",fg= "red")
    mensaje.pack(pady=10)
    frameBotones=Frame(ventanaActualizar,bg="#FFFFFF",bd=5)
    frameBotones.pack(pady=20)
    mensajeRegistrar = Label(ventanaActualizar,text = "")
    mensajeRegistrar.pack(pady=20)
    crearBotones(ventana,frameBotones,ventanaActualizar,mensaje,mensajeRegistrar,donantes,cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo)

def cargarDatosActualizar(donantes,posicion,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo):
    nombre.set(donantes[posicion][1])
    fechaNacimiento.set(donantes[posicion][2])
    tipoSangre.set(donantes[posicion][3])
    sexo.set(donantes[posicion][4])
    peso.set(donantes[posicion][5])
    telefono.set(donantes[posicion][6])
    correo.set(donantes[posicion][7])

def abrirVentanaActualizar(ventana,ventanaBuscarActualizar,donantes,posicion):
    ventanaBuscarActualizar.destroy()
    ventanaActualizar=Toplevel()
    ventanaActualizar.title("Actualizar donador")
    ubicarVentana(ventanaActualizar,900,900)
    ventanaActualizar.config(bg="#FFFFFF")
    frameInsertar=Frame(ventanaActualizar,bg="#BB4242",bd=5)
    frameInsertar.pack(pady=20)
    nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo=crearEntradas(frameInsertar)
    nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo = cargarDatosActualizar(donantes,posicion,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo)
    mensajeActualizar=Label(ventanaActualizar,text="",font=("Arial",12,"bold"),bg="white",fg="red")
    mensajeActualizar.pack(pady=10)
    frameBotones=Frame(ventanaActualizar,bg="#FFFFFF",bd=5)
    frameBotones.pack(pady=20)
    Button(frameBotones,text="Actualizar",font=("Arial",12,"bold"),bg="#4773C3",fg="white",command=lambda:guardarActualizacion(donantes,posicion,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo,mensajeActualizar)).grid(row=0,column=0,padx=10)
    Button(frameBotones,text="Limpiar",font=("Arial",12,"bold"),bg="#4773C3",fg="white",command=lambda:limpiarActualizacion(nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo,mensajeActualizar)).grid(row=0,column=1,padx=10)
    Button(frameBotones,text="Regresar",font=("Arial",12,"bold"),bg="#43C345",fg="white",command=lambda:[ventanaActualizar.destroy(),ventana.deiconify()]).grid(row=0,column=2,padx=10)

def buscarDonanteActualizar(ventana,ventanaBuscarActualizar,donantes,cedulaBuscar,mensaje):
    resultado=buscarDonante(donantes,cedulaBuscar.get())
    if resultado[0]==False:
        mensaje.config(text=resultado[1],fg="red")
        return
    mensaje.config(text="Donante encontrado correctamente",fg="green")
    abrirVentanaActualizar(ventana,ventanaBuscarActualizar,donantes,resultado[2])


#=======Funcion principal=======


def insertarDonador(ventana,donantes):
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
    crearBotones(ventana,frameBotones,ventanaInsertar,mensaje,mensajeRegistrar,donantes,cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo)

def generar(donantes):
    print("hola")

def actualizarDonador(ventana,donantes):
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
    Button(ventanaBuscarActualizar,text="Buscar",font=("Arial",12,"bold"),bg="#4773C3",fg="white",command=lambda:buscarDonanteActualizar(ventana,ventanaBuscarActualizar,donantes,cedulaBuscar,mensaje)).pack(pady=20)
    Button(ventanaBuscarActualizar,text="Regresar",font=("Arial",12,"bold"),bg="#43C345",fg="white",command=lambda:[ventanaBuscarActualizar.destroy(),ventana.deiconify()]).pack(pady=10)

def eliminar():
    print("hola")

def lugares():
    print("Insertar lugar")

def reportes(donantes):
    print(donantes)

def salir():
    ventana.destroy()

# ---------------- BOTONES ----------------
Button(frameMenu,text="1. Insertar donador",font=("Arial",14),
    width=30,height=2,bg="#1565c0",fg="white",
    command=lambda:insertarDonador(ventana,donantes)).grid(row=1,column=0)
Button(frameMenu,text="2. Generar donadores",font=("Arial",14),
    width=30,height=2,bg="#1565c0",fg="white",command=generar).grid(row=1,column=1)
Button(frameMenu,text="3. Actualizar datos",font=("Arial",14),
    width=30,height=2,bg="#1565c0",fg="white",command=lambda:actualizarDonador(ventana,donantes)).grid(row=2,column=0)
Button(frameMenu,text="4. Eliminar donador",font=("Arial",14),
    width=30,height=2,bg="#1565c0",fg="white",
    command=eliminar).grid(row=2,column=1)
Button(frameMenu,text="5. Insertar lugar",font=("Arial",14),
    width=30,height=2,bg="#1565c0",fg="white",command=lugares).grid(row=3,column=0)
Button(frameMenu,text="6. Reportes",font=("Arial",14),width=30,
    height=2,bg="#1565c0",fg="white",command=lambda:reportes(donantes)).grid(row=3,column=1)
Button(frameMenu,text="7. Salir",font=("Arial",14),width=30,
    height=2,bg="#2e7d32",fg="white",command=salir).grid(row=4,column=0,columnspan=2)
# ---------------- FOOTER ----------------
footer = Label(ventana,text="TEC - Taller de Programación",
    font=("Arial black",12),bg="#1f255c",fg="white")
footer.pack(side="bottom",pady=20, padx= 20)
# ---------------- EJECUTAR ----------------
ventana.mainloop()
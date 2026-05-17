from tkinter import *
from tkinter import ttk
import re
# ---------------- VENTANA PRINCIPAL ----------------
ventana = Tk()
ventana.title("Banco de Sangre")
ventana.geometry("700x600")
ventana.config(bg="#ffffff")
ventana.resizable(False,False)
# ---------------- TITULO ----------------
titulo = Label(ventana,text="DONAR SANGRE, ES DONAR VIDA",
    font=("Arial",24,"bold"),bg="#ffffff",fg="black")
titulo.pack(pady=30)
# ---------------- SUBTITULO ----------------
subtitulo = Label(ventana,text="Sistema de Información - Banco de Sangre",
    font=("Arial",14),bg="#ffffff",fg="black")
subtitulo.pack(pady=5)
# ---------------- MARCO DEL MENU ----------------
frame_menu = Frame(ventana,bg="white",bd=4,relief="ridge")
frame_menu.pack(pady=40)
# Inicializaciones 
donantes = []
# ---------------- FUNCIONES ----------------
# Funcion Inseratar Donantes

def cedulaInser(frameInsertar):
    Label(frameInsertar, text = "Cedula", font=("Arial",14,"bold")).grid(row= 0,column=0)
    cedula = StringVar()
    Entry(frameInsertar,textvariable=cedula).grid(row=0,column=1)
    cedula = cedula.get()
    return cedula

def cedulaInserAux(frameInsertar):
    cedula = cedulaInser(frameInsertar)
    cedula = cedula.replace("-","")
    formato = r"[1-9]{1}-[1-9]{4}-[1-9]{4}"
    for i in cedula:
        if i.isdigit() == False:
            return (False,"Los datos ingresados nada mas deben ser numneros")
    if int(cedula[0]) != 0:
        return (False,"El primer dato de la cedula debe ser diferente a 0")
    elif formato == cedula:
        return (True,cedula)
    else:
        return (False,"Formato invalido ejemplo formato correcto #-####-####")
    
def nombreInser(frameInsertar):
    Label(frameInsertar, text = "Nombre completo", font=("Arial",14,"bold")).grid(row= 1,column=0)
    nombre = StringVar()
    Entry(frameInsertar,textvariable=nombre).grid(row=1,column=1)
    return nombre

def fechaNacimientoInser(frameInsertar):
    Label(frameInsertar, text = "Fecha de nacimiento", font=("Arial",14,"bold")).grid(row= 2,column=0)
    fechaNacimiento = StringVar()
    Entry(frameInsertar,textvariable= fechaNacimiento).grid(row=2,column=1)
    return fechaNacimiento

def tipoSangreInser(frameInsertar):
    Label(frameInsertar, text = "Tipo de sangre", font=("Arial",14,"bold")).grid(row= 3,column=0)
    tipoSangre = StringVar()
    ttk.Combobox(frameInsertar,textvariable=tipoSangre,
        values=["O+","O-","A+","A-","B+","B-","AB+","AB-"]
        ).grid(row=3, column = 1)
    return tipoSangre

def sexoInser(frameInsertar):
    frameSexo = Frame(frameInsertar, bg = "white", bd = 5)
    Label(frameSexo, text = "Sexo", font=("Arial",14,"bold")).grid(row= 0,column=0)
    sexo = BooleanVar()
    Radiobutton(frameSexo, text= "Masculino",variable=sexo,value = True).grid(row=0,column=1)
    Radiobutton(frameSexo, text= "Femenino",variable=sexo,value = False).grid(row=1,column=1)
    frameSexo.grid(row=4)
    return sexo

def pesoInser(frameInsertar):
    Label(frameInsertar, text = "Peso(kg)", font=("Arial",14,"bold")).grid(row= 5,column=0)
    peso = StringVar()
    Entry(frameInsertar,textvariable=peso).grid(row=5,column=1)
    return peso

def telefonoInser(frameInsertar):
    Label(frameInsertar, text = "Telefono", font=("Arial",14,"bold")).grid(row= 6,column=0)
    telefono = StringVar()
    Entry(frameInsertar,textvariable= telefono).grid(row=6,column=1)
    return telefono

def correoInser(frameInsertar):
    Label(frameInsertar, text = "Correo", font=("Arial",14,"bold")).grid(row= 7,column=0)
    correo = StringVar()
    Entry(frameInsertar,textvariable=correo).grid(row=7,column=1)
    return correo

def registrar(donantes,cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo):
    donantes.append([cedula.get(),nombre.get(),fechaNacimiento.get(),tipoSangre.get(),
        sexo.get(),peso.get(),telefono.get(),correo.get() ])
    print(donantes)
def limpiar(cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo):
    cedula.set("")
    nombre.set("")
    fechaNacimiento.set("")
    tipoSangre.set("")
    sexo.set(True)
    peso.set("")
    telefono.set("")
    correo.set("")
def salirInser(ventanaInsertar):
    ventanaInsertar.destroy()
def crearBotones(frameBotones,ventanaInsertar,donantes,cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo):
    Button(frameBotones,text="Registrar",font=("Arial",12,"bold"),
        bg="#97e6df",fg="black",
        command=lambda: registrar(donantes,cedula,nombre,fechaNacimiento,
            tipoSangre,sexo,peso,telefono,correo)
    ).grid(row=0,column=0)
    Button(frameBotones,text="Limpiar",
        font=("Arial",12,"bold"),bg="#97e6df",fg="black",
        command=lambda: limpiar(cedula,nombre,fechaNacimiento,
            tipoSangre,sexo,peso,telefono,correo)
            ).grid(row=0,column=1)
    Button(frameBotones,
        text="Salir",
        font=("Arial",12,"bold"),
        bg="#97e6df",
        fg="black",
        command=lambda: salirInser(ventanaInsertar)
    ).grid(row=0,column=2)
def insertarDonador(donantes):
    ventanaInsertar=Toplevel()
    ventanaInsertar.title("Insertar donador")
    ventanaInsertar.geometry("700x600")
    ventanaInsertar.config(bg="#F0BEBE")
    frameInsertar=Frame(ventanaInsertar,bg="#D8FFF5",bd=5)
    frameInsertar.pack(pady=20)
    cedula=cedulaInser(frameInsertar)
    nombre=nombreInser(frameInsertar)
    fechaNacimiento=fechaNacimientoInser(frameInsertar)
    tipoSangre=tipoSangreInser(frameInsertar)
    sexo=sexoInser(frameInsertar)
    peso=pesoInser(frameInsertar)
    telefono=telefonoInser(frameInsertar)
    correo=correoInser(frameInsertar)
    frameBotones=Frame(ventanaInsertar,bg="#DEFDFF",bd=5)
    frameBotones.pack(pady=20)
    crearBotones(frameBotones,ventanaInsertar,donantes,cedula,nombre,fechaNacimiento,tipoSangre,sexo,peso,telefono,correo)

def generar():
    print("Generar donadores")

def actualizar():
    print("Actualizar donador")

def eliminar():
    print("Eliminar donador")

def lugares():
    print("Insertar lugar")

def reportes(donantes):
    print(donantes)

def salir():
    ventana.destroy()

# ---------------- BOTONES ----------------
Button(frame_menu,text="1. Insertar donador",font=("Arial",14),
    width=30,height=2,bg="#77c1ec",fg="white",
    command=lambda:insertarDonador(donantes)).grid(row=1,column=0)
Button(frame_menu,text="2. Generar donadores",font=("Arial",14),
    width=30,height=2,bg="#77c1ec",fg="white",command=generar).grid(row=1,column=1)
Button(frame_menu,text="3. Actualizar datos",font=("Arial",14),
    width=30,height=2,bg="#77c1ec",fg="white",command=actualizar).grid(row=2,column=0)
Button(frame_menu,text="4. Eliminar donador",font=("Arial",14),
    width=30,height=2,bg="#77c1ec",fg="white",
    command=eliminar).grid(row=2,column=1)
Button(frame_menu,text="5. Insertar lugar",font=("Arial",14),
    width=30,height=2,bg="#77c1ec",fg="white",command=lugares).grid(row=3,column=0)
Button(frame_menu,text="6. Reportes",font=("Arial",14),width=30,
    height=2,bg="#77c1ec",fg="white",command=lambda:reportes(donantes)).grid(row=3,column=1)
Button(frame_menu,text="7. Salir",font=("Arial",14),width=30,
    height=2,bg="#62D885",fg="white",command=salir).grid(row=4)
# ---------------- FOOTER ----------------
footer = Label(ventana,text="TEC - Taller de Programación",
    font=("Arial black",12),bg="#ffffff",fg="black")
footer.pack(side="bottom",pady=10)
# ---------------- EJECUTAR ----------------
ventana.mainloop()
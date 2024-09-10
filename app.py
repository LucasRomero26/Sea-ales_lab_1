import streamlit as st
from pathlib import Path
import base64
import matplotlib.pyplot as plt
import numpy as np

# Configuración inicial de la página
st.set_page_config(
    page_title='Streamlit cheat sheet',
    # layout="wide",
    initial_sidebar_state="expanded",

)

# ---------------------------------------------------------------Funcion encargada de la graficación--------------------------------------

def Graf_EscDes(n,x_n,n_des,n_esc,n_desI,x_nesc,Valor_des,Valor_esc,inv,Inter_P):

    def limites():

       x_min=np.min(x_n)                                                           # Ya que la funcion np.max y np.min no son buenas comparando numeros enteros. Se debe extraer primero
       x_max=np.max(x_n)                                                           # Todos los minimos y maximos.
       n_min=np.min(n)
       n_max=np.max(n)
       n_des_min=np.min(n_des)
       n_des_max=np.max(n_des)
       n_esc_min=np.min(n_esc)
       n_esc_max=np.max(n_esc)
       n_desI_min=np.min(n_desI)
       n_desI_max=np.max(n_desI)

       y_min=min(n_min,n_des_min,n_esc_min,n_desI_min)                             # Todos limites derechos y izquierdos se comparan y se conservan los de mayor magnitud.
       y_max=max(n_max,n_des_max,n_esc_max,n_desI_max)

       plt.axis([y_min-2,y_max+2,x_min-2,x_max+2])


    if (Valor_des<0):
        sig_lable='-'
    else:
        sig_lable='+'

    if (np.abs(Valor_esc)>1):

        tipo_lable=' '
    else:

      if (Inter_P==1):
            tipo_lable='(Interpolacion Cero)'
      elif (Inter_P==2):
            tipo_lable='(Interpolacion Escalón)'
      elif (Inter_P==3):
            tipo_lable='(Interpolacion Lineal)'

    #-----------------------------------Dimenciones de la Graficas----------------------------------------

    if (inv==False):
        plt.figure(figsize=(15,5))
    else:
        plt.figure(figsize=(15,12))

    if (inv==False):
        plt.subplot(1,3,1)
    else:
        plt.subplot(2,2,1)

    #---------------------------------------Grafica señal Original-------------------------------------

    plt.stem(n,x_n,basefmt=" ", label=f'$x[n]$')
    plt.title("Señal Discreta")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limites()
    plt.grid(True)
    plt.legend()

    #---------------------------------------Grafica señal Escalada-------------------------------------

    if (inv==False):
     plt.subplot(1,3,2)
    else:
     plt.subplot(2,2,2)

    plt.stem(n_esc,x_nesc,linefmt='r', basefmt=" ", label=f'$x[{np.abs(Valor_esc)}n]$')
    plt.title(f'Señal Discreta Escalada {tipo_lable}')
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limites()
    plt.grid(True)
    plt.legend()

     #---------------------------------------Grafica señal Desplazada-------------------------------------

    if (inv==False):
     plt.subplot(1,3,3)
    else:
     plt.subplot(2,2,3)

    plt.stem(n_des,x_nesc,linefmt='g', basefmt=" ", label=f'$x[{np.abs(Valor_esc)}n{sig_lable}{np.abs(Valor_des)}]$')
    plt.title("Señal Discreta Desplazada")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limites()
    plt.grid(True)
    plt.legend()

   #---------------------------------------Grafica señal Reflejada-------------------------------------

    if (inv==True):

     plt.subplot(2,2,4)
     plt.stem(n_desI,x_nesc,linefmt='g', basefmt=" ", label=f'$x[{Valor_esc}n{sig_lable}{np.abs(Valor_des)}]$')
     plt.title("Señal Discreta Reflejada")
     plt.xlabel("Tiempo (s)")
     plt.ylabel("Amplitud")
     limites()
     plt.grid(True)
     plt.legend()

#---------------------------------------------------------------Funcion encargada de la interpolacion Lineal-------------------------------

def interpolacion_lineal(n1, x_n1, n2, x_n2, n):

    # Fórmula de interpolación lineal
    sol = x_n1 + (x_n2 - x_n1) * (n - n1) / (n2 - n1)
    return sol

#---------------------------------------------------------------Funcion de Traformacion Metodo 1---------------------------------------------------

def Trasform_EscDes(n,x_n,Valor_esc,Valor_des,Inter_P=1,Grafic=True,Lock=True):

 #----------------------------------------------Escalado---------------------------------------------------#

    if (np.abs(Valor_esc)>1):

     n_esc = np.array([x // (np.abs(Valor_esc)) for x in n if x % np.abs(Valor_esc) == 0])          # Se crea el vector de n escalado. Se aplica la division entera del valor abs de a
                                                                                                    # factor de escalado para cada dato de el vector de n, pero solo se guardan
                                                                                                    # los resultados enteros.

     x_nesc = np.array([x_n[np.digitize(np.abs(Valor_esc)*i, n) - 1] for i in n_esc])          # Se arma el vector de amplitudes diezmado. Primero se toma cada valor de n escalado y se regresa
                                                                                               # a su valor original. Luego se busca el indice de ese valor en el vector n sin escalar
                                                                                               # Para esto se usa la funcion digitize (). Como las dimeciones de n y X[n] son las misma,
                                                                                               # basta con este indice para extraer el valor de x[n] correspondiente.
    else:

     Z=int(1/np.abs(Valor_esc))                                                               # El factor que se multiplica cada valor de tiempo es 1/M.
     n_esc=np.arange(np.min(n)*Z,np.max(n)*Z+1,dtype=int)                                     # Se escala el vector n.
     L_n=len(n)                                                                               # Longitud del vector n.
     L_nesc=len(n_esc)                                                                        # Longitud del vector n escalado.

     x_nesc = np.arange(1,L_nesc+1,dtype=float)                                               # Se crea un vector para las amplitudes de la señal escalada.

     for k in range(L_nesc):                                                                  # Se analiza los indeces del vector n escalado.

       if k % Z ==0:                                                                          # Si la señal se expandio un factor de Z entonces los indices multiplos de Z seran los
                                                                                              # indices de las Muestras expandidas. Sino entonces los indices son de aquellas muetras que
                                                                                              # Deben interpolarse.
         r=int(k*np.abs(Valor_esc))
         x_nesc[k]=x_n[r]

       else:                                                                                   # Define el metodo de interpolacion

          if (Inter_P==1):
             x_nesc[k]=0
          elif (Inter_P==2):
             x_nesc[k]=x_nesc[k-1]
          elif (Inter_P==3):
             x_nesc[k]=interpolacion_lineal(n_esc[r*Z], x_n[r], n_esc[(r+1)*Z], x_n[r+1], n_esc[k]) # Formula de interpolación

 #--------------------------------------------Desplazamiento-----------------------------------------------#

    if (Valor_des % np.abs(Valor_esc) != 0 ) and (Lock==True):
      return print("¡Error no es posible desplazar en un valor no entero!")

    N_0=int(Valor_des/np.abs(Valor_esc))

    n_des=n_esc-(N_0)                                                                # Restar el valor del desplazamiento basta para obtener el vecto n desplazado
                                                                                    # Si N0>0 se presenta un adelanto. Si N0<0 se presenta un atraso.

 #----------------------------------------------Invercion---------------------------------------------------#

    if (Valor_esc<0):                                                                         # Si el señal debe reflejarse se invierte la dirrecio del vector n escalado.
      n_desI=-n_des
      Key_inv=True

      n_des_retur=np.flip(n_desI)                                                            # np.flip invierte el orden de los datos de n_esc y x_nesc
      x_nesc_retur=np.flip(x_nesc)

    else:

      n_desI=n_des
      Key_inv=False

      n_des_retur=n_des
      x_nesc_retur=x_nesc

 #----------------------------------------------Salida-----------------------------------------------------#

    if (Grafic==True):

     Graf_EscDes(n,x_n,n_des,n_esc,n_desI,x_nesc,Valor_des,Valor_esc,Key_inv,Inter_P)   # En el caso de que se desse graficar el parametro Grafic=True [Por defecto] y la funcion graficara la trasformacion.

    else:

      return  n_des_retur, x_nesc_retur                                                  # En el caso de que desee obtener los valores de la señal trasformada el parametro Grafic=False y la
                                                                                         # Funcion entregara una tubla con los valores de n escala y x[n] escala.

#---------------------------------------Funcion para graficar tres señales-----------------------------------------------

def Graf_3Sig_Op(n1,x1,n2,x2,n3,x3,Suma=True):

    def limitesSig_Op():

     n1_min=np.min(n1)
     n1_max=np.max(n1)
     n2_min=np.min(n2)
     n2_max=np.max(n2)
     n3_min=np.min(n3)
     n3_max=np.max(n3)
     x1_min=np.min(x1)
     x1_max=np.max(x1)
     x2_min=np.min(x2)
     x2_max=np.max(x2)
     x3_min=np.min(x3)
     x3_max=np.max(x3)

     y_min=min(n1_min,n2_min,n3_min)
     y_max=max(n1_max,n2_max,n3_max)
     x_min=min(x1_min,x2_min,x3_min)
     x_max=max(x1_max,x2_max,x3_max)

     plt.axis([y_min-2,y_max+2,x_min-2,x_max+2])

    plt.figure(figsize=(15,12))

    plt.subplot(2,2,1)
    plt.stem(n1,x1,basefmt=" ", label=f'$x_{1}[n]$')
    plt.title(f"Señal Discreta $x_{1}[n]$")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limitesSig_Op()
    plt.grid(True)
    plt.legend()

    plt.subplot(2,2,2)
    plt.stem(n2,x2,linefmt='r',basefmt=" ", label=f'$x_{2}[n]$')
    plt.title(f"Señal Discreta $x_{2}[n]$")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limitesSig_Op()
    plt.grid(True)
    plt.legend()


    plt.subplot(2,2,3)
    plt.stem(n1,x1,linefmt="b", basefmt=" ", label=f'$x_{1}[n]$')

    if (Suma==True):

     plt.stem(n2,x2,linefmt="r",basefmt=" ", label=f'$x_{2}[n]$')
     plt.title(f"Señal Discreta $x_{1}[n]+x_{2}[n]$")
    else:

     plt.stem(n2,-x2,linefmt="r",basefmt=" ", label=f'$-x_{2}[n]$')
     plt.title(f"Señal Discreta $x_{1}[n]-x_{2}[n]$")

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limitesSig_Op()
    plt.grid(True)
    plt.legend()

    plt.subplot(2,2,4)
    plt.stem(n3,x3,linefmt='g',basefmt=" ", label=f'$x_{3}[n]$')
    plt.title(f"Señal Discreta $x_{3}[n]$")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limitesSig_Op()
    plt.grid(True)
    plt.legend()

#--------------------------------------Funcion para Operar señales--------------------------------------------------------

def Operacion_Señales(n1,x1,n2,x2,Operacion=True,Grafic=True):

    # Como muchas veces las dimenciones no concuerdan debemos redefinir la señal mas pequeña a la misma longitud de la mas grande.
    # No es escalar la señal, porque la posicion de los valores debe respetarse. En pocas palabras la señal no se "estira".


    #-----------------------------------------Preparan las funciones-----------------------------------------------

  Min_n1=np.min(n1)
  Max_n1=np.max(n1)

  Min_n2=np.min(n2)
  Max_n2=np.max(n2)

  n_op=np.arange(min(Min_n1,Min_n2),max(Max_n1,Max_n2)+1)                         # El vector comun n donde se realizara la operacion. Si la longitud de las partes es el mismo
                                                                                  # resultara en el mismo n.

  x1_op=np.zeros(len(n_op),dtype=float)                                            # Se crean los vectores para contener la amplitud de las señales a operar. Rellenar con cero
  x2_op=np.zeros(len(n_op),dtype=float)                                            # incialmente es convenienete. Proximamamente se adicionaran las amplitudes de x1 y x2

  x1_op[np.isin(n_op, n1)] = x1                                                   # La función np.isin comprueba la presencia de elementos de n1 (o n2) en np.op y genera un array
                                                                                  # booleano de la misma longitud de n.op que indica si cada elemento n1 se encuentra en n.op.
                                                                                  # --->[True, False, False, True,.....]
                                                                                  # Esta instruccion asigna todos los elementos de x1 a x1_op. En orden los valores de x1
                                                                                  # tendran las mismas pocisiones que el array booleano marca como True. Las pocisiones False
                                                                                  # mantendran el cero inicial.
  x2_op[np.isin(n_op, n2)] = x2

 #---------------------------------------Operar----------------------------------------------------------------

  if (Operacion==True):                                                            # Si Operacion = True [Por defecto] se hara una suma. Si Operacion = False se hara una resta.
    x_op=x1_op+x2_op
  else:
    x_op=x1_op-x2_op

 #----------------------------------------------Salida-----------------------------------------------------#

  if (Grafic==True):

    Graf_3Sig_Op(n1,x1,n2,x2,n_op,x_op,Operacion)                                 # En el caso de que se desse graficar el parametro Grafic=True [Por defecto] y la funcion graficara la trasformacion.

  else:
    return n_op,x_op



#---------------------------------------Funcion para graficar tres señales-----------------------------------------------

def Graf_3Sig_Op(n1,x1,n2,x2,n3,x3,Suma=True):

    def limitesSig_Op():

     n1_min=np.min(n1)
     n1_max=np.max(n1)
     n2_min=np.min(n2)
     n2_max=np.max(n2)
     n3_min=np.min(n3)
     n3_max=np.max(n3)
     x1_min=np.min(x1)
     x1_max=np.max(x1)
     x2_min=np.min(x2)
     x2_max=np.max(x2)
     x3_min=np.min(x3)
     x3_max=np.max(x3)

     y_min=min(n1_min,n2_min,n3_min)
     y_max=max(n1_max,n2_max,n3_max)
     x_min=min(x1_min,x2_min,x3_min)
     x_max=max(x1_max,x2_max,x3_max)

     plt.axis([y_min-2,y_max+2,x_min-2,x_max+2])

    plt.figure(figsize=(15,12))

    plt.subplot(2,2,1)
    plt.stem(n1,x1,basefmt=" ", label=f'$x_{1}[n]$')
    plt.title(f"Señal Discreta $x_{1}[n]$")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limitesSig_Op()
    plt.grid(True)
    plt.legend()

    plt.subplot(2,2,2)
    plt.stem(n2,x2,linefmt='r',basefmt=" ", label=f'$x_{2}[n]$')
    plt.title(f"Señal Discreta $x_{2}[n]$")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limitesSig_Op()
    plt.grid(True)
    plt.legend()


    plt.subplot(2,2,3)
    plt.stem(n1,x1,linefmt="b", basefmt=" ", label=f'$x_{1}[n]$')

    if (Suma==True):

     plt.stem(n2,x2,linefmt="r",basefmt=" ", label=f'$x_{2}[n]$')
     plt.title(f"Señal Discreta $x_{1}[n]+x_{2}[n]$")
    else:

     plt.stem(n2,-x2,linefmt="r",basefmt=" ", label=f'$-x_{2}[n]$')
     plt.title(f"Señal Discreta $x_{1}[n]-x_{2}[n]$")

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limitesSig_Op()
    plt.grid(True)
    plt.legend()

    plt.subplot(2,2,4)
    plt.stem(n3,x3,linefmt='g',basefmt=" ", label=f'$x_{3}[n]$')
    plt.title(f"Señal Discreta $x_{3}[n]$")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limitesSig_Op()
    plt.grid(True)
    plt.legend()

#--------------------------------------Funcion para Operar señales--------------------------------------------------------

def Operacion_Señales(n1,x1,n2,x2,Operacion=True,Grafic=True):

    # Como muchas veces las dimenciones no concuerdan debemos redefinir la señal mas pequeña a la misma longitud de la mas grande.
    # No es escalar la señal, porque la posicion de los valores debe respetarse. En pocas palabras la señal no se "estira".


    #-----------------------------------------Preparan las funciones-----------------------------------------------

  Min_n1=np.min(n1)
  Max_n1=np.max(n1)

  Min_n2=np.min(n2)
  Max_n2=np.max(n2)

  n_op=np.arange(min(Min_n1,Min_n2),max(Max_n1,Max_n2)+1)                         # El vector comun n donde se realizara la operacion. Si la longitud de las partes es el mismo
                                                                                  # resultara en el mismo n.

  x1_op=np.zeros(len(n_op),dtype=float)                                            # Se crean los vectores para contener la amplitud de las señales a operar. Rellenar con cero
  x2_op=np.zeros(len(n_op),dtype=float)                                            # incialmente es convenienete. Proximamamente se adicionaran las amplitudes de x1 y x2

  x1_op[np.isin(n_op, n1)] = x1                                                   # La función np.isin comprueba la presencia de elementos de n1 (o n2) en np.op y genera un array
                                                                                  # booleano de la misma longitud de n.op que indica si cada elemento n1 se encuentra en n.op.
                                                                                  # --->[True, False, False, True,.....]
                                                                                  # Esta instruccion asigna todos los elementos de x1 a x1_op. En orden los valores de x1
                                                                                  # tendran las mismas pocisiones que el array booleano marca como True. Las pocisiones False
                                                                                  # mantendran el cero inicial.
  x2_op[np.isin(n_op, n2)] = x2

 #---------------------------------------Operar----------------------------------------------------------------

  if (Operacion==True):                                                            # Si Operacion = True [Por defecto] se hara una suma. Si Operacion = False se hara una resta.
    x_op=x1_op+x2_op
  else:
    x_op=x1_op-x2_op

 #----------------------------------------------Salida-----------------------------------------------------#

  if (Grafic==True):

    Graf_3Sig_Op(n1,x1,n2,x2,n_op,x_op,Operacion)                                 # En el caso de que se desse graficar el parametro Grafic=True [Por defecto] y la funcion graficara la trasformacion.

  else:
    return n_op,x_op

# Función para convertir imagen a bytes
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

#Funciones Discretas

# ---------------------------------------------------------------Funcion encargada de la graficación--------------------------------------

def Graf_DesEsc(n,x_n,n_des,n_esc,n_escI,x_nesc,Valor_des,Valor_esc,inv,Inter_P):


    def limites():

       x_min=np.min(x_n)                                                           # Ya que la funcion np.max y np.min no son buenas comparando numeros enteros. Se debe extraer primero
       x_max=np.max(x_n)                                                           # Todos los minimos y maximos.
       n_min=np.min(n)
       n_max=np.max(n)
       n_des_min=np.min(n_des)
       n_des_max=np.max(n_des)
       n_esc_min=np.min(n_esc)
       n_esc_max=np.max(n_esc)
       n_escI_min=np.min(n_escI)
       n_escI_max=np.max(n_escI)

       y_min=min(n_min,n_des_min,n_esc_min,n_escI_min)                             # Todos limites derechos y izquierdos se comparan y se conservan los de mayor magnitud.
       y_max=max(n_max,n_des_max,n_esc_max,n_escI_max)

       plt.axis([y_min-2,y_max+2,x_min-2,x_max+2])


    if (Valor_des<0):
        sig_lable='-'
    else:
        sig_lable='+'

    if (np.abs(Valor_esc)>1):

        tipo_lable=' '
    else:

      if (Inter_P==1):
            tipo_lable='(Interpolacion Cero)'
      elif (Inter_P==2):
            tipo_lable='(Interpolacion Escalón)'
      elif (Inter_P==3):
            tipo_lable='(Interpolacion Lineal)'

    #-----------------------------------Dimenciones de la Graficas----------------------------------------

    if (inv==False):
        plt.figure(figsize=(15,5))
    else:
        plt.figure(figsize=(15,12))

    if (inv==False):
        plt.subplot(1,3,1)
    else:
        plt.subplot(2,2,1)

    #---------------------------------------Grafica señal Original-------------------------------------

    plt.stem(n,x_n,basefmt=" ", label=f'$x[n]$')
    plt.title("Señal Discreta")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limites()
    plt.grid(True)
    plt.legend()

    #---------------------------------------Grafica señal Desplazada-------------------------------------

    if (inv==False):
     plt.subplot(1,3,2)
    else:
     plt.subplot(2,2,2)

    plt.stem(n_des,x_n,linefmt='r', basefmt=" ", label=f'$x[n{sig_lable}{np.abs(Valor_des)}]$')
    plt.title("Señal Discreta Desplazada")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limites()
    plt.grid(True)
    plt.legend()

    #---------------------------------------Grafica señal Escalada-------------------------------------

    if (inv==False):
     plt.subplot(1,3,3)
    else:
     plt.subplot(2,2,3)

    plt.stem(n_esc,x_nesc,linefmt='g', basefmt=" ", label=f'$x[{np.abs(Valor_esc)}n{sig_lable}{np.abs(Valor_des)}]$')
    plt.title(f'Señal Discreta Escalada {tipo_lable}')
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limites()
    plt.grid(True)
    plt.legend()

   #---------------------------------------Grafica señal Reflejada-------------------------------------

    if (inv==True):

     plt.subplot(2,2,4)
     plt.stem(n_escI,x_nesc,linefmt='g', basefmt=" ", label=f'$x[{Valor_esc}n{sig_lable}{np.abs(Valor_des)}]$')
     plt.title("Señal Discreta Reflejada")
     plt.xlabel("Tiempo (s)")
     plt.ylabel("Amplitud")
     limites()
     plt.grid(True)
     plt.legend()

#---------------------------------------------------------------Funcion encargada de la interpolacion Lineal-------------------------------

def interpolacion_lineal(n1, x_n1, n2, x_n2, n):

    # Fórmula de interpolación lineal
    sol = x_n1 + (x_n2 - x_n1) * (n - n1) / (n2 - n1)
    return sol

#---------------------------------------------------------------Funcion de Traformacion Metodo 1---------------------------------------------------

def Trasform_DesEsc(n,x_n,Valor_esc,Valor_des,Inter_P=1,Grafic=True):

 #--------------------------------------------Desplazamiento-----------------------------------------------#

 n_des=n-(Valor_des)                                                                  # Restar el valor del desplazamiento basta para obtener el vecto n desplazado
                                                                                      # Si n0>0 se presenta un adelanto. Si n0<0 se presenta un atraso.

 #----------------------------------------------Escalado---------------------------------------------------#

 if (np.abs(Valor_esc)>1):

    n_esc = np.array([x // (np.abs(Valor_esc)) for x in n_des if x % np.abs(Valor_esc) == 0])        # Se crea el vector de n escalado. Se aplica la division entera del valor abs de a
                                                                                                     # factor de escalado para cada dato de el vector de n desplazado, pero solo se guardan
                                                                                                     # los resultados enteros.

    x_nesc = np.array([x_n[np.digitize(np.abs(Valor_esc)*i, n_des) - 1] for i in n_esc])      # Se arma el vector de amplitudes diezmado. Primero se toma cada valor de n escalado y se regresa
                                                                                              # a su valor original. Luego se busca el indice de ese valor en el vector n sin escalar
                                                                                              # Para esto se usa la funcion digitize (). Como las dimeciones de n y X[n] son las misma,
                                                                                              # basta con este indice para extraer el valor de x[n] correspondiente.

 else:

    Z=int(1/np.abs(Valor_esc))                                                       # El factor que se multiplica cada valor de tiempo es 1/M.
    n_esc=np.arange(np.min(n_des)*Z,np.max(n_des)*Z+1)                               # Se escala el vector n desplazado.
    L_ndes=len(n_des)                                                                # Longitud del vector n desplazado.
    L_nesc=len(n_esc)                                                                # Longitud del vector n escalado.

    x_nesc = np.arange(1,L_nesc+1,dtype=float)                                       # Se crea un vector para las amplitudes de la señal escalada.

    for k in range(L_nesc):                                                          # Se analiza los indeces del vector n escalado.

        if k % Z ==0:                                                                # Si la señal se expandio un factor de Z entonces los indices multiplos de Z seran los
                                                                                     # indices de las Muestras expandidas. Sino entonces los indices son de aquellas muetras que
                                                                                     # Deben interpolarse.

         r=int(k*np.abs(Valor_esc))

         x_nesc[k]=x_n[r]

        else:

         if (Inter_P==1):                                                         # Define el metodo de interpolacion  (Inter_P=1 [Por defecto]-->Interpolacion con 0)
            x_nesc[k]=0                                                           #                                    (Inter_P=2--> Interpolacion Escalon)
         elif (Inter_P==2):                                                       #                                    (Inter_P=3--> Interpolacion Lineal)
            x_nesc[k]=x_nesc[k-1]
         elif (Inter_P==3):
            x_nesc[k]=interpolacion_lineal(n_esc[r*Z], x_n[r], n_esc[(r+1)*Z], x_n[r+1], n_esc[k]) # Formula de interpolación

 #----------------------------------------------Invercion---------------------------------------------------#

 if (Valor_esc<0):                                                                         # Si el señal debe reflejarse se invierte la direccion del vector n escalado.
    n_escI=-n_esc
    Key_inv=True

    n_esc_retur=np.flip(n_escI)                                                            # np.flip invierte el orden de los datos de n_esc y x_nesc.
    x_nesc_retur=np.flip(x_nesc)

 else:
    n_escI=n_esc
    Key_inv=False

    n_esc_retur=n_esc
    x_nesc_retur=x_nesc

  #----------------------------------------------Salida-----------------------------------------------------#

 if (Grafic==True):

    Graf_DesEsc(n,x_n,n_des,n_esc,n_escI,x_nesc,Valor_des,Valor_esc,Key_inv,Inter_P)   # En el caso de que se desse graficar el parametro Grafic=True [Por defecto] y la funcion graficara la trasformacion.

 else:

    return n_esc_retur, x_nesc_retur                                                   # En el caso de que desee obtener los valores de la señal trasformada el parametro Grafic=False y la
                                                                                       # Funcion entregara una tubla con los valores de n escala y x[n] escala.

# ---------------------------------------------------------------Funcion encargada de la graficación--------------------------------------

def Graf_EscDes(n,x_n,n_des,n_esc,n_desI,x_nesc,Valor_des,Valor_esc,inv,Inter_P):

    def limites():

       x_min=np.min(x_n)                                                           # Ya que la funcion np.max y np.min no son buenas comparando numeros enteros. Se debe extraer primero
       x_max=np.max(x_n)                                                           # Todos los minimos y maximos.
       n_min=np.min(n)
       n_max=np.max(n)
       n_des_min=np.min(n_des)
       n_des_max=np.max(n_des)
       n_esc_min=np.min(n_esc)
       n_esc_max=np.max(n_esc)
       n_desI_min=np.min(n_desI)
       n_desI_max=np.max(n_desI)

       y_min=min(n_min,n_des_min,n_esc_min,n_desI_min)                             # Todos limites derechos y izquierdos se comparan y se conservan los de mayor magnitud.
       y_max=max(n_max,n_des_max,n_esc_max,n_desI_max)

       plt.axis([y_min-2,y_max+2,x_min-2,x_max+2])


    if (Valor_des<0):
        sig_lable='-'
    else:
        sig_lable='+'

    if (np.abs(Valor_esc)>1):

        tipo_lable=' '
    else:

      if (Inter_P==1):
            tipo_lable='(Interpolacion Cero)'
      elif (Inter_P==2):
            tipo_lable='(Interpolacion Escalón)'
      elif (Inter_P==3):
            tipo_lable='(Interpolacion Lineal)'

    #-----------------------------------Dimenciones de la Graficas----------------------------------------

    if (inv==False):
        plt.figure(figsize=(15,5))
    else:
        plt.figure(figsize=(15,12))

    if (inv==False):
        plt.subplot(1,3,1)
    else:
        plt.subplot(2,2,1)

    #---------------------------------------Grafica señal Original-------------------------------------

    plt.stem(n,x_n,basefmt=" ", label=f'$x[n]$')
    plt.title("Señal Discreta")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limites()
    plt.grid(True)
    plt.legend()

    #---------------------------------------Grafica señal Escalada-------------------------------------

    if (inv==False):
     plt.subplot(1,3,2)
    else:
     plt.subplot(2,2,2)

    plt.stem(n_esc,x_nesc,linefmt='r', basefmt=" ", label=f'$x[{np.abs(Valor_esc)}n]$')
    plt.title(f'Señal Discreta Escalada {tipo_lable}')
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limites()
    plt.grid(True)
    plt.legend()

     #---------------------------------------Grafica señal Desplazada-------------------------------------

    if (inv==False):
     plt.subplot(1,3,3)
    else:
     plt.subplot(2,2,3)

    plt.stem(n_des,x_nesc,linefmt='g', basefmt=" ", label=f'$x[{np.abs(Valor_esc)}n{sig_lable}{np.abs(Valor_des)}]$')
    plt.title("Señal Discreta Desplazada")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    limites()
    plt.grid(True)
    plt.legend()

   #---------------------------------------Grafica señal Reflejada-------------------------------------

    if (inv==True):

     plt.subplot(2,2,4)
     plt.stem(n_desI,x_nesc,linefmt='g', basefmt=" ", label=f'$x[{Valor_esc}n{sig_lable}{np.abs(Valor_des)}]$')
     plt.title("Señal Discreta Reflejada")
     plt.xlabel("Tiempo (s)")
     plt.ylabel("Amplitud")
     limites()
     plt.grid(True)
     plt.legend()

#---------------------------------------------------------------Funcion encargada de la interpolacion Lineal-------------------------------

def interpolacion_lineal(n1, x_n1, n2, x_n2, n):

    # Fórmula de interpolación lineal
    sol = x_n1 + (x_n2 - x_n1) * (n - n1) / (n2 - n1)
    return sol

#---------------------------------------------------------------Funcion de Traformacion Metodo 1---------------------------------------------------

def Trasform_EscDes(n,x_n,Valor_esc,Valor_des,Inter_P=1,Grafic=True,Lock=True):

 #----------------------------------------------Escalado---------------------------------------------------#

    if (np.abs(Valor_esc)>1):

     n_esc = np.array([x // (np.abs(Valor_esc)) for x in n if x % np.abs(Valor_esc) == 0])          # Se crea el vector de n escalado. Se aplica la division entera del valor abs de a
                                                                                                    # factor de escalado para cada dato de el vector de n, pero solo se guardan
                                                                                                    # los resultados enteros.

     x_nesc = np.array([x_n[np.digitize(np.abs(Valor_esc)*i, n) - 1] for i in n_esc])          # Se arma el vector de amplitudes diezmado. Primero se toma cada valor de n escalado y se regresa
                                                                                               # a su valor original. Luego se busca el indice de ese valor en el vector n sin escalar
                                                                                               # Para esto se usa la funcion digitize (). Como las dimeciones de n y X[n] son las misma,
                                                                                               # basta con este indice para extraer el valor de x[n] correspondiente.
    else:

     Z=int(1/np.abs(Valor_esc))                                                               # El factor que se multiplica cada valor de tiempo es 1/M.
     n_esc=np.arange(np.min(n)*Z,np.max(n)*Z+1,dtype=int)                                     # Se escala el vector n.
     L_n=len(n)                                                                               # Longitud del vector n.
     L_nesc=len(n_esc)                                                                        # Longitud del vector n escalado.

     x_nesc = np.arange(1,L_nesc+1,dtype=float)                                               # Se crea un vector para las amplitudes de la señal escalada.

     for k in range(L_nesc):                                                                  # Se analiza los indeces del vector n escalado.

       if k % Z ==0:                                                                          # Si la señal se expandio un factor de Z entonces los indices multiplos de Z seran los
                                                                                              # indices de las Muestras expandidas. Sino entonces los indices son de aquellas muetras que
                                                                                              # Deben interpolarse.
         r=int(k*np.abs(Valor_esc))
         x_nesc[k]=x_n[r]

       else:                                                                                   # Define el metodo de interpolacion

          if (Inter_P==1):
             x_nesc[k]=0
          elif (Inter_P==2):
             x_nesc[k]=x_nesc[k-1]
          elif (Inter_P==3):
             x_nesc[k]=interpolacion_lineal(n_esc[r*Z], x_n[r], n_esc[(r+1)*Z], x_n[r+1], n_esc[k]) # Formula de interpolación

 #--------------------------------------------Desplazamiento-----------------------------------------------#

    if (Valor_des % np.abs(Valor_esc) != 0 ) and (Lock==True):
      return print("¡Error no es posible desplazar en un valor no entero!")

    N_0=int(Valor_des/np.abs(Valor_esc))

    n_des=n_esc-(N_0)                                                                # Restar el valor del desplazamiento basta para obtener el vecto n desplazado
                                                                                    # Si N0>0 se presenta un adelanto. Si N0<0 se presenta un atraso.

 #----------------------------------------------Invercion---------------------------------------------------#

    if (Valor_esc<0):                                                                         # Si el señal debe reflejarse se invierte la dirrecio del vector n escalado.
      n_desI=-n_des
      Key_inv=True

      n_des_retur=np.flip(n_desI)                                                            # np.flip invierte el orden de los datos de n_esc y x_nesc
      x_nesc_retur=np.flip(x_nesc)

    else:

      n_desI=n_des
      Key_inv=False

      n_des_retur=n_des
      x_nesc_retur=x_nesc

 #----------------------------------------------Salida-----------------------------------------------------#

    if (Grafic==True):

     Graf_EscDes(n,x_n,n_des,n_esc,n_desI,x_nesc,Valor_des,Valor_esc,Key_inv,Inter_P)   # En el caso de que se desse graficar el parametro Grafic=True [Por defecto] y la funcion graficara la trasformacion.

    else:

      return  n_des_retur, x_nesc_retur                                                  # En el caso de que desee obtener los valores de la señal trasformada el parametro Grafic=False y la
                                                                                         # Funcion entregara una tubla con los valores de n escala y x[n] escala.

# Funciones para las diferentes páginas
def pagina1():
    st.title("Transformación de Señales")
    st.markdown("Este laboratorio está diseñado para aplicar de manera práctica los conceptos teóricos adquiridos en el curso de Señales y Sistemas. Aquí, tendrás la oportunidad de realizar operaciones básicas de transformación de señales y visualizar los resultados en un entorno gráfico computacional.")
    st.markdown("Para comenzar a utlizar la app dirigete al sidebar en la parte derecha y presiona el selecbox debajo de Funciones de la APP. Alli podras seleccionar con que tipo de señal quieres trabajar, asi como también poder regresar a esta pestaña.")
    # st.image("kuromi.png",width=300,)
    # Centrar la imagen con HTML y CSS
    st.markdown(
        """
        <style>
        .stImage {
            display: flex;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.subheader("Explicación Teorica (Resumen)")
    st.markdown("La transformación de señales hace referencias a las modificaciones que puede recibir una señal en los parámetros que la conforman. Existen dos tipos de transformaciones, por escalamiento y por desplazamiento, las cuales afectan a la amplitud y el tiempo de la señal.\nSe analiza por separado las transformaciones para el tiempo continuo y para el tiempo discreto, ya que existen diferencias relevantes.")
    st.markdown("##### Escalamiento por Amplitud #####")
    st.markdown(r"Una señal $x(t)$ esta siendo escalada por amplitud cuando es multiplicada por un valor $A$, es decir, $Ax(t)$ donde si $|A|$ es mayor que uno, es una amplificación y si es menor que uno es una atenuación, $y(t) = Ax(t)$.")
    st.markdown("##### Desplazamiento en el tiempo #####")
    st.markdown(r"Una señal $x(t)$ es desplazada en el tiempo si la variable $t$ en dicha señal está siendo sumana o restada por un valor $t_0$, donde se translada a la derecha si es $-t_0$, un retardo, o se translada a la izquierda si es un $+t_0$, es decir, un adelanto. Si la señal sufe una reflexión, es decir, que la variable t está siendo multiplicada por menos uno $x(-t)$, las translaciones son en dirección contraria.")
    st.markdown("##### Escalamiento en el tiempo #####")
    st.markdown(r"Una señal $x(t)$ es escalada en el tiempo cuando la variable t es multiplicada por un valor absoluto $|a|$ mayor o menor que uno, es decir, $x(at)$. Si $|a|$ es mayor que 1 la función se comprime ese factor, si es menor que uno la función se expande ese mismo factor. Cada valor de $t$ se multiplica por el inverso de $a$ para obtener los nuevos valores.")
    st.markdown(r"Existen dos maneras de transformar una señal $x(t)$ en el tiempo, primero desplazar y luego escalar en el tiempo, o el proceso contrario.")


def pagina2():
    st.title("Señales Continuas")
    st.write("Bienvenido a la Página de Señales Continuas.")
    
    # Selectbox dentro de la página de señales continuas
    seleccion_continua = st.selectbox("Seleccione la señal continua:", 
                                      ("Señal Continua 1", "Señal Continua 2"))
    if seleccion_continua == "Señal Continua 1":
        st.write("")
        # Datos de las funciones
        # Función 1
        x1 = np.arange(-2, -1, 0.0001)
        y1 = 2 * x1 + 4

        # Función 2
        x2 = np.arange(-1, 1, 0.0001)
        y2 = 2 * x2 / x2
        y2[np.isnan(y2)] = 0  # Manejar la división por cero

        # Función 3
        x3 = np.arange(1, 2, 0.0001)
        y3 = -2 * x3 + 4

        # Concatenación
        x = np.concatenate((x1, x2, x3))
        y = np.concatenate((y1, y2, y3))
        plt.style.use("dark_background")
        fig, ax = plt.subplots()
        fig.patch.set_alpha(0.0)  # Fondo de la figura
        ax.patch.set_alpha(0.0)   # Fondo del área de los ejes
        plt.xlabel('t',fontsize=12)
        plt.ylabel('x(t)',fontsize=12)    
        plt.xticks(np.arange(-2, 2+1, step=1))
        plt.yticks(np.arange(0, 2+1, step=0.5))
        ax.plot(x, y, color="#bf8bff")

        st.pyplot(fig)
        st.header("Método de Transformación")
        seleccion_transformacion1= st.selectbox("Seleccione método de transformación:", 
                                      ("Método 1 (Desplazamiento - Escalamiento)", "Método 2 (Escalamiento - Desplazamiento)"),index=None,placeholder="Seleccione una opción")
        if seleccion_transformacion1 == "Método 1 (Desplazamiento - Escalamiento)":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("")
                seleccion_valores_a1 = st.selectbox("Seleccione un valor de [a]",("-2","-3","-4","-5","-1/2","-1/3","-1/4","-1/5","2","3","4","5","1/2","1/3","1/4","1/5"),index=None,placeholder="Seleccione una opción",)
            with col2:
                st.markdown("")
                seleccion_valores_to1 = st.selectbox("Seleccione un valor de [to]",("-1","-2","-3","-4","-5","-6","1","2","3","4","5","6"),index=None,placeholder="Seleccione una opción",)
            if (seleccion_valores_a1  != None) and (seleccion_valores_to1 != None):
                # Definición de los ejes de tiempos de las funciones a trozos
                delta = 0.01
                t1 = np.arange(-2, -1, delta)
                t2 = np.arange(-1, 1, delta)
                t3 = np.arange(1, 2, delta)

                # Definición de las funciones a trozos
                x1_t = 2 * t1 + 4
                x2_t = 2 * np.ones(len(t2))
                x3_t = -2 * t3 + 4

                # Concatenación de las funciones a trozos
                t_total = np.concatenate((t1, t2, t3))
                x_total = np.concatenate((x1_t, x2_t, x3_t))

                # Gráfico de la señal original
                fig, ax = plt.subplots()
                plt.grid(True, linestyle=':')  # Cuadrícula
                plt.title('Señal Original Continua 1')  # Título
                fig.patch.set_alpha(0.0)  # Fondo de la figura
                ax.patch.set_alpha(0.0)   # Fondo del área de los ejes
                plt.xlabel('t')  # Nombre del eje X
                plt.ylabel('x(t)')  # Nombre del eje Y
                ax.plot(t_total, x_total, color="#bf8bff")
                plt.ylim(0, 2.5)
                st.pyplot(fig)

                # Desplazamiento temporal
                a1 = eval(seleccion_valores_a1)
                to1 = float(seleccion_valores_to1)
                td1 = t_total - to1  # Desplazamiento en el tiempo

                # Gráfico de la señal desplazada
                fig2, ax2 = plt.subplots()
                plt.grid(True, linestyle=':')  # Cuadrícula
                plt.title('Paso 1 (Desplazamiento)')  # Título
                fig2.patch.set_alpha(0.0)  # Fondo de la figura
                ax2.patch.set_alpha(0.0)   # Fondo del área de los ejes
                plt.xlabel('t')  # Nombre del eje X
                plt.ylabel('x(t)')  # Nombre del eje Y
                #Señal Original
                ax2.plot(t_total, x_total, color="#bf8bff", label="Señal Original")
                #Señal Desplazada
                ax2.plot(td1, x_total, color="#ffffff", linestyle='--', label="Señal Desplazada")
                # Agregar la leyenda para distinguir ambas señales
                ax2.legend()
                plt.ylim(0, 2.5)
                st.pyplot(fig2)

                # Escalamiento en el tiempo
                tesc1 = td1 / a1  # tesc: escalamiento en el tiempo

                # Gráfico de la señal desplazada-escalada
                fig3, ax3 = plt.subplots()
                ax3.plot(t_total, x_total, color="#bf8bff", label="Señal Original")
                ax3.plot(tesc1, x_total, color="#e5d0ff",linestyle = "--",label="Señal Desplazada-Escalada")  # Asegurar el uso de x_total para consistencia
                ax3.grid(True, linestyle=':') 
                fig3.patch.set_alpha(0.0)  # Fondo de la figura
                ax3.patch.set_alpha(0.0)   # Fondo del área de los ejes
                ax3.set_title('Paso 2 (Escalamiento)')  # Título corregido
                ax3.set_xlabel('t')  # Nombre del eje X
                ax3.set_ylabel('x(t)')  # Nombre del eje Y
                ax3.legend()
                plt.ylim(0, 2.5)
                st.pyplot(fig3)
            else:
                st.write("No se han completado los campos")
                
        elif seleccion_transformacion1 == "Método 2 (Escalamiento - Desplazamiento)":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("")
                seleccion_valores_a12 = st.selectbox("Seleccione un valor de [a]",("-2","-3","-4","-5","-1/2","-1/3","-1/4","-1/5","2","3","4","5","1/2","1/3","1/4","1/5"),index=None,placeholder="Seleccione una opción",)
            with col2:
                st.markdown("")
                seleccion_valores_to12 = st.selectbox("Seleccione un valor de [to]",("-1","-2","-3","-4","-5","-6","1","2","3","4","5","6"),index=None,placeholder="Seleccione una opción",)
            if (seleccion_valores_a12  != None) and (seleccion_valores_to12 != None):
                #Definición de los ejes de tiempos de las funciones a trozos
                delta=0.01
                t1=np.arange(-2,-1,delta)
                t2=np.arange(-1,1,delta)
                t3=np.arange(1,2,delta)

                #Definición de las funciones a trozos
                x1_t= 2*t1+4
                x2_t= 2*np.ones(len(t2))
                x3_t=-2*t3+4

                #Concatenación de las funciones a trozos
                t1=np.concatenate((t1,t2,t3))
                x1_t=np.concatenate((x1_t,x2_t,x3_t))

                a2=eval(seleccion_valores_a12)
                to2=float(seleccion_valores_to12)

                tesc2=t1/a2 #escalamiento en el tiempo
                td2=tesc2-(to2/a2) #desplazamiento en el tiempo

                fig5, ax5 = plt.subplots()
                ax5.plot(t1,x1_t, color="#bf8bff", label="Señal Original")
                ax5.grid(True, linestyle=':')
                plt.title("Señal Original Continua 1")
                fig5.patch.set_alpha(0.0)  # Fondo de la figura
                ax5.patch.set_alpha(0.0)   # Fondo del área de los ejes
                ax5.set_xlabel('t')  # Nombre del eje X
                ax5.set_ylabel('x(t)')  # Nombre del eje Y
                plt.ylim(0, 2.5)
                st.pyplot(fig5)

                fig7, ax7 = plt.subplots()
                ax7.plot(t1,x1_t, color="#bf8bff", label="Señal Original")
                ax7.plot(tesc2,x1_t, color="#e5d0ff", linestyle="--", label="Señal Escalada")
                ax7.grid(True, linestyle=':')
                plt.title("Paso 1 (Escalamiento)")
                fig7.patch.set_alpha(0.0)  # Fondo de la figura
                ax7.patch.set_alpha(0.0)   # Fondo del área de los ejes
                ax7.set_xlabel('t')  # Nombre del eje X
                ax7.set_ylabel('x(t)')  # Nombre del eje Y
                ax7.legend()
                plt.ylim(0, 2.5)
                st.pyplot(fig7)

                fig6, ax6 = plt.subplots()
                ax6.plot(t1,x1_t, color="#bf8bff", label="Señal Original")
                ax6.plot(td2,x1_t, color="#e5d0ff", linestyle="--", label="Señal Escalada-Desplazada")
                ax6.grid(True, linestyle=':')
                plt.title("Paso 2 (Desplazamiento)")
                fig6.patch.set_alpha(0.0)  # Fondo de la figura
                ax6.patch.set_alpha(0.0)   # Fondo del área de los ejes
                ax6.set_xlabel('t')  # Nombre del eje X
                ax6.set_ylabel('x(t)')  # Nombre del eje Y
                plt.ylim(0, 2.5)
                ax6.legend()
                st.pyplot(fig6)

            else:
                st.write("No se han completado los campos")
            
    elif seleccion_continua == "Señal Continua 2":
        st.write("")
        # Datos de las funciones
        # Función 1
        x1 = np.arange(-3, -2, 0.0001)
        y1 = x1 + 3

        # Función 2
        x2 = np.arange(-2, -1, 0.0001)
        y2 = 2 * x2 / x2
        y2[np.isnan(y2)] = 0  # Manejar la división por cero

        # Función 3
        x3 = np.arange(-1, 0, 0.0001)
        y3 = x3 + 3

        # Función 4
        x4 = np.arange(0, 2, 0.0001)
        y4 = -x4 + 3

        # Función 5
        x5 = np.arange(2, 3, 0.0001)
        y5 = 1 * x5 / x5
        y5[np.isnan(y5)] = 0  # Manejar la división por cero

        # Función 6
        y6 = np.linspace(0, 1, 1000)  # Puedes ajustar el rango según sea necesario
        x6 = np.full_like(y6, 3)


        # Concatenación
        x = np.concatenate((x1, x2, x3, x4, x5, x6))
        y = np.concatenate((y1, y2, y3, y4, y5,y6))
        plt.style.use("dark_background")
        fig, ax = plt.subplots()
        fig.patch.set_alpha(0.0)  # Fondo de la figura
        ax.patch.set_alpha(0.0)   # Fondo del área de los ejes
        plt.xlabel('t',fontsize=12)
        plt.ylabel('x(t)',fontsize=12)    
        plt.xticks(np.arange(-3, 3+1, step=1))
        plt.yticks(np.arange(0, 3+1, step=0.5))
        ax.plot(x, y, color="#bf8bff")

        st.pyplot(fig)
        st.header("Método de Transformación")
        seleccion_transformacion2= st.selectbox("Seleccione método de transformación:", 
                                      ("Método 1 (Desplazamiento - Escalamiento)", "Método 2 (Escalamiento - Desplazamiento)"),index=None,placeholder="Seleccione una opción",)
        if seleccion_transformacion2 == "Método 1 (Desplazamiento - Escalamiento)":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("")
                seleccion_valores_a2 = st.selectbox("Seleccione un valor de [a]",("-2","-3","-4","-5","-1/2","-1/3","-1/4","-1/5","2","3","4","5","1/2","1/3","1/4","1/5"),index=None,placeholder="Seleccione una opción",)
            with col2:
                st.markdown("")
                seleccion_valores_to2 = st.selectbox("Seleccione un valor de [to]",("-1","-2","-3","-4","-5","-6","1","2","3","4","5","6"),index=None,placeholder="Seleccione una opción",)
            if (seleccion_valores_a2  != None) and (seleccion_valores_to2 != None):
                st.write("")

                #Definición de los ejes de tiempos de las funciones a trozos
                delta=0.01
                t1=np.arange(-3,-2,delta)
                t2=np.arange(-2,-1,delta)
                t3=np.arange(-1,0,delta)
                t4=np.arange(0,2,delta)
                t5=np.arange(2,3,delta)
                t6=np.arange(3,3+delta,delta)

                #Definición de las funciones a trozos
                x1_t= t1+3
                x2_t= 2*np.ones(len(t2))
                x3_t= t3+3
                x4_t= -t4+3
                x5_t= 1*np.ones(len(t5))
                x6_t= np.zeros(len(t6))

                #Concatenación de las funciones a trozos
                t=np.concatenate((t1,t2,t3,t4,t5,t6))
                x_t=np.concatenate((x1_t,x2_t,x3_t,x4_t,x5_t,x6_t))

                a1=eval(seleccion_valores_a2)
                to1=float(seleccion_valores_to2)

                td1=t-to1
                t_esc1=td1/a1

                fig8, ax8 = plt.subplots()
                ax8.plot(t,x_t, color="#bf8bff", label="Señal Original")
                ax8.grid(True, linestyle=':')
                plt.title("Señal Original Continua 2")
                fig8.patch.set_alpha(0.0)  # Fondo de la figura
                ax8.patch.set_alpha(0.0)   # Fondo del área de los ejes
                ax8.set_xlabel('t')  # Nombre del eje X
                ax8.set_ylabel('x(t)')  # Nombre del eje Y
                plt.ylim(0, 3.5)
                st.pyplot(fig8)

                fig9, ax9 = plt.subplots()
                ax9.plot(t,x_t, color="#bf8bff", label="Señal Original")
                ax9.plot(td1,x_t, color="#e5d0ff", linestyle="--", label="Señal Desplazada")
                ax9.grid(True, linestyle=':')
                plt.title("Paso 1 (Desplazamiento)")
                fig9.patch.set_alpha(0.0)  # Fondo de la figura
                ax9.patch.set_alpha(0.0)   # Fondo del área de los ejes
                ax9.set_xlabel('t')  # Nombre del eje X
                ax9.set_ylabel('x(t)')  # Nombre del eje Y
                plt.ylim(0, 3.5)
                st.pyplot(fig9)

                fig10, ax10 = plt.subplots()
                ax10.plot(t,x_t, color="#bf8bff", label="Señal Original")
                ax10.plot(t_esc1,x_t, color="#e5d0ff", linestyle="--", label="Señal Desplazada")
                ax10.grid(True, linestyle=':')
                plt.title("Paso 2 (Escalamiento)")
                fig10.patch.set_alpha(0.0)  # Fondo de la figura
                ax10.patch.set_alpha(0.0)   # Fondo del área de los ejes
                ax10.set_xlabel('t')  # Nombre del eje X
                ax10.set_ylabel('x(t)')  # Nombre del eje Y
                plt.ylim(0, 3.5)
                st.pyplot(fig10)
            else:
                st.write("No se han completado los campos")

        elif seleccion_transformacion2 == "Método 2 (Escalamiento - Desplazamiento)":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("")
                seleccion_valores_a21 = st.selectbox("Seleccione un valor de [a]",("-2","-3","-4","-5","-1/2","-1/3","-1/4","-1/5","2","3","4","5","1/2","1/3","1/4","1/5"),index=None,placeholder="Seleccione una opción",)
            with col2:
                st.markdown("")
                seleccion_valores_to21 = st.selectbox("Seleccione un valor de [to]",("-1","-2","-3","-4","-5","-6","1","2","3","4","5","6"),index=None,placeholder="Seleccione una opción",)
            if (seleccion_valores_a21 != None) and (seleccion_valores_to21 != None):
                    st.write("")
                    #Definición de los ejes de tiempos de las funciones a trozos
                    delta=0.01
                    t1=np.arange(-3,-2,delta)
                    t2=np.arange(-2,-1,delta)
                    t3=np.arange(-1,0,delta)
                    t4=np.arange(0,2,delta)
                    t5=np.arange(2,3,delta)
                    t6=np.arange(3,3+delta,delta)

                    #Definición de las funciones a trozos
                    x1_t= t1+3
                    x2_t= 2*np.ones(len(t2))
                    x3_t= t3+3
                    x4_t= -t4+3
                    x5_t= 1*np.ones(len(t5))
                    x6_t= np.zeros(len(t6))

                    #Concatenación de las funciones a trozos
                    t=np.concatenate((t1,t2,t3,t4,t5,t6))
                    x_t=np.concatenate((x1_t,x2_t,x3_t,x4_t,x5_t,x6_t))

                    a2=eval(seleccion_valores_a21)
                    to2=float(seleccion_valores_to21)

                    t_esc2=t/a2 #escalamiento en el tiempo
                    td2=t_esc2-(to2/a2) #desplazamiento en el tiempo

                    fig11, ax11 = plt.subplots()
                    ax11.plot(t,x_t, color="#bf8bff", label="Señal Original")
                    ax11.grid(True, linestyle=':')
                    plt.title("Señal Original Continua 2")
                    fig11.patch.set_alpha(0.0)  # Fondo de la figura
                    ax11.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    ax11.set_xlabel('t')  # Nombre del eje X
                    ax11.set_ylabel('x(t)')  # Nombre del eje Y
                    plt.ylim(0, 3.5)
                    st.pyplot(fig11)

                    fig12, ax12 = plt.subplots()
                    ax12.plot(t,x_t, color="#bf8bff", label="Señal Original")
                    ax12.plot(t_esc2,x_t, color="#e5d0ff", linestyle="--", label="Señal Escalada")
                    ax12.grid(True, linestyle=':')
                    plt.title("Paso 1 (Escalamiento)")
                    fig12.patch.set_alpha(0.0)  # Fondo de la figura
                    ax12.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    ax12.set_xlabel('t')  # Nombre del eje X
                    ax12.set_ylabel('x(t)')  # Nombre del eje Y
                    plt.ylim(0, 3.5)
                    st.pyplot(fig12)

                    fig100, ax100 = plt.subplots()
                    ax100.plot(t,x_t, color="#bf8bff", label="Señal Original")
                    ax100.plot(td2,x_t, color="#e5d0ff", linestyle="--", label="Señal Desplazada")
                    ax100.grid(True, linestyle=':')
                    plt.title("Paso 2 (Desplazamiento)")
                    fig100.patch.set_alpha(0.0)  # Fondo de la figura
                    ax100.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    ax100.set_xlabel('t')  # Nombre del eje X
                    ax100.set_ylabel('x(t)')  # Nombre del eje Y
                    plt.ylim(0, 3.5)
                    st.pyplot(fig100)
            else:
                st.write("No se han completado los campos")


def pagina3():
    st.title("Señales Discretas")
    st.write("Bienvenido a la Página de Señales Discretas.")
    
    # Selectbox dentro de la página de señales discretas
    seleccion_discreta = st.selectbox("Seleccione la señal discreta:", 
                                      ("Señal discreta 1", "Señal discreta 2"))
    if seleccion_discreta == "Señal discreta 1":
        st.write("Has seleccionado una señal de Señal discreta 1.")
        st.latex(r''' x[n]=\{0, 0, 0, 0, 0, \underset{\uparrow }{3}, 0, 5, 4, -2, -4, -1, 2, 5, 7, 4, -2, 0, 0, 0, 0, 0\}  ''')

        n_Cinicio=-5
        n_Cfin=16

        n_C=np.arange(n_Cinicio,n_Cfin+1)                                                # Vector de los valores de muestra n de la señal c)
        x_Cn=[0,0,0,0,0,-3,0,5,4,-2,-4,-1,2,5,7,4,-2,0,0,0,0,0]                                               # Vector de los valores de muestra n de la señal d)

        figd1, axd1 = plt.subplots()                                                                                 # Crea los vectores de amplitud para la señal d) de forma individual. Uno para cada subintervalo
        plt.stem(n_C,x_Cn, basefmt=" ", label=f'$x[n]$')
        plt.title("Señal Discreta D")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.title("Señal Discreta C")
        plt.xlabel("Tiempo (s)")
        figd1.patch.set_alpha(0.0)  # Fondo de la figura
        axd1.patch.set_alpha(0.0)   # Fondo del área de los ejes
        plt.ylabel("Amplitud")
        plt.axis([n_Cinicio-1,n_Cfin+1,np.min(x_Cn)-1,np.max(x_Cn)+1])                   # Establece los limites de los ejes a traves de los valores maximos de n y X[n]. Para mejor visual se adiciona una unidad a cada limite.
        plt.grid(True, linestyle=(":"))
        plt.legend()
        st.pyplot(figd1)
        
        st.header("Método de Transformación")
        seleccion_transformacion3= st.selectbox("Seleccione método de transformación:", 
                                      ("Método 1 (Desplazamiento - Escalamiento)", "Método 2 (Escalamiento - Desplazamiento)"),index=None,placeholder="Seleccione una opción")
        if seleccion_transformacion3 == "Método 1 (Desplazamiento - Escalamiento)":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("")
                seleccion_valores_M = st.selectbox("Seleccione un valor de [M]",("-2","-3","-4","-5","-1/2","-1/3","-1/4","-1/5","2","3","4","5","1/2","1/3","1/4","1/5"),index=None,placeholder="Seleccione una opción",)
            with col2:
                st.markdown("")
                seleccion_valores_no= st.selectbox("Seleccione un valor de [no]",("-1","-2","-3","-4","-5","-6","1","2","3","4","5","6"),index=None,placeholder="Seleccione una opción",)
            if (seleccion_valores_M  != None) and (seleccion_valores_no != None):
                st.write("")
                tipo_interpolación = st.selectbox("Escoja forma de Interpolación",("Lineal","Escalon","Ceros"),index=None,placeholder="Seleccione una opción",)
                if tipo_interpolación != None:
                    M = eval(seleccion_valores_M)
                    no = float(seleccion_valores_no)
                    if tipo_interpolación == "Lineal":
                        interpolacion = 3
                    elif tipo_interpolación == "Escalon":
                        interpolacion = 2
                    else:
                        interpolacion = 1
                        
                    n_tras, x_tras = Trasform_DesEsc(n_C,x_Cn,M,no, Inter_P = interpolacion ,Grafic=False) #Grafica Final
                    n2_tras, x2_tras = Trasform_DesEsc(n_C,x_Cn,1,no, Inter_P = interpolacion ,Grafic=False) #Grafica desplazada

                    #Grafica Original
                    figd31 ,axd31 = plt.subplots()
                    plt.style.use("dark_background")
                    axd31.stem(n_C,x_Cn, basefmt=" ")
                    figd31.patch.set_alpha(0.0)  # Fondo de la figura
                    axd31.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    plt.xlabel('Tiempo s')
                    plt.ylabel('Amplitud')
                    plt.title('Gráfica Original')
                    # Mostrar la gráfica
                    plt.grid(True,linestyle=":")
                    st.pyplot(figd31)
                    
                    #Grafica desplazada
                    figd31 ,axd31 = plt.subplots()
                    plt.style.use("dark_background")
                    axd31.stem(n2_tras, x2_tras, basefmt=" ")
                    figd31.patch.set_alpha(0.0)  # Fondo de la figura
                    axd31.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    plt.xlabel('Tiempo s')
                    plt.ylabel('Amplitud')
                    plt.title('Paso 1 (Desplazamiento)')
                    # Mostrar la gráfica
                    plt.grid(True,linestyle=":")
                    st.pyplot(figd31)

                    #Grafica Final
                    figd3 ,axd3 = plt.subplots()
                    plt.style.use("dark_background")
                    axd3.stem(n_tras, x_tras, basefmt=" ")
                    figd3.patch.set_alpha(0.0)  # Fondo de la figura
                    axd3.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    plt.xlabel('Tiempo s')
                    plt.ylabel('Amplitud')
                    plt.title('Paso 2 (Escalamiento)')
                    # Mostrar la gráfica
                    plt.grid(True,linestyle=":")
                    st.pyplot(figd3)
            else:
                st.write("No se han completado los campos")



        elif seleccion_transformacion3 == "Método 2 (Escalamiento - Desplazamiento)":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("")
                seleccion_valores_M1 = st.selectbox("Seleccione un valor de [M]",("-2","-3","-4","-5","-1/2","-1/3","-1/4","-1/5","2","3","4","5","1/2","1/3","1/4","1/5"),index=None,placeholder="Seleccione una opción",)
            with col2:
                st.markdown("")
                seleccion_valores_no1 = st.selectbox("Seleccione un valor de [no]",("-1","-2","-3","-4","-5","-6","1","2","3","4","5","6"),index=None,placeholder="Seleccione una opción",)
            m1 = eval(seleccion_valores_M1)
            no1 = float(seleccion_valores_no1)
            n_Cinicio=-5
            n_Cfin=16

            n_C=np.arange(n_Cinicio,n_Cfin+1)                                                # Vector de los valores de muestra n de la señal c)
            x_Cn=[0,0,0,0,0,-3,0,5,4,-2,-4,-1,2,5,7,4,-2,0,0,0,0,0]
            if ((no1/(float(m1))) % 1) == 0:
                interpolacion = st.selectbox("Seleccione Método de Interpolación",("Lineal","Escalon","Ceros"),index=None,placeholder="Seleccione una opción")
                if interpolacion == "Lineal":
                   valor_interpolacion = 3
                elif interpolacion == "Escalon":
                   valor_interpolacion = 2
                elif interpolacion == "Ceros":
                   valor_interpolacion = 1
                else:
                   valor_interpolacion = None
                if valor_interpolacion != None:
                    n_des,x_des = Trasform_EscDes(n_C,x_Cn,m1,no1,Inter_P=valor_interpolacion,Grafic=False)

                    n_esc,x_esc = Trasform_EscDes(n_C,x_Cn,m1,0,Inter_P=valor_interpolacion,Grafic=False)

                    #Original
                    figd3 ,axd3 = plt.subplots()
                    plt.style.use("dark_background")
                    axd3.stem(n_C, x_Cn, basefmt=" ")
                    figd3.patch.set_alpha(0.0)  # Fondo de la figura
                    axd3.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    plt.xlabel('Tiempo s')
                    plt.ylabel('Amplitud')
                    plt.title('Señal Original')
                    # Mostrar la gráfica
                    plt.grid(True,linestyle=":")
                    st.pyplot(figd3)

                    #Escalada
                    figd4 ,axd4 = plt.subplots()
                    plt.style.use("dark_background")
                    axd4.stem(n_esc, x_esc, basefmt=" ")
                    figd4.patch.set_alpha(0.0)  # Fondo de la figura
                    axd4.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    plt.xlabel('Tiempo s')
                    plt.ylabel('Amplitud')
                    plt.title('Paso 1 (Señal Escalada)')
                    # Mostrar la gráfica
                    plt.grid(True,linestyle=":")
                    st.pyplot(figd4)

                    #Desplazada
                    figd5 ,axd5 = plt.subplots()
                    plt.style.use("dark_background")
                    axd5.stem(n_des, x_des, basefmt=" ")
                    figd5.patch.set_alpha(0.0)  # Fondo de la figura
                    axd5.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    plt.xlabel('Tiempo s')
                    plt.ylabel('Amplitud')
                    plt.title('Paso 2 (Señal Desplazada)')
                    # Mostrar la gráfica
                    plt.grid(True,linestyle=":")
                    st.pyplot(figd5)
            else:
               st.write(r''' No se puede realizar dado que $N_o$ no es un número entero.''')


    elif seleccion_discreta == "Señal discreta 2":
        st.write("Has seleccionado una señal de Señal discreta 2.")
        st.latex(r'''   x[n]=\left\{\begin{matrix} 0, &-10\leq n\leq -6 \\ (2/3)^{n},& -5\leq n\leq 0 \\ (8/5)^{n},& 1\leq n\leq 5  \\ 0,& 6\leq n\leq 10 \end{matrix}\right.  ''')
        n_Dinicio=-10
        n_Dfin=10

        n_D=np.arange(n_Dinicio,n_Dfin+1)                                                # Vector de los valores de muestra n de la señal d)

                                                                                        # Crea los vectores de amplitud para la señal d) de forma individual. Uno para cada subintervalo
        x_DnA=np.zeros(5)                                                                # Funcion numpy.Zeros(x) para crear un vector de 0 de longitud x
        x_DnB=np.power((2/3),np.arange(-5,1))                                            # Funcion numpy.power(x,[y]) para crear un vector de potencias de base x y exponetes contenidos en el vector [y]
        x_DnC=np.power((8/5),np.arange(1,6))
        x_DnD=np.zeros(5)

        x_Dn=np.concatenate((x_DnA,x_DnB,x_DnC,x_DnD))                                   # Concatena cada vector individual para obtener el vector de los valores de la señal d) x[n]

        figd2, axd2 = plt.subplots()
        axd2.stem(n_D,x_Dn, basefmt=" ", label=f'$x[n]$')
        plt.title("Señal Discreta D")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        figd2.patch.set_alpha(0.0)  # Fondo de la figura
        axd2.patch.set_alpha(0.0)   # Fondo del área de los ejes
        plt.axis([n_Dinicio-1,n_Dfin+1,np.min(x_Dn)-1,np.max(x_Dn)+1])
        plt.grid(True, linestyle=":")
        plt.legend()

        st.pyplot(figd2)


        st.header("Método de Transformación")
        seleccion_transformacion4= st.selectbox("Seleccione método de transformación:", 
                                      ("Método 1 (Desplazamiento - Escalamiento)", "Método 2 (Escalamiento - Desplazamiento)"),index=None,placeholder="Seleccione una opción",)
        if seleccion_transformacion4 == "Método 1 (Desplazamiento - Escalamiento)":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("")
                seleccion_valores_M2 = st.selectbox("Seleccione un valor de [M]",("-2","-3","-4","-5","-1/2","-1/3","-1/4","-1/5","2","3","4","5","1/2","1/3","1/4","1/5"),index=None,placeholder="Seleccione una opción",)
            with col2:
                st.markdown("")
                seleccion_valores_no2= st.selectbox("Seleccione un valor de [no]",("-1","-2","-3","-4","-5","-6","1","2","3","4","5","6"),index=None,placeholder="Seleccione una opción",)
            
            if (seleccion_valores_M2 != None) and (seleccion_valores_no2 != None):
                st.write("")
                tipo_interpolación = st.selectbox("Escoja forma de Interpolación",("Lineal","Escalon","Ceros"),index=None,placeholder="Seleccione una opción",)
                if tipo_interpolación != None:
                    M = eval(seleccion_valores_M2)
                    no = float(seleccion_valores_no2)
                    if tipo_interpolación == "Lineal":
                        interpolacion = 3
                    elif tipo_interpolación == "Escalon":
                        interpolacion = 2
                    else:
                        interpolacion = 1
                        
                    n_tras, x_tras = Trasform_DesEsc(n_D,x_Dn,M,no, Inter_P = interpolacion ,Grafic=False) #Grafica Final
                    n2_tras, x2_tras = Trasform_DesEsc(n_D,x_Dn,1,no, Inter_P = interpolacion ,Grafic=False) #Grafica desplazada

                    #Grafica Original
                    figd31 ,axd31 = plt.subplots()
                    plt.style.use("dark_background")
                    axd31.stem(n_D,x_Dn, basefmt=" ")
                    figd31.patch.set_alpha(0.0)  # Fondo de la figura
                    axd31.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    plt.xlabel('Tiempo s')
                    plt.ylabel('Amplitud')
                    plt.title('Gráfica Original')
                    # Mostrar la gráfica
                    plt.grid(True,linestyle=":")
                    st.pyplot(figd31)
                    
                    #Grafica desplazada
                    figd31 ,axd31 = plt.subplots()
                    plt.style.use("dark_background")
                    axd31.stem(n2_tras, x2_tras, basefmt=" ")
                    figd31.patch.set_alpha(0.0)  # Fondo de la figura
                    axd31.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    plt.xlabel('Tiempo s')
                    plt.ylabel('Amplitud')
                    plt.title('Paso 1 (Desplazamiento)')
                    # Mostrar la gráfica
                    plt.grid(True,linestyle=":")
                    st.pyplot(figd31)

                    #Grafica Final
                    figd3 ,axd3 = plt.subplots()
                    plt.style.use("dark_background")
                    axd3.stem(n_tras, x_tras, basefmt=" ")
                    figd3.patch.set_alpha(0.0)  # Fondo de la figura
                    axd3.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    plt.xlabel('Tiempo s')
                    plt.ylabel('Amplitud')
                    plt.title('Paso 2 (Escalamiento)')
                    # Mostrar la gráfica
                    plt.grid(True,linestyle=":")
                    st.pyplot(figd3)
            else:
                st.write("No se han completado los campos")



        elif seleccion_transformacion4 == "Método 2 (Escalamiento - Desplazamiento)":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("")
                seleccion_valores_M13 = st.selectbox("Seleccione un valor de [M]",("-2","-3","-4","-5","-1/2","-1/3","-1/4","-1/5","2","3","4","5","1/2","1/3","1/4","1/5"),index=None,placeholder="Seleccione una opción",)
            with col2:
                st.markdown("")
                seleccion_valores_no13 = st.selectbox("Seleccione un valor de [no]",("-1","-2","-3","-4","-5","-6","1","2","3","4","5","6"),index=None,placeholder="Seleccione una opción",)
            m1 = eval(seleccion_valores_M13)
            no1 = float(seleccion_valores_no13)
            n_Dinicio=-10
            n_Dfin=10

            n_D=np.arange(n_Dinicio,n_Dfin+1)                                                # Vector de los valores de muestra n de la señal d)

                                                                                            # Crea los vectores de amplitud para la señal d) de forma individual. Uno para cada subintervalo
            x_DnA=np.zeros(5)                                                                # Funcion numpy.Zeros(x) para crear un vector de 0 de longitud x
            x_DnB=np.power((2/3),np.arange(-5,1))                                            # Funcion numpy.power(x,[y]) para crear un vector de potencias de base x y exponetes contenidos en el vector [y]
            x_DnC=np.power((8/5),np.arange(1,6))
            x_DnD=np.zeros(5)

            x_Dn=np.concatenate((x_DnA,x_DnB,x_DnC,x_DnD)) 
            if ((no1/(float(m1))) % 1) == 0:
                interpolacion = st.selectbox("Seleccione Método de Interpolación",("Lineal","Escalon","Ceros"),index=None,placeholder="Seleccione una opción")
                if interpolacion == "Lineal":
                   valor_interpolacion = 3
                elif interpolacion == "Escalon":
                   valor_interpolacion = 2
                elif interpolacion == "Ceros":
                   valor_interpolacion = 1
                else:
                   valor_interpolacion = None
                if valor_interpolacion != None:
                    n_des,x_des = Trasform_EscDes(n_D,x_Dn,m1,no1,Inter_P=valor_interpolacion,Grafic=False)

                    n_esc,x_esc = Trasform_EscDes(n_D,x_Dn,m1,0,Inter_P=valor_interpolacion,Grafic=False)

                    #Original
                    figd3 ,axd3 = plt.subplots()
                    plt.style.use("dark_background")
                    axd3.stem(n_D, x_Dn, basefmt=" ")
                    figd3.patch.set_alpha(0.0)  # Fondo de la figura
                    axd3.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    plt.xlabel('Tiempo s')
                    plt.ylabel('Amplitud')
                    plt.title('Señal Original')
                    # Mostrar la gráfica
                    plt.grid(True,linestyle=":")
                    st.pyplot(figd3)

                    #Escalada
                    figd4 ,axd4 = plt.subplots()
                    plt.style.use("dark_background")
                    axd4.stem(n_esc, x_esc, basefmt=" ")
                    figd4.patch.set_alpha(0.0)  # Fondo de la figura
                    axd4.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    plt.xlabel('Tiempo s')
                    plt.ylabel('Amplitud')
                    plt.title('Paso 1 (Señal Escalada)')
                    # Mostrar la gráfica
                    plt.grid(True,linestyle=":")
                    st.pyplot(figd4)

                    #Desplazada
                    figd5 ,axd5 = plt.subplots()
                    plt.style.use("dark_background")
                    axd5.stem(n_des, x_des, basefmt=" ")
                    figd5.patch.set_alpha(0.0)  # Fondo de la figura
                    axd5.patch.set_alpha(0.0)   # Fondo del área de los ejes
                    plt.xlabel('Tiempo s')
                    plt.ylabel('Amplitud')
                    plt.title('Paso 2 (Señal Desplazada)')
                    # Mostrar la gráfica
                    plt.grid(True,linestyle=":")
                    st.pyplot(figd5)
            else:
               st.write(r''' No se puede realizar dado que $N_o$ no es un número entero.''')

# Menú de la barra lateral
with st.sidebar:
    st.image("logo.svg", use_column_width="auto")
    st.title('Kuromi :violet[Math]',)
    st.text("Por:")
    st.text("Samantha Acevedo,\nJose Mendoza,\nLucas Romero.")
    x = st.header("Funciones de la APP")
    # Selección de página
    pagina_seleccionada = st.selectbox("Seleccione una función", ("Home", "Señales Continuas", "Señales Discretas","Operaciones de Funciones"),index=0,)

def pagina4():
    st.title("Operaciones con Funciones")
    st.markdown("### Primera Operación ###")
    st.markdown(r''' $x \left( \dfrac{1}{4} - \dfrac{t}{3} \right) + x \left( \dfrac{t}{2} - \dfrac{1}{3} \right)$ ''')
    st.markdown("Seleccione la función continua para aplicar la operación.")
    funcion_continua = st.selectbox("",("Función Continua 1 (A)", "Función continua 2 (B)"),index=None, placeholder="Seleccione una opcion")
    if funcion_continua == "Función Continua 1 (A)":
       
        #Definición de los ejes de tiempos de las funciones a trozos
        delta=0.01
        t1=np.arange(-2,-1,delta)
        t2=np.arange(-1,1,delta)
        t3=np.arange(1,2,delta)

        #Definición de las funciones a trozos
        x1_t= 2*t1+4
        x2_t= 2*np.ones(len(t2))
        x3_t=-2*t3+4

        #Concatenación de las funciones a trozos
        t1=np.concatenate((t1,t2,t3))
        x1_t=np.concatenate((x1_t,x2_t,x3_t))

        figz ,axz = plt.subplots()
        plt.style.use("dark_background")
        axz.plot(t1, x1_t, color ="#bf8bff")
        figz.patch.set_alpha(0.0)  
        axz.patch.set_alpha(0.0)   
        plt.xlabel('Tiempo s')
        plt.ylabel('Amplitud')
        plt.title('Grafica Original')
        # Mostrar la gráfica
        plt.grid(True,linestyle=":")
        st.pyplot(figz)

        #Hacemos primero la transformación x(-t/3+1/4)

        a3=-1/3
        to3=1/4

        td3=t1-to3 #td:desplazamiento en el tiempo
        tesc3=td3/a3 #tesc: escalamiento en el tiempo
        
        fig2 ,ax2 = plt.subplots()
        plt.style.use("dark_background")
        ax2.plot(tesc3,x1_t,color = "#dabcff")
        fig2.patch.set_alpha(0.0)  
        ax2.patch.set_alpha(0.0)   
        plt.xlabel('Tiempo s')
        plt.ylabel('Amplitud')
        plt.title('Transformación Número 1')
        # Mostrar la gráfica
        plt.grid(True,linestyle=":")
        st.pyplot(fig2)

        #Hacemos la segunda transformación x(t/2-1/3)

        a4=1/2
        to4=-1/3

        td4=t1-to4 #td:desplazamiento en el tiempo
        tesc4=td4/a4 #tesc: escalamiento en el tiempo

        fig3 ,ax3 = plt.subplots()
        plt.style.use("dark_background")
        ax3.plot(tesc4,x1_t, color="#ffffff")
        fig3.patch.set_alpha(0.0)  
        ax3.patch.set_alpha(0.0)   
        plt.xlabel('Tiempo s')
        plt.ylabel('Amplitud')
        plt.title('Transformación Número 2')
        # Mostrar la gráfica
        plt.grid(True,linestyle=":")
        st.pyplot(fig3)

        #Para realizar la suma debemos igualar el tamaño de ambas funciones rellenando con ceros los extremos
        delta_esc=tesc4[2]-tesc4[1]
        min_esc3=min(tesc3) #Minimo valor de tiempo de la señal x(-t/3+1/4)
        min_esc4=min(tesc4) #Minimo valor de tiempo de la señal x(t/2-1/3)
        max_esc3=max(tesc3) #Maximo valor de tiempo de la señal x(-t/3+1/4)
        max_esc4=max(tesc4) #Maximo valor de tiempo de la señal x(t/2-1/3)

        #Se observa cual es el valor maximo y minimo entre los vectores de tiempo de ambas funciones transformadas para definir los vectores que serán rellenados con ceros
        if min_esc3<min_esc4:
            t_inic=np.arange(min_esc3,min_esc4,delta_esc)
        if min_esc3>min_esc4:
            t_inic=np.arange(min_esc4,min_esc3,delta_esc)
        if max_esc3>max_esc4:
            t_fin=np.arange(max_esc4,max_esc3,delta_esc)
        if max_esc3<max_esc4:
            t_fin=np.arange(max_esc3,max_esc4,delta_esc)

        # Una vez definidos los vectores se mide su longitud para determinar la cantidad de ceros a agregar
        L_t_inic=len(t_inic)
        L_t_fin=len(t_fin)

        # Se recontruye la señal x(t/2-1/3) pero con las dimensiones de la señal x(-t/3+1/4)
        x_t_esc=np.concatenate((np.zeros(L_t_inic),x1_t,np.zeros(L_t_fin))) #x1_t contiene los valores de amplitud, lo que se modificó fueron los vectores de tiempo
        t_nesc=np.concatenate((t_inic,tesc4,t_fin))

        # Se reescala el vector de tiempo de la señal x(-t/3+1/4)
        t1n=np.arange((2-to3)/(a3),(1-to3)/(a3),delta_esc)
        t2n=np.arange((1-to3)/(a3),(-1-to3)/(a3),delta_esc)
        t3n=np.arange((-1-to3)/(a3),(-2-to3)/(a3)+delta_esc,delta_esc)
        tnew=np.concatenate((t1n,t2n,t3n))

        #Se definen nuevamente los intervalos de la señal x(-t/3+1/4) con el nuevo intervalo de tiempo escalado
        x1n_t= (2*t1n/3)+7/2
        x2n_t= 2*np.ones(len(t2n))
        x3n_t= (-2*t3n/3)+9/2
        x_tnew = np.concatenate((x1n_t,x2n_t,x3n_t))

        figb, axb = plt.subplots()

        axb.plot(tnew,x_tnew, color = "#dabcff")
        axb.plot(t_nesc,x_t_esc,color="#ffffff")
        axb.axis([-10,10,0,2.5])
        plt.title("Señales Transformadas")
        plt.xlabel('Tiempo s')
        plt.ylabel('Amplitud')
        figb.patch.set_alpha(0.0)  
        axb.patch.set_alpha(0.0)
        axb.grid('on',linestyle=":")
        st.pyplot(figb)


        #Se grafica la señal final
        y_t= x_t_esc + x_tnew

        figb1, axb1 = plt.subplots()
        axb1.plot(tnew,y_t, color = "#bf8bff")
        axb1.axis([-10,10,0,5])
        plt.title("Suma de Señales")
        plt.xlabel('Tiempo s')
        plt.ylabel('Amplitud')
        figb1.patch.set_alpha(0.0)  
        axb1.patch.set_alpha(0.0)
        axb1.grid('on',linestyle=":")
        st.pyplot(figb1)

    elif funcion_continua == "Función continua 2 (B)":
        st.write("")
        plt.figure(figsize=(20,10))

        #Definición de los ejes de tiempos de las funciones a trozos
        delta=0.01
        t1=np.arange(-3,-2,delta)
        t2=np.arange(-2,-1,delta)
        t3=np.arange(-1,0,delta)
        t4=np.arange(0,2,delta)
        t5=np.arange(2,3,delta)
        t6=np.arange(3,3+delta,delta)

        #Definición de las funciones a trozos
        x1_t= t1+3
        x2_t= 2*np.ones(len(t2))
        x3_t= t3+3
        x4_t= -t4+3
        x5_t= 1*np.ones(len(t5))
        x6_t= np.zeros(len(t6))

        #Concatenación de las funciones a trozos
        t=np.concatenate((t1,t2,t3,t4,t5,t6))
        x_t=np.concatenate((x1_t,x2_t,x3_t,x4_t,x5_t,x6_t))

        fig, ax = plt.subplots()
        ax.plot(t,x_t,color="#bf8bff")
        ax.grid('on', linestyle=":")
        plt.xlabel('Tiempo s')
        plt.ylabel('Amplitud')
        fig.patch.set_alpha(0.0)  
        ax.patch.set_alpha(0.0)
        plt.title('Señal original')
        st.pyplot(fig)

        #Hacemos primero la transformación x(-t/3+1/4)

        a3=-1/3
        to3=1/4

        td3=t-to3 #td:desplazamiento en el tiempo
        t_esc3=td3/a3 #tesc: escalamiento en el tiempo

        fig2, ax2 = plt.subplots()
        ax2.plot(t_esc3,x_t,color="#dabcff")
        ax2.axis([-10,10,0,5])
        ax2.grid('on',linestyle=":")
        plt.title('Transformación Número 1')
        plt.xlabel('Tiempo s')
        plt.ylabel('Amplitud')
        fig2.patch.set_alpha(0.0)  
        ax2.patch.set_alpha(0.0)
        st.pyplot(fig2)

        #Hacemos la segunda transformación x(t/2-1/3)

        a4=1/2
        to4=-1/3

        td4=t-to4 #td:desplazamiento en el tiempo
        t_esc4=td4/a4 #tesc: escalamiento en el tiempo

        fig3, ax3 = plt.subplots()
        ax3.plot(t_esc4,x_t,color="#ffffff")
        ax3.axis([-10,10,0,5])
        ax3.grid('on',linestyle=":")
        plt.title('Transformación Número 2')
        plt.xlabel('Tiempo s')
        fig3.patch.set_alpha(0.0)  
        ax3.patch.set_alpha(0.0)
        plt.ylabel('Amplitud')
        st.pyplot(fig3)

        #Para realizar la suma debemos igualar el tamaño de ambas funciones rellenando con ceros los extremos
        delta_esc=0.02
        min_esc3=min(t_esc3) #Minimo valor de tiempo de la señal x(-t/3+1/4)
        min_esc4=min(t_esc4) #Minimo valor de tiempo de la señal x(t/2-1/3)
        max_esc3=max(t_esc3) #Maximo valor de tiempo de la señal x(-t/3+1/4)
        max_esc4=max(t_esc4) #Maximo valor de tiempo de la señal x(t/2-1/3)

        #Se observa cual es el valor maximo y minimo entre los vectores de tiempo de ambas funciones transformadas para definir los vectores que serán rellenados con ceros
        if min_esc3<min_esc4:
            t_inic=np.arange(min_esc3,min_esc4,delta_esc)
        if min_esc3>min_esc4:
            t_inic=np.arange(min_esc4,min_esc3,delta_esc)
        if max_esc3>max_esc4:
            t_fin=np.arange(max_esc4+delta_esc,max_esc3+delta_esc,delta_esc)
        if max_esc3<max_esc4:
            t_fin=np.arange(max_esc3+delta_esc,max_esc4+delta_esc,delta_esc)

        # Una vez definidos los vectores se mide su longitud para determinar la cantidad de ceros a agregar
        L_t_inic=len(t_inic)
        L_t_fin=len(t_fin)

        # Se recontruye la señal x(t/2-1/3) pero con las dimensiones de la señal x(-t/3+1/4)
        x_tesc=np.concatenate((np.zeros(L_t_inic),x_t,np.zeros(L_t_fin))) #x1_t contiene los valores de amplitud, lo que se modificó fueron los vectores de tiempo
        t_nesc=np.concatenate((t_inic,t_esc4,t_fin))

        # Se reescala el vector de tiempo de la señal x(-t/3+1/4)
        t1n=np.arange((3-to3)/(a3),(3-to3)/(a3)+delta_esc,delta_esc)
        t2n=np.arange((3-to3)/(a3)+delta_esc,(2-to3)/(a3),delta_esc)
        t3n=np.arange((2-to3)/(a3),(0-to3)/(a3),delta_esc)
        t4n=np.arange((0-to3)/(a3),(-1-to3)/(a3),delta_esc)
        t5n=np.arange((-1-to3)/(a3),(-2-to3)/(a3),delta_esc)
        t6n=np.arange((-2-to3)/(a3),(-3-to3)/(a3)+delta_esc,delta_esc)
        tnew=np.concatenate((t1n,t2n,t3n,t4n,t5n,t6n))


        #Se definen nuevamente los intervalos de la señal x(-t/3+1/4) con el nuevo intervalo de tiempo escalado
        x1n_t= 0*np.ones(len(t1n))
        x2n_t= 1*np.ones(len(t2n))
        x3n_t= -(-t3n/3+1/4)+3
        x4n_t= (-t4n/3+1/4)+3
        x5n_t= 2*np.ones(len(t5n))
        x6n_t= (-t6n/3+1/4)+3
        x_tnew = np.concatenate((x1n_t,x2n_t,x3n_t,x4n_t,x5n_t,x6n_t))

        fig4, ax4 = plt.subplots()
        ax4.plot(tnew,x_tnew,color="#dabcff")
        ax4.plot(t_nesc,x_tesc,color="#ffffff") #Se grafica la señal completada con ceros
        ax4.axis([-10,10,0,5])
        ax4.grid('on',linestyle=":")
        plt.title("Señales Transformadas")
        plt.xlabel('Tiempo s')
        plt.ylabel('Amplitud')
        fig4.patch.set_alpha(0.0)  
        ax4.patch.set_alpha(0.0)
        st.pyplot(fig4)


        #Se grafica la señal final
        y_t= x_tesc + x_tnew

        fig5, ax5 = plt.subplots()
        ax5.plot(tnew,y_t,color="#bf8bff")
        ax5.axis([-10,10,0,6.5])
        plt.xlabel('Tiempo s')
        plt.ylabel('Amplitud')
        ax5.grid('on', linestyle=":")
        fig5.patch.set_alpha(0.0)  
        ax5.patch.set_alpha(0.0)
        st.pyplot(fig5)


    st.markdown("### Segunda Operación ###")
    st.markdown(r''' $x \left[4 - \dfrac{n}{3} \right] +  x \left[ \dfrac{n}{4} - 3 \right]$ ''')
    funcion_discreta = st.selectbox("",("Función Discreta 1 (A)", "Función Discreta 2 (B)"),index=None,placeholder="Seleccione una opción")
    if funcion_discreta == "Función Discreta 1 (A)":
        n_Cinicio=-5
        n_Cfin=16
        n_C=np.arange(n_Cinicio,n_Cfin+1)                                                # Vector de los valores de muestra n de la señal c)
        x_Cn=[0,0,0,0,0,-3,0,5,4,-2,-4,-1,2,5,7,4,-2,0,0,0,0,0]
        interpolacion = st.selectbox("Seleccione Metodo de Interpolacion",("Lineal","Escalon","Ceros"),index=None,placeholder="Seleccione una opción")
        if interpolacion == "Lineal":
           valor_interpolacon = 3
        elif interpolacion =="Escalon":
           valor_interpolacon = 2
        elif interpolacion == "Ceros":
           valor_interpolacon = 1
        else:
           valor_interpolacon = None
        if valor_interpolacon != None:
            N1,X1= Trasform_DesEsc(n_C,x_Cn,-1/3,4,Inter_P= valor_interpolacon,Grafic=False)
            N2,X2= Trasform_DesEsc(n_C,x_Cn,1/4,-3,Inter_P= valor_interpolacon,Grafic=False)
            n_op,x_op = Operacion_Señales(N1,X1,N2,X2,Grafic=False)

            fig1, ax1 = plt.subplots()
            ax1.stem(N1,X1,linefmt="violet", markerfmt="o", basefmt="k")
            plt.style.use("dark_background")
            plt.xlabel('Tiempo s')
            plt.ylabel('Amplitud')
            ax1.grid('on', linestyle=":")
            fig1.patch.set_alpha(0.0)  
            ax1.patch.set_alpha(0.0)
            st.pyplot(fig1)

            fig2, ax2 = plt.subplots()
            ax2.stem(N2,X2)
            plt.xlabel('Tiempo s')
            plt.ylabel('Amplitud')
            plt.style.use("dark_background")
            ax2.grid('on', linestyle=":")
            fig2.patch.set_alpha(0.0)  
            ax2.patch.set_alpha(0.0)
            st.pyplot(fig2)

            fig4, ax4 = plt.subplots()
            ax4.stem(N2,X2)
            plt.style.use("dark_background")
            ax4.stem(N1,X1,linefmt="violet", markerfmt="o", basefmt="k")
            plt.xlabel('Tiempo s')
            plt.ylabel('Amplitud')
            ax4.grid('on', linestyle=":")
            fig4.patch.set_alpha(0.0)  
            ax4.patch.set_alpha(0.0)
            st.pyplot(fig4)

            fig3, ax3 = plt.subplots()
            ax3.stem(n_op,x_op)
            plt.xlabel('Tiempo s')
            plt.style.use("dark_background")
            plt.ylabel('Amplitud')
            ax3.grid('on', linestyle=":")
            fig3.patch.set_alpha(0.0)  
            ax3.patch.set_alpha(0.0)
            st.pyplot(fig3)


    elif funcion_discreta == "Función Discreta 2 (B)":
        n_Dinicio=-10
        n_Dfin=10
        n_D=np.arange(n_Dinicio,n_Dfin+1)                                                                                                              
        x_DnA=np.zeros(5)                                                                
        x_DnB=np.power((2/3),np.arange(-5,1))  
        x_DnC=np.power((8/5),np.arange(1,6))                                          
        x_DnD=np.zeros(5)

        x_Dn=np.concatenate((x_DnA,x_DnB,x_DnC,x_DnD))
        interpolacion = st.selectbox("Seleccione Metodo de Interpolacion",("Lineal","Escalon","Ceros"),index=None,placeholder="Seleccione una opción")
        if interpolacion == "Lineal":
           valor_interpolacon = 3
        elif interpolacion =="Escalon":
           valor_interpolacon = 2
        elif interpolacion == "Ceros":
           valor_interpolacon = 1
        else:
           valor_interpolacon = None
        if valor_interpolacon != None:
            N1,X1= Trasform_DesEsc(n_D,x_Dn,-1/3,4,Inter_P= valor_interpolacon,Grafic=False)
            N2,X2= Trasform_DesEsc(n_D,x_Dn,1/4,-3,Inter_P= valor_interpolacon,Grafic=False)
            n_op,x_op = Operacion_Señales(N1,X1,N2,X2,Grafic=False)

            fig1, ax1 = plt.subplots()
            ax1.stem(N1,X1,linefmt="violet", markerfmt="o", basefmt="k")
            plt.style.use("dark_background")
            plt.xlabel('Tiempo s')
            plt.ylabel('Amplitud')
            ax1.grid('on', linestyle=":")
            fig1.patch.set_alpha(0.0)  
            ax1.patch.set_alpha(0.0)
            st.pyplot(fig1)

            fig2, ax2 = plt.subplots()
            ax2.stem(N2,X2)
            plt.xlabel('Tiempo s')
            plt.ylabel('Amplitud')
            plt.style.use("dark_background")
            ax2.grid('on', linestyle=":")
            fig2.patch.set_alpha(0.0)  
            ax2.patch.set_alpha(0.0)
            st.pyplot(fig2)

            fig4, ax4 = plt.subplots()
            ax4.stem(N2,X2)
            plt.style.use("dark_background")
            ax4.stem(N1,X1, linefmt="violet", markerfmt="o", basefmt="k")
            plt.xlabel('Tiempo s')
            plt.ylabel('Amplitud')
            ax4.grid('on', linestyle=":")
            fig4.patch.set_alpha(0.0)  
            ax4.patch.set_alpha(0.0)
            st.pyplot(fig4)

            fig3, ax3 = plt.subplots()
            ax3.stem(n_op,x_op)
            plt.xlabel('Tiempo s')
            plt.style.use("dark_background")
            plt.ylabel('Amplitud')
            ax3.grid('on', linestyle=":")
            fig3.patch.set_alpha(0.0)  
            ax3.patch.set_alpha(0.0)
            st.pyplot(fig3)




# Mostrar la página seleccionada
if pagina_seleccionada == "Home":
    pagina1()
elif pagina_seleccionada == "Señales Continuas":
    pagina2()
elif pagina_seleccionada == "Señales Discretas":
    pagina3()
elif pagina_seleccionada == "Operaciones de Funciones":
    pagina4()
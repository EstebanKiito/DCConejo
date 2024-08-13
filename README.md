# Tarea 2: DCConejoChico 🐇💨

Hola querid@ Ayudante, espero que tratar de corregir mi Tarea 2 sea un trabajo ameno, trate de comentar donde fuera necesario en mi codigo, separe mi codigo en funciones y en archivos externos para las rutas de imagenes. 
Espero tenga un buen tiempo corregiendo mi tarea, muchas gracias y disfrute de mi DCConejoChico 🐰.

## Consideraciones generales :octocat:

1. Consideracion muy importante!: Quizas en otros computadores no pase, pero en mi Mac, al enviar un mensaje al usuario de tipo QMessageBox, este sale de la pantalla, por lo que no se puede mover a ConejoChico de inmediato, hay que pulsar adentro de la pantalla de juego, para poder volver a mover al jugador

2. Conejo al morir, no aparece instantaneamente en la entrada dado el mensaje, por lo que una vez que se muera hay que pulsar alguna tecla ("WASD") para volver a la entrada y seguir jugando

3. No logre implementar las bombas, por lo que no puedo matar a los lobos sin otra forma que no sea "kil" como cheatcode, para efectos de que el ranking funcione, usar el comando "inf" como cheatcode para sumar puntaje y ver

4. Mis funciones mover, son qtimers que solo van actualizando la posicion cada cierto tiempo, el frontend solo tiene los Qlabels con las imagenes, con un metodo para ir moviendo y a la vez, actualizando el sprite para realizar las animaciones del movimiento, las rutas estan en otro archivo, llamado rutas.py, ahi tengo una clase con atributos donde van las rutas

5. Usuarios invalidos es simplemente un atributo de instancia de la clase Backend, hecho de una lista, pueden añadirse ahi los usuarios invalidos

6. Estoy suponiendo que siempre los mapas son de 16 x 16 y que ademas el nivel 3 es el final, dado que cierro el programa mandando un mensaje de felicitaciones al nivel 3.

7. Considere que el conejo con colisionara con los cañones.


## Cosas implementadas y no implementadas :white_check_mark: :x:

### Entrega Final: 46 pts (75%)
##### ✅ Ventana Inicio
- Ventana Inicio funciona perfectamente, se espera que se ingrese correctamente un usuario o Nuevo, o con alguna Partida guardada.

##### ✅ Ventana Juego
- Ventana Juego funciona perfectamente, tiene el inventario, actualizacion en tiempo real de las vidas, el tiempo, y el puntaje del jugador, ademas de un titulo (en la ventana) del jugador y el nivel que esta jugando

##### ✅ ConejoChico:
- ConejoChico: Puede moverse perfectamente, colisiona con los enemigos y los bloques, funciona con un Qtimer que lo mueve cada vez que se pulsa una tecla, tiene un solo problema y es que al pasar de nivel queda la imagen seteada en la entrada, no implemente el cambio de velocidades entre niveles
En la Logica del juego

##### ✅ Lobos:
- Lobos: Pueden moverse perfectamente, tanto vertical como horizontalmente.Colisionan con los bloques, funciona con un Qtimer que lo mueve siempre, una vez parta el juego, pueden eliminarse con "kil" y pausarse con "p".

##### ✅ Cañón de Zanahorias
- Cañon Zanahorias: Funcionan a la perfeccion, no lo considere como una pared, por lo que conejo no colisionara contra ellos, pero si puede morir al estar encima de uno, ya que las zanahorias salen desde ahi

##### ❌ Bomba Manzana
##### ❌ Bomba Congeladora

##### ✅ Fin del nivel
- Para ello hago un mensaje al usuario de tipo QmessageBox interactivo

##### ✅ Fin del Juego
- Para ello hago un mensaje al usuario de tipo QmessageBox interactivo
- Cierra la partida, avisa al servidor de desconexion

##### ❌ Recoger (G)

##### ✅ Cheatcodes (Pausa, K+I+L, I+N+F)
- Estan bien aplicados, puedes comprobar instantaneamente la suma de puntaje - para "inf", el conejo y las entidades dejan de moverse al estar en pausa (p) y para kil, todas las entidades que no sean bombas desaparecen, los cañones simplemente dejan de disparar zanahorias

##### ✅ Networking
- Hice una buena conexion entre servidor y cliente, se envian mensajes siempre que se ingrese un usuario o se abra el juego, o cuando el jugador pase de nivel, o termine el juego.

##### ✅ Decodificación y ✅ Desencriptación
Implemente correctamente los metodos, se pueden enviar y recibir mensajes de manera correcta entre servidor y cliente, los mensajes llegan a salvo con estas tecnicas

##### ✅ Funciones
Reutlizo algunas funciones de cliente y servidor, no todas, porque no haye funcionalidad para mi juego en todas, pero si reutilizo algunas, para ello, tengo el modulo funciones_cliente o funciones_servidor para recurrir a ellas

##### ✅ Archivos
- Archivo Puntajes.txt es actualizado y leido de manera correcta por el servidor, siempre que el cliente quiera acceder a la info dentro de el


## Ejecución :computer:
El archivo principal de la tarea a ejecutar es  ```main.py``` el cual se encuentra dentro de la carpeta entrega_final/cliente
Ademas de correr el ```servidor.py``` que se encuentra en entrega_final/cliente

### Archivos del Servidor:
1. ```funciones_extras.py``` en ```servidor```
2. ```funciones_servidor.py``` en ```servidor```
3. ```puntajes.txt``` en ```servidor```
4. ```host_servidor.json``` en ```servidor```

### Archivos del Cliente:
1. ```main.py``` -> Ejecuta tanto el backend como el frontend, y comienza la conexion con el servidor
2. ```host_cliente.json``` -> contiene el host de la comunicacion con el server

### En ```cliente/frontend``` se encuentran:
1. ```ventana.py``` -> Contiene la Ventana Inicio
2. ```ventana_juego.py``` -> Cont la Ventana Juego
3. ```rutas.py```  -> Contiene una clase, con un atributo que contiene las rutas de los sprites, con el fin de separar las rutas de la misma ventana del juego

### En ```cliente/backend``` se encuentran:
1. ```logica.py``` -> Contiene 2 clases:
    a. Backend -> Es la encargada de contactar al servidor
    b. LogicaJuego -> la encargada de manejar toda la logica detras del juego

2. ```funciones_extras.py``` 
3. ```funciones_cliente.py```
4. ```parametros.py```
5. ```clases.py``` -> Contiene 2 clases:
    a. Conejo -> Es la encargada de modelar el movimiento del conejo (QTimer)
    b. EntidadNpc -> Es la encargada de modelar el movimientos de los npc del juego, como lo son los lobos y los cañones de zanahorias


## Librerías :books:
### Librerías externas utilizadas
No utilice librerias externas mas que las necesarias para ejecutar la Gui con PyQt6


## Consideraciones adicionales :thinking:

### 1. 
Para enviarme mensajes entre cliente y servidor, mi protocolo es siempre 1. Mandar un mensaje con la operacion, dada la forma en que hice mis funciones de decodificar y desencriptar, tengo que mandar varios numeros por ej : "11111111" o "22222222" Lo hago con el fin de mandarle al servidor una operacion, un 1 un 2 o un 3, cada una representa una operacion como pedir ranking, ingresar usuario, reescribirlo, o simplemente salir (que seria con un 0)

### 2. Para el siguiente codigo (ventana_juego.py) que puede verse complejo , intentare explicar que hago:

```python
def colocar_entidad(self, entidad: str, posicion_inicial: tuple, id: int):
        """---Este metodo rellena el mapa con los assets principales de las Entidades del juego---"""
        rutas = Rutas()
        rutas_entidades = rutas.rutas_sprites["rutas_entidades"]
        rutas_zanahorias = rutas.rutas_sprites["rutas_zanahorias"]
        entidad_img = QLabel(entidad, self)
        ruta = rutas_entidades[entidad]
        pixeles = QPixmap(ruta)
        self.setear_imagen(entidad_img, pixeles)
        x, y = posicion_inicial
        if y < 10:
            entidad_img.move( 310 + (40 * x) , 20 + (40 * y) )
        else:
            entidad_img.move( 310 + (40 * x) , 10 + (40 * y) )
        self.entidades[id] = [entidad_img,entidad]
        entidad_img.show()
        # --- Para zanahorias : cambio la imagen del cañon por la zanahoria ----
        if entidad in ["CU","CD","CR","CL"]:
            zanahoria_img = QLabel(entidad, self)
            ruta = rutas_zanahorias[entidad]
            pixeles = QPixmap(ruta)
            self.setear_imagen(zanahoria_img, pixeles)
            self.entidades[id][0] = zanahoria_img
            x, y = posicion_inicial
            if y < 10:
                zanahoria_img.move( 310 + 40*x , 20 + 40*y )
            else:
                zanahoria_img.move( 310 + 40*x , 10 + 40*y )
            zanahoria_img.show()
        # --- Emitir señal para empezar a mover a los NPC en el mapa ---
        self.senal_empezar_a_mover.emit(id)
```
Basicamente voy desde el backend (LogicaJuego) leyendo entidad por entidad en el mapa, le asigno un id, y la mando por señales a este metodo, el cual comprueba si es cañon o cualquier otra, esto lo hago porque mi diccionario self.entidades tiene adentro cada llave con una lista con el label y el nombre, entonces cuando es un cañon, quiero reemplazarle el sprite por el de una zanahoria, asi posteriormente, cuando se active el timer de mover, no estaré moviendo el cañon, si no la zanahoria.

### 3. Movimiento de las piezas:

Quiero explicar con mas detalles como se mueven las piezas en mi tablero:

1. En el backend reviso en mapa las posiciones (x,y) o (col, fil) de cada entidad a la que le asigno una Clase, la instancio y la guardo en un diccionario

2. Cada una de estas instancias posee una posicion self.x y self.y la cual envio a mi frontend

3. el frontend tiene la posicion x,y y yo arbitrariamente la desplazo 310 + 40*x por ejemplo, porque calcule que mi tablero partia desde esa posicion.
Entonces, mis piezas se van colocando segun x,y pero desplazadas alrededor del mapa, segun una cantidad de pixeles

4. Para hacer el movimiento, simplemente dentro de mi las clases, hay un timer que se activa apenas se instancia (entidadesNPC) y cada vez que se apreta una tecla (conejo)

5. Lo que hacen los metodos mover, no es modificar el mapa, si no que voy dando sumas de apoco en las posiciones self.x y self.y haciendo que el conejo en el frontend en realidad se mueva de a poquitos pixeles.

6. Cada vez que mando una posicion con una pyqtsignal, mando ademas un numero entre 1 y 3, para asi cambiar el sprite cada vez que la entidad se mueva, dando asi la imprecion de estar animado
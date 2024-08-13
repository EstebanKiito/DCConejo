# Tarea 2: DCConejoChico 🐇💨

¡Hola, querid@ lector! Espero que disfrutes de mi Tarea 2. He comentado mi código donde fue necesario y lo he organizado en funciones y archivos externos para las rutas de imágenes. ¡Muchas gracias y disfruta de mi DCConejoChico 🐰! Espero que esto sirva como método de estudio. No me considero un gran programador, pero he puesto mucho esfuerzo en esta tarea y creo que puede ser útil para alguien que esté trabajando con PyQt, ¡que me encantó!

## Consideraciones Generales :octocat:

1. **Consideración muy importante:** En mi Mac, al enviar un mensaje al usuario con `QMessageBox`, este aparece fuera de la pantalla. Por lo tanto, debes pulsar dentro de la pantalla del juego para poder mover al jugador de nuevo.

2. Cuando el conejo muere, no aparece instantáneamente en la entrada. Después de morir, hay que pulsar alguna tecla ("WASD") para volver a la entrada y continuar jugando.

3. Las funciones de movimiento están basadas en **QTimers** que actualizan la posición cada cierto tiempo. El frontend solo tiene los `QLabels` con las imágenes, junto con un método para mover y actualizar el sprite para las animaciones. Las rutas están en otro archivo llamado `rutas.py`, donde tengo una clase con atributos para las rutas.

4. Los usuarios inválidos se gestionan mediante una lista en la clase `Backend`, a la que puedes añadir usuarios inválidos.

5. Suponemos que siempre los mapas son de 16x16 y que el nivel 3 es el final. El programa se cierra enviando un mensaje de felicitaciones al nivel 3.

6. El conejo colisionará con los cañones.

## Cosas Implementadas y No Implementadas :white_check_mark: :x:

### Entrega Final: 46 pts (75%)

##### ✅ Ventana Inicio
- La ventana de inicio funciona perfectamente, permitiendo ingresar un usuario nuevo o cargar una partida guardada.

##### ✅ Ventana Juego
- La ventana de juego funciona perfectamente, mostrando el inventario, actualizaciones en tiempo real de las vidas, el tiempo y el puntaje del jugador, además de un título con el nombre del jugador y el nivel en juego.

##### ✅ ConejoChico:
- **ConejoChico**: Se mueve perfectamente, colisiona con los enemigos y bloques, y funciona con un `QTimer` que actualiza la posición con cada tecla pulsada. Sin embargo, al pasar de nivel, la imagen queda fijada en la entrada. No se implementó el cambio de velocidades entre niveles.

##### ✅ Lobos:
- **Lobos**: Se mueven perfectamente tanto vertical como horizontalmente, colisionan con los bloques, y se mueven con un `QTimer`. Pueden eliminarse con "kil" y pausarse con "p".

##### ✅ Cañón de Zanahorias
- **Cañón Zanahorias**: Funcionan a la perfección. No se considera como una pared, por lo que el conejo no colisionará contra ellos, pero puede morir si está sobre uno, ya que las zanahorias salen de allí.

##### ✅ Fin del Nivel
- Se muestra un mensaje al usuario usando un `QMessageBox` interactivo.

##### ✅ Fin del Juego
- Se muestra un mensaje al usuario usando un `QMessageBox` interactivo.
- Cierra la partida y avisa al servidor de desconexión.

##### ✅ Cheatcodes (Pausa, K+I+L, I+N+F)
- Los cheatcodes están bien implementados. Puedes comprobar instantáneamente la suma de puntaje. "inf" permite pausar el juego (el conejo y las entidades dejan de moverse), "kil" hace que todas las entidades que no sean bombas desaparezcan, y los cañones dejan de disparar zanahorias.

##### ✅ Networking
- Se realiza una buena conexión entre el servidor y el cliente, enviando mensajes cuando se ingresa un usuario, se abre el juego, se pasa de nivel o se termina el juego.

##### ✅ Decodificación y ✅ Desencriptación
- Los métodos de decodificación y desencriptación están correctamente implementados, permitiendo enviar y recibir mensajes entre servidor y cliente de manera segura.

##### ✅ Funciones
- Se reutilizan algunas funciones de cliente y servidor, no todas, porque no encontré funcionalidad para mi juego en todas. Sin embargo, reutilizo algunas a través del módulo `funciones_cliente` o `funciones_servidor`.

##### ✅ Archivos
- El archivo `Puntajes.txt` es actualizado y leído correctamente por el servidor, siempre que el cliente quiera acceder a la información dentro de él.

---

## Ejecución :computer:

El archivo principal de la tarea es `main.py`, que se encuentra dentro de la carpeta `entrega_final/cliente`. También debes ejecutar `servidor.py`, que se encuentra en `entrega_final/cliente`.

### Archivos del Servidor:
1. `funciones_extras.py` en `servidor`
2. `funciones_servidor.py` en `servidor`
3. `puntajes.txt` en `servidor`
4. `host_servidor.json` en `servidor`

### Archivos del Cliente:
1. `main.py` -> Ejecuta tanto el backend como el frontend, y comienza la conexión con el servidor.
2. `host_cliente.json` -> Contiene el host de la comunicación con el servidor.

### En `cliente/frontend` se encuentran:
1. `ventana.py` -> Contiene la Ventana Inicio.
2. `ventana_juego.py` -> Contiene la Ventana Juego.
3. `rutas.py` -> Contiene una clase con atributos para las rutas de los sprites, separando las rutas de la ventana del juego.

### En `cliente/backend` se encuentran:
1. `logica.py` -> Contiene 2 clases:
    a. `Backend` -> Encargada de contactar al servidor.
    b. `LogicaJuego` -> Encargada de manejar toda la lógica del juego.
2. `funciones_extras.py`
3. `funciones_cliente.py`
4. `parametros.py`
5. `clases.py` -> Contiene 2 clases:
    a. `Conejo` -> Modela el movimiento del conejo (con `QTimer`).
    b. `EntidadNpc` -> Modela el movimiento de los NPC del juego, como lobos y cañones de zanahorias.

## Librerías :books:

### Librerías Externas Utilizadas
No se utilizaron librerías externas más allá de las necesarias para ejecutar la GUI con PyQt6.

## Consideraciones Adicionales :thinking:

### 1. 
Para enviar mensajes entre cliente y servidor, mi protocolo siempre manda un mensaje con una operación. Dado el formato de mis funciones de decodificación y desencriptación, se envían varios números como "11111111" o "22222222", donde cada número representa una operación específica, como pedir ranking, ingresar un usuario, reescribirlo o salir (con "0").

### 2. 
Para el siguiente código en `ventana_juego.py`, que puede parecer complejo, aquí te explico lo que hace:

```python
def colocar_entidad(self, entidad: str, posicion_inicial: tuple, id: int):
    """---Este método coloca las entidades del juego en el mapa---"""
    rutas = Rutas()
    rutas_entidades = rutas.rutas_sprites["rutas_entidades"]
    rutas_zanahorias = rutas.rutas_sprites["rutas_zanahorias"]
    entidad_img = QLabel(entidad, self)
    ruta = rutas_entidades[entidad]
    pixeles = QPixmap(ruta)
    self.setear_imagen(entidad_img, pixeles)
    x, y = posicion_inicial
    if y < 10:
        entidad_img.move(310 + (40 * x), 20 + (40 * y))
    else:
        entidad_img.move(310 + (40 * x), 10 + (40 * y))
    self.entidades[id] = [entidad_img, entidad]
    entidad_img.show()
    
    # --- Para zanahorias: cambio la imagen del cañón por la zanahoria ---
    if entidad in ["CU", "CD", "CR", "CL"]:
        zanahoria_img = QLabel(entidad, self)
        ruta = rutas_zanahorias[entidad]
        pixeles = QPixmap(ruta)
        self.setear_imagen(zanahoria_img, pixeles)
        self.entidades[id][0] = zanahoria_img
        x, y = posicion_inicial
        if y < 10:
            zanahoria_img.move(310 + 40 * x, 20 + 40 * y)
        else:
            zanahoria_img.move(310 + 40 * x, 10 + 40 * y)
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

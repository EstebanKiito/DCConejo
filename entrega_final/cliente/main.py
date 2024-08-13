import backend.logica as logica
import frontend.ventana as ventana
import frontend.ventana_juego as ventana_juego
from PyQt6.QtWidgets import QApplication
import sys
import json

if __name__ == "__main__":
    # Hook para imprimir errores
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication(sys.argv)

    frontend = ventana.VentanaInicio()
    PORT = 8001 if len(sys.argv) < 2 else int(sys.argv[1])
    with open('host_cliente.json', 'r') as archivo:
        host = json.load(archivo)
        HOST = host["host"] if len(sys.argv) < 3 else sys.argv[2]
    backend = logica.Backend(PORT, HOST)
    juego = ventana_juego.VentanaJuego()

    ranking = backend.pedir_raking()
    frontend.actualizar_ranking(ranking)

    logica_juego = logica.LogicaJuego()

    # Conectamos señales
    frontend.senal_pedir_ranking.connect(backend.operacion_ranking)
    backend.senal_actualizar_ranking.connect(frontend.actualizar_ranking)
    
    frontend.senal_salir.connect(backend.operacion_salir)
    frontend.senal_procesar_usuario.connect(backend.procesar_nombre)
    backend.senal_usuario_revisado.connect(frontend.recibir_info_usuario)

    frontend.senal_abrir_juego.connect(logica_juego.start)
    backend.senal_abrir_ventana_juego.connect(juego.mostrar_ventana_juego)
    backend.senal_enviar_user_nivel.connect(juego.setear_nivel)
    backend.senal_enviar_nivel.connect(logica_juego.abrir_mapa)
    backend.senal_enviar_nivel_2.connect(logica_juego.abrir_mapa)
    backend.senal_enviar_puntaje.connect(logica_juego.setear_puntaje)
    juego.senal_detener_tiempo.connect(logica_juego.detener_tiempo)

    logica_juego.senal_enviar_entidad.connect(juego.colocar_entidad)
    logica_juego.senal_actualizar_tiempo_vidas_puntajes.connect(juego.reloj)
    logica_juego.senal_mover_icono.connect(juego.mover_entidad)

    juego.senal_tecla.connect(logica_juego.tecla_a_conejo)
    logica_juego.senal_cambiar_spirte_conejo.connect(juego.animacion_conejo)
    logica_juego.senal_cambiar_spirte.connect(juego.animacion)

    juego.senal_pausa.connect(logica_juego.pausa)
    logica_juego.senal_detener_juego.connect(juego.salir)
    logica_juego.senal_victoria.connect(juego.pasar_nivel)
    logica_juego.senal_pasarse_el_juego.connect(juego.pasar_juego)

    backend.senal_desconexion_server.connect(juego.desconexion_servidor)    
    logica_juego.senal_backend_avanzar_nivel.connect(juego.reset_entidades)

    logica_juego.avisar_backend_avanzar_nivel.connect(backend.nuevo_nivel)
    logica_juego.senal_perdiste.connect(juego.perdiste)
    
    juego.senal_cheatcode.connect(logica_juego.cheatcode)
    logica_juego.senal_matar_todos.connect(juego.matar_todos)

    sys.exit(app.exec())

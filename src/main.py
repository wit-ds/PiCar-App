import asyncio
import websockets
import json
import threading
import logging
import os
from flask import Flask, render_template, Response, send_from_directory
from flask_cors import CORS
import components.raspberry as raspberryInfos
import logic

# Configuration du journal pour une meilleure traçabilité
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Intégration de la caméra
from components.camera_opencv import Camera
camera = Camera()

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

dir_path = os.path.dirname(os.path.realpath(__file__))

@app.route('/api/img/<path:filename>')
def sendimg(filename):
    return send_from_directory(dir_path+'/dist/img', filename)

@app.route('/js/<path:filename>')
def sendjs(filename):
    return send_from_directory(dir_path+'/dist/js', filename)

@app.route('/css/<path:filename>')
def sendcss(filename):
    return send_from_directory(dir_path+'/dist/css', filename)

@app.route('/api/img/icon/<path:filename>')
def sendicon(filename):
    return send_from_directory(dir_path+'/dist/img/icon', filename)

@app.route('/fonts/<path:filename>')
def sendfonts(filename):
    return send_from_directory(dir_path+'/dist/fonts', filename)

@app.route('/<path:filename>')
def sendgen(filename):
    return send_from_directory(dir_path+'/dist', filename)

@app.route('/')
def index():
    return send_from_directory(dir_path+'/dist', 'index.html')

async def check_permit(websocket):
    """
    Vérifie les informations d'identification envoyées par le client via le WebSocket.
    """
    while True:
        recv_str = await websocket.recv()
        cred_dict = recv_str.split(":")
        if len(cred_dict) != 2:
            response_str = "Format invalide. Utilisez 'username:password'."
            await websocket.send(response_str)
            continue

        username, password = cred_dict
        if username == "admin" and password == "123456":
            response_str = (
                "Félicitations, vous êtes connecté au serveur.\r\n"
                "Vous pouvez maintenant effectuer d'autres actions."
            )
            await websocket.send(response_str)
            return True
        else:
            response_str = (
                "Désolé, le nom d'utilisateur ou le mot de passe est incorrect. "
                "Veuillez réessayer."
            )
            await websocket.send(response_str)

async def recv_msg(websocket):
    """
    Reçoit et traite les messages du client via le WebSocket.
    """
    while True:
        response = {
            'status': 'ok',
            'title': '',
            'data': None
        }

        try:
            data = await websocket.recv()
            data = json.loads(data)
        except json.JSONDecodeError:
            logger.warning('Le message reçu n\'est pas un JSON valide.')
            continue
        except websockets.exceptions.ConnectionClosed:
            logger.info('Connexion fermée par le client.')
            break
        except Exception as e:
            logger.error(f'Erreur inattendue lors de la réception du message : {e}')
            break

        if not data:
            logger.warning('Message JSON vide reçu.')
            continue

        if isinstance(data, str):
            if data == 'get_info':
                response['title'] = 'get_info'
                response['data'] = {
                    'cpu_temp': raspberryInfos.get_cpu_tempfunc(),
                    'cpu_usage': raspberryInfos.get_cpu_use(),
                    'ram_info': raspberryInfos.get_ram_info(),
                    'swap_info': raspberryInfos.get_swap_info(),
                    'gpu_temp': raspberryInfos.get_gpu_tempfunc()
                }
            else:
                robot.move(data, response)
        else:
            logger.warning('Type de message non pris en charge.')

        logger.info(f'Données reçues : {data}')
        response_json = json.dumps(response)
        await websocket.send(response_json)
        # logger.info(f'Données envoyés : {response_json}')

async def main_logic(websocket, path):
    """
    Gère la logique principale de la connexion WebSocket.
    """
    if await check_permit(websocket):
        await recv_msg(websocket)

def start_websocket_server():
    """
    Démarre le serveur WebSocket dans une boucle d'événements asynchrone.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(main_logic, '0.0.0.0', 8888)
    loop.run_until_complete(start_server)
    logger.info('Serveur WebSocket en attente de connexion...')
    loop.run_forever()

if __name__ == '__main__':
    # Initialisation de l'objet robot
    robot = logic.PiCar()

    try:
        # Démarrage de l'application Flask dans un thread séparé
        flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
        flask_thread.start()
        logger.info('Application Flask démarrée.')

        # Démarrage du serveur WebSocket dans un thread séparé
        websocket_thread = threading.Thread(target=start_websocket_server)
        websocket_thread.start()
        logger.info('Serveur WebSocket démarré.')
    except Exception as e:
        logger.error(f'Erreur lors du démarrage des serveurs : {e}')
        robot.setError('init error', e)

    robot.setInitied()

    try:
        # Attente de la fin des threads
        flask_thread.join()
        websocket_thread.join()
    except KeyboardInterrupt:
        logger.info('Interruption par l\'utilisateur détectée.')
    except Exception as e:
        logger.error(f'Erreur inattendue : {e}')
    finally:
        robot.cleanup()
        logger.info('Nettoyage et arrêt du programme.')

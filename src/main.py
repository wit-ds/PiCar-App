#!/usr/bin/env/python

import time
import threading
import socket
import asyncio
import websockets
import json

import flaskRoute
import raspberryInfos
import robotLight

async def check_permit(websocket):
    while True:
        recv_str = await websocket.recv()
        cred_dict = recv_str.split(":")
        if cred_dict[0] == "admin" and cred_dict[1] == "123456":
            response_str = "congratulation, you have connect with server\r\nnow, you can do something else"
            await websocket.send(response_str)
            return True
        else:
            response_str = "sorry, the username or password is wrong, please submit again"
            await websocket.send(response_str)

async def recv_msg(websocket):
    # global speed_set, modeSelect
    # move.setup()
    # direction_command = 'no'
    # turn_command = 'no'

    while True: 
        response = {
            'status' : 'ok',
            'title' : '',
            'data' : None
        }

        data = ''
        data = await websocket.recv()
        # try:
        #     data = await websocket.recv()
        # except:
        #     print("WEB interface disconnected!")
        #     move.destroy()      # motor stop.
        #     scGear.moveInit()   # servo  back initial position.

        try:
            data = json.loads(data)
        except Exception as e:
            print('not A JSON')

        if not data:
            continue

        if isinstance(data,str):
            # robotCtrl(data, response)

            # switchCtrl(data, response)

            # functionSelect(data, response)

            # configPWM(data, response)

            if 'get_info' == data:
                response['title'] = 'get_info'
                response['data'] = [
                    raspberryInfos.get_cpu_tempfunc(), 
                    raspberryInfos.get_cpu_use(), 
                    raspberryInfos.get_ram_info(),
                    raspberryInfos.get_swap_info(),
                    raspberryInfos.get_gpu_tempfunc()
                ]

            # if 'wsB' in data:
            #     try:
            #         set_B=data.split()
            #         speed_set = int(set_B[1])
            #     except:
            #         pass
            
            # elif 'reboot' == data:
            #     try:
            #         os.system('sudo reboot')
            #     except:
            #         pass
            
            # elif 'shutdown' == data:
            #     try:
            #         os.system('sudo halt')
            #     except:
            #         pass
                
            # elif 'AR' == data:
            #     modeSelect = 'AR'
            #     screen.screen_show(4, 'ARM MODE ON')
            #     try:
            #         fpv.changeMode('ARM MODE ON')
            #     except:
            #         pass

            # elif 'PT' == data:
            #     modeSelect = 'PT'
            #     screen.screen_show(4, 'PT MODE ON')
            #     try:
            #         fpv.changeMode('PT MODE ON')
            #     except:
            #         pass

            # #CVFL
            # elif 'CVFL' == data:
            #     flask_app.modeselect('findlineCV')

            # elif 'CVFLColorSet' in data:
            #     color = int(data.split()[1])
            #     flask_app.camera.colorSet(color)

            # elif 'CVFLL1' in data:
            #     pos = int(data.split()[1])
            #     flask_app.camera.linePosSet_1(pos)

            # elif 'CVFLL2' in data:
            #     pos = int(data.split()[1])
            #     flask_app.camera.linePosSet_2(pos)

            # elif 'CVFLSP' in data:
            #     err = int(data.split()[1])
            #     flask_app.camera.errorSet(err)

            # elif 'defEC' in data:#Z
            #     fpv.defaultExpCom()

        # elif(isinstance(data,dict)):
        #     if data['title'] == "findColorSet":
        #         color = data['data']
        #         flask_app.colorFindSet(color[0],color[1],color[2])

        # if not functionMode:
        #     if OLED_connection:
        #         screen.screen_show(5,'Functions OFF')
        else:
            pass

        print(data)
        response = json.dumps(response)
        await websocket.send(response)

async def main_logic(websocket, path):
    await check_permit(websocket)
    await recv_msg(websocket)


if __name__ == '__main__':
    # switch.switchSetup()
    # switch.set_all_switch_off()

    global flask_app
    flask_app = flaskRoute.webapp()
    flask_app.startthread()

    # """ 
    # If the Raspberry Pi is disconnected from the Internet, stop the car from moving.
    # Reconnect to the network, you can continue to control the car.
    # If you need this function, please enable the following three lines of code.
    # Note: The program will additionally occupy the running memory of the Raspberry Pi.
    # """
    # testNC_threading=threading.Thread(target=test_Network_Connection)
    # testNC_threading.setDaemon(False)
    # testNC_threading.start()                                     


    try:
        RL=robotLight.RobotLight()
        RL.start()
        RL.breath(70,70,255)
    except:
        print('Utilisez "sudo pip3 install rpi_ws281x" pour installer le package WS_281x\nUtilisez la commande "sudo pip3 install rpi_ws281x" pour installer rpi_ws281x')
        pass

    try:
        start_server = websockets.serve(main_logic, '0.0.0.0', 8888)
        asyncio.get_event_loop().run_until_complete(start_server)
        print('waiting for connection...')
    except Exception as e:
        print(e)
        RL.setColor(0,0,0)

    try:
        RL.setColor(0,80,255)
    except:
        pass

    try:
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        print(e)
        RL.setColor(0,0,0)
        # move.destroy()

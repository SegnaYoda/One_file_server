import socket
import json
from typing import Set


class AccountStorageInterface:
    def __init__(self):
        pass
    def save_account(self):
        pass
    def get_account():
        pass
    def put_account(self):
        pass
    def delete_account(self):
        pass

class ServerInterface:   
    def start_my_server(self):
        pass
    def load_page_from_get_request(self):
        pass

class Acount(AccountStorageInterface):   #класс аккаунтов
    def __init__(self, name, city, age, id = None):
        self.name = name
        self.city = city
        self.age = age
        self.id = id

class ArrayAccountsStorage(AccountStorageInterface):
    def save_account(self, new_acount): #функция по добавлению нового аккаунта в словарь acount_set и добавление id в этот аккаунт
        global list_id, acount_set
        self.new_acount = new_acount
        print('***SAVE***')
        for i in list_id:  #перебор словаря с id
            if list_id[i] == False: #если знач id False, значит id не занят
                acount_set[i] = self.new_acount
                list_id[i] = True
                print('!добавлен новый аккаунт!!!')
                print('list_id', list_id)
                for key in acount_set: print(acount_set.get(key).name, acount_set.get(key).id)
                return i 
        j = len(list_id) + 1        #если все id заняты создаются новые id
        list_id[j] = True
        acount_set[j] = self.new_acount
        print('second wave')
        return j
    def get_account():
        print('***GET***')
        global acount_set
        time_list = []
        for key in acount_set: 
            time_list.append(json.dumps(acount_set.get(key).__dict__))
        print(time_list)
        print(type(json.dumps('Information found.').encode('utf-8') + json.dumps(time_list, indent=4).encode('utf-8')))
        return json.dumps('Information found.').encode('utf-8') + json.dumps(time_list, indent=4).encode('utf-8')
    def put_account(self, data_put):
        global acount_set
        self.data_put = data_put
        print('***PUT***')
        if ('id' in self.data_put) and (self.data_put['id'] in list_id) and (list_id[self.data_put['id']] == True):
            update_data = acount_set[self.data_put['id']]
            print('id , который необходимо обновить', self.data_put['id'])
            for key in self.data_put:
                if key == 'name': update_data.name = self.data_put[key]
                elif key == 'city': update_data.city = self.data_put[key]
                elif key == 'age': update_data.age = self.data_put[key]
            acount_set[self.data_put['id']] = update_data
            return 'Обновление аккаунта завершено.'.encode('utf-8')
        else: 
            print('Такого аккаунта не найдено. Проверьте правильность ввода данных.')
            return 'Такого аккаунта не найдено. Проверьте правильность ввода данных.'.encode('utf-8')
    def delete_account(self, data_delete):
        global list_id, acount_set
        self.data_delete = data_delete
        print('***DELETE***')
        print(self.data_delete)
        if ('id' in self.data_delete) and (self.data_delete['id'] in list_id) and (list_id[self.data_delete['id']] == True):
            del acount_set[self.data_delete['id']]
            list_id[self.data_delete['id']] = False
            print('id', self.data_delete['id'], 'удален')
            return 'Удаление аккаунта завершено.'.encode('utf-8')
        else: 
            print('Такого аккаунта не найдено. Проверьте правильность ввода данных.')
            return 'Такого аккаунта не найдено. Проверьте правильность ввода данных.'.encode('utf-8')
    
class Server(ServerInterface):
    def start_my_server(self):  #Сервер
        try:
            # START SERVER:
    
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #AF_INET говрит о сетевом использовании, SOCK_STREAM - использование протокола TCP
            server.bind(('127.0.0.1', 2000))    # создание сервера по указанным адресам
            server.listen(10)  # сервер ожидает запросы, + указано количество клиентов в очереди, остальным будет отказано в соединении
            while True:
                print('***************************************' + '\n' + 'jdite rabotaem...')
            # ОЖИДАНИЕ:
                client_socket, address = server.accept()    # определяет наличие запросов, старт процесса установления TCP соединения через "тройное рукопожатие" SYN - SYN+ACK - ACK
                # по окончанию рукопажатия метод .accept возвращает сокет клиента(client_socket) и его ip адрес (address)
            # ОБРАБОТКА ЗАПРОСА:
                data= client_socket.recv(1024).decode('utf-8')  # буфер получаемых данных равен 1024
                '''
                # правильная обработка полученных данных, учитывающих, что наши данные будут приходить по частям, но будут собираться вместе
                def myreceive(sock, msglen):    #msglen - длина документа
                    msg = ''
                    while len(msg) < msglen:
                        chunk = sock.recv(msglen-len(msg))
                        if chunk == '':
                            raise RuntimeError('broken')
                        msg = msg + chunk
                    return msg
                '''
                print(data)
                if len(data) != 0:
                    print('command' + '\t' + '\t' + data.split(' ')[1] + '\n')
                content = self.load_page_from_get_request(data)
            # ANSWER TO CLIENT:
                client_socket.send(content)
                '''
                # при условии, что клиент не готов принять файл целиком (файл большой по размерам), необходимо отправлять данные по частям
                def mysend(sock,  msg):
                    totalsent = 0
                    while totalsent < len(msg):
                        sent = sock.send(msg[totalsent:])
                        if sent == 0:
                            raise RuntimeError('broken')
                        totalsent = totalsent + sent
                '''
                client_socket.close() #закрыть соединение
                client_socket.shutdown(socket.SHUT_WR)
        except KeyboardInterrupt:
            print('zakryavaem....')
    def load_page_from_get_request(self, request_data):  # обработчик запроса
        global acount_set, list_id
        self.request_data = request_data
        HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8 \r\n\r\n'.encode('utf-8')
        # заголовок HTTP для корректной работы ответа сервера клиенту
        try:
            path_req = self.request_data.split(' ')[0]       # ---> POST <--- /list HTTP/1.1
            path_host = self.request_data.split(' ')[1]      # GET ---> /list <--- HTTP/1.1
            if path_host == '/acount' or '/Acount':  # CRUD realisation
                if path_req == 'POST':  # POST  create      добавление нового аккаунта
                    data_post = Acount(**json.loads(self.request_data.split('\r\n\r\n')[1]))
                    data_post.id = ArrayAccountsStorage.save_account(self, data_post)
                    return HDRS + 'Dannye polucheny.'.encode('utf-8')
                elif path_req == 'GET':  # GET   read       отправление списка аккаунтов
                    return 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n'.encode('utf-8') + ArrayAccountsStorage.get_account()
                elif path_req == 'PUT':  # PUT    update
                    a = json.loads(self.request_data.split('\r\n\r\n')[1])
                    print(a)
                    return HDRS + ArrayAccountsStorage.put_account(self, a)
                elif path_req == 'DELETE':  # DELETE  delete
                    return HDRS + ArrayAccountsStorage.delete_account(self, json.loads(self.request_data.split('\r\n\r\n')[1]))
                elif path_req == 'PATCH':  # PATCH 
                    print('_____%______')
                    print(self.request_data)
                    print('_____%______')
                    print(type(self.request_data.split('\r\n\r\n')[1]))
                    print('_____%______')
                    #print(json.loads(self.request_data.split('\r\n\r\n')[1]))
                    print('_____%______')
                    #lits = json.loads(self.request_data.split('\r\n\r\n')[1])
                    #for i in lits:
                        #print(json.loads(i))
                    
                    return 'HTTP/1.1 200 OK\r\nContent-Type: text/json; charset=utf-8 \r\n\r\n'.encode('utf-8') + (self.request_data.split('\r\n\r\n')[1]).encode('utf-8')

            elif path_host == '/list_auto':
                with open('list/list1.html', 'rb') as file:
                    response = file.read()
                return HDRS + response

            elif path_host == '/favicon.ico':
                with open('list/favicon.ico', 'rb') as file:
                    response = file.read()
                return HDRS + response
            else:
                return 'HTTP/1.1 404 Page not found\r\nContent-Type: text/json; charset=utf-8\r\n\r\n'.encode('utf-8')

        except IndexError:
            return HDRS + 'IndexError: list index out of range'.encode('utf-8')
    

my_server = Server()

misha = Acount('Misha', 'Minsk', 26, id = 1)
serg = Acount('Serg', 'Volo', 28, id = 2)

acount_set = { 1: misha, 2: serg }
list_id = {1: True, 2: True, 3: False}

if __name__ == '__main__':
    my_server.start_my_server()






#Misha = json.dumps(Misha, indent=4, cls=ACOUNT)
# print(json.dumps(Misha.__dict__))




# test for post new acount:         
# {"name": "Fedor", "city": "Lissabon", "age": 97}
# {"name": "Olga", "city": "Milan", "age": 23}

# test for update acount:
# { "id": 2, "name": "Dina", "age": 15}

# test for delete acount:
# { "id": 2}

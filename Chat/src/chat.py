from connection import *
from server import *
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from serialize import load_from_file, save_to_file
import os
from filesplitter import FileSplitterReader, FileSplitterWriter
import time

class ChatHttpServer(BaseHTTPRequestHandler):
    timeout = 5
    def do_POST(self): # do Post Request
        path = self.path
        req = self.rfile.read(int(self.headers['Content-Length']))
        obj = None
        if len(req) > 0:
            obj = json.loads(req.decode('utf-8'))
        res = json.dumps(self.server.callback(self.path, obj)).encode('utf-8') # from Python to Json
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(res)

    def do_GET(self): # do Get Request
        path = self.path
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open(self.server.base + '/html' + path, 'rb') as f:
            self.wfile.write(f.read())
        
    def log_message(self, format: str, *args) -> None:
        pass

class ChatClient:
    def __init__(self, port = 8000, info = ('127.0.0.1', 8080), base=os.path.join(os.path.expanduser('~'), '.chatclient')) -> None:
        self.base = base
        self.new_msg_list = []
        self.render_server = HTTPServer(('127.0.0.1', port), ChatHttpServer)
        self.login = 0
        self.file_name_map = {}
        self.recv_thread_ctrl_continue = set()
        self.recv_thread_ctrl_wait = set()
        self.file_list = {}
        self.download = os.path.join(self.base, 'files')
        self.userId = 'Guest'
        if not os.path.exists(self.download):
            os.makedirs(self.download)
        def __send_file(self, conn : RawConnection, target : str, file_reader : FileSplitterReader, fileName : str):
            head = ('f'+target+'/'+fileName+'\0').encode('utf-8')
            head2 = ('e'+target+'/'+fileName+'/'+target).encode('utf-8')
            while not file_reader.eof():
                self.connection.send(head+file_reader.read()[1])
            self.connection.send(head2)
        def __callback(req_path, req_obj):
            # 页面渲染通信部分
            if req_path == '/send_msg':
                self.connection.send(json.dumps({'type':'Private-Message', 'target':req_obj['target'], 'msg_type':req_obj['type'], 'msg':req_obj['msg']}).encode('utf-8'))
                return None
            elif req_path == '/send_group_msg':
                self.connection.send(json.dumps({'type':'Group-Message', 'target':req_obj['target'], 'msg_type':req_obj['type'], 'msg':req_obj['msg']}).encode('utf-8'))
            elif req_path == '/fetch_msg_list':
                res = {'msg':self.new_msg_list.copy()}
                self.new_msg_list.clear()
                return res
            elif req_path == '/login':
                self.connection.send(json.dumps({'type':'Login', 'username':req_obj['username'], 'password':req_obj['password']}).encode('utf-8'))
                self.userId = req_obj['username']
                return None
            elif req_path == '/get_login_info':
                return {'login':str(self.login)}
            elif req_path == '/send_file':
                self.file_name_map['fileName']=req_obj['filePath']
                self.connection.send(json.dumps({'type':'Private-File', 'target':req_obj['target'], 'fileName':os.path.basename(req_obj['filePath'])}).encode('utf-8'))
                thread = Thread(target = __send_file, args = (self, self.connection, req_obj['target'], FileSplitterReader(req_obj['filePath']), os.path.basename(req_obj['filePath'])))
                thread.setDaemon(True)
                thread.start()
                return None
            elif req_path == '/file_op':
                if req_obj['op'] == 'start':
                    path = os.path.join(self.download, req_obj['target'], req_obj['fileName'])
                    if not os.path.exists(path+'.chatdownload'):
                        save_to_file(path+'.chatdownload', {'delta':0})
                    delta = int(load_from_file(path+'.chatdownload')['delta'])
                    fw = FileSplitterWriter(path)
                    fw.set_pos(delta)
                    self.file_list[(req_obj['target'], req_obj['fileName'])] = (req_obj['fileName'], path, fw)
                    self.connection.send(json.dumps({'type':'Fetch-File-Data', 'target':req_obj['target'], 'fileName':req_obj['fileName'], 'delta':str(delta)}).encode('utf-8'))
                elif req_obj['op'] == 'stop':
                    self.connection.send(json.dumps({'type':'Stop-Recv-File-Data', 'target':req_obj['target'], 'fileName':req_obj['fileName']}).encode('utf-8'))
                return None
        self.render_server.callback = __callback
        self.render_server.base = self.base
        def __serve():
            self.render_server.serve_forever()
        self.thread = Thread(target=__serve)
        self.thread.setDaemon(True)
        self.thread.start()
        self.connection = RawConnection(connect_to(info))
        @self.connection
        def __client_callback(conn : RawConnection, msg, self=self):
            # 客户端通信部分
            if msg[0] == ord('f'):
                spl = msg.index(b'\0')
                fileId = msg[1:spl].decode('utf-8')
                data = msg[spl+1:]
                t = tuple(fileId.split('/'))
                name, path, writer = self.file_list[t]
                writer.write(data)
                if writer.part_recv%100 == 0:
                    print('Recv {}: ({}k)'.format(fileId, writer.part_recv))
                return
            elif msg[0] == ord('e'):
                fileId = msg[1:].decode('utf-8')
                t = tuple(fileId.split('/'))
                name, path, writer = self.file_list[t]
                tmpf = path+'.chatdownload'
                save_to_file(tmpf, {'delta':writer.part_recv})
                #name, path, writer = self.file_list[t]
                self.file_list.pop(t)
                return
            data = json.loads(msg.decode('utf-8'))
            print('[Client]', self.userId, msg)
            if data['type'] == 'Private-Message':
                self.new_msg_list.append({'source':'private', 'type':data['msg_type'], 'userId':data['userId'], 'msg':data['msg'], 'target':data['target']})
            elif data['type'] == 'Group-Message':
                self.new_msg_list.append({'source':'group', 'type':data['msg_type'], 'groupId':data['groupId'], 'userId':data['userId'], 'msg':data['msg']})
            elif data['type'] == 'Login-Info':
                self.login = 1
            elif data['type'] == 'Private-Message':
                self.new_msg_list.append({'source':'private', 'userId':data['userId'], 'fileName':data['fileName']})
            elif data['type'] == 'Private-File':
                self.new_msg_list.append({'source':'private', 'userId':data['userId'], 'type':'file', 'fileName':data['fileName'], 'size':data['size'], 'target':data['target']})

class ChatServer:
    def __init__(self, base=os.path.join(os.path.expanduser('~'), '.chatserver')) -> None:
        config = load_from_file(os.path.join(base, 'config.json'))
        self.base = base
        conf_users = config['users']
        conf_groups = config['groups']
        self.password_list = {}
        self.group_list = {}
        self.file_list = {}
        for i in conf_users:
            self.password_list[i['username']] = i['password']
        for i in conf_groups:
            self.group_list[i['name']] = i['members']
        print(self.password_list)
        self.address = ('127.0.0.1', 8080)
        self.server = RawServer(self.address)
        self.connection_list = {}
        self.off_msg_list = {}
        self.not_stop_flags = set()
        def __send_file(conn : RawConnection, target : str, file_reader : FileSplitterReader, fileName : str, delta : int):
            print('[Server]Send', fileName)
            head = ('f'+target+'/'+fileName+'\0').encode('utf-8')
            head2 = ('e'+target+'/'+fileName).encode('utf-8')
            file_reader.set_pos(delta)
            t = (target, fileName)
            while (not file_reader.eof()) and t in self.not_stop_flags:
                conn.send(head+file_reader.read()[1])
            conn.send(head2)
        @self.server
        def __server_callback(conn : RawConnection, msg):
            # 服务端通信部分
            if msg[0]==ord('f'):
                spl=msg.index(b'\0')
                fileId=msg[1:spl].decode('utf-8')
                data=msg[spl+1:]
                t = tuple(fileId.split('/'))
                path, writer = self.file_list[(conn.id, t[0], t[1])]
                writer.write(data)
                if writer.part_recv%100 == 0:
                    print('Recv {}: ({}k)'.format(conn.id, writer.part_recv))
                return
            elif msg[0]==ord('e'):
                fileId=msg[1:].decode('utf-8')
                t = tuple(fileId.split('/'))
                path, writer = self.file_list[(conn.id, t[0], t[1])]
                self.file_list.pop((conn.id, t[0], t[1]))
                del writer
                target = t[0]
                name = t[1]
                if target in self.connection_list.keys():
                    self.connection_list[target].send(json.dumps({'type':'Private-File', 'target':target, 'fileName':name,'userId':conn.id, 'size':os.path.getsize(path), 'timestamp':time.time()}).encode('utf-8'))
                else:
                    if not target in self.off_msg_list.keys():
                        self.off_msg_list[target] = []
                    self.off_msg_list[target].append(json.dumps({'type':'Private-File', 'target':target, 'fileName':name,'userId':conn.id, 'size':os.path.getsize(path), 'timestamp':time.time()}).encode('utf-8'))
                conn.send(json.dumps({'type':'Private-File', 'fileName':name, 'target':target, 'userId':conn.id, 'size':os.path.getsize(path), 'timestamp':time.time()}).encode('utf-8'))
                return
            print('[Server]', conn, conn.id, msg)
            data = json.loads(msg.decode('utf-8'))
            if data['type'] == 'Login':
                username = data['username']
                if username in self.password_list.keys():
                    if self.password_list[username] == data['password']:
                        print(username, 'Login.')
                        self.connection_list[data['username']] = conn
                        conn.id = data['username']
                        conn.send(json.dumps({'type':'Login-Info', 'status':'ok'}).encode('utf-8'))
                        if conn.id in self.off_msg_list.keys():
                            for msg in self.off_msg_list[conn.id]:
                                conn.send(msg)
            elif data['type'] == 'Private-Message':
                data['userId'] = conn.id
                data['timestamp'] = time.time()
                self.connection_list[data['target']].send(json.dumps(data).encode('utf-8'))
                conn.send(json.dumps(data).encode('utf-8'))
            elif data['type'] == 'Group-Message':
                if data['target'] in self.group_list.keys():
                    if conn.id in self.group_list[data['target']]:
                        data['groupId'] = data['target']
                        data.pop('target')
                        data['userId'] = conn.id
                        data['timestamp'] = time.time()
                        for target in self.group_list[data['groupId']]:
                            if target in self.connection_list.keys():
                                self.connection_list[target].send(json.dumps(data).encode('utf-8'))
            elif data['type'] == 'Private-File':
                if not os.path.exists(os.path.join(self.base, 'files', conn.id, data['target'])):
                    os.makedirs(os.path.join(self.base, 'files', conn.id, data['target']))
                path = os.path.join(self.base, 'files', conn.id, data['target'], data['fileName'])
                self.file_list[(conn.id, data['target'], data['fileName'])] = (path, FileSplitterWriter(path))
            elif data['type'] == 'Fetch-File-Data':
                self.not_stop_flags.add((data['target'], data['fileName']))
                path = os.path.join(self.base, 'files', data['target'], conn.id, data['fileName'])
                thread = Thread(target=__send_file, args=(conn, data['target'], FileSplitterReader(path), data['fileName'], int(data['delta'])))
                thread.setDaemon(True)
                thread.start()
            elif data['type'] == 'Stop-Recv-File-Data':
                self.not_stop_flags.remove((data['target'], data['fileName']))
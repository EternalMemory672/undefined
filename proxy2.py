import socket
import re

PROXY_PORT = 1080
bufsize = 65536


class Server:
    def __init__(self, sock=None):
        self.socket = sock

    def recv_all_data(self, from_client=False):
        """
        :param from_client:
            �����տͻ��������ʱ��,�����post���ͻ���Content-Length����ֹ����
            �����get�Ļ�����β����\r\n\r\n
        :return:
        """
        sock = self.socket
        data = sock.recv(bufsize)
        if b'Content-Length' in data:  # ����ûѹ����ʱ����Content-Length�ж������Ƿ������
            length = re.search(r'Content-Length: (\d+)', data.decode(encoding='utf8')).group(1)
            head_length = len(data.split(b'\r\n\r\n')[0]) + 4
            total = int(length) + head_length  # ��Ӧͷ+���ݳ��� = �ܳ���
            while len(data) != total:
                data += sock.recv(bufsize)
        else:  # ����ѹ�������ʱ����b'\r\n0\r\n\r\n'�ж��Ƿ������ ���� from_client=Ture ������get��ʱ��
            condition = b'\r\n\r\n' if from_client else b'\r\n0\r\n\r\n'
            while data[-len(condition):] != condition:
                data += sock.recv(bufsize)
        return data

    @staticmethod
    def get_host_port(data: bytes):
        data = data.decode(encoding='utf8')
        if 'http://' in data:
            host = data.split('\r\n')[1].split()[1]
            port = 80
        else:
            host = re.search(r'\s([^\s]+):443', data).group(1)
            port = 443

        return host, port

    @classmethod
    def get_web_data(cls, addr, _send_data):
        sender = socket.socket()
        sender.connect(addr)
        sender.sendall(_send_data)
        result = cls(sender).recv_all_data()
        sender.close()
        return result


if __name__ == '__main__':
    server = socket.socket()
    server.bind(('0.0.0.0', PROXY_PORT))
    server.listen(1024)
    while True:
        origin_conn, origin_addr = server.accept()
        send_data = Server(origin_conn).recv_all_data(from_client=True)
        target_addr = Server.get_host_port(send_data)
        result_data = Server.get_web_data(target_addr, send_data)
        origin_conn.sendall(result_data)
        origin_conn.close()
    server.close()
    print('end')
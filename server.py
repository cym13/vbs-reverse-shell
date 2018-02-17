#!/usr/bin/env python3

import socketserver

PORT=80

class CmdHttpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(2**14).strip().decode("UTF-8")

        if len(self.data) == 0:
            return

        elif self.data.splitlines()[0].startswith("GET"):
            command = input("%s > " % self.client_address[0]).encode("UTF-8")

            response = (b"HTTP/1.1 200\ncontent-length: "
                        + str(len(command)).encode("UTF-8")
                        + b"\n\n"
                        + command)

            self.request.sendall(response)


        elif self.data.splitlines()[0].startswith("POST"):
            data = self.request.recv(2**14).strip().decode("UTF-8")
            print(data)
            print()

            response = (b"HTTP/1.1 200\ncontent-length: 0\n\n")
            self.request.sendall(response)
            return


        else:
            print(self.data.decode("UTF-8"))
            response = (b"HTTP/1.1 300\ncontent-length: 0\n\n")
            self.request.sendall(response)


def main():
    print("To close connection enter 'EXIT'")
    print("The computer may be stalled by some commands, just try again")
    print()

    with socketserver.TCPServer(("0.0.0.0", PORT), CmdHttpHandler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()

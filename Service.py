
from common import Server
from common import Parser

if __name__ == '__main__':
    parser = Parser.TransDataParser()
    controler = Server.ControlServer("d:\TestByGJY.db")
    controler.setParser(parser)
    controler.start(51999)
    pass
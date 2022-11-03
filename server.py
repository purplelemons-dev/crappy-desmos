
import http.server
import matplotlib.pyplot as plt
from math import pi

class Server (http.server.SimpleHTTPRequestHandler):

    X=[i/100 for i in range(-1000,1000)]

    def _200(self,message:str):
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()
        self.wfile.write(message.encode())
        return
    
    def _404(self):
        self.send_response(404)
        self.send_header("Content-type","text/html")
        self.end_headers()
        self.wfile.write("404 Not Found".encode())
        return
    
    def _200_file(self, filename:str):
        self.send_response(200)
        # Image/JPEG
        if filename.split(".")[-1] in ("jpg","jpeg","png","gif"): self.send_header("Content-type","image/jpeg")
        # Audio/MPEG
        elif filename.split(".")[-1] in ("mp4","mp3","wav"): self.send_header("Content-type","audio/mpeg")
        # Text/JavaScript
        elif filename.split(".")[-1] in ("js"): self.send_header("Content-type","text/javascript")
        # Text/CSS
        elif filename.split(".")[-1] in ("css"): self.send_header("Content-type","text/css")
        # Text/HTML
        else: self.send_header("Content-type","text/html")
        self.end_headers()
        with open(filename, "rb") as f: self.wfile.write(f.read())
        return

    def do_GET (self):
        if self.path == '/':
            self._200_file("pages/index.html")
        elif self.path == '/favicon.ico':
            self._200_file("images/favicon.ico")
        else:
            try: self._200_file(self.path[1:])
            except: self._404()
        return
    
    def do_POST (self):
        if self.path == '/func':
            query=self.rfile.read(int(self.headers['Content-Length'])).decode()
            # Plot the function
            plt.clf()
            query=query.lower().replace("x","{}")
            y=[]
            for x in self.X:
                a=query.format(f"({x})")
                exec(f"y.append({a})")
            plt.plot(self.X,y)
            # Save the plot
            plt.savefig("images/plot.png")
            self._200_file("images/plot.png")
        else: self._404()
        return


if __name__ == "__main__":
    httpd = http.server.HTTPServer(("0.0.0.0", 8080), Server)
    httpd.serve_forever()

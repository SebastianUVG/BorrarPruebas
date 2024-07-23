import struct

def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # 2 bytes
    return struct.pack('=h', w)

def dword(d):
    # 4 bytes
    return struct.pack('=l',d)

class Renderer(object):
    def __init__(self,screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect()
        self.glColor(1,1,1)
        self.glClearColor(0,0,0)
        self.glClear()



    def glColor(self,r,g,b):
        r = min(1,max(0,r))
        g = min(1,max(0,g))
        b = min(1,max(0,b))

        self.currColor = [r,g,b]


    def glClearColor(self,r,g,b):
        r = min(1,max(0,r))
        g = min(1,max(0,g))
        b = min(1,max(0,b))

        self.clearColor = [r,g,b]

    def glClear(self):
        color  = [int(i*255) for i in (self.clearColor)]
        self.screen.fill(color)

        self.frameBuffer = [[self.clearColor for y in range(self.height)]
                            for x in range(self.width)]
    
    def glPoint(self,x,y,color = None):
        #pygame empieza a renderizar desde la esquina superior izquierda
        #hay que voltear el valor de y
        if(0<=x<self.width and 0<=y<self.height):
            #pygame recibe los colores en un rango de 0 a 255
            color  = [int(i*255) for i in (color or self.currColor)]
            self.screen.set_at((x,self.height - 1 - y),color)
            self.frameBuffer[x][y] = color


    def glLine(self,v0,v1,color = None):
        # y = mx + b 
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        #Algoritmo de Lineas de Bresenham
        # Si el punto 0 es igual al punto 1, solamente se dibuja un punto 
        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y0)
            return 
        
        dy = abs(y1 - y0) 
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0,y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0 , y1 = y1, y0

        dy = abs(y1 - y0) 
        dx = abs(x1 - x0)
        offset = 0

        limit = 0.75
        m = dy /dx 
        y = y0

        for x in range(x0,x1+1):
            if steep:
                self.glPoint(y,x,color or self.currColor)
            else:
                self.glPoint(x,y,color or self.currColor)

            offset += m

            if offset >= limit: 
                if y0 <y1 :
                     y+= 1
                else: 
                    y-=1

                limit += 1


    def glFillPolygon(self, polygon, color=None):
        n = len(polygon)
        sum_x = sum(p[0] for p in polygon)
        sum_y = sum(p[1] for p in polygon)
        centroide_x = sum_x / n
        centroide_y = sum_y / n
        self.flood_fill(round(centroide_x), round(centroide_y), color or self.currColor)

    def flood_fill(self, x, y, replacement_color):
        target_color = self.frameBuffer[x][y]
        if target_color == replacement_color:
            return
        stack = [(x, y)]
        while stack:
            current_x, current_y = stack.pop()
            if self.is_valid(current_x, current_y, target_color, replacement_color):
                self.glPoint(current_x, current_y, replacement_color)
                stack.append((current_x + 1, current_y))
                stack.append((current_x - 1, current_y))
                stack.append((current_x, current_y + 1))
                stack.append((current_x, current_y - 1))

    def is_valid(self, x, y, target_color, replacement_color):
        if 0 <= x < self.width and 0 <= y < self.height:
            current_color = self.frameBuffer[x][y]
            return current_color == target_color and current_color != replacement_color
        return False

        

        
    

    def glGenerateFrameBuffer(self, filename):

        with open(filename, "wb") as file:
        # Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # Info Header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    color = self.frameBuffer[x][y]
                    color = bytes([color[2],
                            color[1],
                            color[0]])

                    file.write(color)
                        

                    

    
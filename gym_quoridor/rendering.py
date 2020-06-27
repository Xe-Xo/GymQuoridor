
import numpy as np
import pyglet
from gym_quoridor.quoridorgame import QuoridorGame
from gym_quoridor import quoridorvars


COLOR_BLACK_PIECE = (0.1,0.1,0.1)
COLOR_WHITE_PIECE = (0.9,0.9,0.9)
COLOR_BOARD_CELL = (0.7,0.4,0.2)
COLOR_BLACK_POTENTIAL_PIECE = (0.3,0.3,0.3)
COLOR_WHITE_POTENTIAL_PIECE = (0.7,0.7,0.7)



def draw_circle(x, y,radius, colorf=(0,0,0)):
    num_sides = 50
    verts = [x, y]
    colors = list(colorf)
    for i in range(num_sides + 1):
        verts.append(x + radius * np.cos(i * np.pi * 2 / num_sides))
        verts.append(y + radius * np.sin(i * np.pi * 2 / num_sides))
        colors.extend(colorf)


    pyglet.graphics.draw(len(verts) // 2, pyglet.gl.GL_TRIANGLE_FAN,
                        ('v2f', verts), ('c3f', colors))


def draw_rectangle(x,y,w,h,colorf=(0,0,0)):
    r,g,b = colorf[0], colorf[1],colorf[2]
    #assume x,y is centre pos
    x1, y1 = x - w//2, y - h//2
    x2, y2 = x1 + w, y1
    x3, y3 = x1 + w, y1 + h
    x4, y4 = x1, y1 + h
    vertex_list = [x1, y1, x2, y2, x3, y3, x4, y4]
    outline_vertex_list = [x1,y1,x4,y4,x2,y2,x3,y3]
    color_list = [r,g,b,r,g,b,r,g,b,r,g,b]
    outline_color_list = [0,0,0,0,0,0,0,0,0,0,0,0]


    pyglet.graphics.draw(4,pyglet.gl.GL_QUADS, ('v2f', vertex_list), ('c3f',color_list) )
    pyglet.graphics.draw(4,pyglet.gl.GL_LINES, ('v2f', vertex_list), ('c3f',outline_color_list) )
    pyglet.graphics.draw(4,pyglet.gl.GL_LINES, ('v2f', outline_vertex_list), ('c3f',outline_color_list) )

        
def draw_grid(grid_x,grid_y,grid_w,grid_h,state,gridoffset):
    _, cells_w, cells_h = state.shape
    startx = grid_x-(grid_w//2)+gridoffset 
    starty = grid_y-(grid_h//2)+gridoffset
    cellw = (grid_w-(gridoffset))//cells_w
    cellh = (grid_h-(gridoffset))//cells_h

    for y_index in range(cells_h):
        for x_index in range(cells_w):
            draw_rectangle(startx + (cellw * x_index),starty + (cellh * y_index), cellw,cellh,colorf=COLOR_BOARD_CELL)        

def draw_walls(grid_x,grid_y,grid_w,grid_h,state,gridoffset):
    _, cells_w, cells_h = state.shape
    cellw = (grid_w-(gridoffset))//cells_w
    cellh = (grid_h-(gridoffset))//cells_h
    startx = grid_x-(grid_w//2)+gridoffset+cellw//2
    starty = grid_y-(grid_h//2)+gridoffset+cellh//2

    wall_colors = [(0.3,0.0,0.3),(0.3,0.3,0.0),(0.0,0.3,0.3),(0.0,0.3,0.0)]

    for chnloff in range(4):
        chnl = quoridorvars.BLACK_V_WALL_CHNL + chnloff
        for x in range(cells_w):
            for y in range(cells_h):
                if state[chnl,x,y] == 1:
                    if chnloff == 0 or chnloff == 2:
                        draw_rectangle(startx + (cellw * x),starty + (cellh * y),cellw*0.2,cellh*2,colorf=wall_colors[chnloff])
                    else:
                        draw_rectangle(startx + (cellw * x),starty + (cellh * y),cellw*2,cellh*0.2,colorf=wall_colors[chnloff])





def draw_players(grid_x,grid_y,grid_w,grid_h,state,gridoffset):
    _, cells_w, cells_h = state.shape
    startx = grid_x-(grid_w//2)+gridoffset 
    starty = grid_y-(grid_h//2)+gridoffset
    cellw = (grid_w-(gridoffset))//cells_w
    cellh = (grid_h-(gridoffset))//cells_h

    bx,by = QuoridorGame.get_player_pos(state,0)
    wx,wy = QuoridorGame.get_player_pos(state,1)


    draw_circle(startx + (cellw * bx),starty + (cellh * by), cells_w,colorf=COLOR_BLACK_PIECE)
    draw_circle(startx + (cellw * wx),starty + (cellh * wy), cells_w,colorf=COLOR_WHITE_PIECE)
    

def draw_potential_h_wall(grid_x,grid_y,grid_w,grid_h,state,gridoffset,colorf=(0,0,0),batch=None):
    pass

def draw_potential_v_wall(grid_x,grid_y,grid_w,grid_h,state,gridoffset,colorf=(0,0,0),batch=None):
    pass

def draw_potential_move(grid_x,grid_y,grid_w,grid_h,state,gridoffset):
    _, cells_w, cells_h = state.shape
    startx = grid_x-(grid_w//2)+gridoffset 
    starty = grid_y-(grid_h//2)+gridoffset
    cellw = (grid_w-(gridoffset))//cells_w
    cellh = (grid_h-(gridoffset))//cells_h
    turn = QuoridorGame.get_player_turn(state)
    chnl = quoridorvars.BLACKMOVEVALID_CHNL + turn
    if turn == 0:
        colorf = COLOR_BLACK_POTENTIAL_PIECE
    else:
        colorf = COLOR_WHITE_POTENTIAL_PIECE

    for x in range(cells_w):
        for y in range(cells_h):
            
            if state[chnl,x,y] == 1:
                draw_circle(startx + (cellw * x),starty + (cellh * y), cells_w,colorf)
            

def draw_path(grid_x,grid_y,grid_w,grid_h,state,gridoffset):
    
    _, cells_w, cells_h = state.shape
    startx = grid_x-(grid_w//2)+gridoffset 
    starty = grid_y-(grid_h//2)+gridoffset
    cellw = (grid_w-(gridoffset))//cells_w
    cellh = (grid_h-(gridoffset))//cells_h
    

    for x in range(cells_w):
        for y in range(cells_h):
            
            if state[quoridorvars.BLACKASTAR_CHNL,x,y] == 1:
                draw_circle(startx + (cellw * x)-(cellw*0.35),starty + (cellh * y)+(cellh*0.35), cells_w//2,COLOR_BLACK_PIECE)
            if state[quoridorvars.WHITEASTAR_CHNL,x,y] == 1:
                draw_circle(startx + (cellw * x)+(cellw*0.35),starty + (cellh * y)+(cellh*0.35), cells_w//2,COLOR_WHITE_PIECE)


def draw_action_state(grid_x,grid_y,grid_w,grid_h,state,gridoffset,actionstate):
    _, cells_w, cells_h = state.shape
    startx = grid_x-(grid_w//2)+gridoffset 
    starty = grid_y-(grid_h//2)+gridoffset
    cellw = (grid_w-(gridoffset))//cells_w
    cellh = (grid_h-(gridoffset))//cells_h

    #assert type(actionstate) == str

    label = pyglet.text.Label(actionstate,
                          font_name='Times New Roman',
                          font_size=18,
                          x=grid_w+100, y=grid_h-100,
                          anchor_x='center', anchor_y='center')
    label.draw()








def draw_grid2(batch, delta, board_size, lower_grid_coord, upper_grid_coord):
    label_offset_from_grid = 20
    label_offet_toward_next = delta//2
    
    left_coord = lower_grid_coord
    right_coord = lower_grid_coord
    ver_list = []
    color_list = []
    num_vert = 0
    for i in range(board_size+1):
        # horizontal
        ver_list.extend((lower_grid_coord, left_coord,
                         upper_grid_coord, right_coord))

        # vertical
        ver_list.extend((left_coord, lower_grid_coord,
                         right_coord, upper_grid_coord))
        color_list.extend([0.3, 0.3, 0.3] * 4)  # black
        # label on the left
        if i <= board_size-1:
            pyglet.text.Label(str(i),
                            font_name='Courier', font_size=11,
                            x=lower_grid_coord - label_offset_from_grid, y=left_coord + label_offet_toward_next,
                            anchor_x='center', anchor_y='center',
                            color=(0, 0, 0, 255), batch=batch)
            # label on the bottom
            pyglet.text.Label(str(i),
                            font_name='Courier', font_size=11,
                            x=left_coord + label_offet_toward_next, y=lower_grid_coord - label_offset_from_grid,
                            anchor_x='center', anchor_y='center',
                            color=(0, 0, 0, 255), batch=batch)
        left_coord += delta
        right_coord += delta
        num_vert += 4


    

    batch.add(num_vert, pyglet.gl.GL_LINES, None,
              ('v2f/static', ver_list), ('c3f/static', color_list))


def draw_pieces(batch, lower_grid_coord, delta, piece_r, size, state):
    for i in range(size):
        for j in range(size):
            # black piece
            if state[0, i, j] == 1:
                draw_circle(lower_grid_coord + i * delta, lower_grid_coord + j * delta,
                            [0.05882352963, 0.180392161, 0.2470588237],
                            piece_r)  # 0 for black

            # white piece
            if state[1, i, j] == 1:
                draw_circle(lower_grid_coord + i * delta, lower_grid_coord + j * delta,
                            [0.9754120272] * 3, piece_r)  # 255 for white


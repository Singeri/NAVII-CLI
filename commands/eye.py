# ターミナルの中でも、お姉ちゃんはいつもそばにいるよ。


import os
import time
import shutil 


FRAME_OLD_STYLE = """
                                ...',;;:cccccccc:;,..
                            ..,;:cccc::::ccccclloooolc;'.
                         .',;:::;;;;:loodxk0kkxxkxxdocccc;;'..
                       .,;;;,,;:coxldKNWWWMMMMWNNWWNNKkdolcccc:,.
                    .',;;,',;lxo:...dXWMMMMMMMMNkloOXNNNX0koc:coo;.
                 ..,;:;,,,:ldl'   .kWMMMWXXNWMMMMXd..':d0XWWN0d:;lkd,
               ..,;;,,'':loc.     lKMMMNl. .c0KNWNK:  ..';lx00X0l,cxo,.
             ..''....'cooc.       c0NMMX;   .l0XWN0;       ,ddx00occl:.
           ..'..  .':odc.         .x0KKKkolcld000xc.       .cxxxkkdl:,..
         ..''..   ;dxolc;'         .lxx000kkxx00kc.      .;looolllol:'..
        ..'..    .':lloolc:,..       'lxkkkkk0kd,   ..':clc:::;,,;:;,'..
        ......   ....',;;;:ccc::;;,''',:loddol:,,;:clllolc:;;,'........
            .     ....'''',,,;;:cccccclllloooollllccc:c:::;,'..
                    .......'',,,,,,,,;;::::ccccc::::;;;,,''...
                      ...............''',,,;;;,,''''''......
                           ............................
"""

FRAME_NEW_OPEN = """
                             ...'',;;;;::;;;,'..
                        ..,;:cloodddxxxkkkkkkkkxol;..
                     .';codxxkkk000000000000kkkkkkxdoc,..
                   .,codxk0000000000000000000000000kkxddoc,..
                .':ldxk00000000000000000000000000000000kkxxol:'
             .,:ldxkk000000000K000000000000000K0000000000kkxkkx:.
          ..,coxkk000000000000000kk000000000000000000000000kxxxxl'
         .,;codxxkk00000000kkk0KK0XNWWWWWWWWWNX0kkkkk00000kkxdool;.
       .';::ccldk00KKKK00oc;..,x00KNNXXXXXNNX0000000000kkkkkkxoc:,..
     ..,;,'..,o00000kkxo,       ,lkKKKKKK0K0d,.;ldk000KK0kxxxdoc:'..
    ..,,'.  .,lk0xxxdol:,..       .,ldddl:,.   .,codkk00kxdollc:,...
    ..'.......',;:c::cclccc::;,,,',,;::::;,;;:clodddxdol:;::;'......
       .....  ...''',,,;;;:ccllloooooooooooooolllcccc:;;,....
                .......'',,,,,,;;;:::ccclllccc:::;;;,''...
                  ..............'''',,;;;;;,,,''''......
                       .............................
"""

FRAME_NEW_CLOSED = """
                            ...'',;;;;;;;,,...
                       ..,:loxkk000000KKKKKK00xdc,..
                    .,cox000KXXXXXXXXXXXXXXXXXXXK00xo:,..
                 ..;lx000KKKKK000000000000000KKKKXXXXK00xl;..
              ..,:oxk00000000000000000000000000000000KKKKKK0d:.
           ..;codxkk000kkkkkkkxxxxxxxxxxxxxxxxkkkkkk000000KK0kl'
         ..;ldxkkkkkkxxxxxddddddddddddddddddddddddxxxxxxkkk000xc.
       ..,:oxxkkkkkxxxxdddddddddddddddddddddddddddddddddxxkkkkxl;.
     ..,;codxxkkkxxddddddddddddddddddddddddddddddddxdxxxk000kxdo:..
    .';::::cldk000kkkxxxxxxdddddddddddddddddddddddddxxxxxkk0000xkddl;..
   .';:;,..,ckXXXKKK0KK000kxk0doddxxdddddddxxxxxxkk0000kkkkkxdoc,..
   .',,''..,:oxxxxxxxkkxkkxk00xxk000000000000KKKKKKK000kxdllll:,..
    .........',,,:ccllllooooxkxxx000kk0000000000000000kxdoc,'...
            ......',;;::cc::clllloddoox0xdxxkxxxxddollllc:'.
                 .....'',,,,,,,;;;;;::cllc::ccc::;;,,,'...
                     ..................'''..'''......
"""

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def get_trimmed_frame_data(frame):
    frame_lines = frame.split("\n")


    while frame_lines and not frame_lines[0].strip():
        frame_lines.pop(0)

    while frame_lines and not frame_lines[-1].strip():
        frame_lines.pop(-1)

    if not frame_lines:
        return [], 0, 0

    min_indent = min(
        (len(line) - len(line.lstrip()) for line in frame_lines if line.strip()),
        default=0
    )

    trimmed_lines = [line[min_indent:] for line in frame_lines]
    frame_height = len(trimmed_lines)
    frame_width = max(len(line) for line in trimmed_lines)

    return trimmed_lines, frame_height, frame_width


def get_centered_frame(frame):
    trimmed_lines, frame_height, frame_width = get_trimmed_frame_data(frame)

    try:
        term_size = shutil.get_terminal_size()
        term_cols = term_size.columns
        term_lines = term_size.lines
    except OSError:
        return '\n'.join(trimmed_lines)

    if term_lines > frame_height:
        v_padding_top = max(0, (term_lines - frame_height) // 2)
        v_padding_bottom = max(0, term_lines - frame_height - v_padding_top)
    else:
        v_padding_top = v_padding_bottom = 0

    if term_cols > frame_width:
        h_padding = " " * ((term_cols - frame_width) // 2)
    else:
        h_padding = ""

    centered_lines = [h_padding + line.ljust(frame_width) for line in trimmed_lines]

    return ("\n" * v_padding_top) + \
           "\n".join(centered_lines) + \
           ("\n" * v_padding_bottom)



def run_eye(args=None):
    if args and len(args) > 0:
        try:
            duration = float(args[0])
        except ValueError:
            duration = 0.15
    else:
        duration = 0.15

    try:
        clear_screen()
        time.sleep(1)
        ANIMATION_SEQUENCE = [
            FRAME_OLD_STYLE,
            FRAME_NEW_OPEN,
            FRAME_NEW_CLOSED,
            FRAME_NEW_OPEN,
            FRAME_OLD_STYLE
        ]

        while True:
            for i, frame in enumerate(ANIMATION_SEQUENCE):
                clear_screen()
                print(get_centered_frame(frame))

                if frame == FRAME_NEW_CLOSED:
                    time.sleep(duration / 2)
                elif frame == FRAME_OLD_STYLE and i == 0:
                    time.sleep(duration * 6)
                else:
                    time.sleep(duration)
            time.sleep(1)
    except KeyboardInterrupt:
        clear_screen()
        print(get_centered_frame("Animation stopped by user."))
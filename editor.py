from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
#===============================[POCETAK SKRIPTE]=======================================
app = Ursina()
window.fps_counter.enabled=False
window.exit_button.enabled=False
window.fullscreen = True
Sky()
#===================================[VARIJABLE]=========================================
red = color.rgb(255, 0, 0)
ground = Entity(model='plane', scale=(200, 5, 200), texture="grass",collider='mesh')
player = FirstPersonController(origin_y=-.5, speed=15, origin_x = 6)
editor_camera = EditorCamera(enabled=True, ignore_paused=True)
zid = Entity(model='cube',texture='resursi\zid',enabled=False)
kutija = Entity(model='cube',texture='resursi\\box' ,enabled=False)
ruka = Entity(parent=camera.ui,model='cube',color=color.blue,position=(0.75, -0.6),rotation= (150, -10,6),scale = (0.2,0.2,1.5),enabled = False)
zidid = 0
kutija_id = 0
Rotacija = False
Pozicija = False
Save_field = InputField(y=-.02,enabled=False)
Uhvatio_zid = 0.0
#==============================[VARIJABLE - DUGMICI]=====================================
btn_zid = Button(texture='resursi\\zid',position=(-.8,-.25),scale=.1,color=color.white,enabled=False)
btn_kutija = Button(texture='resursi\\box',position=(-.65,-.25),scale=.1,color=color.white,enabled=False)
btn_rot = Button(texture='resursi\\Rotation-icon',position=(-.6,-0.4),scale=.1,color=color.white,enabled=False)
btn_mov = Button(texture='resursi\\Arrows-icon',position=(-.4,-0.4),scale=.1,color=color.white,enabled=False)
btn_save = Button(texture='resursi\\Save-icon',position=(-0.8,-0.4),scale=.1,color=color.white,enabled=False)
btn_save_field = Button('Sacuvaj',position=(-.01,-.09),scale=(.2,.05),color=color.green,text_color=color.black,
                        highlight_color=color.turquoise,enabled=False)
#===================================[VARIJABLE]=========================================
#==================================[DEFINICIJE]=========================================
def izaberi():
    btn_zid.enabled = True
    btn_kutija.enabled = True

def kreiraj_zid():
    global zidid
    zidid += 1
    zid = Entity(model='cube',texture='resursi\zid',scale=(50,10,5),color=color.white,
                idovi=zidid, mrda="aca",position=(0,5,100),collider='cube',edit_mode=True)

    btn_zid.enabled = False
    btn_kutija.enabled = False

textures = ["resursi\\car_textura_0","resursi\\car_textura_1","resursi\\car_textura_2"]
def kreiraj_kutija():
    global kutija_id
    kutija_id += 1
    kutija = Entity(model='resursi\\Car',texture=textures,origin_y=-.5, scale=2,
                    k_idovi=kutija_id,mrda="aca",position=(0,5,100),collider='cube',edit_mode=False)
        
    btn_zid.enabled = False
    btn_kutija.enabled = False

def rotacija():
    global Rotacija
    global Pozicija
    Rotacija = True
    Pozicija = False

def pozicija():
    global Rotacija
    global Pozicija
    Pozicija = True
    Rotacija = False

def sacuvaj_field():
    Save_field.enabled = True
    btn_save_field.enabled = True
    Save_field.tooltip = Tooltip('Upisite naziv fajla')

def sacuvaj():
    global Save_field
    cuvanje = f'Editor/{Save_field.text}.py'
    save_file = open(cuvanje, 'w')
    save_file.write('from ursina import *\nfrom ursina.prefabs.first_person_controller import FirstPersonController\n')
    save_file.write('\n#Mozete testirati svoju mapu i nastaviti da radite svoj projekat odavde\n#Koristite ESC za gasenje projekta\n')
    save_file.write('\napp = Ursina()\nwindow.fps_counter.enabled=False\nwindow.exit_button.enabled=True\nwindow.fullscreen = False\n')
    save_file.write("\nSky()\nground = Entity(model='plane', scale=(200, 5, 200), texture='grass',collider='mesh')\n")
    save_file.write("player = FirstPersonController(origin_y=-.5, speed=15, origin_x = 6)\n")
    save_file.write('\n')
    save_file.write('#Vasi objekti koje ste modifikovali pocinju odavde\n')
    for zid in scene.entities:
            if hasattr(zid, 'idovi'):
                zid_poz = f"zid{zid.idovi} = Entity(model='cube',texture='grass',scale=(50,10,5),color=color.white,position=({zid.x},{zid.y},{zid.z}),rotation=({zid.rotation_x},{zid.rotation_y},{zid.rotation_z}))\n"
                save_file.write(zid_poz)
    for kutija in scene.entities:
            if hasattr(kutija, 'k_idovi'):
                kutija_poz = f"kutija{kutija.k_idovi} = Entity(model='cube',texture='box',origin_y=-.5, scale=2,position=({kutija.x},{kutija.y},{kutija.z}),rotation=({kutija.rotation_x},{kutija.rotation_y},{kutija.rotation_z}))\n"
                save_file.write(kutija_poz)
    save_file.write('\n')
    save_file.write('\ndef input(key):')
    save_file.write("\n    if key == 'escape':")
    save_file.write("\n        quit()")
    save_file.write('\n\napp.run()')
    save_file.close()
    Save_field.enabled = False
    btn_save_field.enabled = False

def input(key):
    global Uhvatio_zid
    global Rotacija
    global Pozicija

    if key == 'escape':
        quit()

    if key == 'e':
        if editor_camera.enabled == False:
            editor_camera.enabled = True
            ruka.enabled = False
            btn_rot.enabled = True
            btn_mov.enabled = True
            btn_save.enabled = True
            mouse.locked = False
            mouse.visible = True
        elif editor_camera.enabled == True:
            editor_camera.enabled = False
            ruka.enabled = True
            application.paused = False
            Pozicija = False
            Rotacija = False
            Uhvatio_zid = 0.0
            btn_rot.enabled = False
            btn_mov.enabled = False
            btn_save.enabled = False
            mouse.locked = True
            mouse.visible = False

    if key == 'left mouse down':
        if editor_camera.enabled:
            if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'mrda'):
                Uhvatio_zid = mouse.hovered_entity
                mouse.hovered_entity.blink(color.red)
                mouse.hovered_entity.edit_mode = True
                if btn_rot.enabled == False:
                    btn_rot.enabled = True

                if btn_mov.enabled == False:
                    btn_mov.enabled = True

                if btn_save.enabled == False:
                    btn_save.enabled = True

    if held_keys['left mouse']:
        ruka.position = (0.6, -0.5)
    elif held_keys['right mouse']:
        ruka.position = (0.6, -0.5)
    else:
        ruka.position = (0.75, -0.6)

    if Pozicija == True:
        Uhvatio_zid.x += held_keys['d'] * 1
        Uhvatio_zid.x -= held_keys['a'] * 1
        Uhvatio_zid.y += held_keys['up arrow'] * 1
        Uhvatio_zid.y -= held_keys['down arrow'] * 1
        Uhvatio_zid.z += held_keys['w'] * 1
        Uhvatio_zid.z -= held_keys['s'] * 1
    if Rotacija == True:
        Uhvatio_zid.rotation_x += held_keys['left arrow'] * 1
        Uhvatio_zid.rotation_x -= held_keys['right arrow'] * 1
        Uhvatio_zid.rotation_y += held_keys['up arrow'] * 1
        Uhvatio_zid.rotation_y -= held_keys['down arrow'] * 1
        Uhvatio_zid.rotation_z += held_keys['w'] * 1
        Uhvatio_zid.rotation_z -= held_keys['s'] * 1
#==================================[DEFINICIJE]=========================================
#==============================[DUGMICI - FUNKCIJE]=====================================
btn_zid.on_click = kreiraj_zid
btn_zid.tooltip = Tooltip('Kreiraj zid')
btn_kutija.on_click = kreiraj_kutija
btn_kutija.tooltip = Tooltip('Kreiraj kutiju')
btn_rot.on_click = rotacija
btn_rot.tooltip = Tooltip('Rotiraj')
btn_mov.on_click = pozicija
btn_mov.tooltip = Tooltip('Pomeraj')
btn_save.on_click = sacuvaj_field
btn_save.tooltip = Tooltip('Sacuvaj projekat')
btn_save_field.on_click = sacuvaj
#==============================[DUGMICI - FUNKCIJE]=====================================
class DropdownMenuButton(Button):
    def __init__(self, text='', **kwargs):
        super().__init__(
            scale=(.35,.025),
            origin=(-.5,.5),
            pressed_scale=1,
            enabled = False,
            text=text,
            **kwargs
            )

        if self.text_entity:
            self.text_entity.x = .05
            self.text_entity.origin = (-.5, 0)
            self.text_entity.scale *= .8


class DropdownMenu(DropdownMenuButton):

    def __init__(self, text='', buttons=list(), **kwargs):
        super().__init__(text=text)
        self.position = window.top_left
        self.buttons = buttons
        for i, b in enumerate(self.buttons):
            b.world_parent = self
            b.original_scale = b.scale
            b.x = 0
            b.y = -i-1 *.98
            b.enabled = False

            if isinstance(b, DropdownMenu):
                for e in b.buttons:
                    e.x = 1
                    e.y += 1

        self.arrow_symbol = Text(world_parent=self, text='>', origin=(.5,.5), position=(.95, 0), color=color.gray)
        for key, value in kwargs.items():
            setattr(self, key, value)


    def open(self):
        for i, b in enumerate(self.buttons):
            invoke(setattr, self.buttons[i], 'enabled', True, delay=(i*.02))

    def close(self):
        for i, b in enumerate(reversed(self.buttons)):
            b.enabled = False


    def on_mouse_enter(self):
        super().on_mouse_enter()
        self.open()

    def input(self, key):
        if key == 'left mouse down' and mouse.hovered_entity and mouse.hovered_entity.has_ancestor(self):
            self.close()

    def update(self):
        if self.hovered or mouse.hovered_entity and mouse.hovered_entity.has_ancestor(self):
            return

        self.close()

if __name__ == '__main__':

    mouse.locked = False
    mouse.visible = True

    from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

    # DropdownMenu(text='File')
    DropdownMenu('KREIRAJ', buttons=(
        DropdownMenuButton('ZID',on_click=kreiraj_zid),
        DropdownMenuButton('KUTIJU',on_click=kreiraj_kutija),
        #DropdownMenu('Reopen Project', buttons=(
            #DropdownMenuButton('Project 1'),
            #DropdownMenuButton('Project 2'),
            #)),
        DropdownMenuButton('Izadji',on_click=application.quit),
        ))
app.run()
# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess

from libqtile.config import Drag, Key, Screen, Group, Drag, Click, Rule
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile import qtile


# mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')
myTerm = "urxvt"

@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


# Most of our keybindings are in sxhkd file - except these

keys = [

# # SUPER + FUNCTION KEYS
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
# # SUPER + SHIFT KEYS
    Key([mod, "shift"], "r", lazy.restart()),
# # QTILE LAYOUT KEYS
#     Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),
# # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
#    Key([mod], "k", lazy.layout.up()),
#    Key([mod], "j", lazy.layout.down()),
#    Key([mod], "h", lazy.layout.left()),
#    Key([mod], "l", lazy.layout.right()),
# # RESIZE UP, DOWN, LEFT, RIGHT
    # Key([mod, "control"], "l",
    #     lazy.layout.grow_right(),
    #     lazy.layout.grow(),
    #     lazy.layout.increase_ratio(),
    #     lazy.layout.delete(),
    #     ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    # Key([mod, "control"], "h",
    #     lazy.layout.grow_left(),
    #     lazy.layout.shrink(),
    #     lazy.layout.decrease_ratio(),
    #     lazy.layout.add(),
    #     ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    # Key([mod, "control"], "k",
    #     lazy.layout.grow_up(),
    #     lazy.layout.grow(),
    #     lazy.layout.decrease_nmaster(),
    #     ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    # Key([mod, "control"], "j",
    #     lazy.layout.grow_down(),
    #     lazy.layout.shrink(),
    #     lazy.layout.increase_nmaster(),
    #     ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
# # FLIP LAYOUT FOR MONADTALL/MONADWIDE
#    Key([mod, "shift"], "f", lazy.layout.flip()),
# # FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),
# # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
# # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),
# # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
# # Switch focus to specific monitor (out of two)
    Key([mod], "w",
        lazy.to_screen(1),
        desc='Keyboard focus to monitor 1'
        ),
    Key([mod], "e",
        lazy.to_screen(0),
        desc='Keyboard focus to monitor 2'
        ),
    ]

groups = []

group_names = ["1", "2", "3", "4", "5"]
group_labels = ["", "", "", "", ""]
group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "Bsp"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

# # CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

# # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])

def init_layout_theme():
    return {"margin":5,
            "border_width":2,
            "border_focus": "#50fa7b",
            "border_normal": "#bd93f9"
            }

layout_theme = init_layout_theme()

layouts = [
    layout.MonadTall(margin=8, border_width=2, border_focus="#50fa7b", border_normal="#bd93f9"),
    layout.MonadWide(margin=8, border_width=2, border_focus="#50fa7b", border_normal="#bd93f9"),
#    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme, fullscreen_border_width=3, max_border_width=3),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme),
    ]

# # COLORS FOR THE BAR

def init_colors():
    return [["#282a36", "#282a36"], # color 0 Background
            ["#6272a4", "#6272a4"], # color 1 Current Line/Selection
            ["#f8f8f2", "#f8f8f2"], # color 2 Foreground
            ["#ffb86c", "#ffb86c"], # color 3 Orange
            ["#8be9fd", "#8be9fd"], # color 4 Cyan
            ["#ff79c6", "#ff79c6"], # color 5 Pink
            ["#ff5555", "#ff5555"], # color 6 Red
            ["#50fa7b", "#50fa7b"], # color 7 Green
            ["#bd93f9", "#bd93f9"], # color 8 Purple
            ["#f1fa8c", "#f1fa8c"]] # color 9 Yellow


colors = init_colors()


# # WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Fira Code",
                fontsize = 14,
                padding = 3,
                background = "#44475a",
                foreground = colors[2],
                )

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "%s@%s: ", (os.environ["USER"], socket.gethostname())

    widgets_list = [
######> Left side bar
        widget.Spacer(
            length = 10,
            padding = 5
        ),
        widget.CurrentLayout(
            font = "Fira Code SemiBold",
            fontsize = 12,
            foreground = colors[0],
            background = colors[8]
            ),
        widget.GroupBox(
            font="Fira Code SemiBold",
            fontsize = 20,
            borderwidth = 3,
            center_aligned = True,
            spacing = 5,
            disable_drag = True,
            active = colors[1],
            inactive = colors[2],
            highlight_method = "line",
            this_current_screen_border = colors[7],
            other_current_screen_border = colors[3],
            ),
        widget.Sep(
            linewidth = 1,
            padding = 10,
            ),
        widget.TextBox(
            text = "",
            fontsize = 23,
            padding = 5,
            foreground = colors[5],
            ),
        widget.WindowName(
            font="Fira Code Retina",
            fontsize = 12,
            ),
        widget.NvidiaSensors(
            format = '{temp}°C ♀ {fan_speed}',
            threshold = 80,
            update_interval = 60,
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("mailspring")},
        ),

######> Right side bar

        # widget.TextBox(
        #     text = " ⟳",
        #     padding = 2,
        #     # foreground = colors[7],
        #     # background = colors[6],
        #     ),
        widget.TextBox(
            text= "",
            fontsize = 15,
            padding = 5,
            foreground = colors[3],
            ),
        widget.HDDGraph(
            type = 'box',
            space_type = 'free',
            foreground = colors[2],
            border_color = colors[8],
            graph_color = colors[7],
            frecuency = 1600,
            # margin_x = 20,
            # margin_y = 5,
            mouse_callbacks = {
                'Button1': lambda : qtile.cmd_spawn(f"{myTerm} -e gtop")
            }
            ),
        widget.CheckUpdates(
            update_interval = 60,
            distro = "Arch_checkupdates",
            display_format = "⟳ {updates} Update(s)",
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
            colour_have_updates = colors[7],
            colour_no_updates = colors[2],
            ),
        widget.Sep(
            linewidth = 1,
            padding = 10,
            ),
        widget.Systray(
            icon_size=20,
            padding = 8
            ),
        widget.Sep(
            linewidth = 1,
            padding = 10,
            ),
        widget.TextBox(
            text = " Vol:",
            padding = 0
            ),
        widget.Volume(
            padding = 5
            ),
        widget.Sep(
            linewidth = 1,
            padding = 10,
            ),
        widget.Net(
            interface="enp7s0",
            format = '{down} ↓↑ {up}',
            update_interval = 5,
            ),
        widget.Sep(
            linewidth = 1,
            padding = 10,
            ),
        widget.Clock(
            # mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("code")},
            format="%A, %B %d - %H:%M"
            ),
        widget.Spacer(
            length = 5
        ),
        widget.TextBox(
            text = "",
            fontsize = 28,
            padding = 6,
            foreground = colors[0],
            background = colors[2],
            mouse_callbacks = {
                'Button1': lambda : qtile.cmd_spawn(
                    f'{myTerm} -e code {home}/.config/qtile/config.py'
                ),
            },
        ),
        widget.Spacer(
            length = 10,
            padding = 5
        ),
    ]
    return widgets_list

widgets_list = init_widgets_list()

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, opacity=1, margin=[5, 10, 0, 10])),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26, opacity=1, margin=[5, 10, 0, 10]))]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

# # ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assign apps to groups ##################
#########################################################
@hook.subscribe.client_new
def assign_app_group(client):
    d = {}
# #     #####################################################################################
#     ### Use xprop fo find  the value of WM_CLASS(STRING) -> First field is sufficient ###
#     #####################################################################################
    # d[group_names[0]] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
    #           "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#     d[group_names[1]] = [ "Atom", "Subl", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#                "atom", "subl", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#     d[group_names[2]] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#     d[group_names[3]] = ["Gimp", "gimp" ]
    d[group_names[4]] = ["Vlc","vlc", "Mpv", "mpv", "Mailspring", "mailspring" ]
#     ######################################################################################
#
    wm_class = client.window.get_wm_class()[0]

    for i in range(len(d)):
        if wm_class in list(d.values())[i]:
            group = list(d.keys())[i]
            client.togroup(group)
            client.group.cmd_toscreen(toggle=False)

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME

main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]

floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'Arcolinux-welcome-app.py'},
    {'wmclass': 'Arcolinux-tweak-tool.py'},
    {'wmclass': 'Arcolinux-calamares-tool.py'},
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},
    {'wmclass': 'makebranch'},
    {'wmclass': 'maketag'},
    {'wmclass': 'Arandr'},
    {'wmclass': 'feh'},
    {'wmclass': 'Galculator'},
    {'wmclass': 'arcolinux-logout'},
    {'wmclass': 'xfce4-terminal'},
    {'wname': 'branchdialog'},
    {'wname': 'Open File'},
    {'wname': 'pinentry'},
    {'wmclass': 'ssh-askpass'},
])

follow_mouse_focus = False
bring_front_click = False
auto_fullscreen = True
focus_on_window_activation = "smart"
cursor_warp = True
wmname = "LG3D"

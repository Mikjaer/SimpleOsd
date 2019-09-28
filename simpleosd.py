#!/usr/bin/python

'''
Copyright (c) Me
# apt-get install python-gi-cairo
# You need a composite manager
'''
import signal, gi, cairo, threading, time, os, argparse, fileinput 
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk, Pango


class SimpleOsd(Gtk.Window):

    text = ""

    def __init__(self):
        super(SimpleOsd, self).__init__()
       
      
        self.setup()       
       # self.init_ui()

        
    def setup(self):    
        
        self.set_app_paintable(True)   
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.set_keep_below(True)
        
        screen = self.get_screen()
        visual = screen.get_rgba_visual()       
        if visual != None and screen.is_composited():
            self.set_visual(visual)          
        
        
    def render(self):    

        self.connect("draw", self.on_draw)        
       
        css = '* { text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000; }'
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)

        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()

        context.add_provider_for_screen(screen, css_provider,
                       Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        lbl = Gtk.Label()
        lbl.set_text(self.text)        
        
        fd = Pango.FontDescription("Serif 30")
        lbl.modify_font(fd)                
        lbl.modify_fg(Gtk.StateFlags.NORMAL,Gdk.color_parse("white"))        
        
        self.add(lbl)
        

        self.set_keep_above(True)

        self.resize(300, 250)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
                                      
    
    def on_draw(self, wid, cr):
        
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        
    
def countdown_thread(timeOut):
    print "OK";
    while timeOut > 0:
        time.sleep(1)
        timeOut -= 1
    os._exit(0)


if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", action="store", default=5, help="How long time, in seconds, to show message")
    parser.add_argument("--text", action="store", default="-", help="Text to show, default: - (Read from STDIN)")
    iargs = parser.parse_args()

    text = ""
    if iargs.text != "-":
        text = iargs.text
    else:
        for line in fileinput.input():
            text=text+line

    threading.Thread(target=countdown_thread, args=(int(iargs.timeout),)).start()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = SimpleOsd()
    app.text = text
    app.render()
    Gtk.main()

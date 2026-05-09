import av, av.audio.resampler
import os
import threading as th
import pyray as rl
import numpy as np
import pygame as pg

clock = pg.Clock()
INPUT_LOCAL_NTSC = 0
INPUT_NET_NTSC = 1
INPUT_MPEGSPOOL = 2
INPUT_LOCAL_SDI = 3
INPUT_NET_SDI = 4

ASPECT_RATIO_CHANGE = False

SDI_URL = "" #emulated sdi path

queue = []
looping = False

def queueMovie(movieFile):
    testp = os.path.join(os.environ["RENDEREROOT"], "net", movieFile+".mpg")
    if os.path.exists(movieFile+".mpg"):
        rpath = movieFile+".mpg"
    elif os.path.exists(testp):
        rpath = testp
    else:
        return
    
    queue.append(rpath)

def setMovieLooping(val):
    global looping
    looping = val

class TSStream:
    def __init__(self, url):
        print("opening")
        self.av = av.open(url)
        print("open")
        self.size = (0, 0)
        self.frames = []
        self.audio = []
        self.atb = 1
        self.vtb = 1
        
        self.astf = None
        
        self.prune = 0
        
        self.astream = None
        self.aparams = ()
    
    def thread_runner(self):
        buf = 1600
        print("TR")
        vst = self.av.streams.video[0]
        dec = (vst,)
        dar = vst.display_aspect_ratio or (vst.width/vst.height)
        print("SIZE: ", vst.width, vst.height, "DAR", dar)
        self.size = (round(vst.height * dar * (1+0.125*ASPECT_RATIO_CHANGE)), vst.height)
        if len(self.av.streams.audio) > 0:
            ast = self.av.streams.audio[0]
            dec = (vst, ast)
        
        resampler = av.audio.resampler.AudioResampler(
            format='s16', 
            layout='stereo', 
            rate=48000
        )
        
        print("decoding")
        for frame in self.av.decode(*dec):
            if isinstance(frame, av.VideoFrame):
                self.vtb = frame.time_base
                self.frames.append((frame.pts/frame.time_base, frame.reformat(width=self.size[0], height=480, format="rgba").to_ndarray().tobytes()))
                
                self.frames = [f for f in self.frames if not f[0] < self.prune]
            elif isinstance(frame, av.AudioFrame):
                #self.aparams = (frame.sample_rate, 16, frame.layout.nb_channels)
                self.aparams = (48000, 16, 2)
                if not self.astream:
                    #rl.set_audio_stream_buffer_size_default(buf)
                    self.astream = rl.load_audio_stream(*self.aparams)
                    rl.play_audio_stream(self.astream)
                self.atb = frame.time_base
                
                self.astf = {8: "char", 16: "int16_t", 32: "float"}[16]
                
                for rf in resampler.resample(frame):
                    self.audio.append(
                        (frame.pts/frame.time_base, rf.to_ndarray().tobytes())
                    )
        
        print("decode end")

class Handler():
    def __init__(self, url):
        self.ts = TSStream(url)
        tth = th.Thread(target=self.ts.thread_runner).start()
        self.buf = 1600
        
        self.ppts = 0
        
        self.size = (0, 0)
        self.astream = rl.load_audio_stream(48000, 16, 2)
        rl.play_audio_stream(self.astream)
        
        self.frame = None
        th.Thread(target=self.runner).start()
    
    def set_volume(self, volume):
        rl.set_audio_stream_volume(self.ts.astream, volume)
    
    def runner(self):
        ts = self.ts
        samples = bytearray()
        
        cpts = 0
        
        while True:
            self.ppts = cpts
            self.size = self.ts.size
            if len(ts.audio) > 0:
                if ts.astream and rl.is_audio_stream_processed(ts.astream):
                    cant = False
                    #it's times four, because 2 channels and 2 bytes. how revolutionary!
                    first = True
                    while len(samples) < self.buf*4:
                        if len(ts.audio) == 0:
                            cant = True
                            break
                        cc = ts.audio.pop(0)
                        cpts = cc[0]
                        samples.extend(cc[1])
                        first = False
                    if not cant:
                        npa = np.frombuffer(samples[:self.buf*4], dtype=np.int16)
                        rl.update_audio_stream(ts.astream, rl.ffi.new(ts.astf+" []", npa.tolist()), self.buf)
                        samples = samples[self.buf*4:]
            else:
                print("DROWNING")
            if ts.frames:
                frr = min(ts.frames, key=lambda x : abs(cpts-x[0]))
                ts.prune = frr[0]
                self.frame = frr[1]
            
            clock.tick_busy_loop(30)

rl.init_audio_device()

if __name__ == "__main__":
    import sys
    rl.init_window(720, 480, "ts card testing example")
    
    handler = Handler(sys.argv[1])
    
    rl.set_target_fps(30)
    ttex = None
    pr = 0
    
    tla = 0
    
    buf = 1600
    
    
    cc = None
    
    while not rl.window_should_close():
        rl.begin_drawing()
        changed = False
        if handler.size != (0, 0) and not ttex:
            timg = rl.gen_image_color(*handler.size, rl.BLACK)
            ttex = rl.load_texture_from_image(timg)
        if handler.frame:
            rl.update_texture(ttex, rl.ffi.new("char []", handler.frame))
            rl.draw_texture(ttex, round(-ttex.width/2+360), 0, rl.WHITE)
        
        rl.draw_text(str(handler.ppts), 10, 10, 20, rl.BLACK)
        rl.draw_text(str(handler.ts.prune), 10, 50, 20, rl.BLACK)
        
        rl.end_drawing()
import av, av.audio.resampler
import os
import threading as th
import pyray as rl
import numpy as np
import pygame as pg
from fractions import Fraction
import miniaudio as ma
import audioop as aop
import multiprocessing as mp
import tkinter as tk
import time

print("single pringle ready to mingle")

ready_to_init_mixer = th.Event()

clock = pg.Clock()
INPUT_LOCAL_NTSC = 0
INPUT_NET_NTSC = 1
INPUT_MPEGSPOOL = 2
INPUT_LOCAL_SDI = 3
INPUT_NET_SDI = 4

DISABLE_AUDIO = False

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


def pipe_stream(aqueue, volval, vsptsval, vsperfval):
    print("pipe stream")
    samples = bytearray()
    required_frames = yield b""
    intern_buf = []
    done = False
    while True:
        required_bytes = required_frames * 2 * 2
        while len(samples) < required_bytes:
            if len(intern_buf) == 0:
                ib = aqueue.recv()
                intern_buf.extend(ib)
            ap = intern_buf.pop(0)
            if not done and ap[0] != 0:
                done = True
                print("done")
                vsptsval.value = float(ap[0])
                vsperfval.value = time.perf_counter()
            volled = ap[1] #aop.mul(ap[1], 2, self.vol)
            samples.extend(volled)
        required_frames = yield aop.mul(samples[:required_bytes], 2, volval.value)
        samples = samples[required_bytes:]
    
def pb_jams(aqueue, volval, vsptsval, vsperfval):
    print("i'm pb jams")
    def make_pbj():
        with ma.PlaybackDevice(output_format=ma.SampleFormat.SIGNED16, nchannels=2, sample_rate=48000) as dev:
            stream = pipe_stream(aqueue, volval, vsptsval, vsperfval)
            next(stream)
            dev.start(stream)
            while True:
                time.sleep(0.02)
    th.Thread(target=make_pbj).start()
    win = tk.Tk()
    win.title("renderE stream audio")
    label = tk.Label(win, text="Record this window for stream audio in OBS.\nThank you for using renderE!", font=("", 18))
    label.pack()
    win.mainloop()

def pg_jams():
    print("i'm pg jams")

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
        self.has_audio = False
        self.ready = th.Event()
        
        self.astream = None
        self.aparams = ()
    
    def thread_runner(self):
        print("TR")
        vst = self.av.streams.video[0]
        dec = (vst,)
        
        if not (vst.width or vst.height):
            dar = 0
        else:
            dar = vst.display_aspect_ratio or (vst.width/vst.height)
            print("SIZE: ", vst.width, vst.height, "DAR", dar)
        self.has_audio = (len(self.av.streams.audio) > 0)
        self.size = (720, 480)
        if len(self.av.streams.audio) > 0:
            ast = self.av.streams.audio[0]
            dec = (vst, ast)
        
        resampler = av.audio.resampler.AudioResampler(
            format='s16', 
            layout='stereo', 
            rate=48000
        )
        
        print("decoding")
        self.ready.set()
        
        for frame in self.av.decode(*dec):
            if isinstance(frame, av.VideoFrame):
                self.vtb = frame.time_base
                self.frames.append((frame.pts*frame.time_base, frame.reformat(width=self.size[0], height=480, format="rgba").to_ndarray().tobytes()))
                
                self.frames = [f for f in self.frames if not f[0] < self.prune]
            elif isinstance(frame, av.AudioFrame):
                #self.aparams = (frame.sample_rate, 16, frame.layout.nb_channels)
                self.aparams = (48000, 16, 2)
                self.atb = frame.time_base
                
                self.astf = {8: "char", 16: "int16_t", 32: "float"}[16]
                
                for rf in resampler.resample(frame):
                    self.audio.append(
                        (frame.pts*frame.time_base, rf.to_ndarray().tobytes())
                    )
        
        print("decode end")
class Handler():
    def __init__(self, url):
        self.ts = TSStream(url)
        
        self.ppts = 0
        
        self.size = (0, 0)
        
        self.frame = None
        self.vol = 1
        self.volval = mp.Value("d", 1.0)
        tth = th.Thread(target=self.ts.thread_runner).start()
        th.Thread(target=self.runner).start()
    
    def set_volume(self, volume):
        self.vol = volume
        self.volval.value = self.vol
    
    
    def runner(self):
        
        def goback(val): #might try using this at some point for the min function
            if val > 0:
                return val
            else:
                return float("inf")
        
        ts = self.ts
        
        cpts = 0
        
        # def audiogen():
        #     lprune = None
        #     nonlocal samples, video_s_pts
        #     print("audiogen")
        #     required_frames = yield b""
        #     print("audiogenf", required_frames)
        #     while True:
        #         required_bytes = required_frames * 2 * 2
        #         while len(samples) < required_bytes:
        #             if len(ts.audio) > 0:
        #                 ap = ts.audio.pop(0)
        #                 if video_s_pts is None:
        #                     video_s_pts = (ap[0], time.perf_counter())
        #             else:
        #                 while True:
        #                     if len(ts.audio) > 0:
        #                         ap = ts.audio.pop(0)
        #                         break
        #                     time.sleep(0.05)
        #                     print("DROWN")
        #             volled = aop.mul(ap[1], 2, self.vol)
        #             samples.extend(volled)
        #         required_frames = yield samples[:required_bytes]
        #         samples = samples[required_bytes:]
        
        self.ts.ready.wait()
        if self.ts.has_audio and not DISABLE_AUDIO:
            print("ts has audio")
            aqueue = mp.Pipe(False)
            
            vsptsval = mp.Value("d", 0.0)
            vsperfval = mp.Value("d", 0.0)
            args = (aqueue[0], self.volval, vsptsval, vsperfval)
            print("arrgs", args)
            p = mp.Process(target=pb_jams, args=args, daemon=True)
            p.start()
            
            
            def auding():
                cl = pg.Clock()
                while True:
                    if len(ts.audio) > 0:
                        #print("putting an audio")
                        alen = len(ts.audio)
                        adata = []
                        for i in range(alen):
                            adata.append(ts.audio.pop(0))
                        #print("putting", tsa)
                        aqueue[1].send(adata)
                    cl.tick_busy_loop(30)
            th.Thread(target=auding).start()
            while True:
                self.size = self.ts.size
                if vsperfval.value != 0:
                    cpts = vsptsval.value + (time.perf_counter()-vsperfval.value)
                    if ts.frames:
                        frr = min(ts.frames, key=lambda x : abs(cpts-x[0]))
                        if frr[1] is not None:
                            self.frame = frr[1]
                            ts.prune = frr[0]-1
                clock.tick_busy_loop(30)
                if not p.is_alive():
                    print("WHAT HAPPENED TO PB JAMS?", p.exitcode)
        else:
            vsperf = 0
            vspts = 0
            while True:
                self.size = self.ts.size
                if ts.frames:
                    if vsperf == 0:
                        vsperf = time.perf_counter()
                        vspts = ts.frames[0][0]
                    cpts = vspts + (time.perf_counter()-vsperf)
                    frr = min(ts.frames, key=lambda x : abs(cpts-x[0]))
                    if frr[1] is not None:
                        self.frame = frr[1]
                        ts.prune = frr[0]-1
                clock.tick_busy_loop(30)
        
        
        # while True:
        #     self.ppts = cpts
        #     self.size = self.ts.size
        #     if len(ts.audio) > 0:
        #         if ts.astream and rl.is_audio_stream_processed(ts.astream):
        #             cant = False
        #             first = True
        #             while len(samples) < self.buf*4:
        #                 if len(ts.audio) == 0:
        #                     cant = True
        #                     break
        #                 cc = ts.audio.pop(0)
        #                 #if cpts == 0:
        #                 cpts = cc[0]
        #                 samples.extend(cc[1])
        #                 first = False
        #             if not cant:
        #                 npa = np.frombuffer(samples[:self.buf*4], dtype=np.int16)
        #                 rl.update_audio_stream(ts.astream, rl.ffi.new(ts.astf+" []", npa.tolist()), self.buf)
        #                 samples = samples[self.buf*4:]
        #     else:
        #         print("DROWNING")
        #     if ts.frames:
        #         frr = min(ts.frames, key=lambda x : abs(cpts-x[0]))
        #         ts.prune = frr[0]
        #         self.frame = frr[1]
            
        #     # if cpts != 0:
        #     #     cpts += Fraction(1, 30)
            
        #     clock.tick_busy_loop(30)


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
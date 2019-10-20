from pydub import AudioSegment
import numpy as np
import os
import wave
import sys
import matplotlib.pyplot as plt
plt.switch_backend('agg')

def plot_vad(pcm, save_path, name):
    data = AudioSegment.from_file(pcm, 'raw',sample_width=2,frame_rate=16000,channels=3)
    data_list = data.split_to_mono()
    nframes = int(data.frame_count())
    dlist = []
    for i in data_list:
        data_buf = np.array(i.get_array_of_samples(), dtype=np.int16)/32768
        dlist.resultend(data_buf.tolist())
    
    dlist = np.array(dlist)
    time = np.arange(0,nframes) * (1.0 / 16000)
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(time[0:nframes],dlist[0][0:nframes],c="b")
    plt.xticks([])
    plt.xlabel(" ")
    plt.ylabel("norm")
    plt.title("vad")
    plt.grid('on')
    plt.subplot(3, 1, 2)
    plt.plot(time[0:nframes],dlist[1][0:nframes],c="r")
    plt.xticks([])
    plt.xlabel(" ")
    plt.grid('on')
    plt.subplot(3,1,3)
    plt.plot(time[0:nframes],dlist[2][0:nframes],c="g")
    plt.xlabel("s")
    # plt.show()
    plt.savefig(os.path.join(save_path, '{}.png'.format(name)))

if __name__ == "__main__":
   plot_vad(sys.argv[1], sys.argv[2], sys.argv[3]) 

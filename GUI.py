import datetime
import pygame
import tkinter
import tkinter.ttk

from utils import parseRSS
from utils import downloadPodcast, getFilenames
from utils import convertMP3ToWav
from Recogniser import recognise


class GUI:
    def __init__(self):
        pygame.mixer.init()
        self.lastIndex = 0

        self.root = tkinter.Tk()
        self.root.title('NECL!')
        self.root.geometry("640x120")
        self.mainframe = tkinter.ttk.Frame(self.root)

        self.rssButton = tkinter.ttk.Button(self.mainframe, text="RSS", command = self.rssButtonPressed)
        self.downloadButton = tkinter.ttk.Button(self.mainframe, text="Download", command = self.downloadButtonPressed)
        self.convertButton = tkinter.ttk.Button(self.mainframe, text="Convert", command = self.convertButtonPressed)
        self.recogniseButton = tkinter.ttk.Button(self.mainframe, text="Recognise", command = self.recogniseButtonPressed)

        self.playButtonText = tkinter.StringVar()
        self.playButton = tkinter.ttk.Button(self.mainframe, textvariable=self.playButtonText, command = self.playButtonPressed)
        self.playButtonText.set("Play")

        self.timePassedText = tkinter.StringVar()
        self.timePassed = tkinter.ttk.Label(self.mainframe, textvariable=self.timePassedText)
        self.assignTimePassed(0)

        # self.playStatus = 'NA'
        self.text = tkinter.Text(self.mainframe, wrap = "word")

        self.mainframe.grid(column=0, row=0, columnspan=7, rowspan=2)
        self.rssButton.grid(column=1, row=0)
        self.downloadButton.grid(column=2, row=0)
        self.convertButton.grid(column=3, row=0)
        self.recogniseButton.grid(column=4, row=0)
        self.playButton.grid(column=5, row=0)
        self.timePassed.grid(column=6, row=0)
        self.text.grid(column=0, row=1, columnspan=7)

        self.root.bind("<Return>", self.playButtonPressed)
        self.root.mainloop()

    def rssButtonPressed(self):
        rssLink = "https://cppcast.com/feed.rss"
        parseResults = parseRSS(rssLink)
        self.link, self.title = parseResults[0]
        self.root.title(self.title)
        print("rssButtonPressed")

    def downloadButtonPressed(self):
        self.filenames = getFilenames(self.link)
        downloadResult = downloadPodcast(self.filenames)
        print("downloadButtonPressed")

    def convertButtonPressed(self):
        conversionResult = convertMP3ToWav(self.filenames)
        print("convertButtonPressed")

    def recogniseButtonPressed(self):
        try:
            self.json = recognise(self.filenames)
        except Exception as e:
            tkinter.messagebox.showerror("Recognition Error", str(e))
        print("recogniseButtonPressed")

    def assignTimePassed(self, ms):
        timeDelta = datetime.timedelta(milliseconds=ms)
        timePassed: str = str(timeDelta)
        self.timePassedText.set(timePassed)

    def playButtonPressed(self):
        if 'Play' == self.playButtonText.get():
            pygame.mixer.music.load(self.filenames['wav'])
            pygame.mixer.music.play()
            self.playButtonText.set('Pause')
            self.root.after(100, self.loop)
        elif 'Pause' == self.playButtonText.get():
            pygame.mixer.music.pause()
            self.playButtonText.set('Resume')
        elif 'Resume' == self.playButtonText.get():
            pygame.mixer.music.unpause()
            self.playButtonText.set('Pause')
            self.root.after(100, self.loop)
        print("playButtonPressed")

    def loop(self):
        if not 'Pause' == self.playButtonText.get():
            return
        pos = pygame.mixer.music.get_pos()
        self.assignTimePassed(pos)
        for i in range(self.lastIndex, len(self.json['result'])):
            wordDict = self.json['result'][i]
            if wordDict['end'] < pos/1000.0 + 1.0:
                self.text.insert(tkinter.END, wordDict['word']+" ")
                self.text.see(tkinter.END)
            else:
                self.lastIndex = i
                break
        self.root.after(100, self.loop)


if __name__ == '__main__':
    GUI()

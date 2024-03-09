from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
import time

class AudioPlayer:
    def __init__(self):
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)

    def playMusic(self, filePath):
        if self.player.source() != QUrl.fromLocalFile(filePath):
            self.player.setSource(QUrl.fromLocalFile(filePath))
        if self.player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
            self.player.play()

    def stopMusic(self):
        self.player.stop()

    def changeAndPlayMusic(self, filePath):
        self.stopMusic()  
        time.sleep(.05)
        self.playMusic(filePath)
    def setVolume(self, volume):
        volume = max(0.0, min(1.0, volume))
        self.audioOutput.setVolume(volume)
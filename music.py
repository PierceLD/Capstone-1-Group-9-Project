#3/8/24
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
import time

class AudioPlayer:
    def __init__(self):
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.effectPlayer = QMediaPlayer()
        self.effectAudioOutput = QAudioOutput()
        self.effectPlayer.setAudioOutput(self.effectAudioOutput)
        self.isMuted = False

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
    def toggleMute(self):
        try:
            self.isMuted = not self.isMuted
            self.audioOutput.setMuted(self.isMuted)
        except Exception as e:
            print(f"Error toggling mute: {e}")
    def playSoundEffect(self, filePath):
        time.sleep(.05)
        self.effectPlayer.setSource(QUrl.fromLocalFile(filePath))
        self.effectPlayer.play()
        time.sleep(.05)
    

    def checkEffectStatus(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.effectPlayer.setSource(QUrl())  
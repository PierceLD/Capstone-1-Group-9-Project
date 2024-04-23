#3/8/24
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
import time
eff = 1.0
master=1.0
mul=0.5
curr=1.0

class AudioPlayer:
    def __init__(self):
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)

        self.player.mediaStatusChanged.connect(self.checkMediaStatus)

        self.effectPlayer = QMediaPlayer()
        self.effectAudioOutput = QAudioOutput()
        self.effectPlayer.setAudioOutput(self.effectAudioOutput)
        
        self.isMuted = False

    def playMusic(self, filePath):
        global curr
        self.audioOutput.setVolume(curr)
        if self.player.source() != QUrl.fromLocalFile(filePath):
            self.player.setSource(QUrl.fromLocalFile(filePath))
        if self.player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
            self.player.play()

    def checkMediaStatus(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.player.play()

    def stopMusic(self):
        print("stopping")
        self.player.stop()

    def changeAndPlayMusic(self, filePath):
        self.stopMusic()  
        time.sleep(.05)
        self.playMusic(filePath)

    def setVolume(self, volume):
        global mul,master,curr
        self.audioOutput.setVolume((volume*mul)*master)
        curr=self.audioOutput.volume()

    def setVolumeM(self, volume=0.5):
        global mul
        mul=volume


    def setMasterVolume(self, volume):
        global master
        normalized_volume = volume / 100.0
        master=normalized_volume


    def setEffectVolume(self, volume):
        global eff
        try:
            normalized_volume = volume / 100.0
            eff = normalized_volume 
        except Exception as e:
            print(f"Failed to set effect volume: {e}")

    def setMusicVolume(self, volume):
        try:
            normalized_volume = volume / 100.0
            self.setVolume(normalized_volume)
            self.player.pause()
            self.player.play()
            #print(f"Music volume set to: {self.audioOutput.volume()}")
        except Exception as e:
            print(f"Failed to set music volume: {e}")




    def toggleMute(self):
        try:
            self.isMuted = not self.isMuted
            self.audioOutput.setMuted(self.isMuted)
        except Exception as e:
            print(f"Error toggling mute: {e}")


    def playSoundEffect(self, filePath, volume=1):
        global eff,master
        self.effectAudioOutput.setVolume((volume*eff)*master)
        time.sleep(.05)
        self.effectPlayer.setSource(QUrl.fromLocalFile(filePath))
        self.effectPlayer.play()
        time.sleep(.05)
        



    def checkEffectStatus(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.effectPlayer.setSource(QUrl())  
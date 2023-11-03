from core.audio_player import AudioPlayer

player = AudioPlayer()

def start():
    player.load_and_play_in_loop("./assets/ring.wav")

def stop():
    player.stop()

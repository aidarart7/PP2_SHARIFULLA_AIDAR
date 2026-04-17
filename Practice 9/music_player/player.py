import pygame
import os


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()

        base_dir = os.path.dirname(os.path.abspath(__file__))
        music_dir = os.path.join(base_dir, "music")

        self.playlist = [
            os.path.join(music_dir, f)
            for f in os.listdir(music_dir)
            if f.endswith(".wav") or f.endswith(".mp3")
        ]

        self.index = 0
        self.playing = False

        pygame.font.init()
        self.font = pygame.font.SysFont(None, 36)

    def load(self):
        pygame.mixer.music.load(self.playlist[self.index])

    def play(self):
        self.load()
        pygame.mixer.music.play()
        self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next(self):
        self.index = (self.index + 1) % len(self.playlist)
        self.play()

    def prev(self):
        self.index = (self.index - 1) % len(self.playlist)
        self.play()

    def get_track_name(self):
        return os.path.basename(self.playlist[self.index])

    def draw(self, screen):
        screen.fill((20, 20, 20))

        text = self.font.render(f"Track: {self.get_track_name()}", True, (255, 255, 255))
        screen.blit(text, (50, 50))

        status = "Playing" if self.playing else "Stopped"
        status_text = self.font.render(status, True, (0, 200, 0))
        screen.blit(status_text, (50, 100))
from math import *
import pygame
from settings import *
import numpy as np
# functions
def WavesToColor(n, m):
    rolling_fft.push(n)

    # Compute FFT magnitudes
    magnitudes = rolling_fft.compute_fft_magnitudes()

    # Use magnitudes of specific frequency components to determine RGB.
    r = int(200 * magnitudes[1] / max(magnitudes))
    g = int(255 * magnitudes[2] / max(magnitudes))
    b = int(255 * magnitudes[3] / max(magnitudes))

    # Ensure RGB values are within [0, 255]
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    return (r, g, b)

class RollingFFT:
    def __init__(self, size):
        self.size = size
        self.buffer = [0] * size

    def push(self, value):
        self.buffer.pop(0)
        self.buffer.append(value)

    def compute_fft_magnitudes(self):
        centered_samples = [sample - np.mean(self.buffer) for sample in self.buffer]

        fft_values = np.fft.fft(self.buffer)
        magnitudes = np.abs(fft_values)
        return magnitudes
rolling_fft = RollingFFT(100)

# classes
class wave_subsection():
    def __init__(self, width, height, amplitudeModifier, wavelengthModifier, wavetype):
        self.width, self.height = width, height
        self.surface = pygame.Surface((self.width, self.height))
        self.x_scale = self.width / (2.1 * pi)
        self.y_scale = self.height / 4
        self.phase_shift = 0
        self.amplitudeModifier = amplitudeModifier
        self.wavelengthModifier = wavelengthModifier
        self.waveType = wavetype
        self.backround = pygame.image.load("assets/graph.png")

        self.wavelenth_up_button = pygame.image.load("assets/plusWavelen.png")
        self.wavelenth_down_button = pygame.image.load("assets/minuswavelenth.png")
        self.amplitude_up_button = pygame.image.load("assets/plusAmp.png")
        self.amplitude_down_button = pygame.image.load("assets/minusamp.png")
        self.wavelength_up_button_position = (10, self.height - 15)
        self.wavelength_down_button_position = (60, self.height - 15)
        self.amplitude_up_button_position = (110, self.height - 15)
        self.amplitude_down_button_position = (160, self.height - 15)

    def draw_buttons(self):
        self.surface.blit(self.wavelenth_up_button, self.wavelength_up_button_position)
        self.surface.blit(self.wavelenth_down_button, self.wavelength_down_button_position)
        self.surface.blit(self.amplitude_up_button, self.amplitude_up_button_position)
        self.surface.blit(self.amplitude_down_button, self.amplitude_down_button_position)

    def draw_sine_wave(self):
        x = 0
        prev_screen_x, prev_screen_y = None, None

        while x <= 2.1 * pi:
            if self.waveType == sin:
                y = self.amplitudeModifier * sin(self.wavelengthModifier * x + self.phase_shift)
            elif self.waveType == cos:
                y = self.amplitudeModifier * cos(self.wavelengthModifier * x + self.phase_shift)
            elif self.waveType == tan:
                y = self.amplitudeModifier * tan(self.wavelengthModifier * x + self.phase_shift)
            else:
                print("invalid wave style")
            screen_x = int(x * self.x_scale)
            screen_y = int(self.height / 2 - y * self.y_scale)

            if prev_screen_x is not None:
                pygame.draw.line(self.surface, (0, 0, 255), (prev_screen_x, prev_screen_y), (screen_x, screen_y))

            prev_screen_x, prev_screen_y = screen_x, screen_y
            x += sine_wave_speed_int

    def draw(self):
        self.surface.blit(self.backround, (0, 0))
        self.draw_sine_wave()
        self.draw_buttons()
        self.phase_shift += 0.05

    def check_button_click(self, mouse_pos):
        x, y = mouse_pos
        button_width, button_height = 40, 11

        # Check if any button is clicked
        if self.wavelength_up_button_position[0] <= x <= self.wavelength_up_button_position[0] + button_width and \
                self.wavelength_up_button_position[1] <= y <= self.wavelength_up_button_position[1] + button_height:
            self.wavelengthModifier += 0.1

        elif self.wavelength_down_button_position[0] <= x <= self.wavelength_down_button_position[0] + button_width and \
                self.wavelength_down_button_position[1] <= y <= self.wavelength_down_button_position[1] + button_height:
            self.wavelengthModifier -= 0.1

        elif self.amplitude_up_button_position[0] <= x <= self.amplitude_up_button_position[0] + button_width and \
                self.amplitude_up_button_position[1] <= y <= self.amplitude_up_button_position[1] + button_height:
            self.amplitudeModifier += 0.1

        elif self.amplitude_down_button_position[0] <= x <= self.amplitude_down_button_position[0] + button_width and \
                self.amplitude_down_button_position[1] <= y <= self.amplitude_down_button_position[1] + button_height:
            self.amplitudeModifier -= 0.1

    def render(self, target_surface, position):
        target_surface.blit(self.surface, position)

class color_subsection():
    def __init__(self, width, height, combined_wave):
        self.width, self.height = width, height
        self.surface = pygame.Surface((self.width, self.height))
        self.combined_wave = combined_wave
        self.current_color = (255, 255, 255)


    def draw(self):
        avg_wave_value = self.combined_wave.get_average_wave_value()
        color = WavesToColor(avg_wave_value, 255)
        self.surface.fill(color)

    def get_color(self):
        avg_wave_value = self.combined_wave.get_average_wave_value()
        color = WavesToColor(avg_wave_value, 255)
        return color

    def render(self, target_surface, position):
        target_surface.blit(self.surface, position)

class DrawableSubsection():
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill("white")

    def draw(self, x, y, color):
        if 0 <= x < self.width and 0 <= y + 50 < self.height:  # Adjust the y-coordinate check
            pygame.draw.circle(self.surface, color, (x, y - 50), 5)  # Add 50 pixels to y-coordinate

    def render(self, target_surface, position):
        target_surface.blit(self.surface, position)



class combined_wave_subsection():
    def __init__(self, width, height, waves):
        self.width, self.height = width, height
        self.surface = pygame.Surface((self.width, self.height))
        self.x_scale = self.width / (2.1 * pi)
        self.y_scale = self.height / 4
        self.phase_shift = 0
        self.waves = waves
        self.backround = pygame.image.load("assets/graph.png")
    def combined_wave_value(self, x):
        total_value = 0
        for wave in self.waves:
            amplitudeModifier = wave.amplitudeModifier
            wavelengthModifier = wave.wavelengthModifier
            waveType = wave.waveType
            if waveType == sin:
                total_value += amplitudeModifier * sin(wavelengthModifier * x + self.phase_shift)
            elif waveType == cos:
                total_value += amplitudeModifier * cos(wavelengthModifier * x + self.phase_shift)
            elif waveType == tan:
                total_value += amplitudeModifier * tan(wavelengthModifier * x + self.phase_shift)

        max_combined_amplitude = sum([wave.amplitudeModifier for wave in self.waves])
        return (total_value / max_combined_amplitude) * self.y_scale

    def get_wave_color(self):
        max_amplitude, _ = self.get_max_min_wave_values()
        m = 255
        r, g, b = WavesToColor(max_amplitude, m)
        return (r, g, b)
    def draw_combined_wave(self):
        x = 0
        prev_screen_x, prev_screen_y = None, None

        while x <= 2.1 * pi:
            y = self.combined_wave_value(x)
            screen_x = int(x * self.x_scale)
            screen_y = int(self.height / 6- y)

            if prev_screen_x is not None:
                pygame.draw.line(self.surface, (0, 255, 255), (prev_screen_x, prev_screen_y), (screen_x, screen_y))

            prev_screen_x, prev_screen_y = screen_x, screen_y
            x += sine_wave_speed_int

    def draw(self):
        self.surface.blit(self.backround, (0, 0))
        self.draw_combined_wave()
        self.phase_shift += 0.05

    def render(self, target_surface, position):
        target_surface.blit(self.surface, position)

    def get_average_wave_value(self):
        x = 2.1 * pi / 2  # Get the value at the midpoint of the wave
        return self.combined_wave_value(x)
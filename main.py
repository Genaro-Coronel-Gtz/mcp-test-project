#!/usr/bin/env python3
"""
Generador de Música Aleatoria
Script para crear música aleatoria usando diferentes métodos
"""

import random
import time
import math
import wave
import struct
import os
from typing import List, Tuple

class MusicGenerator:
    def __init__(self):
        # Escalas musicales (en semitonos desde C)
        self.scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'pentatonic': [0, 2, 4, 7, 9],
            'blues': [0, 3, 5, 6, 7, 10],
            'dorian': [0, 2, 3, 5, 7, 9, 10],
            'mixolydian': [0, 2, 4, 5, 7, 9, 10]
        }
        
        # Frecuencias base (C4 = 261.63 Hz)
        self.base_freq = 261.63
        
        # Duraciones de notas (en segundos)
        self.durations = {
            'whole': 2.0,
            'half': 1.0,
            'quarter': 0.5,
            'eighth': 0.25,
            'sixteenth': 0.125
        }
        
        # Configuración de audio
        self.sample_rate = 44100
        self.channels = 1
        self.sample_width = 2

    def note_to_frequency(self, semitone_offset: int, octave: int = 4) -> float:
        """Convierte una nota (offset en semitonos) a frecuencia"""
        return self.base_freq * (2 ** (octave - 4)) * (2 ** (semitone_offset / 12))

    def generate_sine_wave(self, frequency: float, duration: float, amplitude: float = 0.3) -> List[int]:
        """Genera una onda senoidal para una frecuencia y duración dadas"""
        samples = []
        num_samples = int(self.sample_rate * duration)
        
        for i in range(num_samples):
            # Aplicar envelope (ADSR simplificado)
            envelope = 1.0
            if i < num_samples * 0.1:  # Attack
                envelope = i / (num_samples * 0.1)
            elif i > num_samples * 0.8:  # Release
                envelope = (num_samples - i) / (num_samples * 0.2)
            
            # Generar muestra
            t = i / self.sample_rate
            sample = amplitude * envelope * math.sin(2 * math.pi * frequency * t)
            samples.append(int(sample * 32767))  # Convertir a 16-bit
            
        return samples

    def generate_chord(self, root_note: int, chord_type: str = 'major', octave: int = 4, duration: float = 1.0) -> List[int]:
        """Genera un acorde"""
        chord_intervals = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            'diminished': [0, 3, 6],
            'augmented': [0, 4, 8],
            'seventh': [0, 4, 7, 10],
            'minor_seventh': [0, 3, 7, 10]
        }
        
        intervals = chord_intervals.get(chord_type, [0, 4, 7])
        chord_samples = []
        num_samples = int(self.sample_rate * duration)
        
        # Inicializar array de muestras
        for _ in range(num_samples):
            chord_samples.append(0)
        
        # Sumar las ondas de cada nota del acorde
        for interval in intervals:
            note_freq = self.note_to_frequency(root_note + interval, octave)
            note_samples = self.generate_sine_wave(note_freq, duration, amplitude=0.2)
            
            for i in range(len(note_samples)):
                if i < len(chord_samples):
                    chord_samples[i] += note_samples[i]
        
        # Normalizar para evitar clipping
        max_val = max(abs(sample) for sample in chord_samples)
        if max_val > 32767:
            chord_samples = [int(sample * 32767 / max_val) for sample in chord_samples]
            
        return chord_samples

    def generate_melody(self, scale_name: str = 'major', num_notes: int = 16, octave_range: Tuple[int, int] = (4, 5)) -> List[Tuple[int, float]]:
        """Genera una melodía aleatoria"""
        scale = self.scales.get(scale_name, self.scales['major'])
        melody = []
        
        duration_options = list(self.durations.values())
        
        for _ in range(num_notes):
            # Seleccionar nota de la escala
            note = random.choice(scale)
            # Seleccionar octava
            octave = random.randint(octave_range[0], octave_range[1])
            # Seleccionar duración
            duration = random.choice(duration_options)
            
            melody.append((note + (octave - 4) * 12, duration))
            
        return melody

    def generate_chord_progression(self, scale_name: str = 'major', num_chords: int = 4) -> List[Tuple[int, str, float]]:
        """Genera una progresión de acordes"""
        scale = self.scales.get(scale_name, self.scales['major'])
        progression = []
        
        chord_types = ['major', 'minor', 'seventh'] if scale_name == 'major' else ['minor', 'major', 'minor_seventh']
        
        for _ in range(num_chords):
            root = random.choice(scale)
            chord_type = random.choice(chord_types)
            duration = random.choice([2.0, 4.0])  # Acordes más largos
            
            progression.append((root, chord_type, duration))
            
        return progression

    def save_audio(self, samples: List[int], filename: str):
        """Guarda las muestras de audio en un archivo WAV"""
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(self.sample_width)
            wav_file.setframerate(self.sample_rate)
            
            # Convertir muestras a bytes
            audio_data = b''.join(struct.pack('<h', sample) for sample in samples)
            wav_file.writeframes(audio_data)

    def create_random_song(self, scale_name: str = None, song_length: int = 32):
        """Crea una canción aleatoria completa"""
        if scale_name is None:
            scale_name = random.choice(list(self.scales.keys()))
        
        print(f"Generando canción en escala: {scale_name}")
        
        # Generar melodía
        melody = self.generate_melody(scale_name, song_length)
        print(f"Melodía generada con {len(melody)} notas")
        
        # Generar progresión de acordes
        chord_progression = self.generate_chord_progression(scale_name, song_length // 4)
        print(f"Progresión de acordes: {len(chord_progression)} acordes")
        
        # Crear audio de la melodía
        melody_samples = []
        for note_offset, duration in melody:
            frequency = self.note_to_frequency(note_offset % 12, 4 + note_offset // 12)
            note_samples = self.generate_sine_wave(frequency, duration)
            melody_samples.extend(note_samples)
        
        # Crear audio de los acordes
        chord_samples = []
        for root, chord_type, duration in chord_progression:
            chord_audio = self.generate_chord(root, chord_type, 3, duration)
            chord_samples.extend(chord_audio)
        
        # Combinar melodía y acordes (simplificado)
        max_length = max(len(melody_samples), len(chord_samples))
        combined_samples = []
        
        for i in range(max_length):
            melody_val = melody_samples[i] if i < len(melody_samples) else 0
            chord_val = chord_samples[i] if i < len(chord_samples) else 0
            
            # Mezclar con diferentes volúmenes
            combined = int(melody_val * 0.7 + chord_val * 0.3)
            combined_samples.append(max(-32767, min(32767, combined)))
        
        return combined_samples, scale_name

def print_menu():
    """Muestra el menú de opciones"""
    print("\n" + "="*50)
    print("🎵 GENERADOR DE MÚSICA ALEATORIA 🎵")
    print("="*50)
    print("1. Generar melodía simple")
    print("2. Generar progresión de acordes")
    print("3. Generar canción completa")
    print("4. Generar múltiples canciones")
    print("5. Mostrar escalas disponibles")
    print("6. Salir")
    print("="*50)

def main():
    generator = MusicGenerator()
    
    while True:
        print_menu()
        choice = input("Selecciona una opción (1-6): ").strip()
        
        if choice == '1':
            print("\n🎼 Generando melodía...")
            scale = input("Escala (major/minor/pentatonic/blues/dorian/mixolydian) [Enter para aleatoria]: ").strip()
            if not scale:
                scale = random.choice(list(generator.scales.keys()))
            
            num_notes = input("Número de notas [16]: ").strip()
            num_notes = int(num_notes) if num_notes.isdigit() else 16
            
            melody = generator.generate_melody(scale, num_notes)
            
            # Convertir a audio
            samples = []
            for note_offset, duration in melody:
                freq = generator.note_to_frequency(note_offset % 12, 4 + note_offset // 12)
                note_samples = generator.generate_sine_wave(freq, duration)
                samples.extend(note_samples)
            
            filename = f"melody_{scale}_{int(time.time())}.wav"
            generator.save_audio(samples, filename)
            print(f"✅ Melodía guardada como: {filename}")
            
        elif choice == '2':
            print("\n🎹 Generando progresión de acordes...")
            scale = input("Escala [Enter para aleatoria]: ").strip()
            if not scale:
                scale = random.choice(list(generator.scales.keys()))
            
            num_chords = input("Número de acordes [4]: ").strip()
            num_chords = int(num_chords) if num_chords.isdigit() else 4
            
            progression = generator.generate_chord_progression(scale, num_chords)
            
            # Convertir a audio
            samples = []
            for root, chord_type, duration in progression:
                chord_samples = generator.generate_chord(root, chord_type, 3, duration)
                samples.extend(chord_samples)
            
            filename = f"chords_{scale}_{int(time.time())}.wav"
            generator.save_audio(samples, filename)
            print(f"✅ Acordes guardados como: {filename}")
            
        elif choice == '3':
            print("\n🎵 Generando canción completa...")
            scale = input("Escala [Enter para aleatoria]: ").strip()
            if not scale:
                scale = None
            
            length = input("Longitud de la canción (número de notas) [32]: ").strip()
            length = int(length) if length.isdigit() else 32
            
            samples, used_scale = generator.create_random_song(scale, length)
            filename = f"song_{used_scale}_{int(time.time())}.wav"
            generator.save_audio(samples, filename)
            print(f"✅ Canción guardada como: {filename}")
            print(f"🎼 Escala utilizada: {used_scale}")
            
        elif choice == '4':
            print("\n🎶 Generando múltiples canciones...")
            num_songs = input("¿Cuántas canciones generar? [3]: ").strip()
            num_songs = int(num_songs) if num_songs.isdigit() else 3
            
            print(f"Generando {num_songs} canciones...")
            for i in range(num_songs):
                samples, scale = generator.create_random_song()
                filename = f"random_song_{i+1}_{scale}_{int(time.time())}.wav"
                generator.save_audio(samples, filename)
                print(f"✅ Canción {i+1} guardada: {filename} (Escala: {scale})")
                time.sleep(0.1)  # Pequeña pausa para nombres únicos
            
        elif choice == '5':
            print("\n🎼 Escalas musicales disponibles:")
            print("="*40)
            for scale_name, notes in generator.scales.items():
                print(f"{scale_name.capitalize()}: {notes}")
            print("="*40)
            print("Los números representan semitonos desde C (Do)")
            
        elif choice == '6':
            print("\n👋 ¡Gracias por usar el Generador de Música Aleatoria!")
            break
            
        else:
            print("❌ Opción no válida. Por favor, selecciona un número del 1 al 6.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    print("🎵 Iniciando Generador de Música Aleatoria...")
    print("Asegúrate de tener Python 3.6+ instalado")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Si el error persiste, verifica que tengas los permisos necesarios para crear archivos.")
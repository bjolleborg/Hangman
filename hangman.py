#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 15:38:18 2023

@author: bjolleborg

Das Programm ermöglicht es, auf der Konsole gegen den Computer
Hangman zu spielen.
Der Computer wählt dabei zufällig ein Wort aus der Datenbank.
"""

import sqlite3
from random import randint
from time import sleep

# Datenbank wird eingelesen
con = sqlite3.connect("/Users/friday/Desktop/Data_Science_Institute/Python/Woche_11/Hangman/database.db")

con.row_factory = sqlite3.Row

cur = con.cursor()


# Eigentliches Spiel
while True:
    # Anzahl der Leben per Default auf 10 - kann in den Optionen über die Konsole nachträglich angepasst werden.
    lives = 10
    
    # Begrüßung des Spielers
    print("""
Willkommen bei Hangman!
    
Wähle:
    - Neues Spiel (n)
    - Optionen (o)
    - Beenden (b)
    
    """)
    
    # Auswahl des Spielers
    plr_chs = input("(n/o/b) ")
    
    # Optionen, um Anzahl der Leben anzupassen.
    if plr_chs == "o":
        lives = int(input("Mit wie vielen Leben möchtest du Spielen? (Ich empfehle 10) "))
    
    # Neues Spiel
    elif plr_chs == "n":
        
        # Liste, in die die falsch geratenen Buchstaben eingetragen werden.
        guessed_w = []
        # Liste, in die alle Buchstaben eingetragen werden
        guessed = []
        
        # Anzahl Zeilen - also Worten in der Datenbank
        rows = cur.execute("SELECT COUNT(*) FROM words").fetchone()[0]
        
        # Zufallszahl für die Wahl des Wortes
        rnd_chs = [randint(1, rows)]
        
        # Zufälliges Wort und die Anzahl dessen Buchstaben werden in die Variablen geschrieben
        word , letters = cur.execute("SELECT * FROM words WHERE rowid = (?)", (rnd_chs)).fetchone()
        
        # Buchstabenanzahl wird als Float ausgelesen. Daher hier in int umgewandelt
        letters = int(letters)
        
        # Eine Liste mit _ als Platzhalter für die Buchstaben
        placeholder = ["_"] * letters
        
        while lives > 0:
            
            # Infoausgabe für den Spieler
            print(f"""
Dein Spielstand: {(" ").join(placeholder)}
                  
Bisher falsch geratene Buchstaben: {guessed_w}.
Du hast {lives} Leben.
            """)
            
            # Spieler gibt einen Buchstaben ein.
            letter = input("Rate: ").upper()
            
            # Buchstabe wird in guessed eingetragen, falls er noch nicht enthalten ist
            if letter not in guessed:
                guessed.append(letter)
            # Hinweis, dass Buchstabe schon verwendet wurde.
            else:
                print("Diesen Buchstaben hast du schon versucht!")
                continue
            
            # Buchstabe wird in die Liste falscher Buchstaben eingetragen, falls er nicht im Wort vorkommt.
            if letter not in word and letter not in guessed_w:
                guessed_w.append(letter)
            
            # Falls der Buchstabe im Wort vorkommt, wird er anstelle der entsprechenden _ in placeholder eingetragen
            if letter in word:
                for index, l in enumerate(word):
                    if l == letter:
                        placeholder[index] = l
            # Falls der Buchstabe nicht vorkommt, wird das Leben um 1 verringert
            else:
                lives -= 1
                
                # Ausgabe bei Niederlage
                if lives == 0:
                    print(f"Schade! Du hast {word} nicht erraten.")
                    sleep(1)
            
            # Ausgabe bei Sieg.
            if not "_" in placeholder:
                print(f"""Herzlichen Glückwunsch!
                      
Du hast mein Wort {word} erraten!
""")
                sleep(1)
                break
    
    elif plr_chs == "b":
        break
    
    else:
        print(f"Fehlerhafte Eingabe: {plr_chs}")

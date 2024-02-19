#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 10:24:41 2023

@author: bjolleborg

Das Programm ermöglicht es in der Datenbank database.db zu arbeiten. 
Man kann diese über mehrere Optionen auslesen:
    - Prüfen, ob ein bestimmtes Wort in der Datenbank vorkommt
    - Alle Worte einer bestimmten Länge ausgeben lassen
    - Die gesamte Datenbank ausgeben lassen

Neue Worte in die Datenbank hinzufügen. Das Programm prüft dabei
automatisch, ob das Wort bereits in der Datenbank vorhanden ist,
um Dopplungen zu vermeiden.

Worte aus der Datenbank löschen.
"""

import sqlite3

con = sqlite3.connect("/Users/friday/Desktop/Data_Science_Institute/Python/Woche_11/Hangman/database.db")

con.row_factory = sqlite3.Row

cur = con.cursor()

while True:

    print("""
Hallo!
In diesem Programm kannst du dir einen Überblick über die
bereits vorhandenen Worte in der Datenbank verschaffen
oder der Datenbank neue hinzufügen.

Was möchtest du tun?

- Worte auslesen (a)
- Neue Worte hinzufügen (n)
- Ein Wort aus der Datenbank löschen (l)
- Beenden (e)

    """)
    user_choise = input("(a/n/l/e) ")
    
    if user_choise == "n":
        
        while True:
            word = input("Welches Wort möchtest du zur Datenbank hinzufügen? (oder 'b' um ins Hauptmenü zu gelangen): ").upper()
            
            if word == 'B':
                break
            
            letters = len(word)
            
            cur.execute("""
                        INSERT INTO words (word, letters)
                        SELECT ?, ?
                        WHERE NOT EXISTS (
                            SELECT 1 FROM words WHERE word = ? AND letters = ?
                            )
                        """, (word, letters, word, letters))
            
            con.commit()
            
    elif user_choise == "a":
        print("""
    Suchst du nach einem bestimmten Wort (w) oder 
    möchtest du eine Liste aller Worte mit einer 
    bestimmten Anzahl von Buchstaben (l)?
    Du kannst auch die gesamte Datenbank anzeigen lassen (g).
    
    """)    
         
        choise = input("(w/l/g) ") 
        
        if choise == "w":
            
            word = [input("Welches Wort suchst du? ").upper()]
            
            cur.execute("""
                        SELECT 
                        * 
                        FROM words
                        WHERE word = (?)
                        """, (word))
                        
            if len(tuple(cur.fetchall())) > 0:
                print(f"Das Wort {word} mit {len(word)} Buchstaben befindet sich nicht der Datenbank.")
            else:
                print(f"Das Wort {word} mit {len(word)} Buchstaben befindet sich in der Datenbank.")
            
        elif choise == "l":
            
            letters = [int(input("Wie viele Buchstaben sollen es sein? "))]
            
            wrd_lst = cur.execute("""
                        SELECT *
                        FROM words
                        WHERE letters = (?)
                        """, (letters))
            print(f"Die Worte mit {letters} Buchstaben in der Datenbank sind:")
            for word in cur.execute("SELECT * FROM words WHERE letters = (?)", (letters)):
                print(tuple(word))
        
        elif choise == "g":
            for word in cur.execute("SELECT * FROM words ORDER BY letters"):
                print(tuple(word))
    
    elif user_choise == "e":
        break
    
    elif user_choise == "l":
        
        word = [input("Welches Wort möchtest du löschen? ").upper()]
        
        try: 
            
            cur.execute("""
                    DELETE 
                    FROM words
                    WHERE word = (?)
                    """, (word))
            print(f"Das Wort {word} wurde aus der Datenbank gelöscht.")
        
        except:
            
            print(f"Das Wort {word} befindet sich nicht in der Datenbank.")
        
        finally:
            
            con.commit()
            
con.commit()

con.close()

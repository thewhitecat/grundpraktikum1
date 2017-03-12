# -*- coding: utf-8 -*-
"""
Created on Wed May 21 11:28:53 2015

@author: Schreiber
"""
import numpy as np

def csv_parser(text): 
    '''
    Diese Funktion bekommt einen String mit Komma-separierten Werten überbergeben.
    Dieser String wird in eine numpy.array aus floats umgewandelt.
    Beispiel: 
    <text> wird "1, .5, .2, 100.3" uebergeben
    array([1,.5,.2,100.3]) wird zurueckgegeben
    
    Die Werte koennen auch duch Semikolon getrennt sein.
    '''    
    #Ersetze alle Semikolons durch Kommas
    text=text.replace(';', ',')
    #Spalte die Zeichenkette bei Kommas auf 
    split_list=text.split(',') 
    #Wandle jeden Eintrag der Liste in ein float um
    feld=np.array(split_list, dtype=np.float)
    return feld                                             #gibt ein numpy.array zurueck

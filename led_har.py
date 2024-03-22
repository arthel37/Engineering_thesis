import RPi.GPIO as GPIO
import time
import datetime
import I2C_LCD_driver

#Ustawienie wyprowadzen GPIO

GPIO.setmode(GPIO.BCM) 												#Ustawienie trybu numerowania na zgodny z systemem Broadcom
GPIO.setwarnings(False) 											#Wylaczenie ostrzezen

GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(25,GPIO.OUT) 											#Wyprowadzenia 12, 13, 18, 25 ustawione na wyjscia
GPIO.setup(21,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24,GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 					#Wyprowadzenia 21, 23 i 24 na wejscia podciagniete w dol. Sluza one jako kolejno; przycisk zatwierdzajacy (21), przycisk przesuwajacy listy
																	#w gore (23) i przycisk przesuwajacy listy w dol (24).

GPIO.output(25, GPIO.HIGH) 											#Ustawienie wyprowadzenia 25 w stan wysoki, posluzy za linie zasilania diod

czerwony_led = GPIO.PWM(18, 50) 
zielony_led = GPIO.PWM(13, 50)
niebieski_led = GPIO.PWM(12, 50) 									#Przypisanie wyprowadzeniom 12, 13 i 18 funkcji modulowania szereokosci impulsu

#Ustawienie zmiennych globalnych

ekran = I2C_LCD_driver.lcd() 										#Przypisanie nazwy ekranowi LCD

zliczanie_czerwony = 0
zliczanie_zielony = 0 
zliczanie_niebieski = 0 											#Zmienne odpowiedzialne za kierunek zmiany wypelnienia w trybie RGB

zliczanie_oddychanie = 0 											#Zmienna odpowiedzialna za kierunek zmiany wypelnienia w trybie oddychania

narastanie_czerwony = 0
narastanie_zielony = 0
narastanie_niebieski = 0 											#Inicjalizacja zmiennych odpowiedzialnych za krok zmiany w trybie oddychania

wypelnienie_czerwony = 0
wypelnienie_zielony = 0
wypelnienie_niebieski = 0 											#Inicjalizacja zmiennych odpowiedzialnych za krok zmiany w trybie oddychania

indeks_koloru = 0 													#Zmienna przechowujaca indeks aktualnie wybranego koloru
kolor_info = 0 														#Zmienna kontrolujaca wyswietlenie informacji o wybraniu koloru

kolor_wybrany = 0
tryb_wybrany = 0 													#Zmienne przechowujaca informacje o wybraniu trybu i koloru na poczatku dzialania programu

tryb = 0 															#Inicjalizacja zmiennej przechowujacej informacje o wybranym trybie
tryb_info = 0 														#Zmienna kontrolujaca wyswietlenie informacji o wybraniu trybu

wyswietlanie = 0													#Zmienna kontrolujaca wyswietlany tekst w trakcie dzialania programu

jasnosc = 100														#Zmienna kontrolujaca procentowa wartosc jasnosci w odniesieniu do maksymalnej wartosci wypelnienia nadawanej przy inicjalizacji koloru
jasnosc_wyswietlana = jasnosc										#Zmienna odpowiedzialna za wyswietlana wartosc w czasie zmiany jasnosci
inicjalizacja_jasnosci = 0											#Zmienna przechowujaca informacje o nastepujacej zmianie jasnosci

Har = 0																#Zmienna przechowujace informacje o aktualnie wybranym harmonogramie

H1 = 0
H2 = 0
M1 = 0
M2 = 0

#Inicjalizacja diod

czerwony_led.start(0)
niebieski_led.start(0)
zielony_led.start(0)												


#Petla glowna programu

while 1:
	
	if Har != 0:
		akt_H = datetime.datetime.now().hour				
		akt_M = datetime.datetime.now().minute						#Funkcje modulu "datetime" pozwalajace wczytac z sieci kolejno aktualna godzine oraz minute 
		akt_S = datetime.datetime.now().second
		if (akt_H == H1 and akt_M == M1 and akt_S == 0) or (akt_H == H2 and akt_M == M2 and akt_S == 0):
			tryb = 3												#Jesli wybrany jest harmonogram 1, a godzina zgadza sie z jedna z zadanych por zmiany, uruchamiana jest inicjalizacja harmonogramu,
																	#aby zmienic nastawy sterownika
	
	while tryb_wybrany == 0:										#Petla wyboru trybu
		if tryb_info == 0:
			ekran.lcd_display_string("Wybierz tryb")				#Funkcja sterownika wyswietlacza pozwalajaca wyswietlic ciag znakow
			time.sleep(1)											#Funkcja modulu "time" pozwalajaca na wstrzymanie wykonywania programu przez zadany czas
			ekran.lcd_clear()										#Funkcja sterownika wyswietlacza pozwalajaca skasowac aktualnie wyswietlane znaki
			tryb_info = 1											#Te 3 funkcje pozwalaja przez 1 sekunde po uruchomieniu wyboru trybu wyswietlic napis "Wybierz tryb"
		if tryb == 0:
			ekran.lcd_display_string("RGB")
		if tryb == 1:
			ekran.lcd_display_string("Oddychanie")
		if tryb == 2:
			ekran.lcd_display_string("Statyczny")
		if tryb == 3:
			ekran.lcd_display_string("Harmonogram 1")
		if tryb == 4:
			ekran.lcd_display_string("Harmonogram 2")
		if GPIO.input(23) == GPIO.HIGH:								#Warunek sprawdzajacy, czy zostal wcisniety jeden z przyciskow
			tryb += 1
			time.sleep(1)
			if tryb > 4:
				tryb = 0
			ekran.lcd_clear()
			
		if GPIO.input(24) == GPIO.HIGH:
			tryb -= 1
			time.sleep(1)
			if tryb < 0:
				tryb = 4
			ekran.lcd_clear()
			
		if GPIO.input(21) == GPIO.HIGH:
			time.sleep(1)
			tryb_wybrany = 1
			
			if tryb != 3 and tryb != 4:
				inicjalizajca_koloru = 0
				kolor_wybrany = 0
			else:
				inicjalizajca_koloru = 1
				kolor_wybrany = 1
				
			if tryb == 3:
				Har = 1
			if tryb == 4:
				Har = 2
				tryb = 3
				
			inicjalizacja_rgb = 0
			inicjalizacja_oddychanie = 0
			inicjalizacja_statyczny = 0								#Zmienne kontrolujace inicjalizacje w roznych trybach
			ekran.lcd_clear()
	
	
	
	
	while kolor_wybrany == 0 and tryb != 0:							#Petla wyboru koloru; do kazdego indeksu przypisana jest nazwa i wartosc heksadecymalna danego koloru. 3 ostatnie przechowuja kolory zmienne
																	#dla uzytkownika, ktorych wartosci znajduja sie w zewnetrznych plikach tekstowych
		if kolor_info == 0:
			ekran.lcd_display_string("Wybierz kolor")
			time.sleep(1)
			ekran.lcd_clear()
			kolor_info = 1
		if indeks_koloru == 0:
			ekran.lcd_display_string("Czerwony")
			kolor = 'ff0000'
		if indeks_koloru == 1:
			ekran.lcd_display_string("Zielony")
			kolor = '00ff00'
		if indeks_koloru == 2:
			ekran.lcd_display_string("Niebieski")
			kolor = '0000ff'
		if indeks_koloru == 3:
			ekran.lcd_display_string("Zolty")
			kolor = 'ffff00'
		if indeks_koloru == 4:
			ekran.lcd_display_string("Turkusowy")
			kolor = '00ffff'
		if indeks_koloru == 5:
			ekran.lcd_display_string("Fioletowy")
			kolor = 'ff00ff'
		if indeks_koloru == 6:
			ekran.lcd_display_string("Bialy")
			kolor = 'ffffff'
		if indeks_koloru == 7:
			ekran.lcd_display_string("Kolor uzytk. 1")
			kolor = open('Kolor_uzytkownika_1.txt').readline()
		if indeks_koloru == 8:
			ekran.lcd_display_string("Kolor uzytk. 2")
			kolor = open('Kolor_uzytkownika_2.txt').readline()
		if indeks_koloru == 9:
			ekran.lcd_display_string("Kolor uzytk. 3")
			kolor = open('Kolor_uzytkownika_3.txt').readline() 
			
		if GPIO.input(23) == GPIO.HIGH:
			indeks_koloru += 1
			time.sleep(1)
			if indeks_koloru > 9:
				indeks_koloru= 0
			ekran.lcd_clear()
			
		if GPIO.input(24) == GPIO.HIGH:
			indeks_koloru -= 1
			time.sleep(1)
			if indeks_koloru < 0:
				indeks_koloru = 9
			ekran.lcd_clear()
			
		if GPIO.input(21) == GPIO.HIGH:
			time.sleep(1)
			kolor_wybrany = 1
			ekran.lcd_clear()
    
    
	if tryb == 0: 													#Przechodzące kolory RGB. Kazdy kolor otrzymuje konkretna wartosc wypelnienia przesunieta miedzy soba dokladnie o 30%, ktore nastepnie
																	#sa stopniowo zwiekszane az do osiagniecia wartosci maksymalnej, kiedy to zaczynaja sie zmniejszac az osiagna 0.
		if inicjalizacja_rgb == 0:
			wypelnienie_niebieski = 10
			wypelnienie_zielony = 40
			wypelnienie_czerwony = 70
			inicjalizacja_rgb = 1
			if inicjalizajca_koloru  == 0:
				czerwony_maks = 100
				niebieski_maks = 100
				zielony_maks = 100
				inicjalizajca_koloru = 1
		if zliczanie_czerwony == 0:									#Poniewaz kazdy kolor musi zmieniac sie niezaleznie, kierunek zmiany kazdego jest kontrolowany przez osobna zmienna. Ponadto zaimplementowano\
																	#warunki zabezpieczajce przed osiagnieciem przez program wypelnienia wiekszego niz 100, badz tez mniejszego od 0.
			wypelnienie_czerwony += czerwony_maks*5/100
			if wypelnienie_czerwony >= czerwony_maks:
				zliczanie_czerwony = 1
		if zliczanie_czerwony == 1:
			wypelnienie_czerwony -= czerwony_maks*5/100
			if wypelnienie_czerwony <= 0:
				zliczanie_czerwony = 0
		if zliczanie_niebieski == 0:
			wypelnienie_niebieski += niebieski_maks*5/100
			if wypelnienie_niebieski >= niebieski_maks:
				zliczanie_niebieski = 1
		if zliczanie_niebieski == 1:
			wypelnienie_niebieski -= niebieski_maks*5/100
			if wypelnienie_niebieski <= 0:
				zliczanie_niebieski = 0
		if zliczanie_zielony == 0:
			wypelnienie_zielony += zielony_maks*5/100
			if wypelnienie_zielony >= zielony_maks:
				zliczanie_zielony = 1
		if zliczanie_zielony == 1:
			wypelnienie_zielony -= zielony_maks*5/100
			if wypelnienie_zielony <= 0:
				zliczanie_zielony = 0
               
                
                
	if tryb == 1: 													#Oddychanie. Dzialanie zwiekszania i zmniejszania wypelnienia jest analogiczne jak w przypadku trybu RGB, z ta roznica, ze tryb oddychania
																	#operuje bez przerwy w jednym kolorze, to znaczy ich wypelnienie zwieksza i zmniejsza sie z krokiem stosunkowo rownym.
		
		if inicjalizacja_oddychanie == 0:
			if inicjalizajca_koloru == 0:							#Inicjalizacja koloru dziala poprzez rozlozenie ciagu znakow w zmiennej kolor na 3 rozne zmienne, kazda zawierajaca po dwa znaki, pierwsze 
																	#dwa odpowiadaja za maksymalne wypelnienie koloru czerwonego, drugie zielonego i trzecie niebieskiego. Nastepnie wartosci te zostaja
																	#przeksztalcone na liczby calkowite wyrazajace procent wypelnienia sygnalu PWM poprzez zamienienie ich na liczby dziesietne i ustalenie 
																	#jaka czesc maksymalnej wartosi (255, czyli ff heksadecymalnie) stanowia
				niebieski_maks = int(int(kolor[4:6], base=16)*100/255)
				zielony_maks = int(int(kolor[2:4], base=16)*100/255)
				czerwony_maks = int(int(kolor[0:2], base=16)*100/255)
				inicjalizajca_koloru = 1
			if czerwony_maks == 0 and niebieski_maks != 0:			#W przypadku kiedy kolor nie zawiera barwy czerwonej, konieczne jest uzaleznienie tempa zmiany wypelnienia od pozostalych
				narastanie_niebieski = niebieski_maks/50
				narastanie_zielony = narastanie_niebieski*zielony_maks/niebieski_maks
			elif czerwony_maks == 0 and niebieski_maks == 0:		#Analogicznie jak wyzej w przypadk gdy kolor zawiera jedynie barwe zielona
				narastanie_zielony = zielony_maks/50
			else:													#W przypadku kiedy kolor zawiera wszystkie 3 barwy, krok narastania zostaje uzalezniony od jednej z nich i ustosunkowany w pozostalych
				narastanie_czerwony = czerwony_maks/50
				narastanie_niebieski = narastanie_czerwony*niebieski_maks/czerwony_maks
				narastanie_zielony = narastanie_czerwony*zielony_maks/czerwony_maks
			inicjalizacja_oddychanie = 1
		
		if zliczanie_oddychanie == 0:
			wypelnienie_czerwony += narastanie_czerwony
			wypelnienie_niebieski += narastanie_niebieski
			wypelnienie_zielony += narastanie_zielony
			if wypelnienie_zielony >= zielony_maks and wypelnienie_niebieski >= niebieski_maks and wypelnienie_czerwony >= czerwony_maks:
				zliczanie_oddychanie = 1							#Poniewaz wartosc wypelnienia nie moze przekroczyc 100%, zaimplementowano warunek zabezpieczajacy
				wypelnienie_zielony = zielony_maks
				wypelnienie_niebieski = niebieski_maks
				wypelnienie_czerwony = czerwony_maks
                
		if zliczanie_oddychanie == 1:
			wypelnienie_czerwony -= narastanie_czerwony
			wypelnienie_niebieski -= narastanie_niebieski
			wypelnienie_zielony -= narastanie_zielony
			if wypelnienie_zielony <= 0 and wypelnienie_niebieski <= 0 and wypelnienie_czerwony <= 0:
				zliczanie_oddychanie = 0							#Poniewaz wartosc wypelnienia nie moze byc mniejsza niz 0, zaimplementowano warunek zabezpieczajacy
				wypelnienie_zielony = 0
				wypelnienie_niebieski = 0
				wypelnienie_czerwony = 0
		
	if tryb == 2:													#Statyczny
		if inicjalizacja_statyczny == 0:
			if inicjalizajca_koloru == 0:
				niebieski_maks = int(int(kolor[4:6], base=16)*100/255)
				zielony_maks = int(int(kolor[2:4], base=16)*100/255)
				czerwony_maks = int(int(kolor[0:2], base=16)*100/255)
				inicjalizajca_koloru = 1
			wypelnienie_niebieski = niebieski_maks
			wypelnienie_zielony = zielony_maks
			wypelnienie_czerwony = czerwony_maks
			inicjalizacja_statyczny = 1
		pass
	
	if tryb == 3:
		
		if Har == 1:
			Cz_Przel_1 = open('Har_1_Cz_Przel_1.txt', 'r+')				#Program otwiera plik i odczytuje z niego kolejne zmienne zapisane w odpowiednim formacie dla obu czasow przelaczenia
			Cz_Przel_2 = open('Har_1_Cz_Przel_2.txt', 'r+')
		elif Har == 2:
			Cz_Przel_1 = open('Har_2_Cz_Przel_1.txt', 'r+')
			Cz_Przel_2 = open('Har_2_Cz_Przel_2.txt', 'r+')
			
		H1 = int(Cz_Przel_1.readline())
		M1 = int(Cz_Przel_1.readline())
		tryb1 = int(Cz_Przel_1.readline())
		kolor1 = Cz_Przel_1.readline()
		jasnosc1 = int(Cz_Przel_1.readline())
		
		
		H2 = int(Cz_Przel_2.readline())
		M2 = int(Cz_Przel_2.readline())
		tryb2 = int(Cz_Przel_2.readline())
		kolor2 = Cz_Przel_2.readline()
		jasnosc2 = int(Cz_Przel_2.readline())		
		
		akt_H = datetime.datetime.now().hour
		akt_M = datetime.datetime.now().minute
		
		if H2 > H1:
			if (akt_H > H1 and akt_H < H2) or (akt_H == H1 and akt_M >= M1) or (akt_H == H2 and akt_M < M2):
				tryb = tryb1
				kolor = kolor1
				jasnosc = jasnosc1
			else:
				tryb = tryb2
				kolor = kolor2
				jasnosc = jasnosc2
		elif H1 > H2:
			if (akt_H > H2 and akt_H < H1) or (akt_H == H2 and akt_M >= M2) or (akt_H == H1 and akt_M < M1):
				tryb = tryb2
				kolor = kolor2
				jasnosc = jasnosc2
			else:
				tryb = tryb1
				kolor = kolor1
				jasnosc = jasnosc1
		elif H1 == H2:
			if M2 > M1:
				if akt_H == H1 and akt_M >= M1 and akt_M < M2:
					tryb = tryb1
					kolor = kolor1
					jasnosc = jasnosc1
				else:
					tryb = tryb2
					kolor = kolor2
					jasnosc = jasnosc2
			elif M1 > M2:
				if akt_H == H2 and akt_M >= M2 and akt_M < M1:
					tryb = tryb2
					kolor = kolor2
					jasnosc = jasnosc2
				else:
					tryb = tryb1
					kolor = kolor1
					jasnosc = jasnosc1
	
		inicjalizacja_oddychanie = 0
		inicjalizacja_rgb = 0
		inicjalizacja_statyczny = 0
		
		if tryb == 0:
			czerwony_maks = jasnosc
			zielony_maks = jasnosc
			niebieski_maks = jasnosc
			
		if tryb == 1 or tryb ==2:
			czerwony_maks = int(int(kolor[0:2], base=16)*100/255)*jasnosc/100
			zielony_maks = int(int(kolor[2:4], base=16)*100/255)*jasnosc/100
			niebieski_maks = int(int(kolor[4:6], base=16)*100/255)*jasnosc/100
		
		
	while inicjalizacja_jasnosci == 1:								#Zmiana jasnosci odbywa sie poprzez zmiane maksymalnej wartosci wypelnienia jaka moga w kazdym trybie osiagnac sygnalu dla kazdego z kolorow
																	#rownomiernie
		ekran.lcd_display_string("Zmien jasnosc", 1)
		ekran.lcd_display_string(str(jasnosc_wyswietlana)+"%", 2)
		if GPIO.input(23) == GPIO.HIGH:
			time.sleep(0.5)
			jasnosc_wyswietlana += 5
			if jasnosc_wyswietlana > 100:
				jasnosc_wyswietlana = 100
			ekran.lcd_clear()
		if GPIO.input(24) == GPIO.HIGH:
			time.sleep(0.5)
			jasnosc_wyswietlana -= 5
			if jasnosc_wyswietlana < 0:
				jasnosc_wyswietlana = 0
			ekran.lcd_clear()
		if GPIO.input(21) == GPIO.HIGH:
			time.sleep(1)
			jasnosc = jasnosc_wyswietlana
			if tryb == 0:
				czerwony_maks = jasnosc
				zielony_maks = jasnosc
				niebieski_maks = jasnosc
			if tryb == 1 or tryb ==2:
				czerwony_maks = int(int(kolor[0:2], base=16)*100/255)*jasnosc/100
				zielony_maks = int(int(kolor[2:4], base=16)*100/255)*jasnosc/100
				niebieski_maks = int(int(kolor[4:6], base=16)*100/255)*jasnosc/100
			inicjalizajca_rgb = 0
			inicjalizacja_statyczny = 0
			inicjalizacja_oddychanie = 0
			inicjalizacja_jasnosci = 0
			ekran.lcd_clear()
			
		
	if wyswietlanie == 0:											#Aby umozliwic obsluge programu przy pomocy wyswietlacza i przyciskow, zaimplementowano szereg procedur, ktore umozliwiaja wybor konkretnych
																	#elementow, ktore uzytkownik mialby zmienic w formie przesuwanej listy
		ekran.lcd_display_string("Zmien tryb")
		if GPIO.input(21) == GPIO.HIGH:
			
			time.sleep(1)
			
			tryb_wybrany = 0
			tryb_info = 0
			
			inicjalizacja_rgb = 0
			inicjalizacja_oddychanie = 0
			inicjalizacja_statyczny = 0
			
			wypelnienie_czerwony = 0
			wypelnienie_niebieski = 0
			wypelnienie_zielony = 0
			
			niebieski_maks = 0
			czerwony_maks = 0
			zielony_maks = 0
			
			ekran.lcd_clear()
			
	if wyswietlanie == 1 and tryb != 0:
		ekran.lcd_display_string("Zmien kolor")
		if GPIO.input(21) == GPIO.HIGH:
			
			time.sleep(1)
			
			kolor_wybrany = 0
			kolor_info = 0
			
			inicjalizacja_oddychanie = 0
			inicjalizacja_statyczny = 0
			inicjalizacja_rgb = 0
			
			wypelnienie_czerwony = 0
			wypelnienie_niebieski = 0
			wypelnienie_zielony = 0
			
			niebieski_maks = 0
			czerwony_maks = 0
			zielony_maks = 0
			
			ekran.lcd_clear()
			
	if wyswietlanie == 1 and tryb == 0:
		ekran.lcd_display_string("Zmiana koloru", 1)
		ekran.lcd_display_string("niedostepna", 2)
		
	if wyswietlanie == 2:
		ekran.lcd_display_string("Zmien jasnosc")
		if GPIO.input(21) == GPIO.HIGH:
			time.sleep(1)
			inicjalizacja_jasnosci = 1
			ekran.lcd_clear()
			
	if wyswietlanie == 3:
		ekran.lcd_display_string("Wylacz program")
		if GPIO.input(21) == GPIO.HIGH:
			czerwony_led.stop
			niebieski_led.stop
			zielony_led.stop
			ekran.lcd_clear()
			break
			
	if GPIO.input(23) == GPIO.HIGH:
		time.sleep(1)
		wyswietlanie += 1
		if wyswietlanie > 3:
			wyswietlanie = 0
		ekran.lcd_clear()
	if GPIO.input(24) == GPIO.HIGH:
		time.sleep(1)
		wyswietlanie -= 1
		if wyswietlanie < 0:
			wyswietlanie = 3
		ekran.lcd_clear()
    
	mowa = open('speech.txt', 'r').readline()
    
	if mowa.__contains__('change'):
		if mowa.__contains__('color') and tryb != 0:
			if mowa.__contains__('red'):
				kolor = 'ff0000'
			if mowa.__contains__('green'):
				kolor = '00ff00'
			if mowa.__contains__('blue'):
				kolor = '0000ff'
			if mowa.__contains__('yellow'):
				kolor = 'ffff00'
			if mowa.__contains__('cyan'):
				kolor = '00ffff'
			if mowa.__contains__('purple'):
				kolor = 'ff00ff'
			if mowa.__contains__('white'):
				kolor = 'ffffff'
			if mowa.__contains__('user') and (mowa.__contains__('one') or mowa.__contains__('1')):
				kolor = open('Kolor_uzytkownika_1.txt').readline()
			if mowa.__contains__('user') and (mowa.__contains__('two') or mowa.__contains__('2')):
				kolor = open('Kolor_uzytkownika_2.txt').readline()
			if mowa.__contains__('user') and (mowa.__contains__('three') or mowa.__contains__('3')):
				kolor = open('Kolor_uzytkownika_3.txt').readline()
			inicjalizacja_oddychanie = 0
			inicjalizacja_statyczny = 0
			inicjalizajca_koloru = 0
			
			wypelnienie_czerwony = 0
			wypelnienie_niebieski = 0
			wypelnienie_zielony = 0
			
			niebieski_maks = 0
			czerwony_maks = 0
			zielony_maks = 0
			
			narastanie_czerwony = 0
			narastanie_niebieski = 0
			narastanie_zielony = 0
			time.sleep(1)
		if mowa.__contains__('mode'):
			if mowa.__contains__('RGB'):
				tryb = 0
			if mowa.__contains__('breathing'):
				tryb = 1
				kolor = '0000ff'
			if mowa.__contains__('static'):
				tryb = 2
				kolor = '0000ff'
			if mowa.__contains__('schedule') and (mowa.__contains__('one') or mowa.__contains__('1')):
				Har = 1
				tryb = 3
			if mowa.__contains__('schedule') and (mowa.__contains__('two') or mowa.__contains__('2')):
				Har = 2
				tryb = 3
			inicjalizacja_rgb = 0
			inicjalizacja_oddychanie = 0
			inicjalizacja_statyczny = 0
			inicjalizajca_koloru = 0
			
			wypelnienie_czerwony = 0
			wypelnienie_niebieski = 0
			wypelnienie_zielony = 0
			
			niebieski_maks = 0
			czerwony_maks = 0
			zielony_maks = 0
			time.sleep(1)
		if mowa.__contains__('brightness'):
			if mowa.__contains__('lower'):
				jasnosc -= 20
				if jasnosc < 0:
					jasnosc = 0
			if mowa.__contains__('higher'):
				jasnosc += 20
				if jasnosc > 100:
					jasnosc = 100
			if tryb == 0:
				czerwony_maks = jasnosc
				zielony_maks = jasnosc
				niebieski_maks = jasnosc
			if tryb == 1 or tryb ==2:
				czerwony_maks = int(int(kolor[0:2], base=16)*100/255)*jasnosc/100
				zielony_maks = int(int(kolor[2:4], base=16)*100/255)*jasnosc/100
				niebieski_maks = int(int(kolor[4:6], base=16)*100/255)*jasnosc/100
			inicjalizajca_rgb = 0
			inicjalizacja_statyczny = 0
			inicjalizacja_oddychanie = 0
			inicjalizajca_koloru = 1
			time.sleep(1)
    
	czerwony_led.ChangeDutyCycle(wypelnienie_czerwony)
	niebieski_led.ChangeDutyCycle(wypelnienie_niebieski)
	zielony_led.ChangeDutyCycle(wypelnienie_zielony)				#Nastawienie wypelnienia, czyli w praktyce strumienia swietlnego kazdej z diod

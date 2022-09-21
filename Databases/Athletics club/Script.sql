/*
Created: 28.11.2021
Modified: 08.12.2021
Project: Klub_Lekkoatletyczny
Model: Klub_Lekkoatletyczny_logiczny
Author: Kacper Nowakowski, Lena Zubik
Database: Oracle 12c Release 2
*/


-- Create sequences section -------------------------------------------------

CREATE SEQUENCE KlubSeq1
 INCREMENT BY 1
 START WITH 1
 NOMAXVALUE
 NOMINVALUE
 CACHE 20
/

CREATE SEQUENCE WlascicielSeq1
 INCREMENT BY 1
 START WITH 1
 NOMAXVALUE
 NOMINVALUE
 CACHE 20
/

CREATE SEQUENCE TreningSeq1
 INCREMENT BY 1
 START WITH 1
 NOMAXVALUE
 NOMINVALUE
 CACHE 20
/

CREATE SEQUENCE RealizacjaSeq1
 INCREMENT BY 1
 START WITH 1
 NOMAXVALUE
 NOMINVALUE
 CACHE 20
/

CREATE SEQUENCE KlubowiczSeq1
 INCREMENT BY 1
 START WITH 1
 NOMAXVALUE
 NOMINVALUE
 CACHE 20
/

CREATE SEQUENCE PracownikSeq1
 INCREMENT BY 1
 START WITH 1
 NOMAXVALUE
 NOMINVALUE
 CACHE 20
/

CREATE SEQUENCE AdresSeq1
 INCREMENT BY 1
 START WITH 1
 NOMAXVALUE
 NOMINVALUE
 CACHE 20
/

CREATE SEQUENCE SprzetSeq1
 INCREMENT BY 1
 START WITH 1
 NOMAXVALUE
 NOMINVALUE
 CACHE 20
/

CREATE SEQUENCE LicencjaSeq1
 INCREMENT BY 1
 START WITH 1
 NOMAXVALUE
 NOMINVALUE
 CACHE 20
/

CREATE SEQUENCE Miejsce_treningowSeq1
 INCREMENT BY 1
 START WITH 1
 NOMAXVALUE
 NOMINVALUE
 CACHE 20
/

CREATE SEQUENCE DyscyplinaSeq1
 INCREMENT BY 1
 START WITH 1
 NOMAXVALUE
 NOMINVALUE
 CACHE 20
/

CREATE SEQUENCE OsiagniecieSeq1
 INCREMENT BY 1
 START WITH 1
 NOMAXVALUE
 NOMINVALUE
 CACHE 20
/

CREATE SEQUENCE ZawodySeq1
 INCREMENT BY 1
 START WITH 1
 NOMAXVALUE
 NOMINVALUE
 CACHE 20
/

-- Create tables section -------------------------------------------------

-- Table Kluby

CREATE TABLE Kluby(
  ID_klubu Integer NOT NULL,
  Nazwa Varchar2(35 ) NOT NULL,
  Data_zalozenia Date NOT NULL,
  ID_adresu Integer NOT NULL
)
/

-- Create indexes for table Kluby

CREATE INDEX IX_Klub_ma_adres ON Kluby (ID_adresu)
/

-- Add keys for table Kluby

ALTER TABLE Kluby ADD CONSTRAINT KlubPK PRIMARY KEY (ID_klubu)
/

-- Table Pracownicy

CREATE TABLE Pracownicy(
  ID_pracownika Integer NOT NULL,
  Imie Varchar2(20 ) NOT NULL,
  Nazwisko Varchar2(30 ) NOT NULL,
  Data_urodzenia Date NOT NULL,
  PESEL Char(11 ) NOT NULL,
  Plec Char(1 ) NOT NULL
        CHECK (Plec IN ('K', 'M')),
  Stanowisko Varchar2(25 ) NOT NULL
        CHECK (Stanowisko IN ('administrator', 'księgowy', 'fizjoterapeuta', 'medyk')),
  Data_zatrudnienia Date NOT NULL,
  Termin_umowy Date,
  Nr_konta Char(26 ) NOT NULL,
  Email Varchar2(50 ),
  Telefon Varchar2(12 ),
  ID_klubu Integer NOT NULL,
  ID_adresu Integer NOT NULL
)
/

-- Create indexes for table Pracownicy

CREATE INDEX IX_Zatrudnia_pracownika ON Pracownicy (ID_klubu)
/

CREATE INDEX IX_Pracownik_mieszka ON Pracownicy (ID_adresu)
/

-- Add keys for table Pracownicy

ALTER TABLE Pracownicy ADD CONSTRAINT PracownikPK PRIMARY KEY (ID_pracownika)
/

-- Table Klubowicze

CREATE TABLE Klubowicze(
  ID_klubowicza Integer NOT NULL,
  Imie Varchar2(20 ) NOT NULL,
  Nazwisko Varchar2(30 ) NOT NULL,
  Data_urodzenia Date NOT NULL,
  PESEL Char(11 ) NOT NULL,
  Plec Char(1 ) NOT NULL
        CHECK (Plec IN ('K', 'M')),
  Nr_konta Char(26 ) NOT NULL,
  Email Varchar2(50 ),
  Telefon Varchar2(12 ),
  Data_dolaczenia Date NOT NULL,
  Data_Waznosci_czlonkostwa Date NOT NULL,
  ID_adresu Integer NOT NULL
)
/

-- Create indexes for table Klubowicze

CREATE INDEX IX_Klubowicz_mieszka ON Klubowicze (ID_adresu)
/

-- Add keys for table Klubowicze

ALTER TABLE Klubowicze ADD CONSTRAINT KlubowiczPK PRIMARY KEY (ID_klubowicza)
/

-- Table Sprzet

CREATE TABLE Sprzet(
  ID_sprzetu Integer NOT NULL,
  Nazwa_sprzetu Varchar2(20 ) NOT NULL,
  Ilosc Integer NOT NULL,
  Opis Varchar2(400 ),
  ID_klubu Integer NOT NULL
)
/

-- Create indexes for table Sprzet

CREATE INDEX IX_Skladuje ON Sprzet (ID_klubu)
/

-- Add keys for table Sprzet

ALTER TABLE Sprzet ADD CONSTRAINT SprzetPK PRIMARY KEY (ID_sprzetu)
/

-- Table Miejsca_treningow

CREATE TABLE Miejsca_treningow(
  ID_miejsca_treningu Integer NOT NULL,
  Nazwa_miejsca Varchar2(30 ) NOT NULL,
  Max_liczba_trenujacych Integer NOT NULL,
  Opis Varchar2(400 ),
  ID_klubu Integer NOT NULL
)
/

-- Create indexes for table Miejsca_treningow

CREATE INDEX IX_Wykorzystuje ON Miejsca_treningow (ID_klubu)
/

-- Add keys for table Miejsca_treningow

ALTER TABLE Miejsca_treningow ADD CONSTRAINT Miejsce_treninguPK PRIMARY KEY (ID_miejsca_treningu)
/

-- Table Treningi

CREATE TABLE Treningi(
  ID_treningu Integer NOT NULL,
  Nazwa Varchar2(30 ) NOT NULL,
  Wiek_min Integer,
  Wiek_max Integer,
  Opis Varchar2(400 ),
  ID_klubu Integer NOT NULL
)
/

-- Create indexes for table Treningi

CREATE INDEX IX_Oferuje ON Treningi (ID_klubu)
/

-- Add keys for table Treningi

ALTER TABLE Treningi ADD CONSTRAINT TreningPK PRIMARY KEY (ID_treningu)
/

-- Table and Columns comments section

COMMENT ON COLUMN Treningi.Nazwa IS 'Nazwa treningu.'
/

-- Table Sesje_treningowe

CREATE TABLE Sesje_treningowe(
  ID_klubowicza Integer NOT NULL,
  ID_realizacji Integer NOT NULL
)
/

-- Table Trener_Realizacja

CREATE TABLE Trener_Realizacja(
  ID_realizacji Integer NOT NULL,
  ID_pracownika Integer NOT NULL
)
/

-- Table Miejsca_treningu_Realizacje

CREATE TABLE Miejsca_treningu_Realizacje(
  ID_miejsca_treningu Integer NOT NULL,
  Liczba_wymaganych_miejsc Integer NOT NULL,
  ID_realizacji Integer NOT NULL
)
/

-- Table and Columns comments section

COMMENT ON COLUMN Miejsca_treningu_Realizacje.Liczba_wymaganych_miejsc IS 'Liczba wymaganych miejsc dla danego terningu.'
/

-- Table Sprzety_Realizacje

CREATE TABLE Sprzety_Realizacje(
  ID_sprzetu Integer NOT NULL,
  ID_realizacji Integer NOT NULL,
  Liczba_wymaganego_sprzetu Integer NOT NULL
)
/

-- Table and Columns comments section

COMMENT ON COLUMN Sprzety_Realizacje.Liczba_wymaganego_sprzetu IS 'Liczba wymaganego sprzętu.'
/

-- Table Wlasciciele

CREATE TABLE Wlasciciele(
  ID_wlasciciela Integer NOT NULL,
  Imie Varchar2(20 ) NOT NULL,
  Nazwisko Varchar2(30 ) NOT NULL,
  ID_klubu Integer NOT NULL
)
/

-- Create indexes for table Wlasciciele

CREATE INDEX IX_Wlasciciel_zarzadza ON Wlasciciele (ID_klubu)
/

-- Add keys for table Wlasciciele

ALTER TABLE Wlasciciele ADD CONSTRAINT PK_Wlasciciele PRIMARY KEY (ID_wlasciciela)
/

-- Table and Columns comments section

COMMENT ON TABLE Wlasciciele IS 'Encja właścicela.'
/
COMMENT ON COLUMN Wlasciciele.ID_wlasciciela IS 'Unikatowy identyfikator właściciela.'
/
COMMENT ON COLUMN Wlasciciele.Imie IS 'Imię właściciela.'
/
COMMENT ON COLUMN Wlasciciele.Nazwisko IS 'Nazwisko właściciela.'
/

-- Table Adresy

CREATE TABLE Adresy(
  ID_adresu Integer NOT NULL,
  Kraj Varchar2(30 ) NOT NULL,
  Miasto Varchar2(30 ) NOT NULL,
  Ulica Varchar2(30 ) NOT NULL,
  Nr_lokalu Varchar2(4 ) NOT NULL,
  Kod_pocztowy Char(6 ) NOT NULL
)
/

-- Add keys for table Adresy

ALTER TABLE Adresy ADD CONSTRAINT PK_Adresy PRIMARY KEY (ID_adresu)
/

-- Table and Columns comments section

COMMENT ON TABLE Adresy IS 'Encja adres.'
/
COMMENT ON COLUMN Adresy.ID_adresu IS 'Unikatowy idnetyfikator adresu.'
/
COMMENT ON COLUMN Adresy.Kraj IS 'Kraj zamieszkania.'
/
COMMENT ON COLUMN Adresy.Miasto IS 'Miato w adresie.'
/
COMMENT ON COLUMN Adresy.Ulica IS 'Ulica adresu.'
/
COMMENT ON COLUMN Adresy.Nr_lokalu IS 'Numer lokalu z adresu.'
/
COMMENT ON COLUMN Adresy.Kod_pocztowy IS 'Kod pocztowy adresu.'
/

-- Table Realizacje

CREATE TABLE Realizacje(
  ID_realizacji Integer NOT NULL,
  Cena Number(10,2) NOT NULL,
  Data_rozpoczecia Date NOT NULL,
  Data_zakonczenia Date NOT NULL,
  Max_liczba_trenujacych Integer NOT NULL,
  Aktualna_liczba_zapisanych Integer NOT NULL,
  ID_treningu Integer NOT NULL
)
/

-- Create indexes for table Realizacje

CREATE INDEX IX_Jest_Realizacja ON Realizacje (ID_treningu)
/

-- Add keys for table Realizacje

ALTER TABLE Realizacje ADD CONSTRAINT PK_Realizacje PRIMARY KEY (ID_realizacji)
/

-- Table and Columns comments section

COMMENT ON TABLE Realizacje IS 'Encja realizacji treningu.'
/
COMMENT ON COLUMN Realizacje.ID_realizacji IS 'Unikatowy identyfikator realizacji treningu.'
/
COMMENT ON COLUMN Realizacje.Cena IS 'Cena za osobę danej realizacji.'
/
COMMENT ON COLUMN Realizacje.Data_rozpoczecia IS 'Data rozpoczęcia realizacji danego treningu.
'
/
COMMENT ON COLUMN Realizacje.Data_zakonczenia IS 'Data zakończenia realizacji danego treningu.'
/
COMMENT ON COLUMN Realizacje.Max_liczba_trenujacych IS 'Maksymalna liczba trenujących.'
/
COMMENT ON COLUMN Realizacje.Aktualna_liczba_zapisanych IS 'Aktualna liczba zapisanych uczestników danej realizacji.'
/

-- Table Licencje

CREATE TABLE Licencje(
  ID_licencji Integer NOT NULL,
  Nr_licencji Varchar2(12 ) NOT NULL,
  Data_wydania Date NOT NULL,
  Data_waznosci Date NOT NULL,
  Organ_wystawiajacy Varchar2(30 ) NOT NULL,
  Miasto_wydania Varchar2(30 ) NOT NULL,
  ID_pracownika Integer,
  ID_klubowicza Integer
)
/

-- Create indexes for table Licencje

CREATE INDEX IX_Trener_posiada_licencje ON Licencje (ID_pracownika)
/

CREATE INDEX IX_Klubowicz_ma_licencje ON Licencje (ID_klubowicza)
/

-- Add keys for table Licencje

ALTER TABLE Licencje ADD CONSTRAINT PK_Licencje PRIMARY KEY (ID_licencji)
/

-- Table and Columns comments section

COMMENT ON TABLE Licencje IS 'Encja licencji.'
/
COMMENT ON COLUMN Licencje.ID_licencji IS 'Unikatowy identyfikator licencji.'
/
COMMENT ON COLUMN Licencje.Nr_licencji IS 'Numer licencji.'
/
COMMENT ON COLUMN Licencje.Data_wydania IS 'Data wydania.'
/
COMMENT ON COLUMN Licencje.Data_waznosci IS 'Data ważności.'
/
COMMENT ON COLUMN Licencje.Organ_wystawiajacy IS 'Organ wystawiający licencji.'
/
COMMENT ON COLUMN Licencje.Miasto_wydania IS 'Miasto wydania licencji.'
/

-- Table Dyscypliny

CREATE TABLE Dyscypliny(
  ID_dyscypliny Integer NOT NULL,
  Nazwa_dyscypliny Varchar2(30 ) NOT NULL,
  Opis Varchar2(400 )
)
/

-- Add keys for table Dyscypliny

ALTER TABLE Dyscypliny ADD CONSTRAINT PK_Dyscypliny PRIMARY KEY (ID_dyscypliny)
/

ALTER TABLE Dyscypliny ADD CONSTRAINT Nazwa_dyscypliny UNIQUE (Nazwa_dyscypliny)
/

-- Table and Columns comments section

COMMENT ON TABLE Dyscypliny IS 'Encja dyscypliny.'
/
COMMENT ON COLUMN Dyscypliny.ID_dyscypliny IS 'Unikatowy identyfikator dyscypliny.'
/
COMMENT ON COLUMN Dyscypliny.Nazwa_dyscypliny IS 'Nazwa dyscypliny.'
/

-- Table Osiagniecia

CREATE TABLE Osiagniecia(
  ID_osiagniecia Integer NOT NULL,
  Data_zdobycia Date NOT NULL,
  Zdobyte_miejsce Integer,
  Kraj Varchar2(30 ) NOT NULL,
  Miasto Varchar2(30 ) NOT NULL,
  ID_dyscypliny Integer NOT NULL,
  ID_zawodow Integer NOT NULL
)
/

-- Create indexes for table Osiagniecia

CREATE INDEX IX_Osiagniecie_Dyscypliny ON Osiagniecia (ID_dyscypliny)
/

CREATE INDEX IX_Osiagniecie_Zawody ON Osiagniecia (ID_zawodow)
/

-- Add keys for table Osiagniecia

ALTER TABLE Osiagniecia ADD CONSTRAINT PK_Osiagniecia PRIMARY KEY (ID_osiagniecia)
/

-- Table and Columns comments section

COMMENT ON TABLE Osiagniecia IS 'Encja osiągnięcia.'
/
COMMENT ON COLUMN Osiagniecia.ID_osiagniecia IS 'Uniktowy identyfikator osiągnięcia.'
/
COMMENT ON COLUMN Osiagniecia.Data_zdobycia IS 'Data zdobycia osiągnięcia.'
/
COMMENT ON COLUMN Osiagniecia.Zdobyte_miejsce IS 'Zdobyte miejsce danego osiągnięcia.'
/
COMMENT ON COLUMN Osiagniecia.Kraj IS 'Krak, w którym zdobyto osiągnięcie.'
/
COMMENT ON COLUMN Osiagniecia.Miasto IS 'Miasto, w którym zdobyto osiągnięcie.'
/

-- Table Trenerzy_Osiagniecia

CREATE TABLE Trenerzy_Osiagniecia(
  ID_osiagniecia Integer NOT NULL,
  ID_pracownika Integer NOT NULL
)
/

-- Add keys for table Trenerzy_Osiagniecia

ALTER TABLE Trenerzy_Osiagniecia ADD CONSTRAINT PK_Trenerzy_Osiagniecia PRIMARY KEY (ID_osiagniecia,ID_pracownika)
/

-- Table Klubowicze_osiagniecia

CREATE TABLE Klubowicze_osiagniecia(
  ID_klubowicza Integer NOT NULL,
  ID_osiagniecia Integer NOT NULL
)
/

-- Add keys for table Klubowicze_osiagniecia

ALTER TABLE Klubowicze_osiagniecia ADD CONSTRAINT PK_Klubowicze_osiagniecia PRIMARY KEY (ID_klubowicza,ID_osiagniecia)
/

-- Table Zawody

CREATE TABLE Zawody(
  ID_zawodow Integer NOT NULL,
  Nazwa_zawodow Varchar2(30 ) NOT NULL,
  Opis Varchar2(400 )
)
/

-- Add keys for table Zawody

ALTER TABLE Zawody ADD CONSTRAINT PK_Zawody PRIMARY KEY (ID_zawodow)
/

ALTER TABLE Zawody ADD CONSTRAINT Nazwa_zawodow UNIQUE (Nazwa_zawodow)
/

-- Table and Columns comments section

COMMENT ON TABLE Zawody IS 'Encja zwodów.'
/
COMMENT ON COLUMN Zawody.ID_zawodow IS 'Unikatowy identyfikator zawodów.'
/

-- Table Trenerzy

CREATE TABLE Trenerzy(
  ID_pracownika Integer NOT NULL,
  Specjalizacja Varchar2(25 ) NOT NULL
        CHECK (Specjalizacja IN ('techniczny', 'wytrzymałościowy', 'coach'))
)
/

-- Add keys for table Trenerzy

ALTER TABLE Trenerzy ADD CONSTRAINT PK_Trenerzy PRIMARY KEY (ID_pracownika)
/

-- Table and Columns comments section

COMMENT ON TABLE Trenerzy IS 'Encja trener.'
/
COMMENT ON COLUMN Trenerzy.Specjalizacja IS 'Specjalizacja trenera.'
/

-- Trigger for sequence KlubSeq1 for column ID_klubu in table Kluby ---------
CREATE OR REPLACE TRIGGER ts_Kluby_KlubSeq1 BEFORE INSERT
ON Kluby FOR EACH ROW
BEGIN
  :new.ID_klubu := KlubSeq1.nextval;
END;
/
CREATE OR REPLACE TRIGGER tsu_Kluby_KlubSeq1 AFTER UPDATE OF ID_klubu
ON Kluby FOR EACH ROW
BEGIN
  RAISE_APPLICATION_ERROR(-20010,'Cannot update column ID_klubu in table Kluby as it uses sequence.');
END;
/

-- Trigger for sequence PracownikSeq1 for column ID_pracownika in table Pracownicy ---------
CREATE OR REPLACE TRIGGER ts_Pracownicy_PracownikSeq1 BEFORE INSERT
ON Pracownicy FOR EACH ROW
BEGIN
  :new.ID_pracownika := PracownikSeq1.nextval;
END;
/
CREATE OR REPLACE TRIGGER tsu_Pracownicy_PracownikSeq1 AFTER UPDATE OF ID_pracownika
ON Pracownicy FOR EACH ROW
BEGIN
  RAISE_APPLICATION_ERROR(-20010,'Cannot update column ID_pracownika in table Pracownicy as it uses sequence.');
END;
/

-- Trigger for sequence KlubowiczSeq1 for column ID_klubowicza in table Klubowicze ---------
CREATE OR REPLACE TRIGGER ts_Klubowicze_KlubowiczSeq1 BEFORE INSERT
ON Klubowicze FOR EACH ROW
BEGIN
  :new.ID_klubowicza := KlubowiczSeq1.nextval;
END;
/
CREATE OR REPLACE TRIGGER tsu_Klubowicze_KlubowiczSeq1 AFTER UPDATE OF ID_klubowicza
ON Klubowicze FOR EACH ROW
BEGIN
  RAISE_APPLICATION_ERROR(-20010,'Cannot update column ID_klubowicza in table Klubowicze as it uses sequence.');
END;
/

-- Trigger for sequence SprzetSeq1 for column ID_sprzetu in table Sprzet ---------
CREATE OR REPLACE TRIGGER ts_Sprzet_SprzetSeq1 BEFORE INSERT
ON Sprzet FOR EACH ROW
BEGIN
  :new.ID_sprzetu := SprzetSeq1.nextval;
END;
/
CREATE OR REPLACE TRIGGER tsu_Sprzet_SprzetSeq1 AFTER UPDATE OF ID_sprzetu
ON Sprzet FOR EACH ROW
BEGIN
  RAISE_APPLICATION_ERROR(-20010,'Cannot update column ID_sprzetu in table Sprzet as it uses sequence.');
END;
/

-- Trigger for sequence Miejsce_treningowSeq1 for column ID_miejsca_treningu in table Miejsca_treningow ---------
CREATE OR REPLACE TRIGGER ts_Miejsca_treningow_Miejsce_treningowSeq1 BEFORE INSERT
ON Miejsca_treningow FOR EACH ROW
BEGIN
  :new.ID_miejsca_treningu := Miejsce_treningowSeq1.nextval;
END;
/
CREATE OR REPLACE TRIGGER tsu_Miejsca_treningow_Miejsce_treningowSeq1 AFTER UPDATE OF ID_miejsca_treningu
ON Miejsca_treningow FOR EACH ROW
BEGIN
  RAISE_APPLICATION_ERROR(-20010,'Cannot update column ID_miejsca_treningu in table Miejsca_treningow as it uses sequence.');
END;
/

-- Trigger for sequence TreningSeq1 for column ID_treningu in table Treningi ---------
CREATE OR REPLACE TRIGGER ts_Treningi_TreningSeq1 BEFORE INSERT
ON Treningi FOR EACH ROW
BEGIN
  :new.ID_treningu := TreningSeq1.nextval;
END;
/
CREATE OR REPLACE TRIGGER tsu_Treningi_TreningSeq1 AFTER UPDATE OF ID_treningu
ON Treningi FOR EACH ROW
BEGIN
  RAISE_APPLICATION_ERROR(-20010,'Cannot update column ID_treningu in table Treningi as it uses sequence.');
END;
/

-- Trigger for sequence WlascicielSeq1 for column ID_wlasciciela in table Wlasciciele ---------
CREATE OR REPLACE TRIGGER ts_Wlasciciele_WlascicielSeq1 BEFORE INSERT
ON Wlasciciele FOR EACH ROW
BEGIN
  :new.ID_wlasciciela := WlascicielSeq1.nextval;
END;
/
CREATE OR REPLACE TRIGGER tsu_Wlasciciele_WlascicielSeq1 AFTER UPDATE OF ID_wlasciciela
ON Wlasciciele FOR EACH ROW
BEGIN
  RAISE_APPLICATION_ERROR(-20010,'Cannot update column ID_wlasciciela in table Wlasciciele as it uses sequence.');
END;
/

-- Trigger for sequence AdresSeq1 for column ID_adresu in table Adresy ---------
CREATE OR REPLACE TRIGGER ts_Adresy_AdresSeq1 BEFORE INSERT
ON Adresy FOR EACH ROW
BEGIN
  :new.ID_adresu := AdresSeq1.nextval;
END;
/
CREATE OR REPLACE TRIGGER tsu_Adresy_AdresSeq1 AFTER UPDATE OF ID_adresu
ON Adresy FOR EACH ROW
BEGIN
  RAISE_APPLICATION_ERROR(-20010,'Cannot update column ID_adresu in table Adresy as it uses sequence.');
END;
/

-- Trigger for sequence RealizacjaSeq1 for column ID_realizacji in table Realizacje ---------
CREATE OR REPLACE TRIGGER ts_Realizacje_RealizacjaSeq1 BEFORE INSERT
ON Realizacje FOR EACH ROW
BEGIN
  :new.ID_realizacji := RealizacjaSeq1.nextval;
END;
/
CREATE OR REPLACE TRIGGER tsu_Realizacje_RealizacjaSeq1 AFTER UPDATE OF ID_realizacji
ON Realizacje FOR EACH ROW
BEGIN
  RAISE_APPLICATION_ERROR(-20010,'Cannot update column ID_realizacji in table Realizacje as it uses sequence.');
END;
/

-- Trigger for sequence LicencjaSeq1 for column ID_licencji in table Licencje ---------
CREATE OR REPLACE TRIGGER ts_Licencje_LicencjaSeq1 BEFORE INSERT
ON Licencje FOR EACH ROW
BEGIN
  :new.ID_licencji := LicencjaSeq1.nextval;
END;
/
CREATE OR REPLACE TRIGGER tsu_Licencje_LicencjaSeq1 AFTER UPDATE OF ID_licencji
ON Licencje FOR EACH ROW
BEGIN
  RAISE_APPLICATION_ERROR(-20010,'Cannot update column ID_licencji in table Licencje as it uses sequence.');
END;
/

-- Trigger for sequence DyscyplinaSeq1 for column ID_dyscypliny in table Dyscypliny ---------
CREATE OR REPLACE TRIGGER ts_Dyscypliny_DyscyplinaSeq1 BEFORE INSERT
ON Dyscypliny FOR EACH ROW
BEGIN
  :new.ID_dyscypliny := DyscyplinaSeq1.nextval;
END;
/
CREATE OR REPLACE TRIGGER tsu_Dyscypliny_DyscyplinaSeq1 AFTER UPDATE OF ID_dyscypliny
ON Dyscypliny FOR EACH ROW
BEGIN
  RAISE_APPLICATION_ERROR(-20010,'Cannot update column ID_dyscypliny in table Dyscypliny as it uses sequence.');
END;
/

-- Trigger for sequence OsiagniecieSeq1 for column ID_osiagniecia in table Osiagniecia ---------
CREATE OR REPLACE TRIGGER ts_Osiagniecia_OsiagniecieSeq1 BEFORE INSERT
ON Osiagniecia FOR EACH ROW
BEGIN
  :new.ID_osiagniecia := OsiagniecieSeq1.nextval;
END;
/
CREATE OR REPLACE TRIGGER tsu_Osiagniecia_OsiagniecieSeq1 AFTER UPDATE OF ID_osiagniecia
ON Osiagniecia FOR EACH ROW
BEGIN
  RAISE_APPLICATION_ERROR(-20010,'Cannot update column ID_osiagniecia in table Osiagniecia as it uses sequence.');
END;
/

-- Trigger for sequence ZawodySeq1 for column ID_zawodow in table Zawody ---------
CREATE OR REPLACE TRIGGER ts_Zawody_ZawodySeq1 BEFORE INSERT
ON Zawody FOR EACH ROW
BEGIN
  :new.ID_zawodow := ZawodySeq1.nextval;
END;
/
CREATE OR REPLACE TRIGGER tsu_Zawody_ZawodySeq1 AFTER UPDATE OF ID_zawodow
ON Zawody FOR EACH ROW
BEGIN
  RAISE_APPLICATION_ERROR(-20010,'Cannot update column ID_zawodow in table Zawody as it uses sequence.');
END;
/


-- Create foreign keys (relationships) section ------------------------------------------------- 

ALTER TABLE Pracownicy ADD CONSTRAINT Zatrudnia_Pracownika FOREIGN KEY (ID_klubu) REFERENCES Kluby (ID_klubu)
/



ALTER TABLE Sprzet ADD CONSTRAINT Skladuje FOREIGN KEY (ID_klubu) REFERENCES Kluby (ID_klubu)
/



ALTER TABLE Miejsca_treningow ADD CONSTRAINT Wykorzystuje FOREIGN KEY (ID_klubu) REFERENCES Kluby (ID_klubu)
/



ALTER TABLE Treningi ADD CONSTRAINT Oferuje FOREIGN KEY (ID_klubu) REFERENCES Kluby (ID_klubu)
/



ALTER TABLE Kluby ADD CONSTRAINT Klub_ma_adres FOREIGN KEY (ID_adresu) REFERENCES Adresy (ID_adresu)
/



ALTER TABLE Realizacje ADD CONSTRAINT Trening_ma FOREIGN KEY (ID_treningu) REFERENCES Treningi (ID_treningu)
/



ALTER TABLE Sesje_treningowe ADD CONSTRAINT Na_Realizacje_zapisuje_sie FOREIGN KEY (ID_realizacji) REFERENCES Realizacje (ID_realizacji)
/



ALTER TABLE Trener_Realizacja ADD CONSTRAINT Realizacja_wymaga_Trenera FOREIGN KEY (ID_realizacji) REFERENCES Realizacje (ID_realizacji)
/



ALTER TABLE Sprzety_Realizacje ADD CONSTRAINT Realizacja_potrzebuje FOREIGN KEY (ID_realizacji) REFERENCES Realizacje (ID_realizacji)
/



ALTER TABLE Klubowicze_osiagniecia ADD CONSTRAINT Klubowicz_zdobyl FOREIGN KEY (ID_klubowicza) REFERENCES Klubowicze (ID_klubowicza)
/



ALTER TABLE Trenerzy_Osiagniecia ADD CONSTRAINT Osiagniecie_Trener FOREIGN KEY (ID_osiagniecia) REFERENCES Osiagniecia (ID_osiagniecia)
/



ALTER TABLE Klubowicze_osiagniecia ADD CONSTRAINT Osiagniecie_Klubowicz FOREIGN KEY (ID_osiagniecia) REFERENCES Osiagniecia (ID_osiagniecia)
/



ALTER TABLE Osiagniecia ADD CONSTRAINT Osiagniecie_Dyscypliny FOREIGN KEY (ID_dyscypliny) REFERENCES Dyscypliny (ID_dyscypliny)
/



ALTER TABLE Osiagniecia ADD CONSTRAINT Osiagniecie_Zawody FOREIGN KEY (ID_zawodow) REFERENCES Zawody (ID_zawodow)
/



ALTER TABLE Wlasciciele ADD CONSTRAINT Wlasciciel_zarzadza FOREIGN KEY (ID_klubu) REFERENCES Kluby (ID_klubu)
/



ALTER TABLE Pracownicy ADD CONSTRAINT Pracownik_mieszka FOREIGN KEY (ID_adresu) REFERENCES Adresy (ID_adresu)
/



ALTER TABLE Klubowicze ADD CONSTRAINT Klubowicz_mieszka FOREIGN KEY (ID_adresu) REFERENCES Adresy (ID_adresu)
/



ALTER TABLE Trenerzy ADD CONSTRAINT Pracownik_trener FOREIGN KEY (ID_pracownika) REFERENCES Pracownicy (ID_pracownika)
/



ALTER TABLE Trenerzy_Osiagniecia ADD CONSTRAINT Trener_zdobyl FOREIGN KEY (ID_pracownika) REFERENCES Trenerzy (ID_pracownika)
/



ALTER TABLE Trener_Realizacja ADD CONSTRAINT Trener_realizuje FOREIGN KEY (ID_pracownika) REFERENCES Trenerzy (ID_pracownika)
/



ALTER TABLE Licencje ADD CONSTRAINT Trener_posiada_licencje FOREIGN KEY (ID_pracownika) REFERENCES Trenerzy (ID_pracownika)
/



ALTER TABLE Licencje ADD CONSTRAINT Klubowicz_ma_licencje FOREIGN KEY (ID_klubowicza) REFERENCES Klubowicze (ID_klubowicza)
/



ALTER TABLE Miejsca_treningu_Realizacje ADD CONSTRAINT Realizacja_ma_miejsce FOREIGN KEY (ID_realizacji) REFERENCES Realizacje (ID_realizacji)
/






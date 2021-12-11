# Fischertechnik - MQTT - Web Application

Dieses Projekt entstand während einer Studienarbeit der [DHBW Stuttgart Campus Horb](https://www.dhbw-stuttgart.de/horb/home/) im Studiengang Informatik.
Bearbeiter: Nico Riedlinger

Im Rahmen dieser Arbeit sollen die bestehende Struktur des IoT-Protokolls [MQTT](https://mqtt.org/) von der [9V Modellfabrik](https://www.fischertechnik.de/de-de/produkte/simulieren/simulationsmodelle/536629-sim-fabrik-simulation-9v-simulation) der Firma fischertechnik und die darauf ablaufenden Prozesse angepasst und optimiert werden.

## Verzeichnisstruktur

### ControllableFactory/deps

Von fischertechnik bereitgestellte Bibliotheken und Header Dateien zur Entwicklung von Software für den TXT-Controller in C++.

### ControllableFactory/FactoryLib

Enthalten ist eine Implementierung der Highlevel und Lowlevel API für den TXT-Controller.
<br>
Autor => [Joel Schmid](https://github.com/SchmidJoel/FischertechnikTXTApi)

### ControllableFactory/websiteFactory

C/C++ - Programme für die Modellfabrik. Angepasst für die Verwendung mit der E-Commerce Webseite.
<br>
Ursprünglicher Autor: [Moris Kotsch](https://github.com/KotschM/FischertechnikMQTTWebApplication)

### dhbwFischertechnik

Django-Projekt für die E-Commerce Webseite.
<br>
Ursprünglicher Autor: [Moris Kotsch](https://github.com/KotschM/FischertechnikMQTTWebApplication)

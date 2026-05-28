# Reflektionen
## Entwicklung einer App mit Streamlit

### Aufbau & Vorbereitungen
Ein Storyboard für die App zu gestalten hat uns dabei geholfen, die Planung 
übersichtlich und realistisch zu halten. So konnten wir früh erkennen, welche Funktionen umsetzbar sind und wie die Navigation zwischen den Seiten aussehen soll. 
Einige anfängliche Ideen hätte man nicht gut umsetzen können, was wir in der 
begleiteten Übungsstunde dann herausgefunden und entsprechend angepasst haben — dieser Schritt hat uns viel Zeit gespart, da wir Probleme früh erkannt haben.

Das erste Konzept unserer App haben wir mit mehreren Nutzerinnen getestet und nützliches Feedback erhalten. Besonders hilfreich war das Feedback zur 
Übersichtlichkeit der einzelnen Seiten, und in der jetzigen App-Version konnten diese Ideen miteinbezogen werden. Nach den ersten Planungen haben wir jedoch auch gemerkt, dass man sich schnell in vielen Ideen verlieren kann. Uns hat es daher sehr geholfen, Prioritäten zu setzen und anschliessend auf den Grundfunktionen aufzubauen — konkret haben wir zuerst den Kalender und die Phasenberechnung umgesetzt, bevor wir weitere Seiten hinzugefügt haben.
Eine Persona zu entwickeln hat uns geholfen, Designentscheidungen wie das minimalistische Farbkonzept zu begründen. Andererseits war die Zielgruppe von Anfang an klar, weshalb es aufgrund des persönlichen Zusammenhangs nicht unbedingt nötig gewesen wäre, eine Persona zu erstellen.

### Technische Herausforderungen
Dass wir durch den vorherigen Leistungsnachweis bereits gelernt haben, wie man App-Daten dauerhaft speichert, empfanden wir als sehr hilfreich, da wir uns so stärker auf das Coden und das Design der App konzentrieren konnten. Allerdings haben wir im Nachhinein festgestellt, dass das Speichern von Daten in CSV-Dateien im GitHub-Repository problematisch ist, da dieses öffentlich zugänglich ist und somit keine geeignete Lösung für sensible, nutzerspezifische Daten darstellt.
Der Leistungsnachweis hat uns insgesamt sehr viel Freiheit in der Entwicklung gelassen, was einerseits toll war, um eigene Designs und Funktionen auszuprobieren — andererseits war es zum Teil schwierig zu wissen, ob der gewählte Ansatz den Anforderungen entspricht.

Das Debuggen war manchmal aufwendiger als erwartet, besonders bei Fehlern, die erst auf Streamlit Cloud auftraten und lokal nicht reproduzierbar waren. 
Fehlermeldungen wie der ModuleNotFoundError haben uns dabei gezeigt, wie wichtig eine saubere Projektstruktur ist: Pakete müssen in einer requirements.txt gepflegt werden und Importpfade müssen in einer Multipage-App explizit gesetzt werden. Eine der grössten Herausforderungen war die seitenübergreifende Synchronisation der Phasen, die wir schliesslich durch eine zentrale cycle_utils.py-Datei gelöst haben, welche von allen Seiten importiert wird und die aktuelle Phase anhand der gespeicherten Daten berechnet.

### Was wir über Python & Streamlit gelernt haben
Durch dieses Projekt haben wir gelernt, wie man eine Multipage-App in Streamlit strukturiert und dabei gemeinsame Logik in separate Hilfsdateien auslagert. Mit plotly konnten wir ausserdem interaktive Diagramme erstellen, die den Symptomverlauf über Zeit und im Phasenvergleich visualisieren — eine 
Funktionalität, die wir durch das Projekt besser kennengelernt haben. Durch die Streamlit API Reference konnten wir viele Design-Elemente gezielt einsetzen, und es war hilfreich zu wissen, wo man für solche Informationen nachschauen kann. 
Darüber hinaus haben wir gelernt, wie man Daten mit pandas in Dateien 
speichert, lädt und seitenübergreifend nutzt — ein Grundprinzip, das für viele zukünftige Projekte relevant sein wird.

### Was wir beim nächsten Mal anders machen würden
Rückblickend würden wir von Anfang an auf den DataManager zurückgreifen, anstatt Daten in CSV-Dateien im GitHub-Repository zu speichern. Da das Repository öffentlich zugänglich ist, eignen sich CSV-Dateien nicht für sensible oder nutzerspezifische Daten — eine strukturierte Speicherlösung wie SwitchDrive wäre hier die richtige Wahl gewesen.
Ausserdem würden wir früher über Benutzerkonten nachdenken, damit die App von mehreren Personen gleichzeitig genutzt werden kann, ohne dass sich die Daten gegenseitig überschreiben. Mit den gewonnenen Erfahrungen würden wir ein nächstes Projekt noch strukturierter und gezielter angehen — insgesamt hat die Entwicklung jedoch gut funktioniert und wir sind zufrieden mit dem Ergebnis.
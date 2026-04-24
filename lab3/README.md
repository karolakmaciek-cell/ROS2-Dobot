# Lab 3

## Opis zadania
1. Sprzężenie wizualizacji w środowisku RViz z fizycznym manipulatorem Dobot Magician.
2. Implementacja węzła konwertującego stany złączy odbierane z tematu /dobot_joint_states na format /joint_states wymagany przez model URDF.
3. Wyznaczenie kąta dla dodatkowego złącza na podstawie pozostałych zmiennych w celu zapewnienia pionowej orientacji narzędzia rzeczywistego robota.
4. Zapewnienie pełnej zgodności konfiguracji kinematycznej modelu wizualizowanego w RViz z konfiguracją rzeczywistego manipulatora.
5. Wykorzystanie węzła kinematyki prostej ForwardKin do wizualizacji aktualnej pozycji końcówki wyliczonej na podstawie zmiennych złączowych fizycznego urządzenia.

## Instrukcja uruchomienia
1. source /opt/ros/jazzy/setup.bash
2. export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
3. mkdir ~/anro_ws/src
4. cd ~/anro_ws/src
5. git clone https://gitlab-stud.elka.pw.edu.pl/mwilecze/anro_2026l .
6. cd ..
7. colcon build --packages-select lab3_homework
8. source install/setup.bash
9. ros2 launch lab3_homework lab3_homework.launch.py

Repozytorium zostało zainicjalizowane paczką urdf_tutorial i to na jej podstawie powstała reszta paczki.
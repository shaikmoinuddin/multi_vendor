from datetime import time

for h in range(0, 24):
    for m in range(0, 30):
        print(time(h, m).strftime('%I:%M %p'))
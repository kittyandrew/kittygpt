## KittyGPT - Minimalist version of AutoGPT
Core kittygpt package code is currently under 100 LoC! Take a look for yourself.
Keep in mind, this does not count [extras](./extras), which contains some additional commands.

### Examples
All examples below are provided running `example.py`.

##### Example with `continuous = False` in the `example.py`.
```bash
# User input
Goal: how much free disk space does the system have? what is system ip and uptime?
# Agent log
Command is about to be executed: {'name': 'execute_bash', 'args': {'command': 'df -h; hostname -I; uptime'}}
# Mandatory user confirmation
Press anything once to continue...
# Agent log
Command is about to be executed: {'name': 'execute_bash', 'args': {'command': 'hostname -i'}}
# Mandatory user confirmation
Press anything once to continue...
# Agent output
The system has 377.8G of free disk space, the IP address is 172.17.0.2, and the uptime is 4 days, 13 hours, and 31 minutes.
```

##### Examples with `continuous = True` in the `example.py`.
```bash
# User input
Goal: what is KF51
# Agent output.
Command is about to be executed: {'name': 'wiki_search', 'args': {'query': 'KF51'}}
KF51 refers to the Panther KF51, a German main battle tank that is currently under development by Rheinmetall Landsysteme.
```

```bash
# User input
Goal: who are our austronauts and where do they currently stay?
# Agent log
Command is about to be executed: {'name': 'get_astronauts', 'args': {}}
Command is about to be executed: {'name': 'get_coords_iss', 'args': {}}
# Agent output.
The current astronauts are Sergey Prokopyev, Dmitry Petelin, Frank Rubio, Jing Haiping, Gui Haichow, Zhu Yangzhu, Jasmin Moghbeli, Andreas Mogensen, Satoshi Furukawa, Konstantin Borisov, Oleg Kononenko, Nikolai Chub, and Loral O'Hara. Most of them are on the International Space Station (ISS), which is currently located at longitude 111.5709 and latitude 25.0298. Jing Haiping, Gui Haichow, and Zhu Yangzhu are on the Tiangong, but I am unable to provide the exact location of this craft.
```

```bash
# User input
Goal: Write a paragraph describing following topic: what is spaceX, how many austronauts do we currently have in space and who are they, where are they.
# Agent log
Command is about to be executed: {'name': 'get_astronauts', 'args': {}}
Command is about to be executed: {'name': 'get_coords_iss', 'args': {}}
Command is about to be executed: {'name': 'wiki_search', 'args': {'query': 'SpaceX'}}
# Agent output
Space Exploration Technologies Corp., commonly referred to as SpaceX, is an American spacecraft manufacturer, launch service provider, and defense contractor. Currently, there are 13 astronauts in space. They are Sergey Prokopyev, Dmitry Petelin, Frank Rubio, Jing Haiping, Gui Haichow, Zhu Yangzhu, Jasmin Moghbeli, Andreas Mogensen, Satoshi Furukawa, Konstantin Borisov, Oleg Kononenko, Nikolai Chub, and Loral O'Hara. Most of them are on the International Space Station (ISS), which is currently located at latitude -13.5397 and longitude 82.1498.
```


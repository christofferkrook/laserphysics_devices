# Arduino UNO
A small repo for controlling an Arduino UNO from Python.

## Setup
### Upload Firmata to Arduino UNO
- Download and install the Arduino IDE [here](https://www.arduino.cc/en/software).
- Connect the Arduino to the computer
- In the Arduino IDE, select your Arduino board under "Tools"
- Upload the ```File -> Examples -> Firmata -> Standard Firmata``` sketch. You may need to download the ```Firmata``` package.

### Clone repo and setup environment
- Clone the repository in your preferred way. For example in the command line:
    ```bash
    git clone https://github.com/adrianvagberg/Arduino-UNO.git
    cd Arduino-UNO
   ```
- Create a virtual environment and install dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # For macOS/Linux
    # or
    venv\Scripts\activate     # For Windows
    pip install -r requirements.txt
   ```
- Alternatively, install pyfirmata2 directly and write your own code using:
   ```bash
  pip install pyfirmata2 [--user] [--upgrade]
   ```
  
## Documentation
You can find information on how to use the pyFirmata2 package [here](https://github.com/berndporr/pyFirmata2/blob/master/README.md).
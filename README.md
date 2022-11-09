# artnet2crap
Python script to convert four Art-Net universes into the CRAP protocol for Mate-Light

## Usage

artnet2crap does not have any parameters so far. The IP address of the Mate-Light is hard-coded in `crap_client.py`. Run the process with:

```
python -m artnet2crap.server_main
```

Your light control software of choice (e.g. QLC+) needs to be setup to send the pixel values in four DMX universes (0 – 3). Configure the Art-Net output to Unicast and enter the IP address of the host that `artnet2crap` is running on.
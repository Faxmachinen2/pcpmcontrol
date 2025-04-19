# PCPanel Mini Control

A simple unofficial Python script that maps the PCPanel Mini input dials and buttons to commands.

For a more sophisticated piece of software with an actual UI, check out [nvdweem's PCPanel](https://github.com/nvdweem/PCPanel).

## Getting started

This setup has been designed for `Ubuntu`-based systems and has only been tested on `Pop!_OS 22.04`. PCPanel Mini Control could work on other OSes, but the steps and scripts to set it up will probably be different.

1. Check out this repository:
   ```bash
   git clone https://github.com/Faxmachinen2/pcpmcontrol.git
   cd pcpmcontrol
   ```
1. Make a venv and and install python packages:
   ```bash
   ./setup.bash
   ```
1. Add a udev rule to grant access to the device:
   ```bash
   sudo ./setup-su.bash
   ```
1. Run the PCPanel Mini Control:
   ```bash
   ./run.bash
   ```

If successful, you should see `Connected to device` in the output.

You might also see some errors, because the default configuration expects certain commands to be available (`amixer`, the `audacious` flatpak, and `pactl`).

## Configuration

Change the configuration by editing the `config.yml` file.
The program will automatically detect when the file is changed and reload it.

### Input events

For the PCPanel Mini, there are four press events (one for each knob that can be pressed),
and four turn events (one for each knob that can be turned).
The knobs are numbered 0-3 from left to right.
Substitute `X` with the knob number below.

If you want an event to do nothing, leave it empty (but don't remove it).

* `events.press.X`: Specify a command to run when knob X is pressed.
* `events.turn.X`: Specify a command to run when knob X is turned.
  * See below for pasing the knob value as an argument.

##### Send knob value

You can send the knob value to the commands you specify in `events.turn.X` by including the string `{val[N]}`,
where `N` is the maximum value (the minimum is 0).

The value is a whole number caculated from the native value of the PCPanel Mini knob, which is in the range 0-255.

An advanced format also exists, `{val[N,M]:f}`, that produces a decimal value between N and M.
You can further format this with Python formatting syntax, e.g. `{val[-1.5,1.5]:.2f}` produces numbers with two decimals between -1.50 and 1.50.

##### Example

Call `amixer` to set the master volume when you turn the first knob. The rest of the knobs do nothing:

```yaml
events:
  turn:
    0: 'amixer -q set Master {val[100]}%'
    1: 
    2: 
    3: 
```

When you turn the knob to 25%, `amixer` will be called with the arguments `-q set Master 25%`.
Of course, `amixer` can also take the value as an unsigned short (0-65535), which offers a bit more resolution:

```yaml
    0: 'amixer -q set Master {val[65535]}'
```

This then calls `amixer` with the arguments `-q set Master 16384`.

### Colors

You can change the colors of the LED lighting on your PCPanel Mini.
Colors are specified as an array of three values, representing the red, green and blue components.
Each value must be in the range 0-255.

* `colors.idle`: The color on your PCPanel when it's idle.
* `colors.press`: The color shown on the knob when you press it.
* `colors.min`: The color when you turn a knob all the way down.
* `colors.max`: The color when you turn a knob all the way up.

##### Example

Set the idle color to orange (100% red, 50% green, 0% blue):

```yaml
colors:
  idle: [255, 128, 0]
```

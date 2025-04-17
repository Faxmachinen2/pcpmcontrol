# PCPanel Mini Control

A simple Python script that maps the PCPanel Mini input dials and buttons to commands.

## Getting started

1. Make sure you have Python:
   ```bash
   python3 --version
   ```
1. Check out this repository:
   ```bash
   git clone https://github.com/Faxmachinen2/pcpmcontrol.git
   cd pcpmcontrol
   ```
1. Make a venv and and install python packages:
   ```bash
   ./setup.bash
   ```
1. Run the PCPanel Mini Control:
   ```bash
   ./run.bash
   ```

## Configuration

Change the configuration by editing the `config.yml` file.
The program will automatically detect when the file is changed and reload it.

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

### Events

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
where `N` is the maximum value (the minimum is always 0).

The value is caculated from the native value of the PCPanel Mini knob, which is in the range 0-255.

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

import asyncio
import hid
import yaml
from pathlib import Path

class ValueFormatter:
	def __init__(self, unit):
		self._unit = unit
	def __getitem__(self, param):
		if type(param) is int:
			return round(param * self._unit)
		else:
			minvalue, maxvalue = map(float, param.split(','))
			return minvalue + (maxvalue - minvalue) * self._unit

class Config:
	def __init__(self, config_path):
		self._path = Path(config_path)
		self._data = None
		self._timestamp = 0
		if not self.reload():
			raise Exception("Bad config")
	def reload(self):
		time = self._path.stat().st_mtime
		if time == self._timestamp:
			return False
		self._timestamp = time
		try:
			with open(self._path, 'r') as fh:
				self._data = yaml.safe_load(fh)
				return True
		except Exception as ex:
			print(ex)
			return False
	def __getitem__(self, key):
		return self._data[key]

async def press_event(index, config):
	command = config['events']['press'][index]
	if command:
		print(command)
		await asyncio.create_subprocess_shell(command)

async def turn_event(index, value, config):
	template = config['events']['turn'][index]
	if template:
		val = ValueFormatter(value / 255)
		command = template.format(val=val)
		print(command)
		await asyncio.create_subprocess_shell(command)

async def write_all_colors(device, color):
	assert len(color) == 3
	output_data = [6, 4, 5] + color + [0]*58
	device.write(bytes(output_data))

async def write_one_color(device, index, color, color2=None):
	assert len(color) == 3
	if color2 is not None:
		assert len(color2) == 3
		output_data = [6, 2] + [0] * 7 * index + [2] + color + color2 + [0] * (55 - 7 * index)
	else:
		output_data = [6, 2] + [0] * 7 * index + [1] + color + [0] * (58 - 7 * index)
	device.write(bytes(output_data))

async def read_values(device, event, states, config):
	while True:
		data = await asyncio.to_thread(device.read, 64)
		if data and data[0] in [1, 2]:
			states[(data[0]-1)*4 + data[1]] = data[2]
			event.set()

async def process(device, event, states, config):
	last_seen = [0] * 8
	diffs = [False] * 8
	idle_countdown = 0
	await write_all_colors(device, config['colors']['idle'])
	while True:
		await event.wait()
		pressed = -1
		turned = -1
		for i in range(0, 4):
			if states[i] != last_seen[i]:
				turned = i
				break
		for i in range(4, 8):
			if states[i] != last_seen[i]:
				pressed = i - 4
				break
		if pressed != -1 or turned != -1:
			print(states)
			last_seen = states.copy()
			idle_countdown = 10
			if pressed != -1:
				await write_one_color(device, pressed, config['colors']['press'])
				if (states[pressed+4] == 1):
					await press_event(pressed, config)
			elif turned != -1:
				await write_one_color(device, turned, config['colors']['min'], config['colors']['max'])
				await turn_event(turned, states[turned], config)
		elif idle_countdown > 0:
			idle_countdown -= 1
			if idle_countdown == 0:
				await write_all_colors(device, config['colors']['idle'])
				event.clear()
		await asyncio.sleep(0.1)

async def update_config(config):
	while True:
		await asyncio.sleep(2)
		if config.reload():
			print("Config reloaded")

async def operate(device, config):
	states = [0] * 8
	event = asyncio.Event()
	await asyncio.gather(
		read_values(device, event, states, config),
		process(device, event, states, config),
		update_config(config)
	)

async def main():
	config = Config('config.yml')
	while True:
		try:
			with hid.Device(0x0483, 0xa3c4) as device:
				print("Connected to device")
				await operate(device, config)
		except hid.HIDException as ex:
			print(ex)
		await asyncio.sleep(3)


if __name__ == '__main__':
	asyncio.run(main())

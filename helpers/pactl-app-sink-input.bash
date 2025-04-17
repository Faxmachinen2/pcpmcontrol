#!/bin/bash

command="$1"
player="$2"
value="$3"
playerSinkIndex="$(pactl list sink-inputs |  awk '/application.name |object.serial / {print $0};' | grep -iA 1 "$player" | awk '/object.serial/ {print $3}' |  sed 's/"//g' )"
[[ $playerSinkIndex ]] && pactl $command $playerSinkIndex $value

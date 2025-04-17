#!/bin/bash

command="$1"
player="$2"
value="$3"
playerSourceIndex="$(pactl list source-outputs |  awk '/application.name |object.serial / {print $0};' | grep -iA 1 "$player" | awk '/object.serial/ {print $3}' |  sed 's/"//g' )"
[[ $playerSourceIndex ]] && pactl $command $playerSourceIndex $value

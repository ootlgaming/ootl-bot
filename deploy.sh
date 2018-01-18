#!/bin/bash
sudo rsync -av ./ /opt/ootl-bot
sudo systemctl restart ootl-bot.service

"В данной папке мы обрабатываем все команды которые пишуться через /"

from aiogram import Router

commands_router = Router()

import commands.start
import commands.actions


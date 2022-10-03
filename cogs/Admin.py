# -*- coding: utf-8 -*-
import logging

import disnake
from disnake.ext import commands

from bot.bot import Bot


class Admin(commands.Cog):
    def __init__(self, bot):
        """Initialize the cog"""
        self.bot: Bot = bot

    @commands.slash_command(
        name="logs",
        description="Voir les logs du bot",
        default_member_permissions=disnake.Permissions.all(),
        dm_permission=True,
    )
    async def logs(
        self,
        inter: disnake.UserCommandInteraction,
        level: str = commands.Param(
            description="Le level des logs à obtenir.", choices=["debug", "info"], default="info"
        ),
        previous: int = commands.Param(description="Le nombre de fichier en arrière à obtenir", ge=1, le=5, default=1),
    ):
        await inter.response.defer(ephemeral=True)
        if previous == 1:
            file = disnake.File(f"logs/{level}.log")
            await inter.author.send(file=file)
        else:
            files = [disnake.File(f"logs/{level}.log")]
            for i in range(1, previous):
                try:
                    files.append(disnake.File(f"logs/{level}.log.{i}"))
                except FileNotFoundError:
                    logging.debug(f"logsCmd: file 'logs/{level}.log.{i}' skipped because not found")
            await inter.author.send(files=files)
        await inter.edit_original_message(embed=disnake.Embed(description="Logs sent on private !"))


def setup(bot: commands.InteractionBot):
    bot.add_cog(Admin(bot))

# -*- coding: utf-8 -*-
from typing import List

import disnake
from disnake.ext import commands

from bot.bot import Bot


class VoteType:
    POUR = 1
    CONTRE = -1
    ABSTENTION = 0


class Vote:
    def __init__(self, user: disnake.User, type: VoteType) -> None:
        self.user = user
        self.type = type

    def __int__(self) -> int:
        return self.type


class VoteView(disnake.ui.modal):
    def __init__(self):
        self.votes: List[Vote] = []

    def eval(self, type) -> int:
        i: int = 0
        for vote in self.votes:
            if int(vote) == type:
                i += 1
        return i

    @property
    def pour(self) -> int:
        return self.eval(VoteType.POUR)

    @property
    def contre(self) -> int:
        return self.eval(VoteType.CONTRE)

    @property
    def abstention(self) -> int:
        return self.eval(VoteType.ABSTENTION)

    @property
    def embed(self) -> disnake.Embed:
        return disnake.Embed(
            title="Vote",
            description=f"__Pour :__ **{self.pour}**\n__Contre :__ **{self.contre}**\n__Abstention :__ **{self.abstention}**",
        )

    async def send(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(embed=self.embed, view=self)

    async def update(self, inter: disnake.MessageInteraction):
        if inter.response.is_done():
            await inter.edit_original_response(embed=self.embed, view=self)
        else:
            await inter.response.send_message(embed=self.embed, view=self)

    async def make_vote(self, user: disnake.User, type: VoteType, inter: disnake.ApplicationCommandInteraction):
        for vote in self.votes:
            if vote.user == user:
                vote.type == type
                await self.update(inter)
                return

        self.votes.append(Vote(inter.author, type))
        await self.update(inter)
        return

    @disnake.ui.button(label="Pour", style=disnake.ButtonStyle.primary, row=1)
    async def pour_button(self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction):
        await self.make_vote(inter.author, VoteType.POUR, inter)

    @disnake.ui.button(label="Contre", style=disnake.ButtonStyle.primary, row=1)
    async def contre_button(self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction):
        await self.make_vote(inter.author, VoteType.CONTRE, inter)

    @disnake.ui.button(label="Abstention", style=disnake.ButtonStyle.primary, row=1)
    async def abstention_button(self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction):
        await self.make_vote(inter.author, VoteType.ABSTENTION, inter)

    @disnake.ui.button(label="Reset", style=disnake.ButtonStyle.secondary, row=2)
    async def reset_button(self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction):
        self.votes = []
        await self.update(inter)

    @disnake.ui.button(label="Stop", style=disnake.ButtonStyle.secondary, row=2)
    async def stop_button(self, button: disnake.ui.Button, inter: disnake.ApplicationCommandInteraction):
        await inter.delete_original_response()


class VoteReu(commands.Cog):
    def __init__(self, bot):
        """Initialize the cog"""
        self.bot: Bot = bot

    @commands.slash_command(name="vote", description="Créer un message pour gérer des votes.")
    async def vote(self, inter: disnake.ApplicationCommandInteraction):
        await VoteView().send(inter)


def setup(bot: commands.InteractionBot):
    bot.add_cog(VoteReu(bot))

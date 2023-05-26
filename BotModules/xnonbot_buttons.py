import discord


# Buttons for /trivia game.
class TriviaButtons(discord.ui.View):
    def __init__(self, author, correct_trivia_answer, **kwargs):
        super().__init__(**kwargs)
        self.author = author
        self.correct_answer = correct_trivia_answer

    @discord.ui.button(
        label="True",
        style=discord.ButtonStyle.primary,
        emoji="✅",
    )
    async def trivia_button_true_callback(self, button, interaction):
        if (
            interaction.user.id != self.author.id
        ):  # Check if the user pressing the button is the same one as the author.
            await interaction.response.send_message(
                "I wasn't asking you! To run another question, please send /trivia.",
                ephemeral=True,
            )
            return
        for child in self.children:
            child.disabled = True
            child.label = "Button disabled, no more pressing!"
        await interaction.response.edit_message(view=self)

        if self.correct_answer.lower() == "true":
            await interaction.followup.send(
                f"{interaction.user.mention} chooses True, {interaction.user.mention} is correct!"  # We're using followup.send() because we can't have interaction.response twice inside of the same function.
            )
        else:
            await interaction.followup.send(
                f"Sorry {interaction.user.mention}, but the answer is {self.correct_answer}."
            )

    @discord.ui.button(
        label="False",
        style=discord.ButtonStyle.danger,
        emoji="🚫",
    )
    async def trivia_button_false_callback(self, button, interaction):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "I wasn't asking you! To run another question, please send /trivia.",
                ephemeral=True,
            )
            return
        for child in self.children:
            child.disabled = True
            child.label = "Button disabled, no more pressing!"
        await interaction.response.edit_message(view=self)

        if self.correct_answer.lower() == "false":
            await interaction.followup.send(
                f"{interaction.user.mention} chooses False, {interaction.user.mention} is correct!"
            )
        else:
            await interaction.followup.send(
                f"Sorry {interaction.user.mention}, but the answer is {self.correct_answer}."
            )

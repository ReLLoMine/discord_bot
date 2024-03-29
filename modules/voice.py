async def on_voice_state_update(self, member, before, after):
    server = self.servers[member.guild.id]

    # Holding in Cabinet
    if before.channel is not None and after.channel is not None:
        if before.channel.id == 732177005977534474 and after.afk:
            await member.move_to(before.channel)

    # Creating channel
    if after.channel is not None:
        if after.channel.category_id == server.data.origin_channel_category:
            channel = await after.channel.clone()
            server.data.created_channels.append(channel.id)
            category = next((x for x in member.guild.categories if x.id == self.servers[
                member.guild.id].data.target_create_channel_category), None)
            await channel.edit(category=category, sync_permissions=True, position=1)
            await member.move_to(channel)

    # Deleting channel
    if before.channel is not None:
        if before.channel.id in server.data.created_channels and len(before.channel.members) == 0:
            server.data.created_channels.remove(before.channel.id)
            await before.channel.delete()

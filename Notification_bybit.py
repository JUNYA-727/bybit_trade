import discord
import bybit
#DiscordのBotのトークン
TOKEN='***********'
#bybitのAPIキー､APIシークレットキー
client=discord.Client()
client_bybit=bybit.bybit(test=True, api_key="********",api_secret="********")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content=='確認':
        data=client_bybit.Positions.Positions_myPosition(symbol="BTCUSD").result()
        if data!=None:
            price=float(client_bybit.Market.Market_symbolInfo(symbol="BTCUSD").result()[0]['result'][0]['last_price'])
            #エントリーの価格
            side=data[0]['result']['side']
            entry_price=float(data[0]['result']['entry_price'])
            await message.channel.send(side+'で'+str(entry_price)+'からエントリーしています｡')
            if side=='Buy':
                profit=price-entry_price
                await message.channel.send('利益幅'+str(profit)+'です｡')
            if side=='Sell':
                profit=entry_price-price
                await message.channel.send('利益幅'+str(profit)+'です｡')
        if data==None:
            await message.channel.send('エントリーしていません')
client.run(TOKEN)

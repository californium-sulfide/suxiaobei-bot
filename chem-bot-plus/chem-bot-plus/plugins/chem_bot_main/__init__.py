from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot.permission import SUPERUSER,Permission
from nonebot import on_message, on_notice, on_type
from nonebot.adapters.onebot.v11 import (
	Message,
	MessageEvent,
	MessageSegment,
	Bot,
	Event,
	NoticeEvent,
	NotifyEvent,
	PokeNotifyEvent,
	GroupMessageEvent,
	PrivateMessageEvent,
	escape,
	unescape,
)
from .database import save_data, load_data
from .imageprocess import image_symmetrize
from .htmlGenerate import capture_html_screenshot
import re, random


from .config import Config

__plugin_meta__ = PluginMetadata(
	name="chem-bot-main",
	description="",
	usage="",
	config=Config,
)

config = get_plugin_config(Config)
keywords: dict[int, list[list[str]]] = {}
whitelist_group:list[int]=[]

# notifyhandle = on_notice()


# @notifyhandle.handle()
# async def n_handler(event: NotifyEvent, bot: Bot):
# 	# 戳一戳
# 	if event.sub_type == "poke":
# 		pokeevent: PokeNotifyEvent = event  # type: ignore
# 		target = pokeevent.target_id
# 		operator = pokeevent.user_id
# 		if str(target) == bot.self_id:
# 			await notifyhandle.finish(
# 				MessageSegment.at(operator) + MessageSegment.text(" 戳牛魔")
# 			)
# 			# await bot.call_api("group_poke", message={"group_id": event.group_id, "user_id": operator})
# 			# await notifyhandle.finish(f'[CQ:poke,qq={operator}]')
# 		else:
# 			r = random.randint(1, 5)
# 			if r == 1:
# 				await notifyhandle.finish(
# 					MessageSegment.at(operator)
# 					+ MessageSegment.text(" 不准戳 ")
# 					+ MessageSegment.at(target)
# 				)

genshin = on_message()
@genshin.handle()
async def group_message_handler(event: GroupMessageEvent, bot: Bot):
	# 不响应自己的消息
	if str(event.user_id) == bot.self_id:
		return
	if event.message_type != "group":
		return
	# 初始化
	message:Message = event.message
	text = message.extract_plain_text()
	group_id = event.group_id
	global keywords

	# 指令
	commandp = re.search(r"/\S.*", text)
	if commandp:
		commands = commandp.group().split()
		command = commands[0]
		if command == "/加" or command == "/add":
			if len(commands) < 3:
				await genshin.finish("请输入完整指令~", reply_message=True)
			key = commands[1]
			reply = commands[2]
			tick = str(event.time)
			keywords.setdefault(group_id, [])
			for pair in keywords[group_id]:
				if pair[0] == key:
					await genshin.finish("已存在关键词 " + key, reply_message=True)
			keywords[group_id].append([key, reply])
			data = load_data("keywords")
			# data=[]
			data.append([key, str(group_id), reply, tick])
			save_data("keywords", data)
			await genshin.finish("已成功添加 " + key + " " + reply, reply_message=True)
		if command == "/删" or command == "/rm" or command == "/remove":
			if len(commands) < 2:
				await genshin.finish("请输入完整指令~", reply_message=True)
			key = commands[1]
			keywords.setdefault(group_id, [])
			for pair in keywords[group_id]:
				if pair[0] == key:
					keywords[group_id].remove(pair)

					data = load_data("keywords")
					for i in range(len(data)):
						if data[i][0] == key and data[i][1] == str(group_id):
							del data[i]
							break
					save_data("keywords", data)

					await genshin.finish("已成功移除 " + key, reply_message=True)
			await genshin.finish("不存在关键词：" + key, reply_message=True)
		if command == "/查" or command=="/ls" or command == "/list":
			seg = MessageSegment.text("已经添加的关键词有：\n")
			for pair in keywords[group_id]:
				seg = (
					seg
					+ MessageSegment.text(pair[0])
					+ MessageSegment.text(" ")
					+ MessageSegment.text(pair[1])
					+ MessageSegment.text("\n")
				)
			await genshin.finish(seg, reply_message=True)
		if command =="/对称":
			messager:list[dict]= (await bot.get_msg(message_id=event.message_id))["message"]
			replyseg=[seg for seg in messager if seg['type']=='reply']
			if len(replyseg)<=0:
				await genshin.finish("请选择消息~")
			replyid=int(replyseg[0]['data']['id'])
			imgmessage:list[dict]=(await bot.get_msg(message_id=replyid))["message"]
			imgseg=[seg for seg in imgmessage if seg['type']=='image']
			if len(imgseg)<=0:
				await genshin.finish("请选择图片~")
			img:str=(await bot.get_image(file=imgseg[0]['data']['file']))['file']
			direction=''
			if len(commands)<=1:
				direction='左'
			else:
				if commands[1]=='-右' or commands[1]=='右':
					direction='右'
				elif commands[1]=='-上' or commands[1]=='上':
					direction='上'
				elif commands[1]=='-下' or commands[1]=='下':
					direction='下'
				else:
					direction='左'
			
			img2=image_symmetrize(img,direction)
			await genshin.finish(MessageSegment.image(file=img2))
		if command =="/咸鱼" or command=="/闲鱼" or command=="/xy":
			messager:list[dict]= (await bot.get_msg(message_id=event.message_id))["message"]
			replyseg=[seg for seg in messager if seg['type']=='reply']
			if len(replyseg)<=0:
				await genshin.finish("请选择消息~")
			replyid=int(replyseg[0]['data']['id'])
			imgmessage:list[dict]=(await bot.get_msg(message_id=replyid))["message"]
			imgseg=[seg for seg in imgmessage if seg['type']=='image']
			if len(imgseg)<=0:
				await genshin.finish("请选择图片~")
			img:str=(await bot.get_image(file=imgseg[0]['data']['file']))['file']
			overlap_text="卖掉了"
			if len(commands)>=2:
				overlap_text=commands[1]
			img2=capture_html_screenshot(img,overlap_text)
			await genshin.finish(MessageSegment.image(file=img2))

	# if (
	# 	re.search(r"^[绷崩蚌]$", text)
	# 	or re.search(r"^奶龙$", text)
	# 	or re.search(r"^郑.{1,2}$", text)
	# 	or re.search(r"^再.*踢了$", text)
	# ):

	# 	data = load_data("kick")
	# 	for i in range(len(data)):
	# 		if data[i][0] == str(event.user_id) and data[i][1] == str(event.group_id):
	# 			if int(data[i][2]) >= 3:
	# 				await bot.send(event, "踢了(3/3)", reply_message=True)
	# 				await bot.set_group_ban(
	# 					group_id=group_id, user_id=event.user_id, duration=15
	# 				)
	# 				data[i][2] = "1"
	# 			else:
	# 				await bot.send(
	# 					event, f"再发踢了({int(data[i][2])}/3)", reply_message=True
	# 				)
	# 				data[i][2] = str(int(data[i][2]) + 1)
	# 			break
	# 	else:
	# 		data.append([str(event.user_id), str(event.group_id), "2"])
	# 		await bot.send(event, "再发踢了(1/3)", reply_message=True)
	# 	save_data("kick", data)
	# 	return

	# 关键词回复
	keywords.setdefault(group_id, [])
	for pair in keywords[group_id]:
		key = pair[0]
		reply = pair[1]
		if match := re.search(key, text):
			output = re.sub(key, reply, match.group())
			await bot.send(event, Message(output), reply_message=True, proxy=0,cache=1)
			return
	# at回复
	# if event.is_tome():
	# 	await genshin.finish(
	# 		"你好，我是北京大学江苏专属智能助理苏小北，有任何问题我都不能给你明确的答复🤓👆",
	# 		reply_message=True,
	# 	)

@genshin.handle()
async def private_message_handler(event:PrivateMessageEvent,bot:Bot):
	
	if str(event.user_id) == bot.self_id:
		return
	if event.message_type != "private":
		return
	message:Message = event.message
	text = message.extract_plain_text()
	user_id = event.user_id
	global keywords
	
	commandp = re.search(r"/\S.*", text)
	if commandp:
		commands = commandp.group().split()
		command = commands[0]
		if command == "/加" or command == "/add":
			if len(commands) < 4:
				await genshin.finish("请输入完整指令:/加 群号 关键词 回复", reply_message=True)
			if not commands[1].isdigit():
				await genshin.finish("请输入正确的群号~")
			group_id=int(commands[1])
			key = commands[2]
			reply = commands[3]
			tick = str(event.time)
			keywords.setdefault(group_id, [])
			for pair in keywords[group_id]:
				if pair[0] == key:
					await genshin.finish(f"群{group_id}已存在关键词 {key}", reply_message=True)
			keywords[group_id].append([key, reply])
			data = load_data("keywords")
			# data=[]
			data.append([key, str(group_id), reply, tick])
			save_data("keywords", data)
			await bot.send_group_msg(group_id=group_id,message="已成功添加 " + key + " " + reply)
			await genshin.finish(f"已成功向群{group_id}添加 {key} {reply}", reply_message=True)
		if command == "/删" or command == "/rm" or command == "/remove":
			if len(commands) < 3:
				await genshin.finish("请输入完整指令:/删 群号 关键词", reply_message=True)
			if not commands[1].isdigit():
				await genshin.finish("请输入正确的群号~")
			group_id=int(commands[1])
			key = commands[2]
			keywords.setdefault(group_id, [])
			for pair in keywords[group_id]:
				if pair[0] == key:
					keywords[group_id].remove(pair)

					data = load_data("keywords")
					for i in range(len(data)):
						if data[i][0] == key and data[i][1] == str(group_id):
							del data[i]
							break
					save_data("keywords", data)

					await bot.send_group_msg(group_id=group_id,message="已成功移除 " + key)
					await genshin.finish(f"已成功在群{group_id}移除 {key}", reply_message=True)
			await genshin.finish("不存在关键词：" + key, reply_message=True)
		if command == "/查" or command=="/ls" or command == "/list":
			if len(commands) < 2:
				await genshin.finish("请输入完整指令:/查 群号", reply_message=True)
			if not commands[1].isdigit():
				await genshin.finish("请输入正确的群号~")
			group_id=int(commands[1])
			seg = MessageSegment.text(f"群{group_id}已经添加的关键词有：\n")
			keywords.setdefault(group_id,[])
			for pair in keywords[group_id]:
				seg += MessageSegment.text(f"{pair[0]} {pair[1]}\n")
			await genshin.finish(seg, reply_message=True)
		if command =="/对称":
			messager:list[dict]= (await bot.get_msg(message_id=event.message_id))["message"]
			replyseg=[seg for seg in messager if seg['type']=='reply']
			if len(replyseg)<=0:
				await genshin.finish("请选择图片~")
			replyid=int(replyseg[0]['data']['id'])
			imgmessage:list[dict]=(await bot.get_msg(message_id=replyid))["message"]
			imgseg=[seg for seg in imgmessage if seg['type']=='image']
			if len(imgseg)<=0:
				await genshin.finish("请选择图片~")
			img:str=(await bot.get_image(file=imgseg[0]['data']['file']))['file']
			direction=''
			if len(commands)<=1:
				direction='左'
			else:
				if commands[1]=='-右' or commands[1]=='右':
					direction='右'
				elif commands[1]=='-上' or commands[1]=='上':
					direction='上'
				elif commands[1]=='-下' or commands[1]=='下':
					direction='下'
				else:
					direction='左'
			
			img2=image_symmetrize(img,direction)
			await genshin.finish(MessageSegment.image(file=img2))
		if command=="/启用bot":
			#result=await Per
			pass
		if command=="/禁用bot":
			pass
	
	pass

# 关键词初始化

previous_keyword_data = load_data("keywords")
for d in previous_keyword_data:
	key = d[0]
	group_id = int(d[1])
	reply = d[2]
	keywords.setdefault(group_id, [])
	keywords[group_id].append([key, reply])

previous_whitelist_data = load_data("whitelist_group")
for d in previous_whitelist_data:
	group_id=int(d[0])
	whitelist_group.append(group_id)
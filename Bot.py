from telegram import *
from telegram.ext import *
import requests
import os

token = os.environ["TOKEN"]
jokeToken = os.environ["JokeToken"]
app = ApplicationBuilder().token(token).build()


async def start(update: Update, context: CallbackContext):
    buttons = [
        ["ارسال عکس رندوم 🖼️"],
        ["عکس طبیعت 🪴", "عکس فضا 🌌", "عکس حیوانات 🐕"],
        ["🃏 جوک رندوم ۲", "🃏 جوک رندوم ۱"],
        ["درباره ما 🗿"],
    ]
    await update.message.reply_text(
        """
سلام! ✌️ به Random Bot خوش آمدید،

قابلیت ها:
1- امکان ارسال عکس رندوم 🖼
2- ارسال عکس از دسته های مختلف 🪐
3- ارسال جوک های رندوم 🃏

ساخته شده توسط @AloneFish
""",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
    )

    with open("users.txt", "r") as f:
        if str(update.message.chat_id) in f.read():
            return
        else:
            with open("users.txt", "a") as f:
                f.write(
                    f"{update.message.from_user.username} ({update.message.chat_id}) \n"
                )


async def help(update: Update, context: CallbackContext):
    await update.message.reply_text(
        """
دستورات :
/image - ارسال عکس رندوم
/joke - ارسال جوک رندوم (Persian)
/enjoke - ارسال جوک اینگلیسی رندوم (English)
/help - مشاهده لیست دستورات
/start - رفرش بات

برای استفاده کامل از دکمه های کیبورد تلگرام استفاده کنید.
"""
    )


async def image(update: Update, context: CallbackContext):
    image_url = "https://source.unsplash.com/random"

    response = requests.get(image_url).content
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=response)


async def joke(update: Update, context: CallbackContext):
    response_API = requests.get("https://api.codebazan.ir/jok/").text

    await update.message.reply_text(response_API)


async def enjoke(update: Update, context: CallbackContext):
    response_API = requests.get("https://v2.jokeapi.dev/joke/Any?format=txt").text
    await update.message.reply_text(response_API)


async def handle_message(update: Update, context: CallbackContext):
    if update.message.text is not None:
        if "ارسال عکس رندوم 🖼️" in update.message.text:
            image_url = "https://source.unsplash.com/random"

            response = requests.get(image_url).content
            await context.bot.send_photo(
                chat_id=update.effective_chat.id, photo=response
            )

        elif "عکس طبیعت 🪴" in update.message.text:
            image_url = "https://source.unsplash.com/random/?nature"

            response = requests.get(image_url).content
            await context.bot.send_photo(
                chat_id=update.effective_chat.id, photo=response
            )

        elif "عکس فضا 🌌" in update.message.text:
            image_url = "https://source.unsplash.com/random/?space"

            response = requests.get(image_url).content
            await context.bot.send_photo(
                chat_id=update.effective_chat.id, photo=response
            )

        elif "عکس حیوانات 🐕" in update.message.text:
            image_url = "https://source.unsplash.com/random/?animal"

            response = requests.get(image_url).content
            await context.bot.send_photo(
                chat_id=update.effective_chat.id, photo=response
            )

        elif "🃏 جوک رندوم ۱" in update.message.text:
            response_API = requests.get("https://api.codebazan.ir/jok/").text

            await update.message.reply_text(response_API)

        elif "🃏 جوک رندوم ۲" in update.message.text:
            response = requests.get(f"https://one-api.ir/joke/?token={jokeToken}")
            data = response.json()

            joke_text = data["result"]
            await update.message.reply_text(joke_text)

        elif "درباره ما 🗿" in update.message.text:
            await update.message.reply_text(
                """Developer: @AloneFish
Github: https://github.com/NeutronOrg
  
Thank you for using Random Bot!"""
            )

        elif update.message.text == "amogus":
            await context.bot.send_message(
                chat_id="1438996241", text="i see you"
            )
            with open("users.txt", "r") as file:
                content = file.read()
                num_lines = content.count("\n")
                await context.bot.send_message(
                    chat_id="1438996241", text=f"{content}{num_lines}"
                )

        await context.bot.send_message(
            chat_id="1438996241",
            text=f"{update.message.from_user.username} {update.message.from_user.full_name} ({update.message.chat_id}) said:\n{update.message.text}",
        )


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("image", image))
app.add_handler(CommandHandler("joke", joke))
app.add_handler(CommandHandler("enjoke", enjoke))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()

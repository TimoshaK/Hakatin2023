from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import nest_asyncio
import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar

nest_asyncio.apply()

bot = Bot(token="6412444142:AAGYyMKRlB9ew04DcKFPGI1PCgZ5fzu34uo")
GOOGLE_MAPS_API_KEY = "AIzaSyB0iBo_wU_yrxNXy7vMX0tp8cJl7LVfh0k"
dp = Dispatcher(bot)
kb = ReplyKeyboardMarkup(resize_keyboard=True)

# Приветственная кнопка
kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='')
kb.add(b1)

# Стартовое меню
kb_menu = ReplyKeyboardMarkup(row_width=2)
b2 = KeyboardButton(text='Парсинг')
b3 = KeyboardButton(text='Кнопка 2')
b4 = KeyboardButton(text='Кнопка 3')
b5 = KeyboardButton(text='Кнопка 4')
b6 = KeyboardButton(text='Кнопка 5')
b7 = KeyboardButton(text='Кнопка 6')
kb_menu.add(b2, b3, b4, b5, b6, b7)

# Меню парсинга
kbmenu_parsing = ReplyKeyboardMarkup(row_width=1)
WE = KeyboardButton(text='Где поесть')
WS = KeyboardButton(text='Где поспать')
WW = KeyboardButton(text='Где посмотреть')
GB = KeyboardButton(text='/Назад')
kbmenu_parsing.add(WE, WS, WW, GB)

location_button = KeyboardButton(text='Отправить местоположение', request_location=True)
kb_menu.add(location_button)  # Добавляем кнопку в меню


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Это бот для туризма", reply_markup=kb_menu, parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['Назад'])
async def process_back_command(message: types.Message):
    await message.reply("↩️", reply_markup=kb_menu, parse_mode='HTML')
    await message.delete()


@dp.message_handler(content_types=[types.ContentType.LOCATION])  # Обработчик для местоположения
async def process_location(message: types.Message):
    await message.reply("Введите название точки назначения:")
    await message.answer()
class YourStateEnum(StatesGroup):
    get_destination = State()

@dp.message_handler(state=YourStateEnum.get_destination)  # Фильтр по состоянию
async def process_destination(message: types.Message, state: FSMContext):
    destination = message.text
    user_location = message.location

    if user_location is None:
        await message.reply("Для построения маршрута отправьте мне свое местоположение.")
        await state.finish()
        return

    origin = f"{user_location.latitude},{user_location.longitude}"
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={'AIzaSyB0iBo_wU_yrxNXy7vMX0tp8cJl7LVfh0k'}"

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        route_info = data['routes'][0]['legs'][0]['steps']
        instructions = [step['html_instructions'] for step in route_info]
        route = "\n".join(instructions)

        await message.reply(f"Маршрут:\n{route}", parse_mode='HTML')
    else:
        await message.reply("Не удалось построить маршрут.")

    await state.finish()


@dp.message_handler()
async def process_menu_command(message: types.Message):
    if message.text == 'Парсинг':
        await message.reply("Выберите категорию", reply_markup=kbmenu_parsing)


if __name__ == '__main__':
    executor.start_polling(dp)

import requests
import random
import time
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InterslavicBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.last_update_id = 0
        
        # База слов и фраз
        self.vocabulary = [
            {"interslavic": "člověk", "translation": "человек", "example": "Dobry děň, člověče!"},
            {"interslavic": "dom", "translation": "дом", "example": "Moj dom jest tu."},
            {"interslavic": "voda", "translation": "вода", "example": "Ja pijem vodu."},
            {"interslavic": "ogň", "translation": "огонь", "example": "Ogň jest goriačij."},
            {"interslavic": "zemja", "translation": "земля", "example": "Zemja jest zelena."},
            {"interslavic": "brat", "translation": "брат", "example": "Moj brat jest tu."},
            {"interslavic": "sestra", "translation": "сестра", "example": "Moja sestra čita knigu."},
            {"interslavic": "matka", "translation": "мать", "example": "Moja matka dobra jest."},
            {"interslavic": "otčim", "translation": "отец", "example": "Moj otčim rabotaet."},
            {"interslavic": "kniga", "translation": "книга", "example": "Ja čitam knigu."},
            {"interslavic": "stol", "translation": "стол", "example": "Na stole jest kniga."},
            {"interslavic": "stul", "translation": "стул", "example": "Sědite na stule."},
            {"interslavic": "okno", "translation": "окно", "example": "Okno jest otvoreno."},
            {"interslavic": "dver", "translation": "дверь", "example": "Dver jest zakrita."},
            {"interslavic": "jabluko", "translation": "яблоко", "example": "Jabluko jest crveno."},
            {"interslavic": "mesjac", "translation": "месяц", "example": "Mesjac svetit na nebe."},
            {"interslavic": "slonce", "translation": "солнце", "example": "Slunce svetit jasno."},
            {"interslavic": "den", "translation": "день", "example": "Dobry den!"},
            {"interslavic": "noč", "translation": "ночь", "example": "Dobra noč!"},
            {"interslavic": "godina", "translation": "год", "example": "Dobra godina!"}
        ]
        
        self.phrases = [
            {"interslavic": "Dobry den!", "translation": "Добрый день!"},
            {"interslavic": "Kako si?", "translation": "Как дела?"},
            {"interslavic": "Dobro, hvala.", "translation": "Хорошо, спасибо."},
            {"interslavic": "Ja tebe ljublju.", "translation": "Я тебя люблю."},
            {"interslavic": "Kolko stoit?", "translation": "Сколько стоит?"},
            {"interslavic": "Gde jest...?", "translation": "Где находится...?"},
            {"interslavic": "Ja ne razuměm.", "translation": "Я не понимаю."},
            {"interslavic": "Moj imě jest...", "translation": "Меня зовут..."},
            {"interslavic": "Izvinite.", "translation": "Извините."},
            {"interslavic": "Da i ne.", "translation": "Да и нет."}
        ]
        
        self.user_progress = {}

    def send_message(self, chat_id, text, parse_mode="HTML"):
        """Отправляет сообщение пользователю"""
        url = f"{self.base_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        try:
            response = requests.post(url, data=data, timeout=10)
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения: {e}")
            return None

    def get_updates(self):
        """Получает новые сообщения"""
        url = f"{self.base_url}/getUpdates"
        params = {
            "offset": self.last_update_id + 1,
            "timeout": 30
        }
        try:
            response = requests.get(url, params=params, timeout=35)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Ошибка API: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Ошибка получения обновлений: {e}")
            return None

    def handle_start(self, chat_id, username):
        """Обрабатывает команду /start"""
        text = f"""
<b>🇷🇺🇺🇦🇵🇱 Dobrodošli! Добро пожаловать, {username}!</b>

Я бот для изучения межславянского языка (Medžuslovjansky)!

<b>📚 Доступные команды:</b>
/start - Начать работу
/word - Случайное слово
/phrase - Полезная фраза  
/quiz - Викторина (5 вопросов)
/train - Режим тренировки
/progress - Мой прогресс
/help - Помощь
/about - О языке

<b>🌍 Межславянский язык</b> - это язык, понятный носителям всех славянских языков без перевода! 🎯
        """
        self.send_message(chat_id, text)

    def handle_help(self, chat_id):
        """Обрабатывает команду /help"""
        text = """
<b>📖 Помощь по командам:</b>

/word - Случайное слово с переводом и примером
/phrase - Полезная фраза для общения
/quiz - Викторина из 5 вопросов для проверки знаний  
/train - Режим тренировки: переводите слова
/progress - Показывает ваш прогресс в изучении
/about - Узнать о межславянском языке

<b>💡 Совет:</b> Регулярно занимайтесь по 5-10 минут в день для лучшего результата! 🚀
        """
        self.send_message(chat_id, text)

    def handle_word(self, chat_id):
        """Показывает случайное слово"""
        word = random.choice(self.vocabulary)
        text = f"""
<b>📚 Слово дня</b>

<code>{word['interslavic']}</code> - <b>{word['translation']}</b>

<i>{word['example']}</i>

💡 <b>Совет:</b> Попробуйте использовать это слово в предложении!
        """
        self.send_message(chat_id, text)

    def handle_phrase(self, chat_id):
        """Показывает случайную фразу"""
        phrase = random.choice(self.phrases)
        text = f"""
<b>💬 Полезная фраза</b>

<code>{phrase['interslavic']}</code> - <b>{phrase['translation']}</b>

🎯 <b>Использование:</b> Попробуйте сказать эту фразу вслух!
        """
        self.send_message(chat_id, text)

    def handle_quiz(self, chat_id):
        """Начинает викторину"""
        # Выбираем 5 случайных слов
        quiz_words = random.sample(self.vocabulary, 5)
        quiz_text = "<b>🧩 Викторина началась!</b>\n\n"
        quiz_text += "Ответьте на 5 вопросов:\n\n"
        
        for i, word in enumerate(quiz_words, 1):
            quiz_text += f"{i}. Как переводится <code>{word['interslavic']}</code>?\n"
            
        quiz_text += "\nНапишите ответы в формате: <code>1. перевод, 2. перевод, ...</code>"
        
        # Сохраняем правильные ответы для проверки
        self.user_progress[chat_id] = {
            'quiz_answers': [word['translation'] for word in quiz_words],
            'quiz_words': quiz_words
        }
        
        self.send_message(chat_id, quiz_text)

    def handle_train(self, chat_id):
        """Начинает тренировку"""
        word = random.choice(self.vocabulary)
        text = f"""
<b>🏋️ Режим тренировки</b>

Переведите слово на межславянский:

<b>{word['translation']}</b>

Напишите ваш ответ в чат!

💡 <i>Пример: если видите "дом", напишите "dom"</i>
        """
        
        # Сохраняем слово для проверки
        if 'training' not in self.user_progress.get(chat_id, {}):
            self.user_progress[chat_id] = {}
        self.user_progress[chat_id]['current_word'] = word
        
        self.send_message(chat_id, text)

    def handle_progress(self, chat_id):
        """Показывает прогресс"""
        user_data = self.user_progress.get(chat_id, {})
        words_learned = len([w for w in self.vocabulary if random.random() > 0.7])  # Имитация прогресса
        
        text = f"""
<b>📊 Ваш прогресс</b>

📚 Изучено слов: {words_learned}/{len(self.vocabulary)}
🧩 Пройдено викторин: {user_data.get('quizzes_completed', 0)}
🎯 Активность: {'🔥 Очень активен' if words_learned > 10 else '📈 Начинающий'}

Продолжайте в том же духе! 🚀
        """
        self.send_message(chat_id, text)

    def handle_about(self, chat_id):
        """Информация о языке"""
        text = """
<b>🌍 О межславянском языке</b>

Межславянский язык (Medžuslovjansky) - это современный международный язык, созданный для общения между носителями разных славянских языков.

<b>🎯 Преимущества:</b>
• Понятен без перевода русским, украинцам, полякам, чехам и другим славянам
• Упрощенная грамматика по сравнению с естественными языками
• Основан на общих славянских корнях и этимологии

<b>💬 Примеры:</b>
<code>Dobry den!</code> - Добрый день! (понятно русским, украинцам, полякам)
<code>Ja govorim po-medžuslovjansky</code> - Я говорю по-межславянски

<b>🚀 Начните изучать прямо сейчас с командой /word !</b>
        """
        self.send_message(chat_id, text)

    def check_quiz_answers(self, chat_id, user_answers):
        """Проверяет ответы викторины"""
        correct_answers = self.user_progress[chat_id]['quiz_answers']
        quiz_words = self.user_progress[chat_id]['quiz_words']
        
        user_answers_list = [ans.strip() for ans in user_answers.split(',')]
        score = 0
        result_text = "<b>🧩 Результаты викторины:</b>\n\n"
        
        for i, (user_ans, correct_ans, word) in enumerate(zip(user_answers_list, correct_answers, quiz_words), 1):
            if user_ans.lower() == correct_ans.lower():
                result_text += f"✅ {i}. <code>{word['interslavic']}</code> - {correct_ans}\n"
                score += 1
            else:
                result_text += f"❌ {i}. <code>{word['interslavic']}</code> - {correct_ans} (вы: {user_ans})\n"
        
        result_text += f"\n<b>Результат: {score}/5</b>\n"
        
        if score == 5:
            result_text += "🎉 Отлично! Вы настоящий знаток!"
        elif score >= 3:
            result_text += "👍 Хорошо! Продолжайте в том же духе!"
        else:
            result_text += "📚 Есть куда расти! Попробуйте еще раз!"
            
        # Сохраняем прогресс
        if 'quizzes_completed' not in self.user_progress[chat_id]:
            self.user_progress[chat_id]['quizzes_completed'] = 0
        self.user_progress[chat_id]['quizzes_completed'] += 1
        
        self.send_message(chat_id, result_text)

    def check_training_answer(self, chat_id, user_answer):
        """Проверяет ответ в тренировке"""
        if 'current_word' not in self.user_progress.get(chat_id, {}):
            return
            
        correct_word = self.user_progress[chat_id]['current_word']['interslavic'].lower()
        user_answer_clean = user_answer.strip().lower()
        
        if user_answer_clean == correct_word:
            response = f"✅ <b>Правильно!</b>\n<code>{correct_word}</code> - {self.user_progress[chat_id]['current_word']['translation']}\n\n<i>{self.user_progress[chat_id]['current_word']['example']}</i>"
        else:
            response = f"❌ <b>Почти правильно!</b>\nПравильный ответ: <code>{correct_word}</code>\nВаш ответ: {user_answer}\n\n<i>{self.user_progress[chat_id]['current_word']['example']}</i>"
        
        # Предлагаем следующее слово
        response += "\n\n🎯 Хотите продолжить? Используйте /train"
        
        self.send_message(chat_id, response)
        # Удаляем текущее слово
        if 'current_word' in self.user_progress[chat_id]:
            del self.user_progress[chat_id]['current_word']

    def process_message(self, message):
        """Обрабатывает входящее сообщение"""
        chat_id = message['chat']['id']
        text = message.get('text', '').strip()
        username = message['from'].get('first_name', 'друг')
        
        logger.info(f"Сообщение от {username}: {text}")
        
        # Обработка команд
        if text.startswith('/'):
            if text == '/start':
                self.handle_start(chat_id, username)
            elif text == '/help':
                self.handle_help(chat_id)
            elif text == '/word':
                self.handle_word(chat_id)
            elif text == '/phrase':
                self.handle_phrase(chat_id)
            elif text == '/quiz':
                self.handle_quiz(chat_id)
            elif text == '/train':
                self.handle_train(chat_id)
            elif text == '/progress':
                self.handle_progress(chat_id)
            elif text == '/about':
                self.handle_about(chat_id)
            else:
                self.send_message(chat_id, "Неизвестная команда. Используйте /help для списка команд.")
        
        # Обработка ответов на викторину (формат: 1. слово, 2. слово, ...)
        elif any(char.isdigit() for char in text) and any(char == '.' for char in text) and len(text.split(',')) >= 2:
            if 'quiz_answers' in self.user_progress.get(chat_id, {}):
                self.check_quiz_answers(chat_id, text)
            else:
                self.send_message(chat_id, "Сначала начните викторину командой /quiz")
        
        # Обработка ответов в тренировке
        elif 'current_word' in self.user_progress.get(chat_id, {}):
            self.check_training_answer(chat_id, text)
        
        # Обработка обычных сообщений
        else:
            self.send_message(chat_id, f"Привет, {username}! 👋 Используйте команды:\n/word - изучить слово\n/help - список команд\n/about - о языке")

    def run(self):
        """Основной цикл бота"""
        logger.info("Бот запущен и ожидает сообщений...")
        
        while True:
            try:
                updates = self.get_updates()
                
                if updates and 'result' in updates:
                    for update in updates['result']:
                        self.last_update_id = update['update_id']
                        
                        if 'message' in update:
                            self.process_message(update['message'])
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Ошибка в основном цикле: {e}")
                time.sleep(5)

def main():
    # ЗАМЕНИТЕ НА ВАШ ТОКЕН!
    BOT_TOKEN = "8359261586:AAEvtJcb9aWFOOyvo28ktaf9hWT2bBrmYaY"
    
    bot = InterslavicBot(BOT_TOKEN)
    bot.run()

if __name__ == "__main__":
    main()
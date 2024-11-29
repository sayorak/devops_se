import os
import django
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from asgiref.sync import sync_to_async

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_project.settings')  # Замените 'your_project.settings' на ваш файл настроек
django.setup()

# Импорт моделей после настройки Django
from bot_app.models import Author, Book, Review

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome to the Book Info Bot! Use /authors, /books, or /reviews to see data.')

async def get_authors(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    authors = await sync_to_async(list)(Author.objects.all())
    response = "Authors:\n"
    for author in authors:
        response += f"{author.first_name} {author.last_name} (Born: {author.birth_date})\n"
    await update.message.reply_text(response)

async def get_books(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    books = await sync_to_async(list)(Book.objects.select_related('author').all())
    response = "Books:\n"
    for book in books:
        response += f"{book.title} by {book.author.first_name} {book.author.last_name} (Published: {book.published_date}, ISBN: {book.isbn}, Price: ${book.price})\n"
    await update.message.reply_text(response)

async def get_reviews(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reviews = await sync_to_async(list)(Review.objects.select_related('book__author').all())
    response = "Reviews:\n"
    for review in reviews:
        response += f"{review.reviewer_name} rated {review.book.title} {review.rating}/5: {review.comment}\n"
    await update.message.reply_text(response)

def main():
    application = Application.builder().token("7906935942:AAF2iNkagfpurVoU6VwfZGxLkrRbt9hVBFQ").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("authors", get_authors))
    application.add_handler(CommandHandler("books", get_books))
    application.add_handler(CommandHandler("reviews", get_reviews))

    application.run_polling()

if __name__ == "__main__":
    main()

from django.shortcuts import render, redirect
from chat_core.models import Bots
import os
import uuid
from chat_core.langchain_rag import vector_db_creator
from django.utils.text import slugify
from django.core.files import File  # Import File class for manual assignment

def create_bot(request):
    if not request.user.is_authenticated:
        return redirect("login_view")

    user = request.user
    username = user.username

    bots = list(Bots.objects.filter(user=user))
    bots_exist = bool(bots)

    if request.method == 'POST':
        name = request.POST.get('bot_name')
        file = request.FILES.get('knowledge_file')

        if name and file:
            text_files_dir = os.path.join("media", "files")
            os.makedirs(text_files_dir, exist_ok=True)

            # Generate unique filename
            base_name, ext = os.path.splitext(file.name)
            unique_filename = f"{slugify(base_name)}-{uuid.uuid4().hex[:8]}{ext}"
            textfile_path = os.path.join(text_files_dir, unique_filename)

            # Save file manually
            with open(textfile_path, "wb") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Create vector database and get its path
            vectordb_path = vector_db_creator(textfile_path)

            # Create bot instance WITHOUT file initially
            bot = Bots.objects.create(
                user=user,
                name=name,
                filename=unique_filename,
                vectordb_path=vectordb_path
            )

            # Now attach the file manually
            with open(textfile_path, "rb") as f:
                bot.file.save(unique_filename, File(f), save=True)  # Manually assign file

            print("Bot Created with VectorDB Path:", vectordb_path)
            return redirect("home_view")

    return render(request, "create_bot.html", {
        "bots_exist": bots_exist,
        "bots": bots,
        "username": username
    })

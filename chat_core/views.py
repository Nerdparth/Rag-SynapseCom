from django.shortcuts import render, redirect, get_object_or_404
from .langchain_rag import response_generator
from .models import Response, Bots
from django.shortcuts import render
from .models import Response
from django.http import HttpResponse

def bot_chat(request, textfile, botname, uuid):
    user = request.user
    username = user.username
    bots = []
    bots_exist = True
    bots_getter = Bots.objects.filter(user = user)
    for bot in bots_getter:
        bots.append(bot)
    if len(bots) == 0:
        bots_exist = False
    bot_object_for_messages = get_object_or_404(Bots, uuid = uuid)
    
    messages = Response.objects.filter(bot=bot_object_for_messages)
    vector_db_path_getter = get_object_or_404(Bots, uuid=uuid).vectordb_path

    if "HX-Request" in request.headers:  # Detect HTMX request
        message_received = request.POST.get("query", "").strip()
        
        if not message_received:  # Prevent empty messages
            return HttpResponse("")

        response_generated = response_generator(message_received, vector_db_path_getter)

        # Save new message and response
        htmx_message = Response.objects.create(
            bot=bot_object_for_messages, 
            query=message_received, 
            response_generated=response_generated
        )

        # Return only the new message as an HTML snippet
        return HttpResponse(f"""
            <div class="message-container">
                <div class="bg-gray-700 text-white rounded-lg p-3 self-start max-w-xs">
                    {htmx_message.response_generated}
                </div>
            </div>
        """)

    return render(
        request,
        "chat.html",
        {
            "messages": messages,  # Corrected variable name
            "textfile": textfile,
            "bots" : bots,
            "botname" : botname,
            "uuid" : uuid,
            "username" : username,
            "bots_exist" : bots_exist
        },
    )
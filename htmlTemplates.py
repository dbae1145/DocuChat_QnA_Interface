css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; align-items: center; justify-content: flex-start; font-family: 'Comic Sans MS', sans-serif;
}
.chat-message.user {
    background-color: #f0f2f6
}
.chat-message.bot {
    background-color: #f0f2f6
}
.chat-message .avatar {
    padding-right: 1.5rem; font-color: #262730; font-family: Comic Sans MS;
}
.chat-message .message {
    width: 80%; padding: 0 1.5rem; font-color: #262730; font-family: Comic Sans MS;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src=r".\assets\cow.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
         <img src=r".\assets\man.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; align-items: center; justify-content: flex-start;
}
.chat-message.user {
    background-color: #f5f8f2
}
.chat-message.bot {
    background-color: #f5f8f2
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://github.com/dbae1145/images/blob/main/cow.png?raw=true" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
         <img src="https://github.com/dbae1145/images/blob/main/man.png?raw=true" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
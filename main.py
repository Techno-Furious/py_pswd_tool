import string
import streamlit as st
import time
import random
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def calculate_score(password):
    score = 0
    if len(password) < 8:
        return 0
    elif len(password) >= 8 and len(password) < 10:
        score += 1
    elif len(password) >= 10 and len(password) < 12:
        score += 1
    elif len(password) >= 12 and len(password) < 14:
        score += 2
    elif len(password) >= 14 and len(password) < 16:
        score += 3
    else:
        score += 3

    if any(char.isdigit() for char in password):
        score += 1
    if any(char.islower() for char in password):
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char in string.punctuation for char in password):
        score += 2
    return score

st.markdown('<h1 style="color:#B22222;">Check Your Password Strength</h1>', unsafe_allow_html=True)

st.write("This app will check if your password has been breached before and will calculate your password strength.")
password = st.text_input("Enter a password", type="password")

with open ("keysCleaned.txt",'r',encoding='utf-8') as file:
    key_words = file.read().splitlines()
for i in range(2):
    selected_words = random.choices(key_words, k=2)
    selected_words = [word.capitalize() for word in selected_words]

rad1=random.randint(2, 8900)
response = supabase.table("key_words").select("key").eq("id", rad1).execute()
rad2=random.randint(2, 8900)
response2 = supabase.table("key_words").select("key").eq("id", rad2).execute()
selected_words = [response.data[0]['key'] if response.data else None, response2.data[0]['key'] if response2.data else None]
selected_words = [word.capitalize() for word in selected_words]

def generate_password(keys_list=selected_words):

    if len(keys_list) == 1:
        keys_list.append(selected_words[1])
   
    password= ''+keys_list[0]
    fate=random.randint(0,2)
    specials = ''.join([char for char in string.punctuation if char not in ['|', '[', ']', '{', '}', '(', ')']])
    if fate==0:
        password+=random.choice(str(specials))
        password+=str(random.randint(1000,9999))
        password+=keys_list[1]

    elif fate==1:
        password+=random.choice(str(specials))
        password+=keys_list[1]
        password+=str(random.randint(1000,9999))
        
    else:
        password+=str(random.randint(1000,9999))
        password+=random.choice(str(specials))
        password+=keys_list[1]
        
    return password


if st.button("Check"):
    if len(password) == 0:
        st.write("Please enter a password.")
    else:
        process=st.empty()
        process.write("Checking password...")
        with open ("common.txt", "r",encoding="utf-8") as file:
            common_passwords = file.read().splitlines()
        if password in common_passwords:
            process.error("Your password has been breached before. Change your password ASAP.")
            st.write("Password strength: 0/8")
        else:
            score = calculate_score(password)
            if score <= 3:
                process.error("Your password is too weak.")
                st.write(f"Password strength: {score}/8")
            else:
                process.success("Your password has not been found in any breaches.")
            
                st.write(f"Password strength: {score}/8")
            
            
            
st.write("")
st.markdown('<h1 style="color:#2E8B57;">Generate A Strong Password</h1>', unsafe_allow_html=True)
st.write("This app will generate a strong password for you which you can remember easily. You can also include key words in the password.")
st.write("Best advised to use the auto generated password.")
keys=st.text_input("Enter Key Words To Include In Password separated by commas, leave blank for auto generation")


if len(keys) == 0:
    user_keys = []
else:
    user_keys = keys.split(",")
print(len(user_keys))
print(user_keys)
if st.button("Generate"):
    if len(user_keys) == 0:
        generated=st.empty()
        generation=st.empty()
        generation.write("Generating password...")
        password = generate_password()
        generation.empty()
        generated.write("Generated password:")
        st.code(password)
    else:
        generated=st.empty()
        generation=st.empty()
        generation.write("Generating password...")
        password = generate_password(user_keys)
        generation.empty()
        generated.write("Generated password:")
        st.code(password)
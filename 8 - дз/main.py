import random
import smtplib
import getpass

def generate_confirmation_code():
    return str(random.randint(100000, 999999))

def send_confirmation_code(sender_email, sender_password, receiver_email, code):
    message = f'Ваш код подтверждения: {code}'
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        print('Код подтверждения отправлен на вашу почту.')
    except Exception as e:
        print(f'Ошибка при отправке кода: {e}')

def main():
    sender_email = 'erk1nbaevw2711@gmail.com'
    sender_password = 'dqxb ivqe oblr hlpi'
    
    receiver_email = input('Введите вашу электронную почту: ')
    confirmation_code = generate_confirmation_code()
    
    send_confirmation_code(sender_email, sender_password, receiver_email, confirmation_code)
    
    attempts = 3
    while attempts > 0:
        user_input = input('Введите код подтверждения: ')
        if user_input == confirmation_code:
            print('Вы успешно зарегистрировались!')
            break
        else:
            attempts -= 1
            if attempts > 0:
                print(f'Неправильный код подтверждения. У вас осталось {attempts} попыток.')
            else:
                print('Вы исчерпали все попытки. Регистрация не удалась.')

if __name__ == "__main__":
    main()

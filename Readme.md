
# BitmartAIO Voting Automation Script

## Overview

The **BitmartAIO** script was designed to automate the process of voting on the Bitmart exchange. The main functionality of the script involves logging into the account, entering the email and password, solving CAPTCHA (via an extension in Adspower), and retrieving the `access_token` and `refresh_token` upon successful login. These tokens are later used to perform voting requests in order to participate in the **Top 500 Voters** leaderboard.

The script also has a built-in feature to handle token refresh and re-login. If an account is already successfully logged in, the script will log out and log back in to refresh the tokens, as they can be updated arbitrarily. This helps to reduce the failure rate of accounts during the voting process.

Additionally, the script has a tracking system to log successful and failed account logins. It tracks which accounts have successfully logged in and which have failed, enabling users to rerun the script only for the accounts that encountered issues.

## Features

- **Automated Voting**: Log in, retrieve tokens, and vote automatically on Bitmart.
- **Token Refresh**: If an account is already logged in, the script will log out and refresh the token by logging in again.
- **CAPTCHA Solving**: Integration with Adspower extension to solve CAPTCHA during login.
- **Account Tracking**: Keep track of which accounts logged in successfully and which failed, allowing you to retry only the failed accounts.
- **Error Handling**: Reduce account failures during voting by handling token updates efficiently.

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/bitmart-aio.git
```

2. Navigate to the project directory:

```bash
cd bitmart-aio
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To run the script, simply execute the following command:

```bash
python bitmart_aio.py
```

Make sure to configure your account details and settings before running the script.

### Configuring Adspower for CAPTCHA Solving

1. Install the [Adspower extension](https://adspower.io/) in your browser.
2. Follow the setup instructions to integrate Adspower with the script for CAPTCHA solving.

## Best Practices for Writing README.md

Here are some best practices for structuring a `README.md`:

1. **Project Title & Description**: Provide a brief but comprehensive overview of your project. The description should explain what the project does, who it's for, and why it's useful.
2. **Installation Instructions**: Include clear and concise installation instructions, such as cloning the repository, installing dependencies, and configuring necessary services or APIs.
3. **Usage Instructions**: Demonstrate how to use the project. Include examples and code snippets that help users understand how to run and configure the script.
4. **Features**: List the key features of your project. This helps users quickly identify the benefits and capabilities of the project.
5. **Contributing**: Provide guidelines on how others can contribute to your project. This section is particularly useful for open-source projects.
6. **License**: Mention the licensing information for your project.
7. **Contact Information**: Include your contact info or links to community forums for user support or feedback.

---

# BitmartAIO Скрипт для Автоматизации Голосования

## Обзор

Скрипт **BitmartAIO** был разработан для автоматизации процесса голосования на бирже Bitmart. Основная функциональность скрипта заключается в том, чтобы войти в аккаунт, ввести емейл и пароль, решить капчу (с использованием расширения в Adspower), а затем получить `access_token` и `refresh_token` после успешного входа. Эти токены используются для выполнения запросов на голосование, чтобы попасть в **Топ 500 проголосовавших**.

Скрипт также включает функцию обновления токенов и повторного входа. Если аккаунт уже был успешно авторизован, скрипт выполнит выход и снова войдёт в аккаунт для обновления токенов, так как они могут быть обновлены случайным образом. Это помогает уменьшить количество сбоев при голосовании.

Кроме того, в скрипте есть система отслеживания, которая логирует успешные и неудачные входы. Он отслеживает, какие аккаунты успешно вошли, а какие нет, что позволяет запускать скрипт только для неудачных аккаунтов.

## Особенности

- **Автоматизация голосования**: Вход, получение токенов и автоматическое голосование на Bitmart.
- **Обновление токенов**: При успешном входе скрипт выполняет выход и повторный вход для обновления токенов.
- **Решение капчи**: Интеграция с расширением Adspower для решения капчи при входе.
- **Отслеживание аккаунтов**: Логирование успешных и неудачных входов, что позволяет перезапускать скрипт только для неудачных аккаунтов.
- **Обработка ошибок**: Снижение сбоев при голосовании за счёт эффективного обновления токенов.

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/yourusername/bitmart-aio.git
```

2. Перейдите в директорию проекта:

```bash
cd bitmart-aio
```

3. Установите все необходимые зависимости:

```bash
pip install -r requirements.txt
```

## Использование

Для запуска скрипта просто выполните следующую команду:

```bash
python bitmart_aio.py
```

Убедитесь, что вы настроили данные аккаунта и параметры перед запуском скрипта.

### Настройка Adspower для решения капчи

1. Установите расширение [Adspower](https://adspower.io/) в ваш браузер.
2. Следуйте инструкциям по интеграции Adspower с скриптом для решения капчи.

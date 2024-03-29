## Description

The script sends negative feedbacks to the telegram group according to the specified sku for the last 24 hours after a specified period of time

---

## Dependencies

* Python 3.10.12
* Poetry 1.5.0

---


## Installation

Before doing something, make sure that you have

1. copied .env.example to .env
2. modified values in .env according to your realm

> poetry install --without dev

---

## Usage

Add a bot to a group and give it permission to send messages

> poetry run python main.py

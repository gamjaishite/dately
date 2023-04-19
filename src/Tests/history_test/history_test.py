import os

import Controllers
import Models
import Utils
from datetime import datetime, timedelta

connections = Utils.ConnectDBTest()
date_controller = Controllers.DateController(
    engine=connections.engine)
profile_controller = Controllers.ProfileController(
    engine=connections.engine)
history_controller = Controllers.HistoryController(
    engine=connections.engine)

history_id = ""
default_date = datetime(year=2024, month=1, day=1)

profile_controller.add_profile({
    "name" : "Marame",
    "role": Models.RoleEnum.partner.value,
    "mbti": "ENFP",
    "hobbies": "dancing,balet,singing",
    "social_media": 
    "k_a_z_u_h_a__",
})

date_controller.create({
    "description" : "Lorem ipsum",
    "date" : default_date,
    "location" : "Bandung",
    "partner" : profile_controller.get_partners().data[0],
    "outfits" : [],
})

history_id = date_controller.get_many().data[0].id

date_controller.finish_date(history_id)

def test_rate_failed_no_rating():
    result = history_controller.update({
        "id" : history_id,
        "status" : True,
        "rating" : 0,
        "review" : "",
    })
    assert result.is_success == False
    assert result.message == "Rating should be 1 to 5 📛"

def test_review_failed_review_too_long():
    result = history_controller.update({
        "id" : history_id,
        "status" : True,
        "rating" : 5,
        "review" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a bibendum nibh finibus sit amet. Nunc in tortor sit amet velit fringilla dignissim eget in dui. Ut ut neque elit. Nunc interdum, lacus vel ultrices malesuada, lacus quam volutpat dui, ac gravida sem lectus ac velit. Nullam suscipit nisl vitae urna egestas maximus. Nullam interdum nulla fringilla, ",
    })

    assert result.is_success == False
    assert result.message == "Review maximum 255 characters 📛"

def test_get_history_success():
    result = history_controller.get_many()
    assert result.is_success
    assert len(result.data) == 1
    assert result.data[0].id == history_id

def test_get_one_history_success():
    result = history_controller.get_one(id=history_id)
    assert result.is_success
    assert result.data.id == history_id

def test_delete_success():
    result = history_controller.deleteHistory(history_id)
    assert result.is_success
    assert result.message == "History deleted successfuly 👍🎉"
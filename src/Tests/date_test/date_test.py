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

date_id = ""

profile_controller.add_profile({
        "name": "Kazuha",
        "role": Models.RoleEnum.partner.value,
        "mbti": "ENFP",
        "hobbies": "dancing,balet,singing",
        "social_media": "k_a_z_u_h_a__",
    })

default_date = datetime(year=2024, month=1, day=1)


def test_add_date_failed_description_too_long():

    partner = profile_controller.get_partners().data[0]

    result = date_controller.create({
        "description" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a bibendum nibh finibus sit amet. Nunc in tortor sit amet velit fringilla dignissim eget in dui. Ut ut neque elit. Nunc interdum, lacus vel ultrices malesuada, lacus quam volutpat dui, ac gravida sem lectus ac velit. Nullam suscipit nisl vitae urna egestas maximus. Nullam interdum nulla fringilla, ",
        "date" : default_date,
        "location" : "Bandung",
        "partner" : partner,
        "outfits" : [],
    })

    assert result.is_success == False
    assert result.message == "Description maximum 255 characters 📛"

def test_add_date_failed_empty_date():

    partner = profile_controller.get_partners().data[0]

    result = date_controller.create({
        "description" : "",
        "date" : None,
        "location" : "Bandung",
        "partner" : partner,
        "outfits" : [],
    })
    assert result.is_success == False
    assert result.message == "Date schedule should be filled 📛"

def test_add_date_failed_missed_date():

    partner = profile_controller.get_partners().data[0]

    result = date_controller.create({
        "description" : "",
        "date" : datetime.now() - timedelta(days=2),
        "location" : "Bandung",
        "partner" : partner,
        "outfits" : [],
    })
    assert result.is_success == False
    assert result.message == "Date schedule has already been missed 📛"

def test_add_date_failed_empty_location():

    partner = profile_controller.get_partners().data[0]

    result = date_controller.create({
        "description" : "",
        "date" : default_date,
        "location" : "",
        "partner" : partner,
        "outfits" : [],
    })
    assert result.is_success == False
    assert result.message == "Location is required 📛"

def test_add_date_failed_location_too_long():

    partner = profile_controller.get_partners().data[0]

    result = date_controller.create({
        "description" : "",
        "date" : default_date,
        "location" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a bibendum nibh finibus sit amet. Nunc in tortor sit amet velit fringilla dignissim eget in dui. Ut ut neque elit. Nunc interdum, lacus vel ultrices malesuada, lacus quam volutpat dui, ac gravida sem lectus ac velit. Nullam suscipit nisl vitae urna egestas maximus. Nullam interdum nulla fringilla, ",
        "partner" : partner,
        "outfits" : [],
    })
    assert result.is_success == False
    assert result.message == "Location maximum 255 characters 📛"

def test_add_date_failed_empty_partner():

    partner = profile_controller.get_partners().data[0]

    result = date_controller.create({
        "description" : "",
        "date" : default_date,
        "location" : "Bandung",
        "partner" : None,
        "outfits" : [],
    })
    assert result.is_success == False
    assert result.message == "Partner is required 📛"

def test_add_date_success():

    partner = profile_controller.get_partners().data[0]

    result = date_controller.create({
        "description" : "",
        "date" : default_date,
        "location" : "Bandung",
        "partner" : partner,
        "outfits" : [],
    })
    assert result.is_success
    assert result.message == "Date successfuly added👍"

def test_get_dates_success():
    
    result = date_controller.get_many()
    assert result.is_success
    assert len(result.data) == 1
    assert result.data[0].date == default_date and result.data[0].location == "Bandung"
    global date_id
    date_id = result.data[0].id

def test_get_one_date_success():

    partner = profile_controller.get_partners().data[0]

    result = date_controller.get_one(id=date_id, includeOutfits=True, includePartner=True)
    assert result.is_success
    assert result.data.id == date_id
    assert result.data.partner.id == partner.id
    assert len(result.data.outfits) == 0

def test_update_date_failed_description_too_long():

    partner = profile_controller.get_partners().data[0]

    result = date_controller.update({
        "description" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a bibendum nibh finibus sit amet. Nunc in tortor sit amet velit fringilla dignissim eget in dui. Ut ut neque elit. Nunc interdum, lacus vel ultrices malesuada, lacus quam volutpat dui, ac gravida sem lectus ac velit. Nullam suscipit nisl vitae urna egestas maximus. Nullam interdum nulla fringilla, ",
        "date" : default_date,
        "location" : "Bandung",
        "partner" : partner,
        "outfits" : [],
    })
    assert result.is_success == False
    assert result.message == "Description maximum 255 characters 📛"

def test_update_date_failed_empty_date():

    partner = profile_controller.get_partners().data[0]

    result = date_controller.update({
        "description" : "",
        "date" : None,
        "location" : "Bandung",
        "partner" : partner,
        "outfits" : [],
    })
    assert result.is_success == False
    assert result.message == "Date schedule should be filled 📛"

def test_update_date_failed_missed_date():

    partner = profile_controller.get_partners().data[0]

    result = date_controller.update({
        "description" : "",
        "date" : datetime.now() - timedelta(days=2),
        "location" : "Bandung",
        "partner" : partner,
        "outfits" : [],
    })
    assert result.is_success == False
    assert result.message == "Date schedule has already been missed 📛"

def test_update_date_failed_empty_location():

    partner = profile_controller.get_partners().data[0]

    result = date_controller.update({
        "description" : "",
        "date" : default_date,
        "location" : "",
        "partner" : partner,
        "outfits" : [],
    })
    assert result.is_success == False
    assert result.message == "Location is required 📛"

def test_update_date_failed_location_too_long():

    partner = profile_controller.get_partners().data[0]

    result = date_controller.update({
        "description" : "",
        "date" : default_date,
        "location" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a bibendum nibh finibus sit amet. Nunc in tortor sit amet velit fringilla dignissim eget in dui. Ut ut neque elit. Nunc interdum, lacus vel ultrices malesuada, lacus quam volutpat dui, ac gravida sem lectus ac velit. Nullam suscipit nisl vitae urna egestas maximus. Nullam interdum nulla fringilla, ",
        "partner" : partner,
        "outfits" : [],
    })
    assert result.is_success == False
    assert result.message == "Location maximum 255 characters 📛"

def test_update_date_failed_empty_partner():

    result = date_controller.update({
        "description" : "",
        "date" : default_date,
        "location" : "Bandung",
        "partner" : None,
        "outfits" : [],
    })
    assert result.is_success == False
    assert result.message == "Partner is required 📛"

def test_update_date_success():

    partner = profile_controller.get_partners().data[0]

    result = date_controller.update({
        "id" : date_id,
        "description" : "",
        "date" : default_date + timedelta(days=1),
        "location" : "Bandung",
        "partner" : partner,
        "outfits" : [],
    })
    assert result.is_success
    assert result.message == "Date successfuly edited👍"

# TODO: Delete Date
def test_delete_date_success():
    result = date_controller.delete(date_id)

    assert result.is_success

# def test_remove_db():
#     os.remove("testing.db")
